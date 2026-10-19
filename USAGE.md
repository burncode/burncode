# burncode GitHub Profile — 完整使用手册（v12.9.3）

> 正式版仅生成一个可点击的 `README.md`；本地 `preview.html` 支持多尺寸与明暗主题对比。

## 1. 目录与工作原理

- `config.json`：全部个人资料、组件排序、社交链接、主题和数据源设置。
- `build.py`：唯一构建入口，使用 Python 标准库。
- `profilegen/`：主题、SVG 渲染器、组件、语言文件、图标和数据提供器。
- `profilegen/icons/custom/outline/`：自己选择的 SVG 图标。
- `assets/sections/<theme>/`：生成的 SVG 区块。**不要手动编辑这些生成文件**。
- `README.md`：唯一正式 GitHub Profile README，引用上述 SVG，项目、文章、社交按钮可分别点击。
- `preview.html`：本地交互预览；GitHub 最终布局仍以实际页面为准。
- `.cache/`：联网获取的 GitHub、Languages、RSS/Atom 等数据缓存。
- `tests/`：单元测试。

## 2. 快速开始

Python 3.10+，无须额外 pip 依赖。在项目根目录 PowerShell 执行：

```powershell
python .\build.py --check
python .\build.py --preview
```

打开 `preview.html`。修改 `config.json` 后重新运行 `python .\build.py --preview` 即可。

```powershell
python .\build.py --refresh-data --preview
python .\build.py --offline --preview
python .\build.py --dry-run
python .\build.py --json --check
python -m unittest discover -s tests -q
```

`--refresh-data` 联网更新缓存；普通构建优先读取缓存；`--offline` 禁止联网。`--force` 仅用于**确认要覆盖自己修改过的生成文件**时，平时不需要。使用 `python build.py --help` 查看其余命令行参数。

## 3. 配置总览

`config.json` 是 JSON 文件，不支持注释。主要字段：

| 字段 | 用途 |
|---|---|
| `profile` | GitHub 用户名、身份、介绍、技术标签、终端系统字段、个人链接 |
| `layout` | **所有可视组件**的顺序和开关（包括 Social） |
| `social` | 社交按钮内容、URL、图标、显示模式 |
| `projects` | 精选项目的名称、简介、标签、仓库与统计 |
| `about` | 关于我的文字与 Highlights |
| `device` | Fastfetch 风格设备信息 |
| `widgets` | Languages、GitHub Stats、Recent Releases、Blog 等数据组件 |
| `themes` / `colors` | 明暗主题、生成主题及颜色覆盖 |
| `i18n` | 中英文界面文案 |
| `companion` / `header_cat` | 像素猫形象、动作、时长及显示开关 |
| `now` / `motto` | 正在做的事情与结尾短句 |
| `studio` / `studio_image` | 头图场景或本地图片 |
| `header_nav` / `layout_mode` | 顶部导航及画布布局偏好 |

## 4. Layout：排序和显示开关

**正式 README 完全按 `layout` 数组顺序生成。** 每种组件最多出现一次。

```json
"layout": [
  {"type":"hero","enabled":true},
  {"type":"about","enabled":true},
  {"type":"social","enabled":true},
  {"type":"projects","enabled":true},
  {"type":"languages","enabled":true},
  {"type":"activity","enabled":true},
  {"type":"blog","enabled":true},
  {"type":"device","enabled":true},
  {"type":"motto","enabled":true}
]
```

支持的类型：`hero`、`about`、`social`、`projects`、`languages`、`activity`、`github_stats`、`currently_building`、`development_focus`、`recent_releases`、`blog`、`device`、`motto`、`footer`。其中 `languages`、`github_stats`、`currently_building`、`development_focus`、`recent_releases`、`blog` 还受 `widgets.<type>.enabled` 控制。设置 `layout[].enabled=false` 可隐藏对应区块；修改顺序即可移动区块。

注意：Social 仅在 `layout` 中明确添加 `{"type":"social","enabled":true}` 时显示；删除该条目或设置 `enabled:false` 即隐藏。Social 的位置严格遵循 `layout` 顺序。

## 5. Social：可点击社交链接

`layout` 决定社交区的位置和显示；顶层 `social` 决定具体按钮，最多 6 个：

```json
"social": [
  {"label":"GitHub","url":"https://github.com/burncode","icon":"github","display":"both"},
  {"label":"Repositories","url":"https://github.com/burncode?tab=repositories","icon":"website","display":"both"}
]
```

`display` 可选 `icon`（仅图标）、`text`（仅文字）、`both`（图文）。按钮各自生成可点击的 SVG 图片，使用外层 HTML `<a>` 链接。图标支持的名字以当前 `build.py` 的校验清单为准。隐藏 Social：把 `layout` 中 `type=social` 的 `enabled` 改为 `false`，无需删除社交数据。

## 6. Profile / About / Projects

`profile.username` 必须是合法 GitHub 用户名。`role`、`tagline`、`tagline_zh` 分别用于身份和简介；`tags` 最多 4 个，`system` 是顶部系统信息键值；`links` 是可选链接数据。

`about.lines` 最多 4 行、每行最多 180 字符；`about.highlights` 最多 3 个短标签。About 中不嵌入无法点击的社交链接，Social 使用独立组件。

`projects` 最多 12 项，每项包括 `name`、`description`、`tags`、`status`、`url`、`icon`、`icon_color`，可选 `repository`（`owner/repo`）、`stars`、`forks`。只有填了有效 `url` 的项目行才可点击；不应填写虚假统计值。

## 7. Device / Fastfetch

Device 是**手工配置**的设备介绍，不会读取你当前电脑硬件。

```json
"device": {
  "logo":"windows",
  "hostname":"workstation",
  "command":"fastfetch --logo small",
  "OS":"Windows 11",
  "Host":"Developer Workstation",
  "Device":"Desktop PC",
  "CPU":"Intel Core i7",
  "GPU":"NVIDIA GeForce",
  "RAM":"32 GB",
  "Storage":"1 TB SSD",
  "Editor":"Emacs",
  "Shell":"PowerShell",
  "logo_animate":true
}
```

**已删除 `Vendor` 字段。** 其他可选设备项：`Type`、`Display`、`WM`、`Uptime`、`Kernel`、`Theme`、`color_seed`。不用的字段直接删除。

`device.logo` 使用 ASCII 模板文件名（不带 `.txt`），与 `OS` 显示文本无关。例：`"logo": "arch"` 对应 `profilegen/widgets/fetch_logos/arch.txt`。可用名称见下方清单；没有系统 SVG 依赖。

## 8. SVG Icons：只用 Custom

图标没有指定来源：你可以挑选任何自己喜欢的 SVG，**按 `ICONS.md` 约定的名称**放进 `profilegen/icons/custom/outline/` 即可。例如 `brand-github.svg`、`terminal.svg`。可选变体分别放 `filled/`、`dashed/`；默认只用 `outline` 就够了。

不需要下载脚本、vendor 目录、字体文件或任何图标依赖。缺失图标不会偷偷替换成其他图标。详细命名表见 `ICONS.md`。

## 9. Languages / GitHub Stats

```json
"languages": {
  "enabled":true,
  "source":"github",
  "mode":"selected",
  "repositories":[],
  "max_repositories":10,
  "cache_hours":168,
  "items":[]
}
```

`source=manual` 时手动填写 `items`：`[{"name":"Python","value":65},{"name":"Ruby","value":35}]`，数值须非负且总和大于 0。`source=github` 时读取 GitHub 语言统计；`mode=selected` 仅统计配置的仓库，若 `repositories=[]` 则尝试从 `projects[].repository` 获取；`mode=profile` 统计个人仓库。缓存路径为 `.cache/languages.json`。

只有仓库列表、模式、用户名与缓存数据相符时才能正确命中缓存。出现“暂无语言数据”时，先检查 `projects[].repository` 是否有真实 `owner/repo`，然后运行 `python build.py --refresh-data --preview`。不要直接把其他仓库的缓存当作当前仓库的数据。

`widgets.github_stats.enabled` 控制统计内容是否启用；数据由项目与账号缓存提供，未获取到的数字不会凭空生成。

## 10. Blog：RSS / Atom / 手动

```json
"blog": {
  "enabled":true,
  "source":"atom",
  "feed_url":"https://burncode.github.io/atom.xml",
  "max_posts":3,
  "cache_hours":12,
  "posts":[]
}
```

`source` 可选 `manual`、`rss`、`atom`；`max_posts` 为 1–5；`cache_hours` 为 1–8760。联网模式需要 `feed_url`；刷新后缓存到 `.cache/blog_feed.json`。手动模式填写 `posts`：`[{"title":"文章标题","url":"https://example.com/post","date":"2026-10-18"}]`。正式 README 的文章标题是独立可点击链接。

如果 Hexo Atom 中的文章链接仍是 `http://yoursite.com/...`，先在博客 `_config.yml` 设置正确 `url` 并重新部署，再刷新缓存。不要把示例文章当成真实发布内容。

## 11. Recent Releases

`widgets.recent_releases` 支持 `enabled`、`repositories`（最多 5 个 `owner/repo`）、`max_repositories`（1–5）、`cache_hours`（1–8760）。开启后通过 GitHub Release 数据与 `.cache/releases.json` 显示最新发布；没有 Release 时允许空状态。Release 条目在正式 README 中独立可点击。

## 12. 主题、翻译、头图与像素猫

- `themes.light` / `themes.dark`：分别选择浅色与深色主题；两者必须包含在 `themes.generate` 中。
- `themes.generate`：指定要生成或校验的主题集合。实际正式 README 只引用 `light` 与 `dark` 对应的两套区块 SVG。
- `colors`：按主题覆盖颜色，键和值需要符合主题加载器约束。
- `i18n.locale`：`zh-CN` 或 `en-US`；翻译词条位于 `profilegen/locales/`。保持两个语言文件的键一致。
- `header_nav`：顶部导航标签；`header_cat`：是否显示猫。
- `companion.character`：`classic_cat`、`tuxedo_cat`、`orange_cat`；`animation`：`wander`、`walk`、`idle`、`static`、`story`；`duration`：4–60 秒；`sequence`：动画动作列表；`banner`：短文字。
- `studio.scene`：使用已有场景；`studio_image`：可选本地 PNG/JPG/WebP/GIF 图片，具体场景列表见源码 `SCENES`。
- `layout_mode`：`showcase` 或 `github`；正式分段输出使用 showcase 宽度，以保证可点击区块坐标一致。

## 13. 发布到 GitHub

GitHub 个人主页要求仓库名与 `profile.username` 一致，并且是公开仓库。提交：

```text
README.md
assets/sections/
config.json
build.py
profilegen/
```

`README.md` 是 GitHub 主页实际显示的文件；不再需要复制 `README.modular.md` 或上传 `assets/modular/`。可用 `preview.html` 本地检查点击区域；GitHub 可能过滤部分 HTML 属性，因此最终效果仍要在真实仓库中核验。

## 14. 常见问题

**反复出现 Refusing to overwrite：** 生成器仅自动覆盖带有自己签名的文件；首次迁移可备份旧 `README.md` 后运行一次 `--force`。后续正常重复运行无需 `--force`。

**社交链接无法点击：** 检查 `layout.social.enabled`、`social[].url`，确认 README 引用 `assets/sections/.../connect-N.svg` 且外层有 `<a href>`。

**社交按钮被拉伸：** 不要给按钮图片设置 `width=100%`；正式模板对 Social 使用独立像素宽度。

**SVG 图标没生效：** 确认文件位于 `outline/` 且文件名与 `ICONS.md` 完全一致；SVG 不要带 `(1)` 等后缀。

**GitHub 统计、语言或博客为空：** 先检查仓库、URL、网络、缓存和 `--refresh-data` 输出，不要捏造数据。

**升级旧版本：** 备份 `config.json`、`.cache/` 和 `profilegen/icons/custom/`，再迁移配置；不要把旧版生成的 README 或 SVG 覆盖到新版本。


## 自选 SVG 图标（v12.8）


`preview.html` 已恢复 720、900、1100px 三档宽度及 Light/Dark 双主题对比，且每档使用正式 README 的可点击区块。


## ASCII Fastfetch 图形

Device 现使用 `profilegen/widgets/fetch_logos/*.txt` 的 ASCII 模板（来自用户提供的 ascii-fetch-svg-expanded）。通过 `device.logo` 选择，例如 `windows`、`ubuntu`、`arch`、`macos`、`debian`、`fedora`，也可直接添加自己的 `myos.txt` 并设为 `myos`，无需改 Python 白名单。颜色根据 `device.color_seed` 稳定生成少量主题强调色；不会每次构建随机变化。所有系统字段来自 `config.json`，不会自动检测设备。

Social 按钮在深色主题中使用对应主题背景与文字色，预览矩阵中的 Social 背景与主题保持一致。


### ASCII 设备 Logo 选择与预览排查（v12.9.1）

- `device.OS` 是右侧纯文字，可写任意系统及版本（例如 `Arch Linux 6.17`），不会决定图案。
- `device.logo` 只对应 `profilegen/widgets/fetch_logos/<名称>.txt`，例如 `arch` → `arch.txt`、`windows11` → `windows11.txt`。
- 可用模板：`almalinux`, `alpine`, `arch`, `centos`, `debian`, `elementary`, `endeavouros`, `fedora`, `gentoo`, `kali`, `linuxmint`, `macos`, `manjaro`, `nixos`, `opensuse`, `popos`, `raspbian`, `rocky`, `ubuntu`, `void`, `windows`, `windows10`, `windows11`, `zorin`。
- 自定义系统只需添加 `.txt` 文件并配置同名 `logo`；未知名称会明确报错，不会偷偷退回 Windows/Arch。
- **编辑配置后需要重新运行** `python build.py --preview`，刷新浏览器页面（Ctrl+F5）；如果还看到旧图案，检查是否编辑了正在运行的项目根目录下的 `config.json`，以及预览是否指向旧版本目录。
- 预览包含多主题/多宽度，生成时都使用当前 `config.json` 的 `device.logo`。

## v12.9.2：结尾终端与设备字段

`closing` 可配置 `prompt`（终端提示符）、`command`（命令）、`output`（输出文本）和 `animate`（是否启用轻微闪烁光标，默认 false）。输出与命令之间留有额外垂直间距。`closing` 属于独立的 `footer` 区块；`motto` 是另一个独立区块。二者均可在 `layout` 中分别开关和排序，互不覆盖。

设备字段不再支持 `Model`，示例默认仅显示 `Shell`，但仍可选填 `Terminal`；两者分别表示命令解释器与终端应用，并非完全同义。设备标签显示为 `OS:  ...`，值使用较高对比度。

本项目没有捆绑、下载或引用外部字体文件；主题中的 `fonts` 只是 SVG 的系统字体回退栈，不是外部字体依赖，否则文字排版会改变。所有外部 SVG 图标只从 `profilegen/icons/custom/` 读取。

## 命令行完整参考（Python build.py）

所有命令均在项目根目录运行；Windows PowerShell 可写成 `python .\build.py ...`。运行 `python build.py --help` 查看当前版本的完整参数。

| 命令 | 作用 | 是否写文件 | 是否联网 |
|---|---|---|---|
| `python build.py` | 按配置重新生成正式 `README.md` 与 `assets/sections/` | 是 | 否，读取已有缓存 |
| `python build.py --preview` | 正式构建并生成 `preview.html`，用于多尺寸明暗预览 | 是 | 否 |
| `python build.py --check` | 校验配置、检查文件状态与当前主题 | 否 | 否 |
| `python build.py --dry-run` | 预演将要新增、修改或保留的文件 | 否 | 否 |
| `python build.py --refresh-data --preview` | 联网更新 GitHub、语言、文章等缓存后重新生成预览 | 是 | 是 |
| `python build.py --offline --preview` | 严格使用本地缓存生成预览，不发网络请求 | 是 | 否 |
| `python build.py --github-status` | 排查仓库识别、缓存与 GitHub 数据来源 | 诊断模式 | 视具体数据路径而定 |
| `python build.py --list-themes` | 列出可用主题名称及明暗类型 | 否 | 否 |
| `python build.py --themes mono` | 只生成 Mono 主题，明暗均使用它 | 是 | 否 |
| `python build.py --themes mono,graphite` | 指定要生成的主题集合 | 是 | 否 |
| `python build.py --light mono --dark graphite` | 显式指定 README 的浅色与暗色主题 | 是 | 否 |
| `python build.py --config my-config.json` | 从指定配置文件读取设置 | 是 | 否 |
| `python build.py --json --check` | 输出适合脚本处理的 JSON 检查结果 | 否 | 否 |
| `python build.py --no-color` | 禁用终端 ANSI 颜色 | 取决于其他参数 | 否 |
| `python build.py --quiet` | 仅显示错误信息 | 取决于其他参数 | 否 |
| `python build.py --force --preview` | 允许覆盖被识别为手动维护的生成文件 | 是，**谨慎** | 否 |
| `python -m unittest discover -s tests -q` | 执行项目自动化测试 | 不写 README | 否 |

**推荐顺序：** 初次运行先 `--check`，随后 `--preview`；配置好真实 GitHub 仓库与博客源后再运行 `--refresh-data --preview`。预览满意后提交 `README.md` 和 `assets/sections/`。`--force` 不要作为日常默认参数。

**常见问题：** `--refresh-data` 不是 GitHub 定时任务，只有你主动运行时才更新；如果 RSS/Atom 或 GitHub 请求失败，会根据缓存和提供器策略回退。`--offline` 与 `--refresh-data` 不应同时用于期望联网更新的场景。`--themes` 指定的主题必须存在于 `profilegen/themes/`。

## Fastfetch Logo 的颜色与动效

`device.logo` 直接匹配 `profilegen/widgets/fetch_logos/<名称>.txt`，不需要 SVG。`device.OS` 只是显示文本，可以包含任意版本号，与 Logo 无关。

- `color_seed`：控制 Logo 上强调色片段的分布；同一配置生成结果稳定，换种子可改变分布。
- `logo_animate`：`true` 时对少量强调色片段施加轻微呼吸动效；`false` 为静态。
- Logo 的主色与信息标签较清晰，设备值使用稍淡的主题次要色。
- GitHub 的 SVG 动画显示受平台渲染限制；即使不播放，静态图形仍可见。

```json
"device": {
  "logo": "arch",
  "OS": "Arch Linux",
  "Host": "Developer Workstation",
  "CPU": "AMD Ryzen",
  "RAM": "32 GB",
  "color_seed": "my-workstation",
  "logo_animate": true
}
```


## GitHub Actions 自动更新（重要）

仓库包含 `.github/workflows/update-profile.yml`，每天 UTC 06:17 运行一次，也可以在 GitHub 仓库的 **Actions → Refresh GitHub profile → Run workflow** 手动触发。请确保仓库的 Actions 权限允许写入内容（Settings → Actions → General → Workflow permissions → Read and write permissions）；若组织策略禁止写入，工作流无法提交结果。

自动执行 `python build.py --check`，然后 `python build.py --refresh-data --no-color`。刷新请求失败时，构建器尽量使用既有缓存，不会编造数字。更新的文件包括正式 `README.md`、`assets/sections/` 和已存在的以下缓存：

| 数据 | 自动更新条件 | 缓存文件 | 无法自动获取时 |
|---|---|---|---|
| 项目 Stars / Forks | `projects[].repository` 填写有效仓库 | `.cache/github.json` | 手动配置项目数据或保留缓存 |
| GitHub 用户统计 | 有效 `profile.username` | `.cache/account.json` | 显示 `—` 或保留缓存 |
| 贡献日历 | GitHub 贡献数据可访问 | `.cache/contributions.json` | 使用缓存；没有缓存时显示装饰占位，不是假数据 |
| 编程语言 | `widgets.languages.enabled=true` 且 `source=github` | `.cache/languages.json` | 改用 `source=manual` 配置 `items`，或保留缓存 |
| 最近发布 | `widgets.recent_releases.enabled=true` 且有仓库 | `.cache/releases.json` | 无数据时显示暂无数据 |
| 博客文章 | `widgets.blog.enabled=true` 且 `source=rss` / `atom`，`feed_url` 有效 | `.cache/blog_feed.json` | 改为 `source=manual` 和 `posts`，或保留缓存 |

**以下内容不会自动发现：** 个人简介、项目说明、Now、Device 硬件配置、社交地址、主题与自定义 SVG/ASCII Logo。这些都需要编辑 `config.json` 或本地素材。

本地首次获取数据：

```powershell
python .\build.py --refresh-data --preview
```

仅使用现有缓存、不联网：

```powershell
python .\build.py --offline --preview
```

如要在 Actions 中保留缓存，应提交 `.cache/*.json`（不要提交任何令牌）；工作流只会暂存上述已知 JSON 文件。`GITHUB_TOKEN` 使用 GitHub Actions 提供的临时令牌，**无需写进配置或仓库**。GitHub Actions 的定时触发在某些情况下可能延迟或暂停；GitHub Pages 博客 RSS 若部署尚未完成，也可能暂时没有新文章。

## Footer 与 Motto（独立区块）

`layout` 中 `footer` 显示终端提示符、命令及输出；`motto` 显示 `config.json` 的 `motto` 短句。二者互相独立，可分别设置 `enabled` 或调整顺序。

Python 源文件顶部统一包含作者、联系邮箱、版权和 MIT 许可信息。
