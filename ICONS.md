# 自定义 SVG 图标清单

本项目**不依赖任何特定图标库**。从你喜欢的来源挑选 SVG，按下表文件名保存即可；请自行确认图标授权。

## 放在哪里

```text
profilegen/icons/custom/
├── outline/    # 默认，建议先用这一个目录
├── filled/     # 可选
└── dashed/     # 可选
```

例如 `github` 对应 `outline/brand-github.svg`，`terminal` 对应 `outline/terminal.svg`。名称是**本项目的文件命名约定**，不是某个外部图标库的专有名称。下载后可以重命名。

## 区块标题图标（最重要）

所有标题都使用 `custom/outline/` 下的 SVG；未提供时显示**相同的默认方框图标**。

| SVG 文件名 | 实际显示位置 |
|---|---|
| `user.svg` | 关于我标题 |
| `folder.svg` | 项目区块标题 |
| `code.svg` | 编程语言标题 / 代码项目 |
| `git-branch.svg` | 动态区块标题 |
| `terminal.svg` | 正在做标题 / 终端项目 |
| `chart-bar.svg` | 统计标题 / 数据类项目 |
| `rss.svg` | 博客区块标题 / RSS |
| `package.svg` | 最近发布标题 / 包管理项目 |
| `tool.svg` | 开发重点标题 / 工具项目 |
| `world.svg` | 联系方式标题 / 网站链接 |

设备 Device 使用 ASCII `.txt` Logo 和命令行标题，底部 Closing 使用终端文字，均不需要区块标题 SVG。

## 文件名称与用途

| 文件名 | 用途 |
|---|---|
| `book.svg` | 阅读类项目图标 |
| `brand-apple.svg` | macOS 系统标志 |
| `brand-arch-linux.svg` | Arch Linux 系统标志 |
| `brand-bilibili.svg` | Bilibili 社交链接 |
| `brand-debian.svg` | Debian 系统标志 |
| `brand-discord.svg` | Discord 社交链接 |
| `brand-fedora.svg` | Fedora 系统标志 |
| `brand-github.svg` | GitHub 社交链接 |
| `brand-instagram.svg` | Instagram 社交链接 |
| `brand-linkedin.svg` | LinkedIn 社交链接 |
| `brand-telegram.svg` | Telegram 社交链接 |
| `brand-ubuntu.svg` | Ubuntu 系统标志 |
| `brand-weibo.svg` | 微博社交链接 |
| `brand-windows.svg` | Windows 系统标志 |
| `brand-x.svg` | X 社交链接 |
| `brand-youtube.svg` | YouTube 社交链接 |
| `brand-zhihu.svg` | 知乎社交链接 |
| `building-monument.svg` | 古建筑项目 |
| `chart-bar.svg` | 统计标题 / 数据类项目 |
| `cloud.svg` | 云端项目 |
| `code.svg` | 编程语言标题 / 代码项目 |
| `cube.svg` | 通用三维项目 |
| `database.svg` | 数据库项目 |
| `device-desktop.svg` | 设备与显示器 |
| `external-link.svg` | 外部链接 |
| `folder.svg` | 项目区块标题 |
| `git-branch.svg` | 动态区块标题 |
| `layout-grid.svg` | 节点与工作流 |
| `mail.svg` | 电子邮件社交链接 |
| `package.svg` | 最近发布标题 / 包管理项目 |
| `photo.svg` | image：标题、项目、工具或状态图标 |
| `puzzle.svg` | puzzle：标题、项目、工具或状态图标 |
| `robot.svg` | AI / Agent 项目 |
| `rss.svg` | 博客区块标题 / RSS |
| `shield.svg` | shield：标题、项目、工具或状态图标 |
| `star.svg` | star：标题、项目、工具或状态图标 |
| `terminal.svg` | 正在做标题 / 终端项目 |
| `tool.svg` | 开发重点标题 / 工具项目 |
| `user.svg` | 关于我标题 |
| `world.svg` | 联系方式标题 / 网站链接 |


## 规则

- SVG 不需要指定 PNG 像素大小，建议保留原始 `viewBox`。
- 只要文件名对应即可，来自哪个图标集都可以；推荐整体线宽和视觉重量接近。
- 颜色建议使用 `currentColor`，以便自动适配明暗主题；多色 SVG 也能加载，但不一定自动换色。
- 缺失文件不会自动下载或使用第三方资源；**统一显示一个中性的方框短横线默认图标**。
- 修改 SVG 后重新运行 `python build.py --preview`；若在同一个 Python 进程内反复生成，需清除图标缓存。
- **Device 左侧 ASCII Logo 不是 SVG**：`device.logo: "arch"` 使用 `profilegen/widgets/fetch_logos/arch.txt`。

## 使用代码

```python
from profilegen.icons.svg_icons import draw
svg = draw('github', 20, 20, 24, '#333333')
svg2 = draw('terminal', 20, 20, 24, '#333333', 'filled')
```

`outline` 为默认变体；没有对应 `filled`/`dashed` 文件时，自动使用 `outline`。
