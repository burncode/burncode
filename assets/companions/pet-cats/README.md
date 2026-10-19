# Pet Cats Pack — LuizMelo

Source: https://luizmelo.itch.io/pet-cat-pack

License: CC0-1.0 (the author's original license is in LICENSE.txt).

The original downloaded archive is assets/pet-cats-pack.zip. No palette changes
or hand-drawn replacement pixels are applied. frames.json contains exact
RGBA pixel runs, produced by tools/import_pet_cats.py; every converted frame is checked
against its original PNG. Normal profile generation needs only Python's stdlib.

Existing configuration aliases map to original pack characters:

| Configuration | Original character |
|---|---|
| classic_cat | Cat-3, gray |
| tuxedo_cat | Cat-2, black (compatibility name; original has no white bib) |
| orange_cat | Cat-1, golden orange |
| spotted_cat | Cat-4, spotted |
| fluffy_cat | Cat-5, long-haired |
| brown_cat | Cat-6, brown |

All 12 original action types are imported, retaining their original alignment.
Cat-3 lacks the author's Itch sheet; this combination is explicitly rejected.
Artwork pixel colors remain identical across light and dark themes. Dark themes
add a thin separate outline to the black cat by default (outline=off disables it).
The display uses 2× integer scaling with crisp SVG pixel edges. Only playback
timing and placement are adapted to the header. Speech bubbles and contrast
outlines are separate project-authored SVG, not modifications to source pixels.
