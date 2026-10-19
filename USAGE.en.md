# burncode GitHub Profile — Complete Guide (v12.7)

This release was rebuilt from the supplied v12.5 source. The official `README.md` now uses independently linkable SVG sections; there is no separate experimental Modular README.

## Quick start

Python 3.10+; no third-party Python packages required.

```powershell
python .\build.py --check
python .\build.py --preview
python .\build.py --refresh-data --preview
python .\build.py --offline --preview
python -m unittest discover -s tests -q
```

Open `preview.html` locally. `--refresh-data` fetches external GitHub/feed data and caches it in `.cache/`; `--offline` never accesses the network. Use `--force` only if you intentionally want to overwrite a manually changed generated file. Use `python build.py --help` for all CLI flags.

## Generated files

- `README.md`: the only official README, with clickable social/project/blog/release images.
- `assets/sections/<light-or-dark-theme>/*.svg`: generated section assets; do not edit manually.
- `preview.html`: interactive preview of the official README.
- `config.json`: source of truth for settings.
- `profilegen/`: SVG renderers, themes, localizations, icons and providers.
- `ICONS.md`: exact manual Tabler icon file names.

## Layout, ordering, and Social

All visible components are controlled by `layout`. Reorder entries to reorder sections; set `enabled:false` to hide them.

```json
"layout": [
  {"type":"hero","enabled":true},
  {"type":"about","enabled":true},
  {"type":"social","enabled":true},
  {"type":"projects","enabled":true},
  {"type":"activity","enabled":true},
  {"type":"blog","enabled":true},
  {"type":"device","enabled":true},
  {"type":"motto","enabled":true}
]
```

Supported types: `hero`, `about`, `social`, `projects`, `languages`, `activity`, `github_stats`, `currently_building`, `development_focus`, `recent_releases`, `blog`, `device`, `motto`, `footer`. Data widgets also require `widgets.<type>.enabled=true`. A legacy config with no Social layout entry inserts it after About for compatibility; specify it explicitly in new configs.

Configure up to six social links in the top-level `social` list:

```json
"social": [
  {"label":"GitHub","url":"https://github.com/burncode","icon":"github","display":"both"},
  {"label":"Repositories","url":"https://github.com/burncode?tab=repositories","icon":"website","display":"both"}
]
```

`display` is `icon`, `text`, or `both`. Each Social button is an independently clickable linked SVG; its layout position is not fixed.

## Device / Fastfetch

Device data is manual, not a live hardware probe. The `Vendor` field has been removed. Optional fields include `OS`, `Host`, `Device`, `Type`, `CPU`, `GPU`, `RAM`, `Storage`, `Display`, `Editor`, `Shell`, `Terminal`, `WM`, `Uptime`, `Kernel`, `Theme`, `hostname`, `command`, `color_seed`.

```json
"device": {
  "logo":"windows",
  "hostname":"workstation",
  "command":"fastfetch --logo small",
  "OS":"Windows 11",
  "Device":"Desktop PC",
  "Model":"Developer Rig",
  "RAM":"32 GB",
  "Editor":"Emacs"
}
```

`device.logo` uses a **short identifier, not an SVG filename**: `windows`, `linux`, `ubuntu`, `arch`, `macos`, `debian`, `fedora`, `generic`. For example, `windows` maps to `brand-windows.svg` and `macos` to `brand-apple.svg`.

## Tabler Icons

Download SVG files manually from https://tabler.io/icons, preferably 24×24 Outline, and place them in `profilegen/icons/vendor/tabler-official/outline/`. Optional `filled/` and `dashed/` folders are available. Keep exact names such as `brand-github.svg`; avoid duplicate-name suffixes like `(1)`. See `ICONS.md` for the full mapping. Missing icons use a fallback.

## Profile, About, and Projects

`profile` contains `username`, `role`, `tagline`, `tagline_zh`, up to four `tags`, `system` fields, and up to eight `links`. `about.lines` contains up to four lines of biography; `about.highlights` up to three short tags. Projects (up to 12) contain `name`, `description`, `tags`, `status`, `url`, `icon`, `icon_color`, optionally `repository` (`owner/repo`), `stars`, and `forks`. A project row is clickable only if its `url` is present.

## Languages, Stats, Releases, Blog

`widgets.languages`: `enabled`, `source` (`manual` or `github`), `mode` (`selected` or `profile`), `repositories` (`owner/repo`), `max_repositories` (1–20), `cache_hours`, and `items`. Manual items have `{ "name":"Python", "value":65 }` entries with nonnegative values. Selected mode uses `projects[].repository` when no explicit repositories are provided. Cache: `.cache/languages.json`.

`widgets.github_stats.enabled` controls the stats widget. Data comes from selected projects and cached account data; unavailable metrics are not fabricated.

`widgets.recent_releases`: `enabled`, `repositories` (up to five), `max_repositories` (1–5), `cache_hours`. Cache: `.cache/releases.json`; release rows are clickable.

`widgets.blog`:

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

`source` is `manual`, `rss`, or `atom`. Manual posts contain `title`, `url`, optional `date`. Feed results are cached in `.cache/blog_feed.json`. Run `python build.py --refresh-data --preview` to refresh. For Hexo, fix a placeholder `yoursite.com` in `_config.yml` and redeploy before refreshing.

## Themes, locale, companion and image

`themes.light` and `themes.dark` select active light/dark themes; both must be in `themes.generate`. `colors` overrides theme colors. `i18n.locale` selects `zh-CN` or `en-US`, with translation resources under `profilegen/locales/`. `header_nav` configures header navigation labels. `header_cat` enables the animated cat. `companion.character` selects one of six cats; `animation` selects a native action or `wander`, `static`, or `story` (`duration` 4–60 seconds). `sequence` accepts 1–16 actions; `outline` accepts `auto`, `off`, or `on`. See the Pet Cats Pack catalog below. `studio.scene` selects a scene; `studio_image` optionally points to a local PNG/JPG/WebP/GIF. `now` and `motto` contain short text lists. `layout_mode` accepts `showcase` or `github`, while the official linked-section output uses showcase coordinates.

## Publishing and troubleshooting

Publish `README.md` and `assets/sections/` in a public repository named exactly like your GitHub username. You can also commit source files for automatic rebuilds. There is no `README.modular.md`, `assets/modular/`, or `preview-modular.html` in the official output.

If overwrite protection triggers, back up manually edited files before using `--force` once; repeated builds should normally work without it. If links do not work, verify `layout`, URLs and outer `<a href>` wrappers. If icons are missing, check exact filenames and paths. If GitHub languages or blog posts are empty, check the selected repositories, feed URL, cache and refresh status. Verify the final GitHub rendering because the platform may sanitize some HTML attributes.


Theme mode labels belong beside the names in `themes.generate`, for example
`"generate": {"paper": "light", "violet": "dark"}`. No separate theme catalog
field is needed. Labels must match each theme file's `mode`; they do not recolor
themes. The legacy array of theme names remains supported.

## Custom SVG icons (v12.8)

Icons can come from any SVG library. Put them in `profilegen/icons/custom/outline/` using the filenames listed in `ICONS.md` (for example `brand-github.svg`). Optional filled and dashed variants go into sibling directories. The old Tabler path is a compatibility fallback only. Respect your chosen icon library's license. `device.logo` still accepts short names such as `windows`. `preview.html` compares Light/Dark at 720/900/1100px using the official clickable README.


## ASCII fetch logos

Device logos now use local editable ASCII templates in `profilegen/widgets/fetch_logos/*.txt`, adapted from the supplied ascii-fetch-svg-expanded. `device.logo` selects a short template name. Sparse accent coloring is deterministic via `device.color_seed`. Device fields are configured manually, not auto-detected. Social button backgrounds and labels follow the active theme.


### ASCII fetch logo selection (v12.9.1)

`device.OS` is arbitrary display text; `device.logo` is the exact stem of a `.txt` file in `profilegen/widgets/fetch_logos/`. For example, `"logo": "arch"` selects `arch.txt`. Add `nixos.txt` and use `"logo": "nixos"` without editing Python. Invalid logo names produce a clear error instead of silently displaying another OS. Run `python build.py --preview` after editing `config.json` and hard-refresh the browser.

## v12.9.2: Closing terminal and device fields

`closing` supports `prompt`, `command`, `output`, and `animate` (subtle optional cursor animation, default false). Legacy `motto` lines remain a fallback for the output. `Model` is removed. `Shell` and `Terminal` remain optional, but only Shell is shown by default. The project ships no external font binaries; theme `fonts` are system fallback font-family stacks. Legacy SVG icon assets remain for backward compatibility; these are not font files.


## Automatic updates via GitHub Actions

`.github/workflows/update-profile.yml` runs daily at 06:17 UTC and supports manual **Actions → Refresh GitHub profile → Run workflow**. Enable **Read and write permissions** for workflow tokens in repository settings.

The workflow runs `python build.py --check --no-color` followed by `python build.py --refresh-data --no-color`, then commits the generated `README.md`, `assets/sections/`, and supported `.cache/*.json` files.

| Source | Auto-refresh condition | Cache |
|---|---|---|
| Repository stars/forks | Valid `projects[].repository` | `.cache/github.json` |
| Public account statistics | Valid `profile.username` | `.cache/account.json` |
| Contributions | GitHub data available | `.cache/contributions.json` |
| Languages | Enabled, `source=github` | `.cache/languages.json` |
| Releases | Enabled with repositories | `.cache/releases.json` |
| RSS/Atom blog | Enabled, valid `feed_url` | `.cache/blog_feed.json` |

Manual-only: profile copy, project descriptions, Now, device hardware, social links, themes, SVG icons, ASCII logos. Remote refresh failure retains available cache; it never invents metrics. For manual language or blog data, use `source=manual`. Run `python build.py --offline --preview` to build from cache only. Never commit API tokens. GitHub scheduled runs may be delayed or paused.

## Separate footer and motto

`footer` renders the configurable terminal command and output (`closing`); `motto` renders the standalone motto lines. Each has its own `layout` toggle and position. Python source headers include author, email, copyright, and MIT license.

### Hero introduction

The header username, navigation and companion retain their settings. The main area contains the username, role and bilingual introduction beside the studio illustration. Use about.highlights for interests and device for workstation details. Remove retired profile.tags, profile.system and theme components.hero.tag_border fields from old configurations; validation reports them as errors. Project tags (projects[].tags) are unchanged.

### Original Pet Cats Pack

The header uses LuizMelo's [Pet Cats Pack](https://luizmelo.itch.io/pet-cat-pack), licensed CC0. Source archive, license, provenance and lossless pixel data are committed. No artwork pixels are redrawn or recolored by theme.

- `classic_cat`: original gray Cat-3.
- `tuxedo_cat`: original black Cat-2; the compatibility name is retained, but the original has no white bib.
- `orange_cat`: original golden-orange Cat-1.
- `spotted_cat`: original spotted Cat-4.
- `fluffy_cat`: original long-haired Cat-5.
- `brown_cat`: original brown Cat-6.
- `walk` plays the original 8-frame walk, `idle` the 10-frame idle, and `static` the original sitting pose.
- `story` follows `companion.sequence`: walking, idle, lie-down/sleep/stretch, and meowing with an auto-sized speech bubble for `banner`. Bubble text is never mirrored.

All native actions are available as `animation` or in a story `sequence` (1–16 entries): `walk`, `run`, `idle`, `sit`, `meow`, `lay_down`, `itch`, `sleep1`, `sleep2`, `lick1`, `lick2`, `stretch`. The author's Cat-3 (`classic_cat`) has no Itch sheet; selecting it reports a clear error. `lay_down` and `stretch` play once and hold their final frame. `sleep` automatically combines lying down, sleeping and waking; `banner` meows with a speech bubble. Existing `wander`, `static` and `story` modes are retained.

```json
"companion": {
  "character": "fluffy_cat",
  "animation": "story",
  "duration": 36,
  "sequence": ["walk", "sit", "lick1", "sleep", "stretch", "banner", "run"],
  "banner": "Hello!",
  "outline": "auto"
}
```

`outline` accepts `auto` (default: a thin silhouette outline for the black cat in dark themes), `off` (unmodified original appearance) or `on` (outline the selected cat in every theme). Original pixel colors remain unchanged.

Pixels and transparency are preserved at integer 2x scale. `duration` controls travel/story timing, while native actions keep their own frame cadence. Run `python tools/preview_cats.py` for all six cats and expandable previews of every original action. `python tools/import_pet_cats.py` rebuilds pixel data from the original archive and requires Pillow; normal profile builds remain standard-library-only.

### Theme illustration maintenance

Each theme selects a matching local studio-<theme>.svg using studio.asset. Illustration backgrounds match the page; reading text uses sans-serif fonts while terminal text and chips retain monospace with explicit CJK fallbacks. Paper artwork stays hand-tuned. After editing other theme colors, run python tools/refresh_theme_studios.py to rebuild their illustrations. Run python tools/preview_themes.py to generate all theme sections and the local theme-preview.html comparison page. The README retains the configured light/dark selection.
