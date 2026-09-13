---
name: figma-html-to-ue5-umg
description: Convert a local Figma Make or HTML/CSS interface plus reference screenshots into a native UE5 UMG Widget Blueprint implementation, including CanvasPanel layout, UI-only interaction logic, animations, image assets, and verification. Use when the user asks to port a web UI into UE5 UMG; do not use for building the web UI itself or implementing gameplay systems.
---

# Figma HTML to UE5 UMG

Produce an editable, testable UE5 UMG result from the supplied HTML/CSS and screenshots. Treat the HTML/CSS as the source of behavior and the screenshots as visual evidence. Do not reproduce the webpage in a browser or deliver frontend code.

## Required workflow

1. Locate and inspect the project, source files, screenshots, and any local skill or repository instructions. Read the relevant React/HTML entry points, CSS, imported components, and asset references. Inspect every provided screenshot at least once.
2. Inventory the source before implementing: pages/states, controls, default values, click/hover/focus behavior, visibility changes, overlays, transitions, text, colors, spacing, and images. Separate behavior that exists in the source from static showcase-only screens and from behavior that must be added to make the UI usable.
3. Choose a reference design size, normally 1920×1080 for game UI. Convert absolute web positions into CanvasPanel Anchors plus Offsets. Use stretch anchors for full-screen/background/header/footer regions and fixed center/edge anchors for stable controls. Never use screenshot pixels as an unexamined final layout.
4. Build a native `UserWidget` whose root is a `CanvasPanel`. Use only native UMG controls unless the user explicitly permits more: `CanvasPanel`, `Button`, `Border`, `TextBlock`, `Image`, and `Overlay`. Use child CanvasPanels for pages, repeated rows, clipping regions, and modal layers. Keep static background, page content, popup/dialog layers, and input blockers separate with explicit ZOrder.
5. Preserve the full control hierarchy and name widgets semantically. Repeated items should have predictable instance names. For every control record Anchors, Offsets, Alignment, size, padding, color, font, opacity, default Visibility, hit-test behavior, and ZOrder. Use zero-radius brushes when the source has square corners. Do not invent rounded cards or background art.
6. Map behavior to UMG events: web `onClick` to `OnClicked`, hover enter/leave to `OnHovered`/`OnUnhovered`, focus/keyboard behavior to UserWidget input handlers, and pointer-wheel behavior to `NativeOnMouseWheel` or an equivalent UI-only handler. Update visual state explicitly rather than binding animated properties every frame. Modal scrims must consume input; hide widgets with `Collapsed` after exit animations so transparent widgets cannot be clicked.
7. Keep gameplay and networking out of the widget. Expose BlueprintAssignable delegates, BlueprintImplementableEvents, or clearly named request functions such as `RequestJoinRoom`, `RequestCreateRoom`, `RequestApplySettings`, and `RequestQuitGame`. The widget may emit these interfaces and render success/failure results, but must not load levels, start sessions, connect sockets, or implement game rules.
8. Convert source transitions into `UWidgetAnimation` assets. For every animation specify target widget, track/property, keyframes, duration, and interpolation. Typical mappings are Render Opacity for fades, Render Transform Translation/Scale for slide/pop animations, Brush Color or ColorAndOpacity for state changes, and a separate scrim track for modal overlays. Hide a panel only after its exit animation finishes.
9. Export only source images that actually exist. Prefer inline SVG/vector geometry converted to transparent Texture2D masks when the destination UI needs tintable icons. Preserve alpha, use UI texture settings, no mipmaps, clamp addressing, and `TextureGroup_UI`. If the source has no image asset, create an explicit placeholder or keep the Image hidden; do not crop icons from screenshots or invent missing artwork. Use `scripts/extract_inline_svg.py` when inline SVG export is useful.
10. Create or update the WBP in the project. When editor automation is available, prefer a deterministic editor commandlet or editor utility that creates the Widget Blueprint, widget tree, animations, fonts, preview map, and assets. If the project cannot compile, fix only task-scoped build issues or report the blocker; do not silently claim a Blueprint was created.
11. Verify in proportion to the task. Compile the project/editor target, load the WBP, run UI-only state checks for initial visibility, page transitions, selection, disabled controls, modal hit testing, settings cancel/save, and animation completion. Test at the reference size plus at least one smaller and one wider/aspect-ratio variant. A commandlet or report should state the WBP path, widget/animation counts, and pass/fail checks.

## Important constraints

- The requested output is UE5 UMG. Do not output HTML, CSS, React, or a browser implementation.
- Use `CanvasPanel` Anchors and Offsets for absolute web layouts. Document every stretch anchor's edge margins and every fixed anchor's size.
- Distinguish normal, hovered, pressed, selected, disabled, ready, and modal states. Preserve selected state when a pointer leaves a control.
- `Border` has a brush and outline; do not assume CSS `border-radius`, `box-shadow`, blur, or dashed borders exist natively. Approximate with native layers or document a required texture/material only when it changes fidelity.
- The allowed native control set does not include `EditableTextBox`, `ScrollBox`, `Slider`, `CheckBox`, or `ComboBox`. If those controls are prohibited, implement the visual approximation with Buttons/Borders and clearly state what native text input, IME, scrolling, slider capture, or dropdown behavior cannot be fully reproduced. If real Chinese IME or production text editing is required, ask to allow `EditableTextBox`.
- Use a legal project font asset. Orbitron does not contain Chinese glyphs; use a composite font with the desired Latin face and a Chinese fallback. Do not download a font without checking project licensing or user authorization.
- Use UI DPI settings consistently. Fix the project font DPI convention before calibrating sizes, and do not confuse font DPI with viewport DPI scaling.
- Do not overwrite existing assets without checking their paths. Preserve user changes and save generated artifacts under a scoped UI folder.

## Deliverable

Leave the project with the WBP and supporting assets, plus a concise implementation report. The report should link to the WBP, preview map if created, source files/scripts, generated textures/fonts, and validation output. State any unverified rendering limitation separately from passed structural/UI-state checks.

For detailed mapping and validation guidance, read [references/umg-mapping.md](references/umg-mapping.md). For deterministic editor automation and asset handling, read [references/editor-automation.md](references/editor-automation.md). Read only the reference needed for the current task.
