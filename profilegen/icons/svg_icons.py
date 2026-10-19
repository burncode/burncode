# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
"""Render locally supplied SVG icons from any compatible icon library."""
from functools import lru_cache
from pathlib import Path
from html import escape
import xml.etree.ElementTree as ET
import re

ROOT = Path(__file__).resolve().parent / 'custom'
ALIASES = {'cube':'cube','heritage':'building-monument','blocks':'layout-grid','bot':'robot','book':'book','email':'mail','website':'world','globe':'world','device':'device-desktop','macos':'brand-apple','windows':'brand-windows','linux':'brand-ubuntu','ubuntu':'brand-ubuntu','arch':'brand-arch-linux','debian':'brand-debian','fedora':'brand-fedora','github':'brand-github','linkedin':'brand-linkedin','youtube':'brand-youtube','instagram':'brand-instagram','telegram':'brand-telegram','discord':'brand-discord','bilibili':'brand-bilibili','zhihu':'brand-zhihu','weibo':'brand-weibo','x':'brand-x','twitter':'brand-x','rss':'rss','folder':'folder','chart':'chart-bar','user':'user','terminal':'terminal','star':'star','shield':'shield','monitor':'device-desktop','code':'code','image':'photo','puzzle':'puzzle','cloud':'cloud','package':'package','link':'external-link','database':'database','wrench':'tool','mail':'mail','shield':'shield','git':'git-branch','robot':'robot'}
@lru_cache(maxsize=512)
def _load(name, variant):
    if variant not in ('outline','filled','dashed'): return None
    mapped = ALIASES.get(name,name)
    if not mapped.replace('-','').isalnum():return None
    path=ROOT/variant/(mapped+'.svg')
    if not path.is_file():return None
    root=ET.parse(path).getroot()
    if root.tag.rsplit('}',1)[-1]!='svg':return None
    allowed={'path','circle','rect','line','polyline','polygon','ellipse'}
    safe={'d','cx','cy','r','x','y','width','height','rx','ry','x1','x2','y1','y2','points','fill','stroke','stroke-width','stroke-linecap','stroke-linejoin','stroke-dasharray','fill-rule','clip-rule','opacity','transform'}
    viewbox=root.attrib.get('viewBox','0 0 24 24')
    if not re.fullmatch(r'[0-9eE+.\-\s]+',viewbox):viewbox='0 0 24 24'
    root_fill=root.attrib.get('fill','none')
    root_stroke=root.attrib.get('stroke','currentColor')
    nodes=[]
    for el in root.iter():
        tag=el.tag.rsplit('}',1)[-1]
        if tag in allowed:
            attrs_dict={k:v for k,v in el.attrib.items() if k in safe}
            if 'fill' not in attrs_dict and root_fill not in ('none','transparent'):
                attrs_dict['fill']='currentColor'
            if 'stroke' not in attrs_dict and root_stroke=='none':attrs_dict['stroke']='none'
            attrs=' '.join(f'{k}="{escape(v,quote=True)}"' for k,v in attrs_dict.items())
            nodes.append(f'<{tag} {attrs}/>')
    return (viewbox, ''.join(nodes)) if nodes else None

def draw(name,x,y,size,color,variant='outline'):
    # Read only user-supplied SVG files from icons/custom/.
    data=_load(name,variant)
    if not data and variant!='outline':data=_load(name,'outline')
    if not data:return ''
    viewbox, shapes=data
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="{escape(viewbox,quote=True)}" color="{escape(color,quote=True)}" fill="none" stroke="{escape(color,quote=True)}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">{shapes}</svg>'
