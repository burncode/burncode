# Studio Asset Pack — AI image prompts / 像素工作室 AI 提示词

**Goal:** create a detailed, coherent pixel-art studio scene for a GitHub Profile README Hero, without text, logos, UI labels, or watermarks.

## 1. Base prompt / 基础提示词

```text
A premium editorial 16-bit pixel-art illustration of an indie software developer's cozy workspace, straight-on camera, exact wide 354:241 composition, pixel-perfect hard edges, crisp square pixel clusters, no anti-aliasing, limited 12-color palette, detailed architectural window with a distant city skyline, simple hanging pendant lamp, clean desk with a single monitor showing abstract terminal blocks, mechanical keyboard, a small black cat with readable ears, eyes and tail sitting beside the monitor, books and one potted plant, carefully layered foreground and background, precise perspective, balanced negative space, architectural illustration quality, high readability when scaled to 360px width, no gradients, no photorealism, no text, no letters, no logos, no watermark.
```

## 2. Daylight — Mono / Paper / Ice

```text
Use the base scene. Bright overcast morning daylight, warm off-white and cool neutral gray interior, desaturated steel-blue city skyline, pale concrete and wood, coral-red terminal cursor as the ONLY vivid accent, calm Scandinavian studio mood. Cat is dark charcoal, positioned on the right third. Strong pixel-grid discipline. No saturated rainbow colors.
```

## 3. Night City — Graphite / Violet

```text
Use the same room layout and camera as Daylight, but at night. Deep graphite walls, dark blue city silhouettes, a few violet neon windows and a dim warm desk lamp. Monitor glow gently lights the black cat silhouette. Limit palette to graphite, midnight blue, cool gray and restrained lavender. Preserve all object positions for day/night theme switching.
```

## 4. Workshop — Sage / Matrix

```text
Use the same wide composition. Cozy open-source hardware workshop with pegboard, shelves, spare circuit boards, tiny soldering station, mechanical keyboard, terminal monitor and black cat. Muted sage green and charcoal palette, a single green indicator light. Pixel-art architectural interior, practical and uncluttered, no cyberpunk visual noise.
```

## 5. Sunset — Amber

```text
Same exact room and camera. Golden hour sunset through tall industrial window, pale peach skyline, muted terracotta books and a softly lit monitor, warm amber accents, black cat in the same position. Sophisticated editorial pixel art, avoid orange oversaturation.
```

## 6. Negative prompt / 反向约束

```text
no text, no readable code, no logos, no watermarks, no smooth gradients, no blur, no 3D rendering, no isometric perspective, no perspective distortion, no oversized cat, no extra monitors, no extra furniture, no humans, no floating objects, no busy decoration, no low-resolution smeared pixels
```

## 7. Production pipeline / 资源制作流程

1. Generate at 3:2 or a near-354:241 aspect ratio, preserving the same layout across themes.
2. Manually crop and align the main objects; keep the cat, monitor and window in stable locations.
3. If using raster PNG, quantize to a limited palette and edit with a pixel editor; PNG is **not** a drop-in replacement for the inline SVG pack.
4. To integrate into `assets/studio/<name>.svg`, redraw or vectorize into allowed SVG geometry with `viewBox="0 0 354 241"`. Avoid `<image>`, `<style>`, `<script>`, filters and external resources.
5. In a theme JSON, set `studio.asset` to the file stem; run `python build.py --preview` and check light/dark at GitHub-like widths.

**Included editable assets:** `assets/studio/studio-day.svg`, `assets/studio/studio-night.svg`. These are handcrafted procedural vector pixel scenes; AI-generated preview images are conceptual references, not production SVG source.
