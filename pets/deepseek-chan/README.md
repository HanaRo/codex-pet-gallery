# DeepSeek 娘

当前版本：[1.0.1](versions/1.0.1/README.md)。[1.0.0](versions/1.0.0/manifest.json) 保留原文件，支持回退。

![捧碗左右摆尾](versions/1.0.1/previews/tail-wag.gif)

| 内容 | 文件 |
| --- | --- |
| 直接使用的透明精灵图 | [spritesheet.png](versions/1.0.1/spritesheet.png) |
| 本地角色配置 | [pet.json](versions/1.0.1/pet.json) |
| 全部动作 | [GIF](versions/1.0.1/previews/all-states.gif) / [MP4](versions/1.0.1/previews/all-states.mp4) |
| 十六方向 | [direction-qa.png](versions/1.0.1/previews/direction-qa.png) |
| 高清条带、提示词与生成记录 | [sources](versions/1.0.1/sources) |
| 切换与中断检查 | [transitions](versions/1.0.1/previews/transitions) |
| 验证及版本差异 | [qa](versions/1.0.1/qa) |

1.0.1 将 idle 改为捧空碗等饭，左右拖动改为被揪起后晃腿、摆尾与轻微身体晃动。站立摇尾巴沿用捧碗形象；扒饭缩小举筷幅度并修正头发、鳍耳偏宽，使相关动作的身体尺度更接近。

技术 jumping 槽位按用户要求表示站立左右摇尾巴；running 表示工作时扒饭。方向注视和部分业务状态仍为旧版姿势，已知切换限制见 [开发说明](../../docs/TRANSITIONS.md)。

初次公开快照日期为 2026-10-22，原画制作始于 2026-10-21。版本目录中的原图、逐帧资源和校验记录保持冻结；修改应新建版本。
