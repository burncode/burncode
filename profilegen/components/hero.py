# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
"""Balanced hero: v10 spacing, restrained coral accents, editable studio."""
from . import studio, companion
from ..text import width, ellipsize
from html import escape

def render(canvas,cfg,y,options):
    c=canvas.c;p=cfg['profile'];h=310
    style={**canvas.theme.get('components',{}).get('hero',{}),**options}
    canvas.rect(1,y,1098,h,stroke=c['border'])
    canvas.line(1,y+44,1099,y+44)
    canvas.text(20,y+29,'▶',14,c['accent'])
    canvas.text(43,y+29,p['username']+'@github:~',14,max_width=350)
    nav = cfg.get('header_nav', ['code', 'build', 'explore'])
    nav_text = '[ ' + ' | '.join(nav) + ' ]'
    canvas.text(1034,y+29,nav_text,12,c['muted'],anchor='end',max_width=550)
    companion.render(canvas, y, cfg)
    for i,col in enumerate((c['muted'],c['accent'],c['foreground'])):
        canvas.rect(1053+i*14,y+19,8,8,col,radius=2)
    # Two-focus composition: identity at left, pixel studio at right.
    # System metadata becomes a quiet single-line ribbon, never a competing card.
    size=canvas.theme['typography']['title_size']
    while width(p['username'],size)>590 and size>30:size-=2
    canvas.text(29,y+127,p['username'],size,bold=True,max_width=595)
    cursor_x=min(614,32+width(p['username'],size)+10)
    canvas.raw(f'<rect x="{cursor_x}" y="{y+116}" width="23" height="8" fill="{c["accent"]}"><animate attributeName="opacity" values="1;0.22;1" dur="2.3s" repeatCount="indefinite"/></rect>')
    canvas.text(31,y+160,'// '+p['role'],19,c['accent'],max_width=615)
    canvas.line(31,y+176,31,y+215,c['accent'])
    canvas.text(44,y+193,p['tagline'],16,max_width=600,family='reading')
    canvas.text(44,y+225,p['tagline_zh'],13,c['muted'],max_width=600,family='reading')
    for i,tag in enumerate(p['tags'][:4]):
        x=30+i*155
        canvas.rect(x,y+237,147,25,stroke=style.get('tag_border',c['border']),radius=2)
        canvas.rect(x+8,y+246,7,7,('#3998e5','#f47a54',c['muted'],'#a987df')[i],radius=4)
        short={'developer tools':'dev tools','creative coding':'creative code'}.get(tag.lower(),tag)
        canvas.text(x+22,y+254,short,11,max_width=117)
    system=p.get('system',{})
    preferred=[('MODE','MODE'),('FOCUS','FOCUS'),('WORK','WORK')]
    tokens=[f'{label}: {system[key]}' for key,label in preferred if system.get(key)]
    canvas.line(28,y+273,674,y+273,style.get('system_divider','#e4e5e6' if canvas.theme.get('mode')=='light' else '#3d4147'))
    canvas.text(31,y+294,'   ·   '.join(tokens),12,c['muted'],max_width=635)
    scene=options.get('scene') or cfg.get('studio',{}).get('scene') or canvas.theme.get('studio',{}).get('scene','night_city')
    scale=style.get('studio_scale',1.0)
    sw,sh=398*scale,243*scale
    asset = style.get('studio_asset') or canvas.theme.get('studio',{}).get('asset')
    if asset:
        studio.render_asset(canvas,694+(398-sw)/2,y+52+(243-sh)/2,sw,sh,asset)
    else:
        studio.render(canvas,694+(398-sw)/2,y+52+(243-sh)/2,sw,sh,scene)
    return h
