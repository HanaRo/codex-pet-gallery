# DeepSeek 娘 · 装学霸版 1.0.0

2026-11-17 首次纳入画廊，采用 2026-10-30 已应用的配色修正版。透明 v2 图集为 1536×2288，单帧 192×208，包含九组常规动作和十六个注视方向，共 73 帧。重新下载的已应用素材与本图集的 RGBA 像素一致。[图集](spritesheet.png) · [清单与校验和](manifest.json) · [像素核对](qa/update-verification.json)

| 状态 | 动作 |
| --- | --- |
| idle | 捧书环顾，最后低头盯着饭碗 |
| running | 双手抬书挡住嘴偷吃，再放下书露出饭碗 |
| running-left / running-right | 被揪起后悬空晃腿、摆尾，伸手扶正滑落的假发 |
| jumping | 双脚着地，鲸尾从身后摆向另一侧再摆回 |
| waving | 一手扶书，一手打招呼 |
| failed | 露出失落表情，低头抱紧书和饭碗 |
| waiting | 轻轻递出书和饭碗，抬头等回应 |
| review | 扫视左右页后睁眼点头 |
| look | 头和视线按十六个方向转动，身体与书碗保持正面 |

## 待机与摇尾巴配色

原来的摇尾巴帧有较深的紫色衣服阴影和蓝色偏色。修正版以待机为配色基准，减淡阴影并校准发色与肤色。此次调色涉及五帧，另有调色前的图集供对照和回退。[配色对照](previews/palette-comparison.png) · [同一时间表下的切换对比](previews/transitions/hover-enter-exit.gif) · [调色前图集](sources/history/atlas-before-tail-palette-fix.png)

## 安装与离线复现

将本目录的 pet.json 和 spritesheet.png 放进 CODEX_HOME/pets/deepseek-gpt-scholar/。支持 v2 的 ChatGPT Work 环境也可直接导入图集。[客户端安装与导入说明](../../../../docs/INSTALL.md)

在仓库根目录运行以下命令。frames.zip 已保存 73 个最终帧，重建结果的 RGBA 像素与发布图一致。sources/ 提供生成概念、高清条带、提示词和生成记录，供后续制作参考。

```bash
python -m pip install -r requirements.txt
python tools/gallery.py verify-files
python tools/gallery.py validate --pet deepseek-gpt-scholar --version 1.0.0
python tools/gallery.py build --pet deepseek-gpt-scholar --version 1.0.0
python tools/gallery.py package --pet deepseek-gpt-scholar --version 1.0.0
```

输出的安装包位于 dist/deepseek-gpt-scholar-1.0.0-pet.zip。[逐帧资源](frames.zip) · [生成记录](sources/generation-plan.json) · [验证报告](qa/)

客户端直接切帧，抬起的书或摆到另一侧的尾巴被中途打断时可能出现位置跳变。112.5° 的低头幅度较小，四个主方向已通过独立盲测。[切换记录](previews/transitions/) · [方向对照](previews/direction-qa.png) · [素材权利说明](../../../../ASSET_LICENSE.md)
