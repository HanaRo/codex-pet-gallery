# Codex Pet Gallery

保存、复现和持续维护 Codex / ChatGPT Work 的社区 Pet 角色素材。每个角色独立编号、独立版本；已经发布的版本保留原文件和校验和。

当前收录 **DeepSeek 娘 1.0.0**：蓝发 Q 版女仆，爱思考也爱干饭。站立时左右摇尾巴，等待时捧碗，工作时扒饭。

![左右摆尾](pets/deepseek-chan/versions/1.0.0/previews/tail-wag.gif)

[完整动作 GIF](pets/deepseek-chan/versions/1.0.0/previews/all-states.gif) · [完整动作 MP4](pets/deepseek-chan/versions/1.0.0/previews/all-states.mp4) · [十六方向注视](pets/deepseek-chan/versions/1.0.0/previews/look-loop.gif)

## 直接使用

- [下载当前精灵图](pets/deepseek-chan/versions/1.0.0/spritesheet.png)
- [客户端角色配置 pet.json](pets/deepseek-chan/versions/1.0.0/pet.json)
- [安装说明](docs/INSTALL.md)

格式为透明 RGBA PNG、1536×2288、v2、192×208 单帧，共 73 个有效帧。目标是支持 v2 自定义 Pet 的客户端；入口和可用性随客户端与账号变化。当前素材已通过 Pets 服务端验证，并与安装后下载的版本逐像素核对一致。

**动画素材不控制客户端循环策略。** 已核查的桌面版本会将吃饭动作播三轮，约 2.46 秒，再切回慢速待机，即使任务仍在执行。详见 [播放逻辑与动作映射](docs/PLAYBACK.md)。

## 复现当前版本

需要 Python 3.11+。以下命令全部离线处理素材；首次安装依赖需要联网。

~~~bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell：.venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt
python tools/gallery.py verify-files
python tools/gallery.py validate --all
python tools/gallery.py build --pet deepseek-chan --version 1.0.0
python tools/gallery.py package --pet deepseek-chan --version 1.0.0
~~~

重新组装的图片写入 dist/deepseek-chan/1.0.0/spritesheet.png；可安装压缩包写入 dist/deepseek-chan-1.0.0-pet.zip。

直接下载仓库中的精灵图，可得到冻结版本的相同文件；从逐帧素材重新组装，可得到相同 RGBA 像素。不同 PNG 编码器可能生成不同文件字节，脚本会分别报告文件哈希与像素哈希。AI 再次生成图片不保证得到完全相同的画面。

详见 [复现说明](docs/REPRODUCING.md)。

## 项目结构

~~~text
catalog.json                         # 多角色索引、各角色最新版本
pets/
  deepseek-chan/
    README.md
    versions/
      1.0.0/
        pet.json                     # 客户端本地角色配置
        manifest.json                # 版本、逐帧清单、校验和、来源
        spritesheet.png              # 可直接使用的最终素材
        layout.json                  # 16 个注视方向的布局
        frames/                      # 从最终图无损拆出的 73 帧
        sources/                     # 高清原画、条带、提示词、生成记录
        previews/                    # GIF / MP4 / 静帧
        qa/                          # 脱敏后的历史验证与视觉检查
tools/                               # 独立组装、校验与打包
docs/                                # 安装、复现、播放规则与发布流程
~~~

后续更新会新增版本目录；其他角色使用新的稳定 id。操作约定见 [贡献与版本管理](CONTRIBUTING.md)。[发布准备](docs/PUBLISHING.md)包含 GitHub 初始化与按角色发布的命令。

## 来源与许可

这是社区素材项目，与 OpenAI、DeepSeek 无官方隶属或背书关系。当前角色参考用户提供的形象，并参考 DeepSeek Whale-chan 社区项目与“深深”的动作设计。

项目新编写的工具代码采用 [MIT](LICENSE)。角色、参考图片与生成素材的权利说明单独见 [ASSET_LICENSE.md](ASSET_LICENSE.md)，来源见 [CREDITS.md](CREDITS.md)。代码许可不替代参考素材的授权。
