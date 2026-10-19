# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
from pathlib import Path
import xml.etree.ElementTree as ET

ASSET_ROOT = Path(__file__).resolve().parents[2] / 'assets' / 'studio'
SAFE_TAGS = {'svg','g','rect','path','circle','ellipse','polygon','polyline','line','text','defs','linearGradient','stop','animate'}
SAFE_ATTRS = {'x','y','x1','x2','y1','y2','width','height','viewBox','fill','stroke','stroke-width','stroke-linecap','stroke-linejoin','opacity','rx','ry','cx','cy','r','d','points','transform','font-size','font-family','font-weight','offset','stop-color','stop-opacity','preserveAspectRatio','id','attributeName','values','dur','begin','repeatCount','shape-rendering'}


def render_asset(canvas, x, y, w, h, name):
    """Inline a safe local studio SVG; no external images or remote resources."""
    import re
    if not isinstance(name,str) or not re.fullmatch(r'[a-zA-Z0-9_-]+',name):
        raise ValueError('Invalid studio asset name')
    path = ASSET_ROOT / (name + '.svg')
    if not path.is_file():
        raise ValueError(f'Studio asset not found: {name}')
    root = ET.parse(path).getroot()
    for el in root.iter():
        tag = el.tag.rsplit('}',1)[-1]
        if tag not in SAFE_TAGS or any(k.rsplit('}',1)[-1] not in SAFE_ATTRS or k.startswith('{') for k in el.attrib):
            raise ValueError(f'Unsafe SVG element or attribute in {name}: {tag}')
    for node in root.iter():
        if node.tag.rsplit('}',1)[-1] == 'animate':
            if node.get('attributeName') != 'opacity' or node.get('repeatCount') != 'indefinite':
                raise ValueError('Only looping opacity animation is allowed in studio assets')
    viewbox = root.get('viewBox','0 0 354 241')
    if not re.fullmatch(r'[0-9. ]+',viewbox):
        raise ValueError('Invalid studio viewBox')
    # Serialize as a nested inline SVG so GitHub can render it without network access.
    from html import escape
    canvas.raw(f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{escape(viewbox)}" preserveAspectRatio="xMidYMid meet">')
    for el in root:
        canvas.raw(ET.tostring(el, encoding='unicode'))
    canvas.raw('</svg>')

"""Self-contained vector pixel studio scenes, recolored by theme tokens.

Scenes are authored in SVG primitives; no external network or raster assets.
The same viewBox guarantees identical sizing across theme plugins.
"""
SCENES = ('night_city', 'daylight', 'workshop', 'rainy_loft', 'sunset', 'none')


def render(canvas, x, y, w, h, scene='daylight'):
    if scene == 'none':
        return
    c = canvas.c
    s = min(w / 354, h / 241)
    canvas.raw(f'<g transform="translate({x} {y}) scale({s:.5f})">')
    bg, fg, edge, muted, accent = (c[k] for k in ('background','foreground','border','muted','accent'))
    canvas.rect(0,0,354,241,c['surface'],edge,radius=3)
    canvas.rect(9,9,336,157,bg,edge,radius=0)
    # The view is built from pixel blocks, not gradients or external images.
    if scene in ('daylight','sunset','rainy_loft'):
        sky = {'daylight':'#e8edf0','sunset':'#f6e6d9','rainy_loft':'#cfd7df'}[scene]
        canvas.rect(10,10,334,155,sky,radius=0)
        if scene == 'sunset':
            canvas.rect(269,35,27,27,accent,radius=0)
        for i in range(9):
            hh=(39,57,47,69,36,63,50,78,45)[i]
            canvas.rect(12+i*38,165-hh,30,hh, '#bfc6cc' if i%2 else '#aeb8c1',radius=0)
            if scene == 'rainy_loft':
                for j in range(3):
                    canvas.line(17+i*38+j*9,22+j*22,12+i*38+j*9,36+j*22,muted)
    elif scene == 'night_city':
        canvas.rect(10,10,334,155,'#242a35',radius=0)
        for i in range(10):
            hh=(56,81,43,69,91,54,76,60,88,49)[i]
            canvas.rect(10+i*34,165-hh,29,hh,'#3e4653' if i%2 else '#323a47',radius=0)
            for j in range(3):
                canvas.rect(17+i*34,165-hh+10+j*14,5,5,accent if j==1 else '#77808d',radius=0)
        canvas.rect(279,27,14,14,accent,radius=0)
    else:
        for i in range(7):
            canvas.line(16,27+i*19,149,27+i*19,edge)
        for i in range(6):
            canvas.rect(22+i*21,120-(i%2)*12,13,39+(i%2)*12,muted,radius=0)
    # Window mullions and a hanging lamp.
    canvas.rect(172,10,5,155,muted,radius=0)
    canvas.rect(10,89,334,4,muted,radius=0)
    canvas.rect(275,9,3,38,fg,radius=0)
    canvas.rect(253,47,47,8,fg,radius=0)
    canvas.rect(261,55,31,5,accent,radius=0)
    # Desk, legs, monitor, keyboard, plant and a small stack of books.
    canvas.rect(18,195,318,7,fg,radius=0)
    canvas.rect(38,202,7,34,muted,radius=0)
    canvas.rect(308,202,7,34,muted,radius=0)
    canvas.rect(74,131,114,63,fg,radius=0)
    canvas.rect(80,137,102,49,'#f5f6f6' if scene!='night_city' else '#161c25',radius=0)
    canvas.text(94,168,'>_',23,accent)
    canvas.rect(120,194,15,6,muted,radius=0)
    canvas.rect(85,202,88,4,muted,radius=0)
    canvas.rect(294,180,29,15,muted,radius=0)
    canvas.line(308,180,299,164,accent)
    canvas.line(308,180,321,157,accent)
    canvas.rect(292,190,33,5,fg,radius=0)
    canvas.rect(47,184,14,11,fg,radius=0)
    canvas.rect(49,181,10,3,accent,radius=0)
    for i in range(3):
        canvas.rect(276+i*6,141-i*6,5,22+i*6,edge,radius=0)
    # Cat silhouette with visible ears, paws, tail, face and nose.
    canvas.rect(213,158,62,37,fg,radius=0)
    canvas.rect(217,143,15,20,fg,radius=0)
    canvas.rect(259,143,15,20,fg,radius=0)
    canvas.rect(220,147,7,7,accent,radius=0)
    canvas.rect(263,147,7,7,accent,radius=0)
    canvas.rect(220,172,6,6,bg,radius=0)
    canvas.rect(258,172,6,6,bg,radius=0)
    canvas.rect(239,181,7,4,accent,radius=0)
    canvas.rect(218,193,10,11,fg,radius=0)
    canvas.rect(261,193,10,11,fg,radius=0)
    canvas.rect(204,171,10,7,fg,radius=0)
    canvas.rect(199,158,7,20,fg,radius=0)
    canvas.raw('</g>')
