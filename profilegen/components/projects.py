# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
from ..icons.svg_icons import draw as icon_draw
from ..icons.headings import title as section_title
"""Showcase project rows: metadata beneath description, subtle colored tag pills at right."""
from ..i18n import tr
from ..text import width, ellipsize
from ..icons import ICONS, PALETTE, draw_icon

TAG_COLORS = ('#448db9','#a080bd','#5c9a7e','#c18d4b','#b77d7d')

def _metric(canvas,x,y,kind,value,c):
    if value is None or value == 0:return x
    # Tiny outline symbols, visually similar to GitHub repository metadata.
    if kind=='Stars':
        canvas.raw(f'<path d="M{x+7} {y-10} l2.2 5 5.4 .6 -4 3.7 1.1 5.3 -4.7 -2.6 -4.7 2.6 1.1 -5.3 -4 -3.7 5.4 -.6 Z" fill="none" stroke="{c["muted"]}" stroke-width="1.3"/>')
    else:
        canvas.raw(f'<path d="M{x+7} {y-9} v9 m-5 -9 h10 M{x+2} {y-9} v-4 M{x+12} {y-9} v-4" fill="none" stroke="{c["muted"]}" stroke-width="1.4"/>')
    canvas.text(x+22,y,str(value),12,c['muted'])
    return x+22+max(28,width(str(value),12)+15)+15

def render(canvas,cfg,y,options):
    c=canvas.c; projects=cfg['projects'];style={**canvas.theme.get('components',{}).get('projects',{}),**options}
    row_height=max(96,int(style.get('row_height',86)))
    h=42+len(projects)*row_height
    canvas.rect(1,y,1098,h,stroke=c['border'])
    section_title(canvas,'projects',27,y+27,tr(cfg,'projects'),17,'  ·  '+f'{len(projects):02}')
    canvas.text(1050,y+27,'↗ github',12,c['muted'],anchor='end')
    canvas.line(1,y+42,1099,y+42)
    fallback=canvas.theme.get('icons',{}).get('projects',[])
    for i,p in enumerate(projects):
        top=y+42+i*row_height
        accent=PALETTE.get(p.get('icon_color','auto'),('#429fe3','#f0a643','#ec7972')[i%3])
        icon_name=p.get('icon') or (fallback[i%len(fallback)] if fallback else ICONS[i%3])
        canvas.text(27,top+row_height/2+5,f'{i+1:02}',15,c['foreground'])
        draw_icon(canvas,84,top+(row_height-42)/2,icon_name,accent,42,style.get('icon_variant','outline'))
        x=145
        canvas.text(x,top+25,p['name'],17,c['foreground'],True,max_width=570)
        canvas.text(x,top+48,p['description'],13,c['muted'],max_width=575,family='reading')
        # language + Stars + Forks all appear on a single calm metadata line.
        meta_y=top+76
        language=p.get('language') or (p.get('tags') or [''])[0]
        if language:
            canvas.rect(x,meta_y-10,7,7,accent,radius=4)
            canvas.text(x+15,meta_y,language,12,c['foreground'],max_width=155)
        xx=x+max(115,min(175,width(language,12)+28))
        xx=_metric(canvas,xx,meta_y,'Stars',p.get('stars'),c)
        _metric(canvas,xx,meta_y,'Forks',p.get('forks'),c)
        # Full labels first, wrapping to a second line if necessary. Never ellipsize tags.
        status=tr(cfg,'development') if p['status']=='IN DEVELOPMENT' else p['status']
        canvas.rect(705,top+12,6,6,accent,radius=3)
        canvas.text(717,top+20,status,11,c['muted'],max_width=305,family='reading')
        tx=705; chip_y=top+34
        for j,tag in enumerate(p.get('tags',[])[:5]):
            # Account for Canvas showcase font scaling when measuring.
            tw=max(54,int(width(tag,13.2)+27))
            if tw>335:
                # Very long tags cannot fit the rail: use the full label as
                # a second-line text entry rather than truncate silently.
                canvas.text(707,top+row_height-10,tag,10,c['muted'],max_width=330)
                continue
            if tx+tw>1045:
                tx=705;chip_y=top+64
            if chip_y>top+64 or tx+tw>1045:break
            color=TAG_COLORS[(j+i)%len(TAG_COLORS)]
            from ..icons.registry import tint
            canvas.rect(tx,chip_y,tw,23,c['background'],stroke=tint(color,c['background'],0.48),radius=3)
            canvas.rect(tx+7,chip_y+9,5,5,color,radius=2)
            canvas.text(tx+18,chip_y+16,tag,11,c['foreground'])
            tx+=tw+7
        canvas.text(1062,top+row_height/2+5,'↗' if p.get('url') else '·',18,c['foreground'],anchor='end')
        if i<len(projects)-1:canvas.line(27,top+row_height,1072,top+row_height,style.get('divider_color',c['border']))
    return h
