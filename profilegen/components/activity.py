# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
"""Compact contribution-inspired *decorative* activity panel; never fake metrics."""
from ..i18n import tr
from ..icons.headings import title as section_title

def render(canvas,cfg,y,options):
    c=canvas.c
    h=146
    style={**canvas.theme.get('components',{}).get('activity',{}),**options}
    active=style.get('active_color',c['accent'])
    empty=style.get('empty_color',c['surface'])
    canvas.rect(1,y,1098,h,stroke=c['border'])
    stats_on=cfg.get("widgets",{}).get("github_stats",{}).get("enabled",False)
    canvas.line(367 if stats_on else 550,y,367 if stats_on else 550,y+h)
    if stats_on:canvas.line(734,y,734,y+h)
    section_title(canvas,'activity',25,y+29,tr(cfg,'activity'))
    contribution=cfg.get('_contributions')
    if contribution:
        total=contribution.get('total',0)
        canvas.text(25,y+48,f'{total:,} contributions · GitHub',10,c['muted'],max_width=420)
        days=contribution.get('days',[])[-105:]
        # Five rows, 26 weeks; no artificial colors or activity counts.
        for idx,day in enumerate(days):
            col=idx//5; row=idx%5
            level=max(0,min(4,int(day.get('level',0))))
            color=(empty,c['muted'],active,active,active)[level]
            canvas.rect(29+col*15,y+61+row*14,11,10,color,radius=0)
    else:
        canvas.text(25,y+48,tr(cfg,'unavailable')+' · decorative',10,c['muted'],max_width=420)
        for row in range(5):
            for col in range(21):
                canvas.rect(29+col*15,y+61+row*14,11,10,active if (col,row) in ((5,2),(12,3),(19,1),(20,4)) else empty,radius=0)
    nx=393 if stats_on else 577
    section_title(canvas,'now',nx,y+29,tr(cfg,'now'))
    for i,item in enumerate(cfg.get('now',[])[:4]):
        canvas.text(nx+3,y+60+i*20,'› '+item,12,c['muted'],max_width=306 if stats_on else 460)
    if stats_on:
        section_title(canvas,'stats',759,y+29,tr(cfg,'stats'))
        account=cfg.get('_account') or {}
        # These are public profile fields from /users/{username}, not guessed metrics.
        metrics=[('Followers',account.get('followers')),('Following',account.get('following')),
                 ('Public repos',account.get('public_repos')),('Public gists',account.get('public_gists')),
                 ('Featured stars',sum(p.get('stars') or 0 for p in cfg.get('projects',[])) if any(p.get('stars') is not None for p in cfg.get('projects',[])) else None)]
        for i,(label,value) in enumerate(metrics):
            canvas.text(768,y+59+i*18,label,11,c['muted'])
            canvas.text(922,y+59+i*18,str(value) if value is not None else '—',12,c['foreground'],True)
        # Reuse our pixel companion visual as the stat panel signature.
        # Compact static pixel silhouette, independent of animated header.
        canvas.raw(f'<g transform="translate(1036 {y+58})"><path d="M7 18 V5 L18 12 H30 L41 5 V18 H45 V42 H4 V18 Z" fill="{c["foreground"]}"/><rect x="13" y="24" width="5" height="5" fill="{c["background"]}"/><rect x="31" y="24" width="5" height="5" fill="{c["background"]}"/><rect x="23" y="34" width="5" height="4" fill="{c["accent"]}"/></g>')
        return h
    return h
