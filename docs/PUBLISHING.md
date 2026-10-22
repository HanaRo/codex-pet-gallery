# 发布到 GitHub

本地项目已经按 codex-pet-gallery 命名。公开发布前，维护者需完成 ASSET_LICENSE.md 中尚未确认的素材来源/许可信息；新编写的脚本代码使用 MIT，不能把这个许可自动扩展到参考图与角色形象。

## 创建仓库

在本项目根目录运行以下命令；根据你的 GitHub 账号、仓库归属与公开/私有选择调整。以下示例会实际创建公开仓库：

~~~bash
git init -b main
git add .
git commit -m "Archive DeepSeek-chan 1.0.0"
gh repo create codex-pet-gallery --public --source=. --remote=origin --push
~~~

如果已经创建远端仓库，可改用 git remote add origin <仓库地址> 后推送。不要把另一项目的 .git 目录或本机工作目录整体复制到这里。

## 按角色发布版本

~~~bash
python tools/gallery.py verify-files
python tools/gallery.py validate --all
python tools/gallery.py build --all
python -m unittest discover -s tests -v
python tools/gallery.py package --pet deepseek-chan --version 1.0.0
git tag -a deepseek-chan-v1.0.0 -m "DeepSeek-chan 1.0.0"
git push origin deepseek-chan-v1.0.0
~~~

随后创建 GitHub Release，选择该标签，上传 dist/deepseek-chan-1.0.0-pet.zip，并摘录 CHANGELOG.md 中对应版本的说明。完整项目源码包含原画、提示词与 QA；角色安装包只包含安装需要的素材、配置和说明。

可用 GitHub CLI：

~~~bash
gh release create deepseek-chan-v1.0.0 dist/deepseek-chan-1.0.0-pet.zip --title "DeepSeek 娘 1.0.0" --notes-file RELEASE_NOTES.md
~~~

初次导入前后运行 verify-files。根目录 SHA256SUMS.txt 是快照完整性清单；有意修改源码、文档或新增版本后，应先检查差异，再运行 python tools/gallery.py checksums 刷新清单并提交。不要用刷新校验和掩盖未知文件变化。
