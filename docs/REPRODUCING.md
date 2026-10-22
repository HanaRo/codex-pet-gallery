# 复现与素材来源

## 三种复现程度

| 目标 | 输入 | 可保证的结果 |
| --- | --- | --- |
| 直接使用当前版本 | spritesheet.png 与 pet.json | 精灵图文件字节与冻结版本完全相同 |
| 重新组装当前版本 | frames.zip 中已批准的 73 张 PNG | 解码后的 RGBA 像素完全相同 |
| 重新绘制、扩展动作 | sources 中原画、高清条带和提示词 | 提供设计与流程依据；AI 结果不保证逐像素一致 |

最终 PNG 文件 SHA-256：

~~~text
be535f9abd7aeca27c0c33bd04b4cfe3267dd907de6d29eaca4341aa552b0af1
~~~

最终图解码后的 RGBA 字节 SHA-256（图像大小为 1536×2288，RGBA 行优先）：

~~~text
64674e1ed187ba8c49a921bb37e8f8e0c725fc82845dc6a49d0697c60d7d0be4
~~~

从已安装 Pet 重新下载的文件与该 RGBA 哈希一致。服务端可能重新编码 PNG，所以下载文件的编码哈希与制作时的文件不一定相同。

## 独立重新组装

~~~bash
python -m pip install -r requirements.txt
python tools/gallery.py verify-files
python tools/gallery.py validate --pet deepseek-chan --version 1.0.1
python tools/gallery.py build --pet deepseek-chan --version 1.0.1
~~~

脚本先校验 atlas、逐帧和原始资料的 SHA-256，再从 frames.zip 读取 73 张已完成去背景与边缘处理的单帧按固定位置粘贴回透明画布。使用直接 RGBA 粘贴，避免再次 alpha 混合改变半透明边缘。重新编码后再次核对全部像素。

它不需要账号、网络、原作者的本机路径、临时上传链接或 Pets 插件。固定 Python/Pillow 版本有助于减少编码差异，但跨平台 PNG 压缩字节相同不作为复现要求；成品原文件已保留以供字节级复现。

## 重新创作与高清原始素材

sources/references 保存基础立绘、吃饭道具立绘、用户提供的参考图及已确认的方向锚点。sources/strips 保存最终选用的 11 组条带，其中左向拖动是原生尺寸逐格镜像派生，其余新绘制条带保存高清源图，sources/prompts 保存当时的提示词记录。

原制作流程使用 Codex 的 imagegen 工具和 Pets 插件 0.1.6 的组装工具：

1. 以统一基础形象生成各状态的独立条带；吃饭状态额外使用捧碗与筷子参考。
2. 按连通图形提取完整角色，去掉纯绿背景，使用共享行缩放；不逐帧单独拉满。
3. 对齐站立动作的双脚，仅作整数平移；当前左右拖动对齐呆毛抓取点，保留悬空晃腿和身体轻晃。
4. 先确认四个正方向，再按顺时针生成并检查十六方向。
5. 合成 v2 atlas，完成一次边缘局部去绿溢色，保留 alpha。
6. 做结构、状态语义、方向、透明边缘和完整动画检查。

1.0.1 的处理参数与结果见 qa/idle、qa/drag、qa/drag-pair、qa/tail-wag、qa/running 和来源生成记录；继承状态的历史记录保存在 1.0.0 的 qa 目录。qa 中的 historical-run 路径仅用于解释当时的记录，不是脚本依赖。

本仓库独立工具从“最终批准帧”开始复现，不承诺把任何新生成的高清条带自动提取成完全一样的帧；历史插件工具未复制进本仓库。模型标识、随机种子没有由当时的工具返回，因此记录为未记录。提示词中的“先前条带”“附图顺序”等引用属于当时的编辑上下文，未保存每张被丢弃的尝试图；应结合已批准的参考和成品理解。

## 验证范围

- tools/gallery.py：项目文件完整性、布局、占位、透明空格、逐帧与成品一致、像素重建。
- qa/：原制作时实际运行的服务端校验、Pets 插件质量门槛、方向语义与已批准的历史方向检查，已移除本机路径与账号标识。
- 新增角色或修改动作仍需重新进行视觉检查。文件哈希与几何验证不能证明动作语义正确。

完整帧图集中保存在 frames.zip，内部路径与 manifest.json 一致，逐个保留原始 PNG 字节与哈希。无需解压即可重建。frames/ 是可选展开缓存；网页上先前已上传的部分展开帧也可直接预览，缺少缓存不影响复现。若缓存存在，验证工具仍会核对它与冻结版本的一致性。

## 重新导出预览

```bash
python tools/render_previews.py --atlas pets/deepseek-chan/versions/1.0.1/spritesheet.png --output dist/previews
python tools/preview_transitions.py --atlas pets/deepseek-chan/versions/1.0.1/spritesheet.png --compare pets/deepseek-chan/versions/1.0.0/spritesheet.png --output dist/transitions
```

PNG/GIF 导出仅需 Pillow；如已安装 ffmpeg，可给第一条命令增加 `--ffmpeg ffmpeg` 导出 MP4。各状态预览循环一轮动作，采用已核查的逐帧时长；默认三轮回落、任意帧中断等行为由切换预览单独展示。预览不修改客户端。
