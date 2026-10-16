# Mussito

**轻声说，自然成文。** 将 iPhone 变成 Mac 的随身麦克风，在熟悉的输入位置完成语音输入。

- [Website (English)](https://xvshiting.github.io/mussito-public/)
- [官网（中文）](https://xvshiting.github.io/mussito-public/zh/)
- [获取 Mussito](https://xvshiting.github.io/mussito-public/download.html)
- [安装与配对](https://xvshiting.github.io/mussito-public/guide.html)
- [帮助与支持](https://xvshiting.github.io/mussito-public/support.html)
- [隐私政策](https://xvshiting.github.io/mussito-public/privacy.html)
- [公开发行版本](https://github.com/xvshiting/mussito-public/releases)

## 当前状态

正在准备第一次公开发布，尚无正式 DMG、App Store 购买链接或公开 TestFlight 邀请。Mac 端计划免费提供，iPhone 端计划付费提供，具体价格和方式以正式上架信息为准。

系统要求：Mac 首发验证面向 Apple Silicon / macOS 15 或更新版本；iPhone 要求 iOS 17 或更新版本，传音及输入功能需配合 Mac 端使用。

此仓库仅用于官网、公开文档、用户反馈与发行文件，不包含应用源码。公开可见不代表应用开源；品牌与网站素材保留其相应权利。

## 反馈

请通过 [Issues](https://github.com/xvshiting/mussito-public/issues) 报告问题、建议功能或咨询隐私问题。反馈是公开的，请勿提交配对二维码、访问凭据、私人录音或未处理的私人文本。

## 维护网站

网站是无框架的静态 HTML/CSS/JS，通过 GitHub Pages 从 `main:/docs` 发布。首次访问默认英文，页头可切换中文；语言保存在页面地址中，不使用 Cookie。无广告、统计脚本或外部字体。

```sh
conda run -n kora python scripts/build_site.py
conda run -n kora python scripts/check_site.py
conda run --no-capture-output -n kora python -m http.server 8790 --bind 127.0.0.1 --directory docs
```

- 英文正文：`content/*.html`（官网默认语言）
- 中文正文：`content/zh/*.html`（公开地址 `/zh/`）
- 共用模板：`site/layout.html`
- 样式、交互与已检查的品牌素材：`docs/assets/`
- 可编辑发布状态：`docs/release.json`
- 安装包：只放 GitHub Releases，不提交进 Git 源码目录

发布流程见 [RELEASING.md](RELEASING.md)。本仓库中的产品截图为开发版界面展示，不代表已公开发布或所有兼容性已验收。
