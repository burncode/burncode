## v12.9.8

- Restore original standalone terminal motto (`echo $MOTTO`) with alternating emphasis and cursor.
- Fix Social ordering in the official README by flushing its links before the next section, including spacer strips.
- Social is now strictly opt-in via `layout`; no implicit insertion after About.
- Add ordering, disable, and motto regression tests.

## v12.9.7

- Restored motto as its own layout block, separate from the terminal footer.
- Footer now renders `closing`; motto only renders `motto` lines.
- Added author, email, copyright and MIT license headers to all Python scripts.
- Updated documentation and tests.

## v12.9.6

- Restored visible motto text alongside the configurable terminal closing output.
- Reduced closing output contrast to match Fastfetch values.
- Made Fastfetch label/value gap content-aware, with a compact one-character-space-like separation.

## v12.9.5

- All section headings use custom SVGs; one consistent default icon when missing.
- Workflow refreshes all supported remote data caches and generated README sections.
- Expanded ICONS.md and bilingual automation documentation.

## v12.9.4

- Fastfetch: reduce label/value horizontal gap by 30px; make seeded logo highlights more visible and quicker to pulse.
- Hero: add a subtle breathing animation to the cursor beside the username.
- Social: reduce vertical toolbar margins in the six-mode preview.

# v12.9.2

- Configurable closing terminal prompt, command, output and optional subtle cursor animation.
- Fastfetch label/value contrast and `Label:` spacing refined; removed Model and redundant default Terminal.
- No bundled font binaries or external font downloads; retained legacy icon SVG resources required by compatibility tests.
