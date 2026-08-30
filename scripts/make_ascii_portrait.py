"""
assets/profile-photo.jpg  ->  Matrix-green ASCII portrait.

Pipeline
    photo -> crop -> background flood-removal -> local contrast ->
    subject-only contrast stretch -> brightness mapping ->
    character ramp -> one SVG <text> run per colour tier per row

The result is emitted twice:
    * assets/ascii-portrait.svg   standalone, full detail, printing animation
    * an SVG fragment imported by generate_hero.py for the hero panel

If the photograph is missing, a clearly-marked placeholder frame is produced
instead. No face is ever invented.

Run:  python scripts/make_ascii_portrait.py
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import theme as T  # noqa: E402

# --------------------------------------------------------------------------
# TUNING  (everything worth adjusting lives here)
# --------------------------------------------------------------------------
ASCII_WIDTH = 96          # columns in the standalone portrait
HERO_WIDTH = 58           # columns in the hero panel portrait
CONTRAST = 1.15           # global contrast multiplier
BRIGHTNESS = 1.0          # global brightness multiplier
INVERT = True             # dark photo subject -> bright green ink
GREEN = T.GREEN           # brightest ink colour
CROP = (0.18, 0.11, 0.85, 0.64)   # left, top, right, bottom (fractions)
FLOOR = 0.12              # ink below this brightness is dropped entirely
GAMMA = 0.82              # <1 lifts midtones so facial structure survives
FADE_BOTTOM = 0.15        # bottom fraction that dissolves into the terminal
CELL_ASPECT = 0.55        # glyph width / line height
BG_TOLERANCE = 30         # flood-fill tolerance when removing the backdrop
BG_SEED_MIN = 150         # only flood from *light* border pixels
LOCAL_CONTRAST = (1.7, 0.55)      # (detail gain, global tone kept)

# Density ramp, sparse -> dense.
RAMP = " .,:;+=xX$#@"

# Ink tiers: (upper density bound, colour)
TIERS = ((0.34, T.GREEN_DARK), (0.67, T.GREEN_2), (1.01, GREEN))

PHOTO = T.repo_path("assets", "profile-photo.jpg")
OUT = T.repo_path("assets", "ascii-portrait.svg")


# --------------------------------------------------------------------------
# IMAGE -> ASCII
# --------------------------------------------------------------------------
def _strip_background(im, mask_out):
    """Flood the backdrop away from light border pixels, leaving the subject.

    Returns (image with backdrop forced to white, boolean backdrop mask).
    """
    import numpy as np
    from PIL import Image, ImageDraw, ImageFilter

    work = im.filter(ImageFilter.GaussianBlur(3))
    w, h = work.size
    seeds = [(x, 0) for x in range(0, w, 2)] + [(x, h - 1) for x in range(0, w, 2)]
    seeds += [(0, y) for y in range(0, h, 2)] + [(w - 1, y) for y in range(0, h, 2)]
    for seed in seeds:
        value = work.getpixel(seed)
        if value != 255 and value >= BG_SEED_MIN:
            ImageDraw.floodfill(work, seed, 255, thresh=BG_TOLERANCE)
    mask = np.array(work) == 255
    arr = np.array(im)
    arr[mask] = mask_out
    return Image.fromarray(arr), mask


def _local_contrast(im, mask):
    """Unsharp-style local normalisation: keeps hair and fabric from turning
    into flat slabs while facial structure stays readable."""
    import numpy as np
    from PIL import Image, ImageFilter

    gain, keep = LOCAL_CONTRAST
    radius = max(6, im.size[0] // 30)
    base = np.array(im).astype(np.float32)
    low = np.array(im.filter(ImageFilter.GaussianBlur(radius))).astype(np.float32)
    out = 128 + (base - low) * gain + (low - 128) * keep
    out = np.clip(out, 0, 255)
    out[mask] = 255
    return Image.fromarray(out.astype(np.uint8))


def _stretch(im, mask):
    """Contrast stretch driven by the subject only, so a bright backdrop can
    not compress the tonal range of the face."""
    import numpy as np
    from PIL import Image

    arr = np.array(im).astype(np.float32)
    subject = arr[~mask]
    lo, hi = np.percentile(subject, 2), np.percentile(subject, 98)
    arr = np.clip((arr - lo) * 255.0 / max(hi - lo, 1), 0, 255)
    arr[mask] = 255
    return Image.fromarray(arr.astype(np.uint8))


def build_rows(width: int = ASCII_WIDTH) -> list[str] | None:
    """Return the portrait as a list of equal-length ASCII rows, or None when
    no photograph is available."""
    if not os.path.exists(PHOTO):
        return None

    from PIL import Image, ImageEnhance

    im = Image.open(PHOTO).convert("L")
    px_w, px_h = im.size
    left, top, right, bottom = CROP
    im = im.crop((int(left * px_w), int(top * px_h),
                  int(right * px_w), int(bottom * px_h)))

    im, mask = _strip_background(im, 255)
    im = _local_contrast(im, mask)
    im = _stretch(im, mask)
    im = ImageEnhance.Contrast(im).enhance(CONTRAST)
    im = ImageEnhance.Brightness(im).enhance(BRIGHTNESS)

    crop_w, crop_h = im.size
    rows_n = max(1, round(width * (crop_h / crop_w) * CELL_ASPECT))
    small = im.resize((width, rows_n), Image.LANCZOS)
    pixels = small.load()

    rows = []
    for y in range(rows_n):
        dissolve = 1.0
        if FADE_BOTTOM:
            start = rows_n * (1 - FADE_BOTTOM)
            if y > start:
                dissolve = max(0.0, 1 - (y - start) / (rows_n - start)) ** 0.8
        line = []
        for x in range(width):
            v = pixels[x, y] / 255.0
            if INVERT:
                v = 1.0 - v
            v = 0.0 if v < FLOOR else ((v - FLOOR) / (1 - FLOOR)) ** GAMMA
            v *= dissolve
            line.append(RAMP[min(int(v * len(RAMP)), len(RAMP) - 1)])
        rows.append("".join(line))
    return _trim(rows)


def _trim(rows: list[str]) -> list[str]:
    """Drop fully blank rows and columns so the portrait fills its frame."""
    while rows and not rows[0].strip():
        rows.pop(0)
    while rows and not rows[-1].strip():
        rows.pop()
    if not rows:
        return rows
    left = min((len(r) - len(r.lstrip())) for r in rows if r.strip())
    right = max((len(r.rstrip())) for r in rows)
    return [r[left:right].ljust(right - left) for r in rows]


# --------------------------------------------------------------------------
# ASCII -> SVG
# --------------------------------------------------------------------------
def _tier_of(char: str) -> int:
    density = (RAMP.index(char) + 1) / len(RAMP)
    for i, (bound, _) in enumerate(TIERS):
        if density <= bound:
            return i
    return len(TIERS) - 1


def rows_to_svg(rows: list[str], x: float, y: float, size: float,
                line_height: float | None = None) -> str:
    """One <text> run per colour tier per row - a few hundred nodes, not tens
    of thousands, so the asset stays small."""
    cell = size * T.CH
    line_height = line_height or size * 1.06
    out = []
    for r, row in enumerate(rows):
        by_tier = [[" "] * len(row) for _ in TIERS]
        for c, char in enumerate(row):
            if char != " ":
                by_tier[_tier_of(char)][c] = char
        ty = y + r * line_height
        for tier, chars in enumerate(by_tier):
            line = "".join(chars)
            stripped = line.rstrip()
            if not stripped.strip():
                continue
            lead = len(stripped) - len(stripped.lstrip())
            seg = stripped[lead:]
            out.append(
                f'<text x="{x + lead * cell:.2f}" y="{ty:.2f}" '
                f'font-size="{size:g}" fill="{TIERS[tier][1]}" '
                f'textLength="{len(seg) * cell:.2f}" lengthAdjust="spacing" '
                f'xml:space="preserve">{T.esc(seg)}</text>')
    return "".join(out)


def print_reveal(x: float, y: float, width: float, height: float,
                 rows_n: int, clip_id: str, duration: float = 2.8) -> tuple[str, str]:
    """Line-printer reveal: a clip rectangle that steps down row by row plus a
    bright print head. Returns (defs fragment, print-head fragment).

    SMIL drives it; without SMIL the clip stays at full height, so the
    portrait is simply complete from the first frame.
    """
    steps = [f"{height * i / rows_n:.1f}" for i in range(rows_n + 1)]
    times = [f"{i / rows_n:.4f}" for i in range(rows_n + 1)]
    clip = (
        f'<clipPath id="{clip_id}">'
        f'<rect x="{x:g}" y="{y:g}" width="{width:g}" height="{height:g}">'
        f'<animate attributeName="height" values="{";".join(steps)}" '
        f'keyTimes="{";".join(times)}" calcMode="discrete" dur="{duration}s" '
        f'begin="0s" fill="freeze"/></rect></clipPath>'
    )
    head_y = [f"{y + height * i / rows_n:.1f}" for i in range(rows_n + 1)]
    head = (
        f'<rect x="{x:g}" y="{y:g}" width="{width:g}" height="2" '
        f'fill="{T.GREEN_BRIGHT}" opacity="0" filter="url(#glow)">'
        f'<animate attributeName="y" values="{";".join(head_y)}" '
        f'keyTimes="{";".join(times)}" calcMode="discrete" dur="{duration}s" fill="freeze"/>'
        f'<animate attributeName="opacity" values="0.85;0.85;0" keyTimes="0;0.9;1" '
        f'dur="{duration}s" fill="freeze"/></rect>'
    )
    return clip, head


PRINT_STAGES = ("INITIALIZING PORTRAIT", "PRINTING 12%", "PRINTING 27%",
                "PRINTING 46%", "PRINTING 68%", "PRINTING 87%")


def print_status(x: float, y: float, size: float = 11,
                 duration: float = 2.8) -> str:
    """Transient PRINTING n% readout settling on IDENTITY LOADED.

    Transient lines are statically hidden and only revealed by animation, so
    a viewer without CSS animation sees the finished state alone.
    """
    slot = duration / (len(PRINT_STAGES) + 1)
    out = []
    for i, stage in enumerate(PRINT_STAGES):
        out.append(
            f'<text x="{x:g}" y="{y:g}" font-size="{size:g}" fill="{T.MUTED}" '
            f'opacity="0" class="stage" xml:space="preserve" '
            f'style="animation-delay:{i * slot:.2f}s">{T.esc(stage + "...")}</text>')
    out.append(
        f'<text x="{x:g}" y="{y:g}" font-size="{size:g}" fill="{GREEN}" '
        f'class="loaded" letter-spacing="1.4" xml:space="preserve">IDENTITY LOADED</text>')
    return "".join(out)


PORTRAIT_CSS = """
    @keyframes stage { 0%%, 100%% { opacity: 0; } 8%%, 92%% { opacity: 1; } }
    .stage { animation: stage %(slot).2fs steps(1) both; }
    .loaded { animation: fin .6s ease-out %(hold).2fs both; }"""


def portrait_css(duration: float = 2.8) -> str:
    slot = duration / (len(PRINT_STAGES) + 1)
    return PORTRAIT_CSS % {"slot": slot, "hold": duration - slot * 0.4}


def placeholder(x: float, y: float, width: float, height: float) -> str:
    """Shown until assets/profile-photo.jpg exists. Never a fabricated face."""
    cx = x + width / 2
    lines = [("[ NO SOURCE IMAGE ]", 13, "g2", 0),
             ("add  assets/profile-photo.jpg", 11, "t2", 26),
             ("then run", 10, "m", 48),
             ("scripts/make_ascii_portrait.py", 10, "m", 66)]
    out = [f'<rect x="{x:g}" y="{y:g}" width="{width:g}" height="{height:g}" '
           f'rx="4" fill="{T.BG_2}" stroke="{T.BORDER}" stroke-width="1" '
           f'stroke-dasharray="5 4"/>']
    top = y + height / 2 - 40
    for label, size, cls, dy in lines:
        out.append(T.text(cx, top + dy, label, size=size, cls=cls, anchor="middle"))
    return "".join(out)


# --------------------------------------------------------------------------
# STANDALONE ASSET
# --------------------------------------------------------------------------
def build_svg() -> str:
    pad, size = 28, 9.0
    rows = build_rows(ASCII_WIDTH)
    line_h = size * 1.06

    if rows:
        art_w = len(rows[0]) * size * T.CH
        art_h = len(rows) * line_h
    else:
        art_w, art_h = 420, 300

    width = art_w + pad * 2
    height = art_h + pad * 2 + 84

    clip_defs, head = ("", "")
    if rows:
        clip_defs, head = print_reveal(pad, pad + 46, art_w, art_h, len(rows),
                                       "portrait-reveal")

    svg = [T.open_svg(width, height, css=portrait_css(),
                      title="ASCII portrait of Rakesh Surampalli, printed in Matrix green",
                      extra_defs="    " + clip_defs + "\n" if clip_defs else "")]
    svg.append(T.panel(0.5, 0.5, width - 1, height - 1, fill="none",
                       stroke=T.BORDER, rx=10))
    svg.append(T.dots(pad + 4, pad - 2))
    svg.append(T.text(pad + 52, pad + 2, "identity // ascii portrait",
                      size=11, cls="m"))
    svg.append(T.rule(pad, pad + 16, width - pad * 2, opacity=0.7))

    if rows:
        svg.append(f'<g clip-path="url(#portrait-reveal)" filter="url(#glow)" '
                   f'opacity="0.96">')
        svg.append(rows_to_svg(rows, pad, pad + 46 + size, size, line_h))
        svg.append("</g>")
        svg.append(head)
    else:
        svg.append(placeholder(pad, pad + 46, art_w, art_h))

    footer = height - pad + 2
    svg.append(T.rule(pad, footer - 22, width - pad * 2, opacity=0.7))
    svg.append(print_status(pad, footer, size=11) if rows else
               T.text(pad, footer, "AWAITING SOURCE IMAGE", size=11, cls="m"))
    svg.append(T.text(width - pad, footer, "RAKESH SURAMPALLI", size=11,
                      cls="g2", anchor="end", letter_spacing=1.4))
    svg.append(T.close_svg())
    return "".join(svg)


def main() -> None:
    T.write_svg(OUT, build_svg())
    if not os.path.exists(PHOTO):
        print("  note: assets/profile-photo.jpg missing - placeholder rendered")


if __name__ == "__main__":
    main()
