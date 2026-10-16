"""Validate generated pages, local links, metadata, and publication state."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote, parse_qs
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.links = []
        self.ids = set()
        self.h1 = 0
        self.title = 0
        self.language = None
        self.alternates = {}
        self.language_link = None
        self.description = False
        self.canonical = False
        self.main = False
        self.warnings = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            assert attrs["id"] not in self.ids, f"{self.path}: duplicate id {attrs['id']}"
            self.ids.add(attrs["id"])
        if tag == "html": self.language = attrs.get("lang")
        if tag == "title": self.title += 1
        if tag == "h1": self.h1 += 1
        if tag == "main": self.main = True
        if tag == "meta" and attrs.get("name") == "description": self.description = bool(attrs.get("content"))
        if tag == "link" and attrs.get("rel") == "canonical": self.canonical = attrs.get("href", "").startswith("https://xvshiting.github.io/mussito-public/")
        if tag == "link" and attrs.get("rel") == "alternate":
            self.alternates[attrs.get("hreflang")] = attrs.get("href")
        if tag == "a" and "data-language-switch" in attrs:
            self.language_link = attrs.get("href")
        for key in ["href", "src"]:
            if key in attrs:
                self.links.append(attrs[key])
        if tag == "img":
            assert "alt" in attrs, f"{self.path}: missing image alt"
        if tag == "script" and attrs.get("src"):
            assert not urlsplit(attrs["src"]).scheme, "Unexpected external script"

pages = {}
for path in DOCS.rglob("*.html"):
    source = path.read_text()
    assert "@@" not in source, f"{path}: template not expanded"
    page = Page(path)
    page.feed(source)
    expected_language = "zh-CN" if path.parent.name == "zh" else "en"
    assert page.language == expected_language, f"{path}: wrong language"
    assert set(page.alternates) == {"en", "zh-CN", "x-default"}, f"{path}: missing language alternatives"
    assert page.alternates["en"] == page.alternates["x-default"], f"{path}: English must be the default"
    assert page.language_link, f"{path}: no language switch"
    counterpart = ((path.parent / ".." / path.name) if expected_language == "zh-CN" else (path.parent / "zh" / path.name)).resolve()
    assert (path.parent / page.language_link).resolve() == counterpart, f"{path}: switch must preserve the page"
    assert page.description and page.canonical and page.main, f"{path}: missing page metadata"
    assert page.h1 == 1 and page.title == 1, f"{path}: expected one h1 and title"
    pages[path.resolve()] = page
assert len(pages) == 12, "Expected six English and six Chinese pages"
assert sum(page.language == "en" for page in pages.values()) == 6
assert sum(page.language == "zh-CN" for page in pages.values()) == 6
links = 0
for path, page in pages.items():
    for link in page.links:
        parts = urlsplit(link)
        if parts.scheme or parts.netloc:
            assert parts.scheme == "https", f"Unexpected external protocol {link}"
            if parts.netloc == "github.com" and parts.path.endswith("/issues/new"):
                template = parse_qs(parts.query).get("template", [""])[0]
                assert template and (ROOT / ".github/ISSUE_TEMPLATE" / template).is_file(), f"Missing feedback form: {link}"
            continue
        target = (path.parent / unquote(parts.path or path.name)).resolve()
        assert target.is_relative_to(DOCS), f"Escapes site root: {link}"
        assert target.is_file(), f"Broken local link: {path.name}: {link}"
        if parts.fragment:
            assert target in pages and unquote(parts.fragment) in pages[target].ids, f"Broken anchor: {link}"
        links += 1

release = json.loads((DOCS / "release.json").read_text())
mac = release["mac"]
assert mac["status"] in ["preparing", "published"]
if mac["status"] == "published":
    assert mac["signed"] is True and mac["notarized"] is True
    assert re.fullmatch(r"[0-9a-f]{64}", mac["sha256"] or "")
    assert re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][a-zA-Z0-9.]+)?", mac["version"] or "")
    assert mac["download_url"].startswith("https://github.com/xvshiting/mussito-public/releases/download/")
    assert mac["download_url"].endswith(".dmg")
else:
    assert mac["download_url"] is None, "Do not expose an unreleased download"
ios = release["iphone"]
assert ios["status"] in ["preparing", "published"]
if ios["status"] == "published":
    assert re.fullmatch(r"https://apps\.apple\.com/[a-z]{2}/app/.+/id\d+", ios["app_store_url"] or "")
else:
    assert ios["app_store_url"] is None

for path in ROOT.rglob("*"):
    if not path.is_file() or any(part in [".git", "build", "node_modules"] for part in path.parts): continue
    assert path.suffix.lower() not in [".swift", ".cpp", ".dmg", ".pkg", ".p12", ".mobileprovision", ".pem"], f"Non-public file: {path}"
    if path.suffix not in [".png", ".jpg", ".webp"]:
        text = path.read_text()
        assert not re.search(r"gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|(?m:^-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----$)", text), f"Possible credential: {path}"
        assert ("mussito://" + "pair?") not in text and ("macsay://" + "pair?") not in text, f"Pairing URL in {path}"
print(f"PASS: {len(pages)} pages, {links} local links, metadata, release state, public file boundaries")
