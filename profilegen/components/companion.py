# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
"""Tiny SVG pixel companions with SMIL action sequences and static fallback."""
from html import escape
CHARACTERS=('classic_cat','tuxedo_cat','orange_cat')
MOTIONS=('wander','walk','idle','static','story')
ACTIONS=('walk','idle','sleep','banner')

def render(canvas,y,cfg,track=(250,750),top=3):
    if not cfg.get('header_cat',True):return
    c=canvas.c;spec=cfg.get('companion',{})
    character=spec.get('character','classic_cat');motion=spec.get('animation','wander')
    duration=spec.get('duration',16)
    sequence=spec.get('sequence',['walk','idle','sleep','banner','walk']) if motion=='story' else []
    banner=spec.get('banner','I LOVE YOU')
    x0,x1=track; yy=y+top
    sprite_scale=1.4  # Preserve original pixel artwork; enlarge only the header companion.
    ink='#d78437' if character=='orange_cat' else c['foreground']
    white='#f5f6f2' if character=='tuxedo_cat' else c['background']
    # All animation takes place in the reserved header track, never over nav links.
    canvas.raw(f'<g id="pixel-companion" transform="translate({x0} {yy})">')
    if motion in ('wander','walk','story'):
        # Animate relative to the initial translation; absolute coordinates here
        # previously doubled the header offset and could push the cat off-track.
        if motion=='story':
            # A continuous round trip with actual holds for idle/sleep/banner.
            # Keep the sprite in the same reserved track throughout the cycle.
            values=f'{x0} {yy};{x1} {yy};{x1} {yy};{x1} {yy};{x1} {yy};{x0} {yy}'
            times='0;0.20;0.40;0.60;0.80;1'
        elif motion=='wander':
            values=f'{x0} {yy};{x1} {yy};{x1} {yy};{x0} {yy};{x0} {yy}'
            times='0;0.35;0.48;0.86;1'
        else:
            values=f'{x0} {yy};{x1} {yy};{x0} {yy}'
            times='0;0.5;1'
        canvas.raw(f'<animateTransform attributeName="transform" type="translate" values="{values}" keyTimes="{times}" dur="{duration}s" repeatCount="indefinite"/>')
    canvas.raw(f'<g id="companion-sprite" transform="scale({sprite_scale})">')
    # Body poses live in the sprite coordinate system; the outer track never changes.
    canvas.raw('<g id="companion-pose">')
    if motion=='story':
        # Travel / sit down / curl up / stretch & rise / travel home.
        # Short transitions avoid sudden snapping between silhouettes.
        canvas.raw(f'<animateTransform attributeName="transform" type="translate" values="0 0;0 0;0 3;0 3;0 5;0 5;0 2;-2 3;0 0;0 0" keyTimes="0;0.19;0.23;0.39;0.43;0.59;0.64;0.72;0.80;1" dur="{duration}s" repeatCount="indefinite"/>')
        canvas.raw(f'<animateTransform attributeName="transform" additive="sum" type="scale" values="1 1;1 1;1 0.88;1 0.88;1 0.78;1 0.78;1.10 0.86;1.16 0.88;1 1;1 1" keyTimes="0;0.19;0.23;0.39;0.43;0.59;0.64;0.72;0.80;1" dur="{duration}s" repeatCount="indefinite"/>')

    # Story state windows are synchronized to the travel animation.
    # One timeline: walk outbound / look around / sleep / banner / walk home.
    # The sequence list remains supported for overlay content and visibility.
    story_times = '0;0.20;0.40;0.60;0.80;1'
    story_walk = '1;0;0;0;1;1'
    story_sleep = '0;0;1;0;0;0'
    # Refined 36x28 pixel cat. All detail remains inside the reserved header track.
    ear_inner = '#e9a3a0' if character != 'orange_cat' else '#f2ba8d'
    highlight = '#737985' if character != 'orange_cat' else '#f4bd78'
    # Tail is drawn behind the body; keep the original motion anchor.
    canvas.raw('<g id="companion-tail">')
    if motion!='static':
        canvas.raw('<animateTransform attributeName="transform" type="rotate" values="0 5 14;-12 5 14;0 5 14;9 5 14;0 5 14" dur="2.8s" repeatCount="indefinite"/>')
    canvas.rect(1,10,5,8,ink,radius=0)
    canvas.rect(0,8,4,5,ink,radius=0)
    canvas.raw('</g>')
    # Distinctive coral ear insets and tiny forehead highlight.
    canvas.rect(6,8,24,14,ink,radius=0)
    canvas.rect(8,2,7,10,ink,radius=0)
    canvas.rect(23,2,7,10,ink,radius=0)
    canvas.rect(10,4,3,5,ear_inner,radius=0)
    canvas.rect(25,4,3,5,ear_inner,radius=0)
    canvas.rect(16,9,5,2,highlight,radius=0)
    if character=='tuxedo_cat':
        canvas.rect(14,16,9,6,white,radius=0)
        canvas.rect(11,5,3,4,white,radius=0)
    elif character=='orange_cat':
        for px in (10,18,26):canvas.rect(px,9,2,4,'#a9552c',radius=0)
    canvas.rect(12,13,3,3,white,radius=0)
    canvas.rect(24,13,3,3,white,radius=0)
    canvas.rect(18,18,4,2,ear_inner,radius=0)
    canvas.rect(9,17,3,2,ear_inner,radius=0)
    canvas.rect(28,17,3,2,ear_inner,radius=0)
    canvas.rect(19,20,2,1,white,radius=0)
    canvas.line(8,18,2,16,c['muted']);canvas.line(29,18,35,16,c['muted'])
    # Two independently animated legs. Opposite phases make a readable pixel walk.
    # They stop during sit/sleep/stretch, unlike the old rigid sliding sprite.
    for side,px in (('front',9),('back',24)):
        canvas.raw(f'<g id="companion-leg-{side}">')
        if motion in ('walk','wander','story'):
            phase = '0 0;2 -2;0 0;-2 -1;0 0' if side=='front' else '0 0;-2 -1;0 0;2 -2;0 0'
            canvas.raw(f'<animateTransform attributeName="transform" type="translate" values="{phase}" dur="0.64s" repeatCount="indefinite"/>')
            if motion=='story':
                canvas.raw(f'<animate attributeName="opacity" values="1;0;0;0;1;1" keyTimes="{story_times}" calcMode="discrete" dur="{duration}s" repeatCount="indefinite"/>')
        canvas.rect(px,22,6,5,ink,radius=0)
        canvas.rect(px,25,6,2,ear_inner,radius=0)
        canvas.raw('</g>')
    if motion=='story':
        # Grounded tucked paws while sitting or asleep, not a floating body.
        canvas.raw(f'<g opacity="0"><animate attributeName="opacity" values="0;1;1;1;0;0" keyTimes="{story_times}" calcMode="discrete" dur="{duration}s" repeatCount="indefinite"/>')
        canvas.rect(10,23,9,4,ink,radius=0)
        canvas.rect(21,23,9,4,ink,radius=0)
        canvas.rect(12,25,5,2,ear_inner,radius=0)
        canvas.rect(23,25,5,2,ear_inner,radius=0)
        canvas.raw('</g>')
    if motion!='static':
        # A brief blink every cycle, with both eyelids synchronized.
        for xx in (12,24):
            canvas.raw(f'<rect x="{xx}" y="13" width="3" height="0" fill="{ink}"><animate attributeName="height" values="0;0;3;0;0" keyTimes="0;0.71;0.73;0.75;1" dur="{duration}s" repeatCount="indefinite"/></rect>')
    if motion=='story':
        # Closed eyelids during sleep, and a small glance during idle.
        canvas.raw(f'<g opacity="0"><animate attributeName="opacity" values="{story_sleep}" keyTimes="{story_times}" calcMode="discrete" dur="{duration}s" repeatCount="indefinite"/>')
        canvas.rect(11,13,6,3,ink,radius=0)
        canvas.rect(23,13,6,3,ink,radius=0)
        canvas.line(12,15,16,15,white)
        canvas.line(24,15,28,15,white)
        canvas.raw('</g>')
        canvas.raw(f'<g opacity="0"><animate attributeName="opacity" values="0;1;0;0;0;0" keyTimes="{story_times}" calcMode="discrete" dur="{duration}s" repeatCount="indefinite"/>')
        canvas.rect(12,13,3,3,ink,radius=0)
        canvas.rect(15,13,3,3,white,radius=0)
        canvas.raw('</g>')
        n=len(sequence)
        def visibility(action):
            vals=['1' if s==action else '0' for s in sequence]
            return ';'.join(vals+[vals[0]])
        def times():return ';'.join(f'{i/n:.5f}' for i in range(n+1))
        if 'sleep' in sequence:
            canvas.raw(f'<g opacity="0"><animate attributeName="opacity" values="{visibility("sleep")}" keyTimes="{times()}" calcMode="discrete" dur="{duration}s" repeatCount="indefinite"/>')
            canvas.text(34,12,'z',11,c['muted']);canvas.text(43,7,'z',9,c['muted']);canvas.text(51,5,'z',7,c['accent'])
            canvas.raw('</g>')
        if 'banner' in sequence:
            # Speech banner follows the cat. Limit to short text so it stays in the header track.
            canvas.raw(f'<g opacity="0"><animate attributeName="opacity" values="{visibility("banner")}" keyTimes="{times()}" calcMode="discrete" dur="{duration}s" repeatCount="indefinite"/>')
            canvas.rect(-122,0,113,24,c['background'],stroke=c['accent'],radius=1)
            canvas.text(-116,16,banner,11,c['accent'],bold=True,max_width=100)
            canvas.raw('</g>')
    canvas.raw('</g>')  # companion-pose
    canvas.raw('</g>')  # companion-sprite
    canvas.raw('</g>')  # animated track
