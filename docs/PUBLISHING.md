# 发布到 GitHub

公开仓库为 [HanaRo/codex-pet-gallery](https://github.com/HanaRo/codex-pet-gallery)。画廊 Release 用 `v<画廊版本>`，角色各自维护 `catalog.json` 中的 `latest` 与角色版本标签。例如装学霸版的角色标签为 `deepseek-gpt-scholar-v1.0.0`。[发布说明索引](../RELEASE_NOTES.md)

## 准备新版本

1. 从已经批准的 atlas 导入新的版本目录，不覆盖任何已发布目录。
2. 保存最终逐帧资源、高清来源、提示词、预览、实际 QA 与已知限制；去掉本机路径、账号 ID、短期 URL 和凭据。
3. 补全 manifest.json 的来源清单、哈希、画面语义、复现记录和 qa_status。更新 catalog.json、README、VERSIONS 和 CHANGELOG，并在 docs/releases/ 写对应版本的说明。
4. 记录素材来源与许可状态。工具代码 MIT 不代表角色及参考图片采用 MIT，现有记录见 ASSET_LICENSE.md。

```bash
python tools/gallery.py checksums
python tools/gallery.py verify-files
python tools/gallery.py validate --all
python tools/gallery.py build --all
python -m unittest discover -s tests -v
python tools/gallery.py package --pet deepseek-chan --version 1.0.1
```

确认旧版本文件未变后提交。安装包应可重复打包，并与版本内 spritesheet.png 逐字节一致。

## Release 的正文与附件

正文先写一句角色与版本介绍，再依次放桌面 ZIP 和 Work PNG 下载、新增或变更的动作、安装说明。源码包、SHA-256、验证与限制放进文末的「开发者下载与校验」。发布页的文件、动图和安装说明链接指向对应版本标签。以下命令以历史 v1.0.1 为例。

从已经提交的 Git 快照导出完整源码，避免混入工作缓存、私密配置或尚未提交的文件：

```bash
git archive --format=zip --prefix=codex-pet-gallery-v1.0.1/ -o dist/codex-pet-gallery-v1.0.1-source.zip HEAD
git tag -a v1.0.1 -m "Codex Pet Gallery v1.0.1"
git tag -a deepseek-chan-v1.0.1 -m "DeepSeek 娘 1.0.1"
git push origin main v1.0.1 deepseek-chan-v1.0.1
```

同时提供角色安装包、完整源码包、单独精灵图和三个附件的 SHA256SUMS.txt。仓库根目录的 SHA256SUMS.txt 校验项目文件；Release 附件中的同名文件校验下载包，二者范围不同。

建议先创建 draft Release 并上传附件，核对远端附件摘要，再正式发布：

```bash
gh release create v1.0.1 --verify-tag --draft --title "v1.0.1 · DeepSeek 娘" --notes-file docs/releases/v1.0.1.md
gh release upload v1.0.1 dist/deepseek-chan-1.0.1-pet.zip dist/codex-pet-gallery-v1.0.1-source.zip dist/deepseek-chan-1.0.1-spritesheet.png dist/SHA256SUMS.txt
gh release edit v1.0.1 --draft=false --latest
```

完整源码包应另解压到干净目录，再运行 verify-files、validate、build 和测试；无需展开 frames.zip，也不依赖 Pets 插件或维护者的本机路径。已发布标签、旧版本目录和旧附件保持冻结，修正另发新版本。
