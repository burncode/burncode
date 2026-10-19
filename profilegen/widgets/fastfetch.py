# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
"""User-configured fastfetch-style SVG with local editable ASCII logo templates.
Based on user-supplied ascii-fetch-svg-expanded; no hardware probing or network calls.
"""
from pathlib import Path
from html import escape
import hashlib
import re
from ..svg import Canvas

LOGOS = Path(__file__).with_name('fetch_logos')
FIELD_KEYS=('OS','Host','Device','Type','CPU','GPU','RAM','Storage','Display','Editor','Shell','Terminal','WM','Uptime','Kernel','Theme')

def available_logos():
    """Discover every installed ASCII logo; no OS whitelist or alias."""
    return sorted(p.stem for p in LOGOS.glob('*.txt') if p.is_file())


def _logo_lines(name):
    """Load exactly the selected logo, never silently show another OS."""
    if not isinstance(name, str) or not re.fullmatch(r'[a-z0-9_-]{1,64}', name):
        raise ValueError(f'Invalid device.logo: {name!r}')
    path = LOGOS / (name + '.txt')
    if not path.is_file():
        raise ValueError(f'Unknown device.logo {name!r}; available: {", ".join(available_logos())}')
    return path.read_text(encoding='utf-8').splitlines()

def render(canvas,cfg,y,options):
    c=canvas.c; info=cfg.get('device',{})
    fields=[(k,str(info[k])) for k in FIELD_KEYS if info.get(k)]
    logo_name=str(info.get('logo') or 'windows11').lower()
    lines=_logo_lines(logo_name)
    # Compact rows; the ASCII block is scaled to the available left rail.
    cell_w=6.7; line_h=11.0
    columns=max((len(re.sub(r'\$[1-9]','',line)) for line in lines),default=0)
    scale=min(1.0,220/max(1,columns*cell_w),210/max(1,len(lines)*line_h))
    char_w=cell_w*scale; char_h=line_h*scale
    logo_h=len(lines)*char_h
    field_h=max(1,len(fields))*25
    content_h=max(logo_h,field_h)
    h=max(190,int(83+content_h+24))
    canvas.rect(1,y,1098,h,stroke=c['border'])
    username=cfg.get('profile',{}).get('username','developer')
    host=str(info.get('hostname') or 'workstation')
    cmd=str(info.get('command') or 'fastfetch')
    canvas.text(28,y+34,f'{username}@{host}:~$',14,c['accent'],True)
    canvas.text(274,y+34,cmd,13,c['muted'],max_width=690)
    canvas.line(28,y+49,1070,y+49,color=c['border'])
    top=y+67
    logo_top=top+(content_h-logo_h)/2
    seed=str(info.get('color_seed') or username)
    digest=hashlib.sha256(seed.encode('utf-8')).digest()
    # Muted multi-accent highlights at character/run level, seeded and stable.
    # The ASCII text remains readable without SVG animation support.
    def blend(a,b,t):
        try:
            aa=[int(a[j:j+2],16) for j in (1,3,5)]
            bb=[int(b[j:j+2],16) for j in (1,3,5)]
            return '#'+''.join(f'{round(v*(1-t)+w*t):02x}' for v,w in zip(aa,bb))
        except (ValueError,IndexError):return a
    base=blend(c['foreground'],c['muted'],0.27)
    accents=[c['accent'],blend(c['accent'],c['foreground'],0.42),blend(c['accent'],c['muted'],0.50)]
    animated=bool(info.get('logo_animate',False))
    for i,line in enumerate(lines):
        x=45; active=0; col=0
        for token in re.split(r'(\$[1-9])',line):
            if not token:continue
            if re.fullmatch(r'\$[1-9]',token):
                active=int(token[1:]);continue
            # Segment text into short runs, rather than coloring a full horizontal row.
            for chunk in re.findall(r'\s+|[^\s]{1,3}',token):
                if not chunk.strip():x+=len(chunk)*char_w;col+=len(chunk);continue
                pick=digest[(i*7+col*3+active)%len(digest)]
                selected=pick%11 in (0,1,2,3) or (active>0 and pick%6==0)
                color=accents[pick%len(accents)] if selected else base
                yy=logo_top+(i+1)*char_h
                node=f'<text x="{x:.2f}" y="{yy:.2f}" xml:space="preserve" font-family="Consolas,DejaVu Sans Mono,monospace" font-size="{char_h:.2f}" fill="{escape(color)}">{escape(chunk)}'
                if selected and animated:
                    delay=((digest[(i+col)%len(digest)]%19)/10)
                    node+=f'<animate attributeName="opacity" values="1;0.24;1" dur="2.1s" begin="{delay:.1f}s" repeatCount="indefinite"/>'
                canvas.raw(node+'</text>')
                x+=len(chunk)*char_w;col+=len(chunk)
    # Keep values close to the longest label; no oversized fixed label rail.
    from ..text import width as text_width
    label_size=12
    label_start=318
    for i,(key,value) in enumerate(fields):
        yy=top+16+i*25+(content_h-field_h)/2
        canvas.text(label_start,yy,key+':',12,blend(c['foreground'],c['muted'],0.38),True)
        value_x=label_start+text_width(key+':',label_size)+19
        canvas.text(value_x,yy,value,12,c['muted'],max_width=1070-value_x)
    return h
