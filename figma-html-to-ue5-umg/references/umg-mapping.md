# HTML/CSS to UMG mapping reference

Use this as a decision table while converting a source UI. It describes implementation choices; source behavior always wins when it supplies a concrete state.

## Layout

| Web pattern | UMG mapping |
|---|---|
| `position:absolute; inset:0` | Full-screen CanvasPanel child, Anchors 0,0→1,1, edge offsets 0 |
| centered fixed dialog | CanvasPanel child, Anchors .5,.5→.5,.5, Alignment .5,.5, fixed Width/Height |
| top bar with fixed height | Horizontal-stretch top anchor, fixed Height and left/right margins |
| bottom action bar | Horizontal-stretch bottom anchor, fixed Height and top/side margins |
| left room/list column | Left anchor with fixed Width and vertical stretch; divider as 1px Border |
| centered form | Center anchor with fixed Width/Height; use a clipped parent if the viewport is short |
| CSS flex/grid repeated items | Child CanvasPanel instances with deterministic calculated positions; keep row/card sizes explicit |
| `overflow:hidden` | CanvasPanel `Clipping = ClipToBoundsAlways` |
| `transform: translate/scale` | Render Transform Translation/Scale; do not change layout offsets for hover animation |

Use a small anchor vocabulary in reports: TL, C, TC, BC, TR, RC, F, HT, HB. Always state Min/Max anchors, Alignment, and what Offsets mean.

## Visuals

Use Border for solid fills and outlines, TextBlock for labels, Image for textures/icons, and Button for hit testing. Put the visual Border/Text/Image beside or underneath a transparent Button so button state brushes do not add unwanted padding or default gray colors. Set decorative children to `Not Hit-Testable`.

For square UI, use zero corner radii. For rounded UI, use a Rounded Box brush only when the source has measurable rounding. For glow, CSS shadows need an Image/material or a separate authored glow asset; do not claim a normal Border outline is a blur.

## Interaction and modal layering

Use a page state enum/string and explicit refresh functions. On selection, update both the visual state and any dependent visibility/height. For modals, use this order:

1. Show the layer and scrim.
2. Make the scrim hit-testable and the panel interactive.
3. Play the entrance animation.
4. On close, block repeated clicks, play the exit animation, then set the layer to `Collapsed` and restore focus.

The outside scrim should consume its click. A transparent surface Button below panel content prevents a click on empty panel space from reaching the scrim. Escape should close the narrowest active layer first: dropdown, dialog, settings, then page.

## Animation checklist

Record each animation as:

```text
Name: AN_SettingsIn
Target: C_SettingsPanel
Tracks: Render Opacity 0→1; Render Transform Translation.Y 16→0; Scale .98→1
Duration: 0.20 s
Interpolation: Cubic Ease Out
Completion: keep final state
```

CSS `transition` usually maps to a short UMG animation per state. Reverse or play a dedicated exit animation, but do not collapse the target before the animation ends.

## Input limitations

If the allowed control set excludes editable text and scroll controls, a Button + TextBlock can represent an input field but cannot provide full IME composition, selection, cursor movement, or native editing semantics. A clipped CanvasPanel with a translated content CanvasPanel can implement deterministic list scrolling through UserWidget pointer-wheel handlers, but it needs explicit bounds and hit-testing.

## Validation matrix

At minimum verify:

| Area | Checks |
|---|---|
| Initial state | Main page visible; secondary pages and modal layers collapsed; correct default selections |
| Navigation | Each existing web click changes the expected page and restores focus on Back |
| Selection | Selected row/card retains selected appearance; disabled/full row cannot be selected |
| Form | Empty/whitespace input disables confirmation; count/mode/toggle update visuals |
| Lobby | Ready state, counts, occupied/empty slots, host-only controls |
| Modal | Scrim consumes clicks; panel empty area does not dismiss; Escape order works |
| Animation | Fade/slide/pop completes before visibility changes; no hidden widget is hit-testable |
| Responsive | Reference resolution, smaller 16:9, and at least one wider or taller aspect ratio |
