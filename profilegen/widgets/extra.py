# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
"""Optional, data-grounded compact widgets; no invented account metrics."""
from ..text import ellipsize
from ..icons.headings import title as section_title

def stats(canvas,cfg,y,options):
    c=canvas.c;h=72
    canvas.rect(1,y,1098,h,stroke=c['border'])
    projects=cfg.get('projects',[])
    stars=sum(p.get('stars') or 0 for p in projects)
    forks=sum(p.get('forks') or 0 for p in projects)
    section_title(canvas,'github_stats',27,y+27,'selected project stats')
    canvas.text(33,y+55,f'{len(projects)} featured projects    ·    {stars} stars    ·    {forks} forks',13,c['muted'])
    return h

def building(canvas,cfg,y,options):
    c=canvas.c;h=78
    canvas.rect(1,y,1098,h,stroke=c['border'])
    section_title(canvas,'currently_building',27,y+27,'currently building')
    for i,p in enumerate(cfg.get('projects',[])[:3]):
        canvas.text(35+i*355,y+56,'› '+p['name'],13,c['muted'],max_width=325)
    return h


def focus(canvas,cfg,y,options):
    from ..i18n import tr
    c=canvas.c; items=cfg.get('development_focus',{}).get('items',[])
    h=54+len(items)*38
    canvas.rect(1,y,1098,h,stroke=c['border'])
    section_title(canvas,'development_focus',27,y+29,tr(cfg,'development_focus'))
    for i,item in enumerate(items):
        yy=y+60+i*38
        canvas.rect(33,yy-10,6,6,c['accent'],radius=3)
        canvas.text(50,yy,item['label'],13,c['foreground'],True,max_width=260)
        canvas.text(240,yy,item['detail'],12,c['muted'],max_width=800)
    return h

def releases(canvas,cfg,y,options):
    from ..i18n import tr
    c=canvas.c;items=cfg.get('_releases',[])
    h=57+max(1,len(items))*35
    canvas.rect(1,y,1098,h,stroke=c['border'])
    section_title(canvas,'recent_releases',27,y+29,tr(cfg,'recent_releases'))
    if not items:canvas.text(36,y+66,tr(cfg,'no_data'),13,c['muted'])
    for i,item in enumerate(items):
        yy=y+65+i*35
        canvas.rect(31,yy-12,6,6,c['accent'],radius=3)
        canvas.text(46,yy,item['repo'],13,c['foreground'],True,max_width=350)
        canvas.text(430,yy,item['tag'],12,c['accent'],max_width=210)
        canvas.text(670,yy,item.get('date',''),12,c['muted'],max_width=300)
    return h


def blog(canvas,cfg,y,options):
    """Quiet editorial links; individual rows stay clickable in modular README."""
    from ..i18n import tr
    from ..text import width
    c=canvas.c;posts=cfg.get('_blog_posts',cfg.get('widgets',{}).get('blog',{}).get('posts',[]))
    h=51+36*max(1,len(posts))
    canvas.rect(1,y,1098,h,stroke=c['border'])
    section_title(canvas,'blog',27,y+29,tr(cfg,'blog'))
    if not posts:canvas.text(36,y+75,tr(cfg,'no_data'),12,c['muted'])
    for i,post in enumerate(posts):
        yy=y+51+i*36
        title=post['title']
        canvas.text(35,yy+22,title,12,c['muted'],max_width=990,family='reading')
        length=min(990,width(title,13.2))
        canvas.line(35,yy+26,35+length,yy+26,color=c['border'])
    return h
