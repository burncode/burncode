"""LuizMelo's CC0 Pet Cats Pack, rendered as lossless self-contained SVG pixels."""
from collections import defaultdict
from functools import lru_cache
from math import ceil
from pathlib import Path
import json
from ..text import width

CHARACTERS=('classic_cat','tuxedo_cat','orange_cat','spotted_cat','fluffy_cat','brown_cat')
NATIVE_ACTIONS={'walk':'Walk','idle':'Idle','run':'Run','meow':'Meow',
                'lay_down':'Laying','itch':'Itch','sleep1':'Sleeping1',
                'sleep2':'Sleeping2','sit':'Sitting','lick1':'Licking 1',
                'lick2':'Licking 2','stretch':'Stretching'}
ACTIONS=tuple(NATIVE_ACTIONS)+('sleep','banner')
MOTIONS=('wander','static','story')+ACTIONS
PACK=Path(__file__).resolve().parents[2]/'assets'/'companions'/'pet-cats'/'frames.json'


@lru_cache(maxsize=1)
def _pack():
    return json.loads(PACK.read_text(encoding='utf-8'))


def _timeline(motion,sequence,duration,character='classic_cat'):
    """Use native frames; sleeping includes original lie-down and wake-up clips."""
    events=[]

    def repeat(action,start,end,step=.1,once=False):
        count=len(_pack()['characters'][character]['actions'][action]['frames'])
        i=0;t=start
        while t<end-1e-9:
            events.append((t,(action,min(i,count-1) if once else i%count)))
            i+=1;t=start+i*step
            if count==1:break

    slots=[]
    if motion=='story':
        slots=[(i*duration/len(sequence),(i+1)*duration/len(sequence),a) for i,a in enumerate(sequence)]
    elif motion=='wander':
        slots=[(0,duration*.35,'walk'),(duration*.35,duration*.48,'idle'),(duration*.48,duration*.86,'walk'),(duration*.86,duration,'idle')]
    else:
        slots=[(0,duration,motion)]
    for start,end,action in slots:
        if action=='sleep':
            laying_end=min(end,start+.8)
            repeat('Laying',start,laying_end,once=True)
            # Leave an actual sleep hold before the author's stretching frames.
            waking_start=end-1.3 if end-start>=2.4 else end
            if laying_end<waking_start:repeat('Sleeping1',laying_end,waking_start)
            if waking_start<end:repeat('Stretching',waking_start,end,once=True)
        else:
            native={'banner':'Meow','static':'Sitting'}.get(action) or NATIVE_ACTIONS[action]
            step=.07 if action=='run' else .12 if action in ('idle','lick1','lick2','itch') else .14 if action in ('banner','meow') else .1
            repeat(native,start,end,step,once=action in ('lay_down','stretch'))
    return events


@lru_cache(maxsize=1024)
def _contour(character,action,index):
    pixels=set()
    for x,y,length,color in _pack()['characters'][character]['actions'][action]['frames'][index]:
        if len(color)==9 and int(color[7:9],16)<128:continue
        pixels.update((x+i,y) for i in range(length))
    edges=[]
    for x,y in sorted(pixels):
        if (x,y-1) not in pixels:edges.append(f'M{x} {y}h1')
        if (x,y+1) not in pixels:edges.append(f'M{x} {y+1}h1')
        if (x-1,y) not in pixels:edges.append(f'M{x} {y}v1')
        if (x+1,y) not in pixels:edges.append(f'M{x+1} {y}v1')
    return ''.join(edges)


def _frames(canvas,character,events,duration,static=False,outline='auto',loop=True):
    cat=_pack()['characters'][character]
    keys=list(dict.fromkeys(key for _,key in events))
    canvas.raw('<defs>')
    for action,index in keys:
        colors=defaultdict(list)
        for x,y,length,color in cat['actions'][action]['frames'][index]:
            colors[color].append(f'M{x} {y}h{length}v1h{-length}z')
        ident=f'pet-cat-{cat["cat"]}-{action.replace(" ","-")}-{index}'
        canvas.raw(f'<g id="{ident}" data-action="{action}" data-frame="{index}">')
        outlined=outline=='on' or (outline=='auto' and canvas.theme.get('mode')=='dark' and character=='tuxedo_cat')
        if outlined:
            canvas.raw(f'<path data-role="contrast-outline" d="{_contour(character,action,index)}" fill="none" stroke="{canvas.c["foreground"]}" stroke-opacity="0.58" stroke-width="0.7" shape-rendering="geometricPrecision"/>')
        for color,paths in colors.items():
            alpha=f' fill-opacity="{int(color[7:9],16)/255:.10f}"' if len(color)==9 else ''
            canvas.raw(f'<path data-role="source-pixels" fill="{color[:7]}"{alpha} d="{"".join(paths)}"/>')
        canvas.raw('</g>')
    canvas.raw('</defs>')
    for key in keys:
        action,index=key
        initial=int(events[0][1]==key)
        canvas.raw(f'<use href="#pet-cat-{cat["cat"]}-{action.replace(" ","-")}-{index}" opacity="{initial}">')
        if not static and len(keys)>1:
            points=[(0,initial)]
            for time,active in events[1:]:
                value=int(active==key)
                if value!=points[-1][1]:points.append((time/duration,value))
            points.append((1,initial if loop else int(events[-1][1]==key)))
            times=';'.join(format(t,'.9g') for t,_ in points)
            values=';'.join(str(v) for _,v in points)
            repeat='indefinite' if loop else '1'
            canvas.raw(f'<animate attributeName="opacity" values="{values}" keyTimes="{times}" calcMode="discrete" dur="{duration}s" repeatCount="{repeat}" fill="freeze"/>')
        canvas.raw('</use>')


def render(canvas,y,cfg,track=(250,750),top=3):
    if not cfg.get('header_cat',True):return
    c=canvas.c;spec=cfg.get('companion',{})
    character=spec.get('character','classic_cat');motion=spec.get('animation','wander')
    duration=spec.get('duration',16)
    sequence=spec.get('sequence',['walk','idle','sleep','banner','walk']) if motion=='story' else []
    banner=spec.get('banner','I LOVE YOU')
    x0,x1=track;yy=y+top
    canvas.raw(f'<g id="pixel-companion" transform="translate({x0} {yy})">')
    facing=[(0,1)]
    if motion in ('walk','run','wander','story'):
        if motion=='story':
            n=len(sequence);positions=[x0];current=x0;direction=1
            for i,action in enumerate(sequence):
                if action in ('walk','run'):
                    target=x1 if direction==1 else x0
                    if facing[-1][1]!=direction:facing.append((i/n,direction))
                    current=target;direction*=-1
                positions.append(current)
            times=[i/n for i in range(n+1)]
        elif motion in ('walk','run'):
            positions=[x0,x1,x0];times=[0,.5,1];facing.append((.5,-1))
        else:
            positions=[x0,x1,x1,x0,x0];times=[0,.35,.48,.86,1];facing.append((.48,-1))
        values=';'.join(f'{x} {yy}' for x in positions)
        key_times=';'.join(format(t,'.9g') for t in times)
        easing=' calcMode="spline" keySplines="'+';'.join(['0.35 0 0.65 1']*(len(times)-1))+'"' if motion=='story' else ''
        canvas.raw(f'<animateTransform attributeName="transform" type="translate" values="{values}" keyTimes="{key_times}"{easing} dur="{duration}s" repeatCount="indefinite"/>')
    canvas.raw('<g id="companion-sprite"><g transform="translate(25 0)"><g id="companion-facing">')
    if len(facing)>1:
        facing.append((1,1))
        values=';'.join(f'{d} 1' for _,d in facing)
        times=';'.join(format(t,'.9g') for t,_ in facing)
        canvas.raw(f'<animateTransform attributeName="transform" type="scale" values="{values}" keyTimes="{times}" calcMode="discrete" dur="{duration}s" repeatCount="indefinite"/>')
    canvas.raw('<g transform="translate(-25 0)">')
    # Only integer scaling enlarges the original pixels. No deformation/recoloring.
    canvas.raw('<g id="companion-pose" transform="scale(2)" data-source="LuizMelo/Pet Cats Pack" shape-rendering="crispEdges">')
    _frames(canvas,character,_timeline(motion,sequence,duration,character),duration,motion=='static',spec.get('outline','auto'),motion not in ('lay_down','stretch'))
    canvas.raw('</g></g></g></g>')
    if (motion=='story' and 'banner' in sequence) or motion=='banner':
        bubble_sequence=sequence if motion=='story' else ['banner']
        n=len(bubble_sequence);visible=[int(a=='banner') for a in bubble_sequence]
        values=';'.join(map(str,visible+[visible[0]]))
        times=';'.join(format(i/n,'.9g') for i in range(n+1))
        canvas.raw(f'<g id="companion-banner" transform="scale(1.4)" opacity="{visible[0]}"><animate attributeName="opacity" values="{values}" keyTimes="{times}" calcMode="discrete" dur="{duration}s" repeatCount="indefinite"/>')
        text_size=13.2 if canvas.density=='showcase' else 11.6 if canvas.density=='github' else 11
        w=ceil(width(banner,text_size))+16;x=-9-w
        canvas.rect(x,0,w,24,c['background'],stroke=c['accent'],radius=4)
        canvas.raw(f'<path d="M-10 8 L-2 13 L-10 18 Z" fill="{c["background"]}"/>')
        canvas.raw(f'<path id="companion-speech-tail" d="M-9 8 L-2 13 L-9 18" fill="none" stroke="{c["accent"]}" stroke-width="{canvas.style["border_width"]}" stroke-linejoin="round"/>')
        canvas.text(x+8,16,banner,11,c['accent'],bold=True)
        canvas.raw('</g>')
    canvas.raw('</g></g>')  # sprite, animated track
