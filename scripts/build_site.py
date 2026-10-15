"""Build the static public site without third-party dependencies."""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://xvshiting.github.io/mussito-public/"
PAGES = {
    "index": ("Mussito — 轻声说，自然成文。", "将 iPhone 变成 Mac 的随身麦克风。用熟悉的输入位置，接住自然说出的话。", "HOME"),
    "download": ("获取 Mussito — Mac 与 iPhone", "查看 Mussito 的发布状态、Mac 系统要求和 iPhone 上架进展。", "DOWNLOAD"),
    "guide": ("开始使用 — Mussito", "从安装 Mac 端、连接 iPhone 到完成第一次语音输入。", "GUIDE"),
    "privacy": ("隐私政策 — Mussito", "了解 Mussito 如何处理麦克风音频、设备配对和本机声纹资料。", ""),
    "support": ("帮助与支持 — Mussito", "查找连接、权限、音频与输入问题的解决方法，并反馈使用问题。", "SUPPORT"),
    "updates": ("发布与更新 — Mussito", "查看 Mussito 的公开发布进度与版本更新记录。", ""),
}
layout = (ROOT / "site/layout.html").read_text()
for slug, (title, description, nav) in PAGES.items():
    canonical = BASE if slug == "index" else BASE + slug + ".html"
    content = (ROOT / f"content/{slug}.html").read_text()
    replacements = {"TITLE": escape(title), "DESCRIPTION": escape(description), "CANONICAL": canonical, "CONTENT": content}
    replacements.update({"NAV_" + key: 'aria-current="page"' if key == nav else "" for key in ["HOME", "GUIDE", "SUPPORT", "DOWNLOAD"]})
    page = layout
    for key, value in replacements.items():
        page = page.replace("@@" + key + "@@", value)
    (ROOT / f"docs/{slug}.html").write_text(page)
(ROOT / "docs/.nojekyll").touch()
(ROOT / "docs/sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(f"  <url><loc>{BASE if slug == 'index' else BASE + slug + '.html'}</loc></url>" for slug in PAGES) + "\n</urlset>\n")
(ROOT / "docs/robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: " + BASE + "sitemap.xml\n")
print(f"Built {len(PAGES)} pages in docs/")
