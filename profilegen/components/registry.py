# Author: burncode
# Email: maohan0118@gmail.com
# Copyright (c) 2026 burncode
# License: MIT
"""Register additional renderers here. Signature: render(canvas, config, y, options) -> height."""
from . import hero, projects, activity, footer, motto
from ..widgets import languages, extra, about, fastfetch

COMPONENTS = {
    'hero': hero.render,
    'projects': projects.render,
    'activity': activity.render,
    'footer': footer.render,
    'languages': languages.render,
    'motto': motto.render,
    'about': about.render,
    'github_stats': extra.stats,
    'currently_building': extra.building,
    'development_focus': extra.focus,
    'recent_releases': extra.releases,
    'blog': extra.blog,
    'device': fastfetch.render,
}
