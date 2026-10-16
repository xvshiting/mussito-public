"""Build English-default and Chinese static pages without dependencies."""
from html import escape
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://xvshiting.github.io/mussito-public/"
PAGES = {
    "index": {
        "en": ("Mussito — Speak softly. Write naturally.", "Turn your iPhone into a microphone for your Mac. Let your words land where you are already writing.", "HOME"),
        "zh": ("Mussito — 轻声说，自然成文。", "将 iPhone 变成 Mac 的随身麦克风。用熟悉的输入位置，接住自然说出的话。", "HOME"),
    },
    "download": {
        "en": ("Get Mussito — Mac and iPhone", "Check Mussito release availability, Mac requirements, and progress toward the iPhone App Store release.", "DOWNLOAD"),
        "zh": ("获取 Mussito — Mac 与 iPhone", "查看 Mussito 的发布状态、Mac 系统要求和 iPhone 上架进展。", "DOWNLOAD"),
    },
    "guide": {
        "en": ("Getting started — Mussito", "Set up your Mac, pair your iPhone, and complete your first voice input session.", "GUIDE"),
        "zh": ("开始使用 — Mussito", "从安装 Mac 端、连接 iPhone 到完成第一次语音输入。", "GUIDE"),
    },
    "privacy": {
        "en": ("Privacy policy — Mussito", "Learn how Mussito handles microphone audio, device pairing, and voice profiles stored on your Mac.", ""),
        "zh": ("隐私政策 — Mussito", "了解 Mussito 如何处理麦克风音频、设备配对和本机声纹资料。", ""),
    },
    "support": {
        "en": ("Help and support — Mussito", "Find help with pairing, permissions, audio, and text input, or report an issue on GitHub.", "SUPPORT"),
        "zh": ("帮助与支持 — Mussito", "查找连接、权限、音频与输入问题的解决方法，并反馈使用问题。", "SUPPORT"),
    },
    "updates": {
        "en": ("Releases and updates — Mussito", "Follow Mussito public release progress and version updates.", ""),
        "zh": ("发布与更新 — Mussito", "查看 Mussito 的公开发布进度与版本更新记录。", ""),
    },
}
LABELS = {
    "en": dict(SKIP="Skip to content", HOME_LABEL="Mussito home", MAIN_NAV="Main navigation", EXPERIENCE="Experience", GUIDE="Guide", SUPPORT="Support", GET="Get Mussito", TAGLINE="Speak softly. Write naturally.", FOOTER_NAV="Footer navigation", PRIVACY="Privacy", CONTACT="Support", UPDATES="Updates", LANG_LABEL="切换到中文", LANG_NAME="中文", OTHER_LANG="zh-CN", OG_LOCALE="en_US", OG_ALTERNATE="zh_CN"),
    "zh": dict(SKIP="跳到正文", HOME_LABEL="Mussito 首页", MAIN_NAV="主导航", EXPERIENCE="体验", GUIDE="使用指南", SUPPORT="帮助", GET="获取 Mussito", TAGLINE="轻声说，自然成文。", FOOTER_NAV="页脚导航", PRIVACY="隐私政策", CONTACT="联系与支持", UPDATES="更新记录", LANG_LABEL="Switch to English", LANG_NAME="EN", OTHER_LANG="en", OG_LOCALE="zh_CN", OG_ALTERNATE="en_US"),
}

def public_url(slug, language):
    directory = "zh/" if language == "zh" else ""
    return BASE + directory + ("" if slug == "index" else slug + ".html")

layout = (ROOT / "site/layout.html").read_text()
asset_versions = {name: sha256((ROOT / "docs/assets" / filename).read_bytes()).hexdigest()[:12] for name, filename in [("CSS_VERSION", "style.css"), ("JS_VERSION", "site.js")]}
urls = []
for language in ("en", "zh"):
    prefix = "../" if language == "zh" else ""
    output = ROOT / "docs" / ("zh" if language == "zh" else "")
    output.mkdir(exist_ok=True)
    for slug, translations in PAGES.items():
        title, description, nav = translations[language]
        source = ROOT / "content" / ("zh" if language == "zh" else "") / (slug + ".html")
        content = source.read_text().replace('src="assets/', 'src="' + prefix + 'assets/')
        replacements = dict(LABELS[language], **asset_versions, TITLE=escape(title), DESCRIPTION=escape(description),
                            CANONICAL=public_url(slug, language), CONTENT=content,
                            LANG="zh-CN" if language == "zh" else "en", SITE_ROOT=".." if language == "zh" else ".",
                            ASSET_PREFIX=prefix, EN_URL=public_url(slug, "en"), ZH_URL=public_url(slug, "zh"),
                            LANG_LINK=("../" if language == "zh" else "zh/") + slug + ".html")
        replacements.update({"NAV_" + key: 'aria-current="page"' if key == nav else "" for key in ["HOME", "GUIDE", "SUPPORT", "DOWNLOAD"]})
        page = layout
        for key, value in replacements.items():
            page = page.replace("@@" + key + "@@", value)
        (output / (slug + ".html")).write_text(page)
        urls.append(public_url(slug, language))
(ROOT / "docs/.nojekyll").touch()
(ROOT / "docs/sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(f"  <url><loc>{url}</loc></url>" for url in urls) + "\n</urlset>\n")
(ROOT / "docs/robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: " + BASE + "sitemap.xml\n")
print(f"Built {len(urls)} pages: English default + Chinese")
