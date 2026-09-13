"""Extract inline SVG blocks from HTML/JSX/TSX and rasterize tintable PNG masks.

Requires resvg-py in the active Python environment. The helper does not guess which
SVGs are important; use --index or inspect the generated manifest.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

try:
    import resvg_py
except ImportError as exc:
    raise SystemExit("Install resvg-py in the active environment before using this helper") from exc


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--index", type=int, action="append", help="SVG index to export; omit to export all")
    parser.add_argument("--size", type=int, default=128)
    args = parser.parse_args()

    source_text = args.source.read_text(encoding="utf-8")
    matches = list(re.finditer(r"<svg\b[\s\S]*?</svg>", source_text, re.IGNORECASE))
    selected = set(args.index) if args.index else set(range(len(matches)))
    args.output.mkdir(parents=True, exist_ok=True)
    manifest = []

    for number, match in enumerate(matches):
        if number not in selected:
            continue
        svg = match.group(0)
        if "xmlns=" not in svg[:160]:
            svg = svg.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
        svg = svg.replace("strokeWidth", "stroke-width")
        svg = svg.replace("strokeLinecap", "stroke-linecap")
        svg = svg.replace("strokeLinejoin", "stroke-linejoin")
        svg = re.sub(r'(stroke|fill)="(?!none")[^"]+"', lambda m: f'{m.group(1)}="white"', svg)
        name = f"T_UI_InlineSVG_{number:03d}"
        output_file = args.output / f"{name}.png"
        output_file.write_bytes(resvg_py.svg_to_bytes(svg_string=svg, width=args.size, height=args.size))
        manifest.append({
            "source": str(args.source),
            "index": number,
            "asset": name,
            "line": source_text[:match.start()].count("\n") + 1,
            "size": [args.size, args.size],
            "tintable_mask": True,
        })

    (args.output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
