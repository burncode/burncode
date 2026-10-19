# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
"""Configurable terminal-style closing section in footer."""
from ..text import width

def render(canvas,cfg,y,options):
    settings=cfg.get('closing',{})

    c=canvas.c
    output=str(settings.get('output') or 'Session closed. Ideas still running.')
    h=86
    canvas.rect(1,y,1098,h,stroke=c['border'])
    prefix=str(settings.get('prompt') or cfg['profile']['username']+'@github:~$')
    command=str(settings.get('command') or 'exit')
    canvas.text(25,y+25,prefix,12,c['muted'])
    canvas.text(25+min(width(prefix,12)*1.08+22,430),y+25,command,12,c['accent'])
    canvas.text(42,y+58,output,13,c['muted'],max_width=1000)
    # Static SVG fallback is always visible; SMIL opacity provides optional gentle animation.
    if settings.get('animate',False):
        canvas.raw(f'<rect x="26" y="{y+49}" width="5" height="12" fill="{c["accent"]}"><animate attributeName="opacity" values="1;0.25;1" dur="2.4s" repeatCount="indefinite"/></rect>')
    else:
        canvas.rect(26,y+49,5,12,c['accent'],radius=0)
    return h
