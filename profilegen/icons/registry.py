# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
"""Reusable 54-unit SVG line icon system with restrained accent details."""
ICONS = ('cube','book','heritage','code','terminal','star','database','bot','puzzle','globe','blocks','wrench','monitor','cloud','shield','image','package')
PALETTE = {'coral':'#ff6654','blue':'#429fe3','amber':'#f0a643','green':'#42a784','violet':'#a987df','neutral':'#8a949e'}

def draw_icon(canvas,x,y,kind,accent,size=42,variant="outline"):
    c=canvas.c
    if variant == "solid":
        canvas.rect(x,y,size,size,c['surface'],radius=3)
    else:
        canvas.rect(x,y,size,size,stroke=c['border'],radius=3)
    from .svg_icons import draw as icon_draw
    from .headings import icon_svg
    # Keep restrained neutral glyph with one small coral accent bar outside the mark.
    glyph=icon_draw(kind,x+size*.26,y+size*.24,size*.48,canvas.c['foreground'],variant)
    if glyph:canvas.raw(glyph)
    else:canvas.raw(icon_svg('default',x+size*.26,y+size*.24,size*.48,canvas.c['foreground']))
    canvas.rect(x+size*.25,y+size*.79,size*.22,2.2,accent,radius=0)



def tint(accent, background, amount=0.5):
    """Blend a bright accent into the current background for quiet borders."""
    a=[int(accent[i:i+2],16) for i in (1,3,5)]
    b=[int(background[i:i+2],16) for i in (1,3,5)]
    return '#'+''.join(f'{round(v*amount+w*(1-amount)):02x}' for v,w in zip(a,b))
