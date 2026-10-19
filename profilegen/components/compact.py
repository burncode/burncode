# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
"""Native 900-unit GitHub layout; no downscaling of the 1100-unit showcase."""
from ..i18n import tr
from ..text import width
from . import studio, companion, projects
from ..icons import draw_icon
from ..icons.headings import title as section_title

W = 900

def hero(canvas, cfg, y, options):
    c=canvas.c; p=cfg['profile']; h=330
    canvas.rect(1,y,W-2,h,stroke=c['border'])
    canvas.line(1,y+44,W-1,y+44)
    canvas.text(17,y+29,'▶',14,c['accent'])
    canvas.text(42,y+29,p['username']+'@github:~',15,max_width=240)
    nav='[ '+' | '.join(cfg.get('header_nav',['code','build','explore']))+' ]'
    canvas.text(840,y+29,nav,12,c['muted'],anchor='end',max_width=235)
    companion.render(canvas,y,cfg,track=(260,560),top=10)
    for i,col in enumerate((c['muted'],c['accent'],c['foreground'])):
        canvas.rect(856+i*13,y+19,8,8,col,radius=2)
    title_size=min(58,canvas.theme['typography']['title_size'])
    while width(p['username'],title_size)>480 and title_size>30:title_size-=2
    canvas.text(27,y+126,p['username'],title_size,bold=True,max_width=480)
    canvas.rect(min(474,34+width(p['username'],title_size)),y+113,22,8,c['accent'],radius=0)
    canvas.text(29,y+174,'// '+p['role'],18,c['accent'],max_width=470)
    canvas.line(29,y+197,29,y+259,c['accent'])
    canvas.text(43,y+220,p['tagline'],15,max_width=465)
    canvas.text(43,y+252,p['tagline_zh'],13,c['muted'],max_width=465)
    scene=options.get('scene') or cfg.get('studio',{}).get('scene') or canvas.theme.get('studio',{}).get('scene','daylight')
    asset=options.get('studio_asset') or canvas.theme.get('studio',{}).get('asset')
    if asset:studio.render_asset(canvas,510,y+65,370,243,asset)
    else:studio.render(canvas,510,y+65,370,243,scene)
    return h

def project_list(canvas,cfg,y,options):
    c=canvas.c; items=cfg['projects']; row_h=118; h=45+row_h*len(items)
    canvas.rect(1,y,W-2,h,stroke=c['border'])
    canvas.text(23,y+29,'▱ / '+tr(cfg,'projects')+' · '+f'{len(items):02}',17,bold=True)
    canvas.text(873,y+29,'↗ github',12,c['muted'],anchor='end')
    canvas.line(1,y+45,W-1,y+45)
    style={**canvas.theme.get('components',{}).get('projects',{}),**options}
    icons=canvas.theme.get('icons',{}).get('projects',[])
    for i,p in enumerate(items):
        top=y+45+i*row_h
        canvas.text(22,top+37,f'{i+1:02}',14,c['muted'])
        icon=p.get('icon') or (icons[i%len(icons)] if icons else projects.ICONS[i%3])
        draw_icon(canvas,59,top+18,icon,c['accent'],38,style.get('icon_variant','outline'))
        canvas.text(112,top+35,p['name'],18,bold=True,max_width=480)
        canvas.multiline(112,top+60,p['description'],530,13,2,18,c['muted'])
        x=112
        if p.get('stars') is not None:x+=70
        if p.get('forks') is not None:canvas.text(x,top+94,'Forks '+str(p['forks']),11,c['muted'])
        status=tr(cfg,'development') if p['status']=='IN DEVELOPMENT' else p['status']
        canvas.rect(668,top+22,7,7,c['accent'],radius=3)
        canvas.text(681,top+30,status,11,max_width=190)
        x=668
        for tag in p['tags'][:3]:
            w=min(94,max(34,round(width(tag,10)+16)))
            if x+w>862:break
            canvas.rect(x,top+45,w,19,stroke=style.get('chip_border',c['border']),radius=2)
            canvas.text(x+7,top+59,tag,10,c['muted'],max_width=w-13)
            x+=w+6
        canvas.text(872,top+94,'↗' if p.get('url') else '·',17,c['foreground'],anchor='end')
        if i<len(items)-1:canvas.line(22,top+row_h,878,top+row_h,style.get('divider_color',c['border']))
    return h

def activity(canvas,cfg,y,options):
    c=canvas.c; h=290
    canvas.rect(1,y,W-2,h,stroke=c['border'])
    section_title(canvas,'activity',24,y+31,tr(cfg,'activity'),17)
    data=cfg.get('_contributions')
    if data:
        canvas.text(24,y+55,f'{data.get("total",0):,} contributions · GitHub',12,c['muted'])
        days=data.get('days',[])[-245:]
        for i,d in enumerate(days):
            level=max(0,min(4,int(d.get('level',0))))
            color=(c['surface'],c['muted'],c['accent'],c['accent'],c['accent'])[level]
            canvas.rect(25+(i//7)*24,y+78+(i%7)*25,17,17,color,radius=2)
    else:
        canvas.text(24,y+55,tr(cfg,'unavailable')+' · decorative',12,c['muted'])
        for col in range(35):
            for row in range(7):
                color=c['accent'] if (col,row) in ((5,2),(12,3),(19,1),(26,4)) else c['surface']
                canvas.rect(25+col*24,y+78+row*25,17,17,color,radius=2)
    return h

def footer(canvas,cfg,y,options):
    c=canvas.c;h=170
    canvas.rect(1,y,W-2,h,stroke=c['border'])
    canvas.line(450,y,450,y+h)
    section_title(canvas,'now',24,y+31,tr(cfg,'now'),17)
    for i,item in enumerate(cfg.get('now',[])[:5]):canvas.text(27,y+62+i*21,'› '+item,13,c['muted'],max_width=402)
    section_title(canvas,'connect',472,y+31,tr(cfg,'connect'),17)
    for i,entry in enumerate(cfg.get('social',[])[:6]):
        x=472+(i%2)*201;yy=y+44+(i//2)*35
        canvas.rect(x,yy,188,27,stroke=c['border'],radius=2)
        canvas.text(x+9,yy+18,'↗ '+entry['label'],12,max_width=165)
    for i,line in enumerate(cfg.get('motto',[])[:2]):
        canvas.text(472,y+144+i*17,line,12,c['accent'] if i else c['foreground'],max_width=390)
    return h
