"""
Shared visual system for every generated profile asset.

One place defines the palette, typography and the small SVG primitives
(panels, terminal chrome, command prompts, chips) so that the hero,
projects, architecture, stack, activity and footer assets all read as
parts of the same terminal UI.

Nothing here touches the network; `write_svg` is the only filesystem write.
"""

from __future__ import annotations

import os

# --------------------------------------------------------------------------
# PALETTE  (strict black + Matrix green - no blue / purple / brand colours)
# --------------------------------------------------------------------------
BG = "#020604"        # page background
BG_2 = "#050B07"      # secondary background
PANEL = "#07110A"     # panel fill
PANEL_LIGHT = "#0A160D"  # raised panel fill
GREEN = "#00FF41"     # matrix green (primary accent)
GREEN_BRIGHT = "#39FF14"  # brightest highlight, used sparingly
GREEN_2 = "#00C832"   # secondary green
GREEN_DARK = "#008F2F"    # dark green
BORDER = "#0B5F27"    # default 1px border
MUTED = "#548C61"     # muted green (labels, dotted leaders)
TEXT = "#D7FFE0"      # primary text
TEXT_2 = "#8BB596"    # secondary text

# Contribution heatmap levels 0..4
HEAT = ["#07110A", "#0A3D18", "#008F2F", "#00C832", "#00FF41"]

# --------------------------------------------------------------------------
# TYPOGRAPHY
# --------------------------------------------------------------------------
# GitHub renders SVG inside <img>, so no webfont may be loaded. Every asset
# falls back through common monospace faces and finally generic `monospace`.
FONT = ('"JetBrains Mono","Fira Code","IBM Plex Mono",'
        '"DejaVu Sans Mono","Courier New",monospace')

# Advance width of a monospace glyph as a fraction of font-size. Practically
# every monospace face ships 0.6em; `textLength` pins down the rest.
CH = 0.6


def w(text: str, size: float) -> float:
    """Rendered width of `text` at `size` px in a monospace face."""
    return len(text) * size * CH


# --------------------------------------------------------------------------
# ESCAPING
# --------------------------------------------------------------------------
def esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


# --------------------------------------------------------------------------
# SVG PRIMITIVES
# --------------------------------------------------------------------------
def defs(extra: str = "") -> str:
    """Filters and patterns shared by every asset."""
    return (
        '<defs>\n'
        '    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">\n'
        '      <feGaussianBlur stdDeviation="1.6" result="b"/>\n'
        '      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>\n'
        '    </filter>\n'
        '    <filter id="glow-soft" x="-40%" y="-40%" width="180%" height="180%">\n'
        '      <feGaussianBlur stdDeviation="3.2" result="b"/>\n'
        '      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>\n'
        '    </filter>\n'
        f'    <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">\n'
        f'      <rect width="4" height="1" fill="{GREEN}" opacity="0.03"/>\n'
        '    </pattern>\n'
        f'    <pattern id="grid" width="34" height="34" patternUnits="userSpaceOnUse">\n'
        f'      <path d="M34 0H0V34" fill="none" stroke="{GREEN}" stroke-width="0.5" opacity="0.05"/>\n'
        '    </pattern>\n'
        f'{extra}  </defs>'
    )


BASE_CSS = """
    text { font-family: %(font)s; white-space: pre; }
    .t { fill: %(text)s; }
    .t2 { fill: %(text2)s; }
    .g { fill: %(green)s; }
    .g2 { fill: %(green2)s; }
    .gd { fill: %(greend)s; }
    .m { fill: %(muted)s; }
    .b { font-weight: 700; }
    @keyframes fin { from { opacity: 0; } to { opacity: 1; } }
    @keyframes blink { 0%%, 48%% { opacity: 1; } 52%%, 96%% { opacity: 0; } 100%% { opacity: 1; } }
    @keyframes pulse { 0%%, 100%% { opacity: .3; } 50%% { opacity: 1; } }
    .cursor { animation: blink 1.15s steps(1) infinite; }
    .dot { animation: pulse 2.6s ease-in-out infinite; }
    /* `.in` elements are visible by default and merely fade in, so every
       asset stays complete and readable when animation is unavailable. */
    .in { animation: fin .55s ease-out both; }
    @media (prefers-reduced-motion: reduce) { * { animation: none !important; } }""" % {
    "font": FONT, "text": TEXT, "text2": TEXT_2, "green": GREEN,
    "green2": GREEN_2, "greend": GREEN_DARK, "muted": MUTED,
}


def open_svg(width: float, height: float, css: str = "", title: str = "",
             extra_defs: str = "", background: bool = True,
             full_width: bool = True) -> str:
    """Root element + shared defs + optional textured background.

    `full_width` assets stretch to the README column; buttons keep their
    intrinsic pixel size so they line up as inline images.
    """
    size_attrs = ('width="100%%"' if full_width
                  else 'width="%(w)g" height="%(h)g"')
    head = (
        '<svg xmlns="http://www.w3.org/2000/svg" ' + size_attrs + ' '
        'viewBox="0 0 %(w)g %(h)g" preserveAspectRatio="xMidYMid meet" '
        'role="img" aria-label="%(title)s">\n'
        '  <title>%(title)s</title>\n'
        '  %(defs)s\n'
        '  <style>%(css)s\n  </style>\n'
    ) % {"w": width, "h": height, "title": esc(title),
         "defs": defs(extra_defs), "css": BASE_CSS + css}
    if background:
        head += (
            f'  <rect width="{width:g}" height="{height:g}" rx="10" fill="{BG}"/>\n'
            f'  <rect width="{width:g}" height="{height:g}" rx="10" fill="url(#grid)"/>\n'
            f'  <rect width="{width:g}" height="{height:g}" rx="10" fill="url(#scan)"/>\n'
        )
    return head


def close_svg() -> str:
    return "</svg>\n"


def panel(x: float, y: float, width: float, height: float, *,
          fill: str = PANEL, stroke: str = BORDER, rx: float = 6,
          stroke_width: float = 1, opacity: float = 1) -> str:
    return (f'<rect x="{x:g}" y="{y:g}" width="{width:g}" height="{height:g}" '
            f'rx="{rx:g}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{stroke_width:g}" opacity="{opacity:g}"/>')


def text(x: float, y: float, content: str, *, size: float = 14,
         cls: str = "t", anchor: str = "start", fit: bool = True,
         letter_spacing: float | None = None, extra: str = "",
         opacity: float | None = None) -> str:
    """A single line of monospace text.

    `fit` pins the advance width with textLength so columns line up
    identically whichever monospace face the viewer has installed.
    """
    attrs = [f'x="{x:g}"', f'y="{y:g}"', f'font-size="{size:g}"',
             f'class="{cls}"', 'xml:space="preserve"']
    if anchor != "start":
        attrs.append(f'text-anchor="{anchor}"')
    if letter_spacing is not None:
        attrs.append(f'letter-spacing="{letter_spacing:g}"')
    elif fit and content.strip():
        attrs.append(f'textLength="{w(content, size):g}" lengthAdjust="spacing"')
    if opacity is not None:
        attrs.append(f'opacity="{opacity:g}"')
    if extra:
        attrs.append(extra)
    return f'<text {" ".join(attrs)}>{esc(content)}</text>'


def dots(x: float, y: float, r: float = 4, gap: float = 15) -> str:
    """Three terminal window indicators, in green shades only."""
    return "".join(
        f'<circle cx="{x + i * gap:g}" cy="{y:g}" r="{r:g}" fill="{c}" opacity="0.7"/>'
        for i, c in enumerate((GREEN_DARK, GREEN_2, GREEN)))


def prompt(x: float, y: float, command: str, *, size: float = 15,
           cursor: bool = True, delay: float = 0.0) -> str:
    """`rakesh@github:~$ <command>` with an optional blinking block cursor."""
    user, tail = "rakesh@github", ":~$ "
    out = [
        text(x, y, user, size=size, cls="g2"),
        text(x + w(user, size), y, tail, size=size, cls="m"),
        text(x + w(user + tail, size), y, command, size=size, cls="t b in",
             extra=f'style="animation-delay:{delay:g}s"'),
    ]
    if cursor:
        cx = x + w(user + tail + command, size) + size * 0.3
        out.append(f'<rect x="{cx:g}" y="{y - size * 0.8:g}" '
                   f'width="{size * 0.52:g}" height="{size * 0.92:g}" '
                   f'fill="{GREEN}" class="cursor"/>')
    return "".join(out)


def rule(x: float, y: float, width: float, *, color: str = BORDER,
         opacity: float = 1) -> str:
    return (f'<line x1="{x:g}" y1="{y:g}" x2="{x + width:g}" y2="{y:g}" '
            f'stroke="{color}" stroke-width="1" opacity="{opacity:g}"/>')


def status_pill(x: float, y: float, label: str, *, size: float = 11,
                color: str = GREEN, height: float = 20) -> tuple[str, float]:
    """`* ACTIVE` pill. The word carries the meaning; colour only reinforces."""
    width = w(label, size) + 30
    svg = (panel(x, y, width, height, fill=BG_2, stroke=color, rx=3, opacity=0.9)
           + f'<circle cx="{x + 11:g}" cy="{y + height / 2:g}" r="3" fill="{color}" class="dot"/>'
           + text(x + 20, y + height / 2 + size * 0.35, label, size=size,
                  cls="g" if color == GREEN else "g2"))
    return svg, width


def chip(x: float, y: float, label: str, *, size: float = 12, pad: float = 9,
         height: float = 24, fill: str = BG_2, stroke: str = BORDER,
         cls: str = "t") -> tuple[str, float]:
    """A bordered technology chip. Returns (svg, width)."""
    width = w(label, size) + pad * 2
    svg = (panel(x, y, width, height, fill=fill, stroke=stroke, rx=3) +
           text(x + pad, y + height / 2 + size * 0.35, label, size=size, cls=cls))
    return svg, width


def chip_row(x: float, y: float, labels, *, size: float = 12, gap: float = 7,
             height: float = 24, max_width: float | None = None,
             line_gap: float = 7, cls: str = "t", stroke: str = BORDER,
             fill: str = BG_2) -> tuple[str, float]:
    """Chips flowed left to right, wrapping at `max_width`.

    Returns (svg, total height consumed).
    """
    out, cx, cy = [], x, y
    for label in labels:
        width = w(label, size) + 18
        if max_width is not None and cx + width > x + max_width and cx > x:
            cx, cy = x, cy + height + line_gap
        svg, width = chip(cx, cy, label, size=size, height=height, cls=cls,
                          stroke=stroke, fill=fill)
        out.append(svg)
        cx += width + gap
    return "".join(out), cy + height - y


def leader(x: float, y: float, left: str, right: str, width_px: float, *,
           size: float = 13, right_cls: str = "g") -> str:
    """`portfolio_engine ......... ONLINE` with dotted leaders."""
    cols = max(int(width_px / (size * CH)), len(left) + len(right) + 2)
    fill_dots = max(cols - len(left) - len(right) - 2, 1)
    line = f"{left} {'.' * fill_dots} "
    return (text(x, y, line, size=size, cls="m") +
            text(x + w(line, size), y, right, size=size, cls=right_cls))


def write_svg(path: str, svg: str) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(svg)
    print(f"  {os.path.relpath(path, repo_path()):<40} "
          f"{len(svg.encode('utf-8')) / 1024:7.1f} KB")


def repo_path(*parts: str) -> str:
    """Path relative to the repository root, wherever the script is run from."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(root, *parts)
