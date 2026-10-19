# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
from ..icons.headings import title as section_title
"""Personal introduction and compact, non-interactive highlights."""
from ..i18n import tr
from ..text import width, wrap
from math import ceil

def render(canvas,cfg,y,options):
    c=canvas.c; lines=cfg.get('about',{}).get('lines',[])
    highlights=cfg.get('about',{}).get('highlights',[])
    # Measure with the same effective size as Canvas.text, including density.
    label_size=13.2 if canvas.density=='showcase' else 11.55 if canvas.density=='github' else 11
    x=35; chip_top=76+(len(lines)-1)*28 if lines else 52
    chips=[];row_height=0
    for label in highlights:
        label_lines=wrap(label,990,label_size,max_lines=70)
        w=max(88,ceil(max((width(part,label_size) for part in label_lines),default=0))+38)
        if x+w>1065 and x>35:
            x=35;chip_top+=row_height+10;row_height=0
        chip_height=28+18*(len(label_lines)-1)
        chips.append((x,chip_top,w,chip_height,label_lines))
        row_height=max(row_height,chip_height)
        x+=w+12
    h=chip_top+row_height+22 if chips else (62+(len(lines)-1)*28+22 if lines else 64)
    canvas.rect(1,y,1098,h,stroke=c['border'])
    section_title(canvas,'about',27,y+29,tr(cfg,'about'))
    for i,line in enumerate(lines):canvas.text(35,y+62+i*28,'› '+line,13,c['muted'],max_width=1000,family='reading')
    for x,top,w,chip_height,label_lines in chips:
        canvas.rect(x,y+top,w,chip_height,stroke=c['border'],radius=3)
        canvas.rect(x+10,y+top+11,5,5,c['accent'],radius=2)
        for i,label in enumerate(label_lines):
            canvas.text(x+23,y+top+19+i*18,label,11,c['muted'])
    return h
