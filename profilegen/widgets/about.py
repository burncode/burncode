# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
from ..icons.headings import title as section_title
"""Personal introduction and compact, non-interactive highlights."""
from ..i18n import tr
from ..text import width

def render(canvas,cfg,y,options):
    c=canvas.c; lines=cfg.get('about',{}).get('lines',[])
    highlights=cfg.get('about',{}).get('highlights',[])
    h=62+len(lines)*25+(40 if highlights else 0)
    canvas.rect(1,y,1098,h,stroke=c['border'])
    section_title(canvas,'about',27,y+29,tr(cfg,'about'))
    for i,line in enumerate(lines):canvas.text(35,y+57+i*25,'› '+line,13,c['muted'],max_width=1000,family='reading')
    x=35;sy=y+60+len(lines)*25
    for i,label in enumerate(highlights):
        w=max(70,min(280,int(width(label,12)+30)))
        canvas.rect(x,sy-16,w,26,stroke=c['border'],radius=3)
        canvas.rect(x+9,sy-5,5,5,c['accent'],radius=2)
        canvas.text(x+20,sy+2,label,11,c['muted'],max_width=w-28)
        x+=w+10
    return h
