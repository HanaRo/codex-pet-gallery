# 安装与导入

安装包中有 pet.json、spritesheet.png 和 layout.json。pet.json 是本地客户端角色描述；release.json / manifest.json 是本项目的版本记录，不是另一种客户端配置格式。

## 本地 Codex / 兼容桌面客户端

适用于读取 CODEX_HOME 下 pets 目录的客户端：

1. 完整解压角色安装包。
2. 在 CODEX_HOME/pets 下创建与 pet.json 中 id 相同的目录。装学霸版使用 deepseek-gpt-scholar，蓝发女仆版使用 deepseek-chan。未设置 CODEX_HOME 时，通常为用户主目录下的 .codex/pets。
3. 将 pet.json 和 spritesheet.png 放进同一目录；不要修改 pet.json 中的 spritesheetPath。layout.json 可一同保留。
4. 在客户端的 Settings → Pets 中刷新并选择对应角色。

~~~text
<CODEX_HOME>/pets/deepseek-gpt-scholar/
├── pet.json
├── spritesheet.png
└── layout.json
~~~

升级时先备份该目录，再替换同一角色的文件。它与通过 Pets 插件创建的云端角色记录是两种来源，安装本地包可能显示为另一条角色记录；这里没有携带任何人的云端 Pet ID。

本仓库没有 Windows 独立桌宠程序，也不会安装常驻进程。

## ChatGPT Work / Pets 插件

在支持创建自定义 Pet 的环境中，附上对应版本的 spritesheet.png，并使用该版本 pet.json 中的名称与描述。例如装学霸版可以这样导入。

> 请先校验这张 v2 精灵图，再使用原图创建名为「DeepSeek 娘 · 装学霸版」的 Pet。描述为「披着白龙学霸伪装的 DeepSeek 娘，戴眼镜捧书、书后藏饭」。jumping 状态使用站立左右摇尾巴的画面。

创建属于自己的角色时，不要复用其他账号的 Pet ID。客户端将分配新 ID。

## 网页上传入口

若 Settings → Personalization → Pet 提供 Upload pet，可按界面要求上传素材。当前项目保存的是 v2 的 1536×2288 PNG；若入口只接受 v1 的 1536×1872，不要拉伸或强行上传这个 v2 文件，可优先使用支持 v2 的 Pets 插件或兼容桌面客户端。

不同入口可用性以当前客户端和账号为准。官方背景文档：https://learn.chatgpt.com/docs/pets

## 安装后只吃一会儿

这可能是客户端将工作动作播三轮后回到待机的规则。更换原图、提高分辨率或修改 GIF 循环标记均不会改变这一规则。见仓库 docs/PLAYBACK.md。
