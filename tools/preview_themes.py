"""Build all themes offline and create a local visual comparison page."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import build


def main():
    panels = []
    for name in build.theme_names():
        theme = build.load_theme(name)
        option = '--light' if theme['mode'] == 'light' else '--dark'
        if build.main(['--offline', '--quiet', option, name]):
            raise RuntimeError(f'Could not generate {name}')
        images = ''.join(f'<img src="assets/sections/{name}/{part}.svg" alt="{name} {part}">' for part in ('hero', 'about', 'project-1', 'activity'))
        panels.append(f'<section><h2>{name}</h2>{images}</section>')
    # Restore the normal README and preview to the configured light/dark pair.
    if build.main(['--offline', '--quiet', '--preview']):
        raise RuntimeError('Could not restore configured theme selection')
    html = '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Theme comparison</title><style>body{margin:0;padding:24px;background:#dcdedf;font:16px system-ui}section{max-width:1100px;margin:0 auto 36px}h2{font-size:18px}img{display:block;width:100%;height:auto;margin-bottom:6px}</style>' + ''.join(panels)
    (ROOT/'theme-preview.html').write_text(html, encoding='utf-8')


if __name__ == '__main__':
    main()
