# 更新角色与新增角色

## 稳定 id 与独立版本

- 一个角色固定使用一个 id，例如 deepseek-chan。不要把账号专属 Pet ID 放进仓库。
- 已发布版本目录保持不变。修改角色画面、帧或配置时，新建版本目录并记录改动。
- 新角色放到 pets/<新id>/versions/<版本>/，在 catalog.json 中增加一项。
- 每个角色的 latest 独立；角色标签使用 <id>-v<版本>，避免多角色版本冲突。整个画廊的 GitHub Release 使用 v<版本>；本次 v1.0.1 与 deepseek-chan-v1.0.1 指向同一提交。
- id 使用小写英文、数字和连字符。版本使用三段数字，例如 1.1.0。
- 建议：文档修订在根文档记录；画面小修用 PATCH，新增动作或明显改版用 MINOR，不兼容格式变更用 MAJOR。

## 导入已经完成的 atlas

工具支持从已经批准的 v2 RGBA PNG 建立版本。它不会生成角色或补齐缺帧：

~~~bash
python tools/add_pet.py --id your-character --name "角色名" --version 1.0.0 --atlas /path/to/approved-spritesheet.png --description "角色描述"
~~~

向同一 id 添加新的版本时使用相同命令并提高版本号；已有版本会被拒绝覆盖。可选 --set-latest 明确更新已经存在角色的 latest。新角色的首个版本自动设为 latest。

工具会创建包含 73 张最终帧的 frames.zip、pet.json、layout.json、manifest.json，登记目录索引，并将视觉检查标记为尚待完成。应补充 sources、预览、来源与语义检查，不能将几何校验当成视觉验收。完成检查后将 manifest.json 的 qa_status 设为 approved 或 approved-with-documented-warnings；打包工具会拒绝尚未完成视觉检查的版本。

## 提交前检查

~~~bash
python tools/gallery.py checksums
python tools/gallery.py verify-files
python tools/gallery.py validate --all
python tools/gallery.py build --all
python -m unittest discover -s tests -v
~~~

实际检查所有状态与十六方向，包括比例、脚底、方向、遮挡、透明边缘、道具与左右手一致性。新视觉请记录来源、参考和生成工具；不要上传访问令牌、签名下载地址、账号专属 ID、私人 Page 引用或原始聊天记录。

## 动作之间的衔接

修改动作前先读 [状态切换约定](docs/TRANSITIONS.md)。检查动作内部循环、自然三轮回落到 idle、任意帧中断、悬停、拖动反向/松手和注视覆盖。第 0 帧同时是状态入口与减少动态效果画面；不能只检查每行最后一帧。

```bash
python tools/preview_transitions.py --atlas pets/deepseek-chan/versions/1.0.1/spritesheet.png --output dist/transitions
```

对比前后版本时增加 `--compare /path/to/before.png`，两版会使用相同的状态事件与客户端快照时长。报告中的轮廓指标只帮助定位跳变，不能代替人工视觉验收，也不能用额外淡化或补间掩盖真实硬切。
