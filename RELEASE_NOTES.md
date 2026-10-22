# Codex Pet Gallery v1.0.1

保存当前已应用的 DeepSeek 娘 1.0.1，更新 33 帧，其余 40 帧（包括全部十六方向）保留 1.0.0 原像素。

## 画面更新

- idle 改为捧空碗等饭，保留呼吸和完整眨眼。
- 左右拖动改为被揪起呆毛后悬空晃腿、左右摆尾和轻微身体晃动。
- 站立摇尾巴保持捧碗，改善与 idle、扒饭之间的道具及姿态衔接。
- 扒饭收小举筷幅度，修正头发、鳍耳偏宽；宽度约 147–149 像素，高度约 191–192，与 idle 接近。

## 下载

| 文件 | 用途 |
| --- | --- |
| [deepseek-chan-1.0.1-pet.zip](https://github.com/HanaRo/codex-pet-gallery/releases/download/v1.0.1/deepseek-chan-1.0.1-pet.zip) | 安装包：配置、精灵图、布局、安装说明与来源记录。 |
| [codex-pet-gallery-v1.0.1-source.zip](https://github.com/HanaRo/codex-pet-gallery/releases/download/v1.0.1/codex-pet-gallery-v1.0.1-source.zip) | 完整仓库源码与素材：包含两个冻结版本、高清来源、提示词、73 帧资源包、预览、QA、重建工具和测试。 |
| [deepseek-chan-1.0.1-spritesheet.png](https://github.com/HanaRo/codex-pet-gallery/releases/download/v1.0.1/deepseek-chan-1.0.1-spritesheet.png) | 单独精灵图，便于通过支持 v2 的 Pets 环境导入。 |
| [SHA256SUMS.txt](https://github.com/HanaRo/codex-pet-gallery/releases/download/v1.0.1/SHA256SUMS.txt) | 上述三个附件的 SHA-256。 |

安装时将安装包内的 pet.json 和 spritesheet.png 放到 CODEX_HOME/pets/deepseek-chan/，入口与兼容性详见 [安装说明](https://github.com/HanaRo/codex-pet-gallery/blob/v1.0.1/docs/INSTALL.md)。源码包可离线验证并从 frames.zip 重建相同 RGBA 像素。

同步保存了状态切换分析、开发约定、准确时长预览工具和校验记录。当前已安装素材与发布图的 RGBA 像素一致。v1.0.0 的版本文件和 Release 附件保留原样。

## 现有限制

客户端仍直接切帧，非 idle 动作通常三轮后回到待机；素材不能改变播放策略。方向注视和部分业务动作沿用原空手姿势，碗仍可能在这些边界消失；拖动反向和松手也可能出现抓取点或悬空姿态跳变。详见 [切换说明](https://github.com/HanaRo/codex-pet-gallery/blob/v1.0.1/docs/TRANSITIONS.md)。

工具代码采用 MIT；角色和参考素材的权利记录单独见 [ASSET_LICENSE.md](https://github.com/HanaRo/codex-pet-gallery/blob/v1.0.1/ASSET_LICENSE.md) 和 [CREDITS.md](https://github.com/HanaRo/codex-pet-gallery/blob/v1.0.1/CREDITS.md)，不将代码许可扩展为素材授权。本项目与 OpenAI、DeepSeek 无官方隶属关系。
