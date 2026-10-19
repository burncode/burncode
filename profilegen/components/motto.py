# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
"""Independent terminal-style motto block (original layout restored)."""
from ..text import width

def render(canvas,cfg,y,options):
    lines=cfg.get('motto',[])
    if not lines:return 1
    c=canvas.c;h=62
    canvas.rect(1,y,1098,h,stroke=c['border'])
    prefix=cfg['profile']['username']+'@github:~$ echo '
    canvas.text(25,y+24,prefix,11,c['muted'])
    canvas.text(25+width(prefix,11)*1.1+12,y+24,'$MOTTO',11,c['accent'],True)
    words=' '.join(lines).split(' ')
    total=sum(width(w+' ',14) for w in words)
    x=max(20,(1100-total)/2)
    for i,w in enumerate(words):
        canvas.text(x,y+46,w,14,c['accent'] if (i%2==1) else c['foreground'],i%2==1)
        x+=width(w+' ',14)*1.1
    canvas.text(min(x+6,1080),y+46,'_',14,c['accent'])
    return h
