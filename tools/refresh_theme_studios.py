"""Rebuild non-paper studio palettes from theme tokens; preserve approved paper art.

Run from any directory: python tools/refresh_theme_studios.py
This writes only assets/studio/studio-<theme>.svg, not theme settings.
"""
import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets' / 'studio'


def mix(a, b, amount):
    channels = [round(int(a[i:i+2], 16)*(1-amount)+int(b[i:i+2], 16)*amount) for i in (1, 3, 5)]
    return '#' + ''.join(f'{v:02x}' for v in channels)


def generate(theme):
    c = theme['colors']
    bg, fg, accent = c['background'], c['foreground'], c['accent']
    dark = theme['mode'] == 'dark'
    template = 'studio-night.svg' if dark else 'studio-paper.svg'
    root = ET.parse(ASSETS / template).getroot()
    if dark:
        sky = mix(bg, accent, .085)
        palette = {
            '#202a39': bg, '#27344b': sky,
            '#3d5067': mix(bg, fg, .20), '#34445b': mix(bg, fg, .15),
            '#47576b': mix(bg, fg, .24), '#536278': mix(bg, fg, .29),
            '#131924': mix(bg, fg, .045), '#121a2a': mix(bg, fg, .065),
            '#2b364b': mix(bg, accent, .12), '#1e2939': mix(bg, accent, .10),
            '#a68bff': accent, '#9b9ff0': mix(accent, fg, .18),
            '#7585d7': mix(accent, bg, .20), '#7c91e6': mix(accent, fg, .08),
            '#647485': mix(bg, fg, .35), '#657481': mix(bg, fg, .35),
            '#7c8c9b': mix(bg, fg, .42), '#627a93': mix(bg, fg, .34),
            '#6b6a86': mix(bg, accent, .35), '#b9a1bb': mix(fg, accent, .25),
        }
    else:
        # Soft sky close to the page; keep the city readable without a hard frame.
        palette = {
            '#fffdf8': bg, '#f0f0e9': mix(bg, c['border'], .43),
            '#c5c9c0': mix(bg, fg, .23), '#b6bfb7': mix(bg, fg, .29),
            '#d4d6cc': mix(bg, fg, .16), '#30332e': mix(bg, fg, .94),
            '#b65f3d': accent, '#f5f2e9': mix(bg, c['surface'], .65),
            '#94a69b': mix(bg, c['muted'], .55),
            '#7b8276': mix(bg, fg, .48), '#92998c': mix(bg, fg, .40),
        }
    for node in root.iter():
        for attr in ('fill', 'stroke', 'stop-color'):
            value = node.get(attr)
            if value in palette:
                node.set(attr, palette[value])
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    (ASSETS / f'studio-{theme["name"]}.svg').write_text(ET.tostring(root, encoding='unicode')+'\n', encoding='utf-8')


if __name__ == '__main__':
    for path in sorted((ROOT/'profilegen'/'themes').glob('*.json')):
        theme = json.loads(path.read_text(encoding='utf-8'))
        if theme['name'] != 'paper':
            generate(theme)
