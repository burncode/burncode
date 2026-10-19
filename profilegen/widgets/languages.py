# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
"""Manually configured language usage widget; no inferred skill claims."""
from ..text import width
from ..icons.headings import title as section_title
from ..i18n import tr

def render(canvas,cfg,y,options):
    data=cfg.get('widgets',{}).get('languages',{})
    items=data.get('items',[])
    c=canvas.c; h=110
    canvas.rect(1,y,1098,h,stroke=c['border'])
    section_title(canvas,'languages',26,y+30,tr(cfg,'languages'),17)
    canvas.text(1070,y+29,tr(cfg,'github_data') if data.get('source')=='github' and items else (tr(cfg,'manual_data') if items else tr(cfg,'no_data')),11,c['muted'],anchor='end')
    x=27; total=sum(v['value'] for v in items)
    palette=[c['accent'],c['foreground'],c['muted'],'#7E9DAD','#B38A66','#8F80A8']
    if total:
        for i,item in enumerate(items):
            seg=1044*item['value']/total
            canvas.rect(x,y+47,seg,13,palette[i%len(palette)],radius=0)
            x+=seg
    if not total:
        canvas.text(27,y+80,tr(cfg,'no_languages')+' · python build.py --refresh-data',13,c['muted'])
    x=27
    for i,item in enumerate(items):
        if x>1040:break
        canvas.rect(x,y+76,7,7,palette[i%len(palette)],radius=0)
        label=f"{item['name']} {item['value']/total*100:.0f}%" if total else item['name']
        canvas.text(x+13,y+84,label,12,c['foreground'],max_width=158)
        x+=min(195,max(105,width(label,12)+33))
    return h
