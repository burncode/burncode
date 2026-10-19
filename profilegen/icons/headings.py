# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
"""Unified section heading icons, sourced exclusively from icons/custom."""
from html import escape
from .svg_icons import draw as custom_draw

# Section title -> user supplied icon name (see ICONS.md).
SECTION_ICONS = {
    'about': 'user', 'projects': 'folder', 'languages': 'code',
    'activity': 'git-branch', 'now': 'terminal', 'stats': 'chart-bar',
    'blog': 'rss', 'github_stats': 'chart-bar',
    'currently_building': 'tool', 'development_focus': 'tool',
    'recent_releases': 'package', 'connect': 'world',
}

def icon_svg(section, x, y, size, color):
    name = SECTION_ICONS.get(section, 'default')
    svg = custom_draw(name, x, y, size, color)
    if svg:
        return svg
    # Same simple, neutral default for EVERY missing icon.
    return (f'<svg x="{x}" y="{y}" width="{size}" height="{size}" '
            f'viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
            f'<rect x="4" y="4" width="16" height="16" rx="2" fill="none" '
            f'stroke="{escape(color,quote=True)}" stroke-width="1.7"/>'
            f'<path d="M9 12h6" stroke="{escape(color,quote=True)}" stroke-width="1.7"/></svg>')

def title(canvas, section, x, baseline, label, font_size=16, suffix='', color=None):
    fg = color or canvas.c['foreground']
    canvas.raw(icon_svg(section, x, baseline-15, 18, fg))
    canvas.text(x+25, baseline, '/ '+label+suffix, font_size, fg, True)
