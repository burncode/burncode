"""Create a local side-by-side gallery for the three pixel companions."""
from pathlib import Path
import sys
import base64

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import build
from profilegen.svg import Canvas, svg_document
from profilegen.components import companion

panels=[]
for theme in ('paper','violet'):
    for character in companion.CHARACTERS:
        pictures=[]
        for motion in ('walk','story')+tuple(companion.NATIVE_ACTIONS):
            native=companion.NATIVE_ACTIONS.get(motion)
            if native and native not in companion._pack()['characters'][character]['actions']:continue
            canvas=Canvas(build.load_theme(theme),width=260)
            canvas.density='showcase'
            companion.render(canvas,0,{'companion':{'character':character,'animation':motion,'duration':8,'banner':'Hello!','sequence':['walk','idle','sleep','banner','walk']}},track=(155,155))
            encoded=base64.b64encode(svg_document(canvas,48,character).encode()).decode()
            pictures.append(f'<div>{motion}<img alt="{character} {motion}" src="data:image/svg+xml;base64,{encoded}"></div>')
        extra='<details><summary>全部原版动作 / All original actions</summary>'+''.join(pictures[2:])+'</details>'
        panels.append(f'<section style="background:{canvas.c["background"]};color:{canvas.c["foreground"]}"><h2>{theme} · {character}</h2>'+''.join(pictures[:2])+extra+'</section>')
(ROOT/'cat-preview.html').write_text('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Pixel cats</title><style>body{background:#ddd;font:14px system-ui;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;padding:20px}section{padding:16px}h2{font-size:15px}img{display:block;width:100%;height:auto}section>div,details>div{margin:16px 0}summary{cursor:pointer;padding:8px 0}@media(max-width:750px){body{grid-template-columns:1fr}}</style>'+''.join(panels),encoding='utf-8')
