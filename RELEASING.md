# 公开版本发布

当前只发布官网与公开文档。开发构建不能直接作为正式下载提供。

## Mac 正式版

1. 在独立的开发仓库生成 Mussito 正式构建。确认发行包只包含公开产品需要的组件。
2. 对应用、动态库、音频驱动及安装包使用适当的 Developer ID 身份签名；完成 hardened runtime 兼容验证、公证和票据附加。
3. 在干净的受支持 Mac 上实际验证 DMG 安装、首次启动、权限、音频组件安装/卸载、手机配对、两种识别模式和取消/断线恢复。
4. 制作最终 DMG，并验证文件完整性及公证票据。计算 SHA-256。发布说明准确列出版本、架构、系统要求、依赖、已验收范围和已知问题。
5. 创建带该 DMG 和 SHA256SUMS.txt 的 GitHub Draft Release，人工核对后再发布。使用 `release-templates/mac-release.md` 作为说明结构；不要把应用源码或开发日志附在公开发行中。
6. 将 `docs/release.json` 的 Mac 状态改为 `published`，填写真实 `version`、`download_url`、`sha256`，确认 `signed` 与 `notarized` 均为 `true`。下载 URL 必须指向本仓库 Releases 的 DMG。
7. 更新 `content/updates.html` 与相关说明，运行构建和链接检查后提交。GitHub Pages 发布后，核对实际下载文件与 SHA-256 一致。

GitHub 自动生成的 Source code ZIP/TAR.GZ 只包含本公开仓库的网页与文档，不是应用源码。安装包以单独的 DMG 资产为准。

## iPhone 正式上架

仅在可用的 App Store 购买页实际存在后，将 `docs/release.json` 的 iPhone 状态改为 `published` 并填写真实链接。同步更新价格/收费方式说明、最低系统要求、隐私政策和公开版本记录。未上架时保持 `preparing`，不使用虚构的 App Store ID。

## 页面发布

GitHub Pages 使用 `main:/docs`。每次调整正文或布局后：

```sh
conda run -n kora python scripts/build_site.py
conda run -n kora python scripts/check_site.py
git diff --check
```

检查 `docs/` 生成结果后提交并推送。当前联系渠道为 GitHub Issues，未经维护者确认不要添加邮箱或客服承诺。
