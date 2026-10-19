# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
"""Compact SVG brand marks for social chips (recognizable, locally rendered).

These are simplified monochrome pictograms, not claims of brand endorsement.
"""
from html import escape
from .svg_icons import draw as icon_draw
from .headings import icon_svg
from .headings import icon_svg

def mark(name,x,y,color,size=19):
    return icon_draw({"email":"mail","website":"world","link":"external-link"}.get(name,name),x,y,size,color) or icon_svg("default",x,y,size,color) or icon_svg("default",x,y,size,color)
