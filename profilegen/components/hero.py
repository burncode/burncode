# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
"""Balanced hero: v10 spacing, restrained coral accents, editable studio."""
from . import studio, companion
from ..text import width

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
    # Center the text/illustration pair with 90-unit outer margins.
    # A bounded text column keeps long introductions clear of the studio.
    size=canvas.theme['typography']['title_size']
    while width(p['username'],size)>400 and size>30:size-=2
    canvas.text(90,y+127,p['username'],size,bold=True,max_width=400)
    cursor_x=min(509,103+width(p['username'],size))
    canvas.raw(f'<rect x="{cursor_x}" y="{y+116}" width="23" height="8" fill="{c["accent"]}"><animate attributeName="opacity" values="1;0.22;1" dur="2.3s" repeatCount="indefinite"/></rect>')
    canvas.text(92,y+171,'// '+p['role'],19,c['accent'],max_width=440)
    canvas.line(92,y+194,92,y+254,c['accent'])
    canvas.text(105,y+216,p['tagline'],16,max_width=440,family='reading')
    canvas.text(105,y+248,p['tagline_zh'],13,c['muted'],max_width=440,family='reading')
    scene=options.get('scene') or cfg.get('studio',{}).get('scene') or canvas.theme.get('studio',{}).get('scene','night_city')
    scale=style.get('studio_scale',1.0)
    sw,sh=398*scale,243*scale
    asset = style.get('studio_asset') or canvas.theme.get('studio',{}).get('asset')
    if asset:
        studio.render_asset(canvas,612+(398-sw)/2,y+55.5+(243-sh)/2,sw,sh,asset)
    else:
        studio.render(canvas,612+(398-sw)/2,y+55.5+(243-sh)/2,sw,sh,scene)
    return h
