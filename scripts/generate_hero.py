"""
assets/hero-terminal.svg - the profile's boot screen.

A single terminal window holding the boot sequence, the identity block, the
core domains, the primary stack and the ASCII portrait printing itself on the
right. Animation is additive only: every element's static state is its final
state, so the hero is complete even where animation never runs.

Run:  python scripts/generate_hero.py
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import make_ascii_portrait as P  # noqa: E402
import theme as T  # noqa: E402

W, H = 1000, 548
PAD = 34
BAR = 36            # title bar height
COL = 552           # x where the portrait column starts

BOOT = ("github activity stream online",
        "loading engineering profile",
        "initializing AI systems",
        "connecting project registry",
        "identity verified")

NAME = "RAKESH SURAMPALLI"
ROLES = ("FULL-STACK AI ENGINEER", "AI PRODUCT BUILDER")

DOMAINS = ("Generative AI", "Agentic Systems",
           "Hybrid RAG", "Full-Stack Engineering",
           "Cloud-Native Systems", "AI Security")

STACK = ("Python", "FastAPI", "React", "LangGraph", "LangChain",
         "PostgreSQL", "Docker", "Kubernetes", "AWS", "Azure", "GCP")

CSS = """
    .boot { animation: fin .45s ease-out both; }
    .name { letter-spacing: 3px; }"""


def build() -> str:
    rows = P.build_rows(P.HERO_WIDTH)

    # -- portrait column geometry ------------------------------------------
    col_w = W - COL - PAD
    panel_top, panel_h = BAR + 20, H - BAR - 20 - PAD + 10
    box_w, box_h = col_w - 44, panel_h - 96      # room inside the panel
    if rows:
        # Largest glyph size that fits the panel in both directions.
        size = min(box_w / (len(rows[0]) * T.CH), box_h / (len(rows) * 1.06))
        line_h = size * 1.06
        art_w, art_h = len(rows[0]) * size * T.CH, len(rows) * line_h
    else:
        size = line_h = 11.0
        art_w, art_h = box_w, 300
    art_x = COL + (col_w - art_w) / 2
    art_top = panel_top + 44 + max(0.0, (box_h - art_h) / 2)

    clip, head = ("", "")
    if rows:
        clip, head = P.print_reveal(art_x, art_top, art_w, art_h, len(rows),
                                    "hero-reveal")

    svg = [T.open_svg(
        W, H, css=CSS + P.portrait_css(),
        title=("Terminal hero: Rakesh Surampalli, Full-Stack AI Engineer and "
               "AI Product Builder. System status online."),
        extra_defs=("    " + clip + "\n") if clip else "")]

    # -- window chrome ------------------------------------------------------
    svg.append(T.panel(0.5, 0.5, W - 1, H - 1, fill="none", stroke=T.BORDER, rx=10))
    svg.append(f'<path d="M0.5 {BAR}.5 H {W - 0.5}" stroke="{T.BORDER}" fill="none"/>')
    svg.append(T.dots(24, BAR / 2))
    svg.append(T.text(72, BAR / 2 + 4, "rakesh@github: ~/profile", size=11.5, cls="m"))
    svg.append(T.text(W - 26, BAR / 2 + 4, "SYSTEM STATUS: ONLINE", size=11.5,
                      cls="g", anchor="end", letter_spacing=1.2))
    svg.append(f'<rect x="{W - 20:g}" y="{BAR / 2 - 6:g}" width="6" height="11" '
               f'fill="{T.GREEN}" class="cursor"/>')

    # -- boot sequence ------------------------------------------------------
    y = BAR + 34
    for i, line in enumerate(BOOT):
        svg.append(T.text(PAD, y, ">", size=12.5, cls="g2 boot",
                          extra=f'style="animation-delay:{i * .32:.2f}s"'))
        svg.append(T.text(PAD + 16, y, line, size=12.5, cls="t2 boot",
                          extra=f'style="animation-delay:{i * .32:.2f}s"'))
        y += 19

    # -- identity -----------------------------------------------------------
    y += 30
    svg.append(T.text(PAD, y, NAME, size=39, cls="t b name in",
                      letter_spacing=3, extra='style="animation-delay:1.5s" '
                                              'filter="url(#glow-soft)"'))
    y += 20
    svg.append(T.rule(PAD, y, COL - PAD - 56, color=T.GREEN, opacity=0.55))
    svg.append(T.rule(PAD, y + 4, COL - PAD - 200, color=T.BORDER))

    y += 34
    svg.append(T.text(PAD, y, ROLES[0], size=16.5, cls="g b", letter_spacing=1.6))
    y += 24
    svg.append(T.text(PAD, y, ROLES[1], size=16.5, cls="g2 b", letter_spacing=1.6))

    # -- core domains -------------------------------------------------------
    y += 38
    svg.append(T.text(PAD, y, "// CORE DOMAINS", size=10.5, cls="m", letter_spacing=1.8))
    y += 20
    for i, item in enumerate(DOMAINS):
        cx = PAD + (i % 2) * 266
        cy = y + (i // 2) * 22
        svg.append(f'<rect x="{cx:g}" y="{cy - 7:g}" width="5" height="5" '
                   f'fill="{T.GREEN_2}"/>')
        svg.append(T.text(cx + 14, cy, item, size=13, cls="t"))

    # -- primary stack ------------------------------------------------------
    y += 3 * 22 + 22
    svg.append(T.text(PAD, y, "// PRIMARY STACK", size=10.5, cls="m", letter_spacing=1.8))
    y += 12
    chips, used = T.chip_row(PAD, y, STACK, size=11.5, height=23,
                             max_width=COL - PAD - 40)
    svg.append(chips)

    # -- status bar ---------------------------------------------------------
    y = H - PAD - 6
    pill, pw = T.status_pill(PAD, y - 15, "STATUS: ONLINE")
    svg.append(pill)
    svg.append(T.text(PAD + pw + 14, y, "MODE: BUILDING", size=11, cls="t2",
                      letter_spacing=1.2))
    svg.append(T.text(PAD + pw + 158, y, "FOCUS: PRODUCTION AI", size=11, cls="m",
                      letter_spacing=1.2))

    # -- portrait column ----------------------------------------------------
    svg.append(T.panel(COL, panel_top, col_w, panel_h, fill=T.BG_2, stroke=T.BORDER))
    svg.append(T.text(COL + 16, BAR + 40, "// IDENTITY", size=10.5, cls="m",
                      letter_spacing=1.8))
    svg.append(T.text(COL + col_w - 16, BAR + 40, "ASCII", size=10.5, cls="gd",
                      anchor="end", letter_spacing=1.8))

    if rows:
        svg.append('<g clip-path="url(#hero-reveal)" filter="url(#glow)" opacity="0.96">')
        svg.append(P.rows_to_svg(rows, art_x, art_top + size, size, line_h))
        svg.append("</g>")
        svg.append(head)
    else:
        svg.append(P.placeholder(art_x, art_top, col_w - 32, art_h))

    foot = H - PAD - 6
    svg.append(T.rule(COL + 16, foot - 20, col_w - 32, opacity=0.7))
    svg.append(P.print_status(COL + 16, foot, size=10.5) if rows else
               T.text(COL + 16, foot, "AWAITING SOURCE IMAGE", size=10.5, cls="m"))
    svg.append(T.close_svg())
    return "".join(svg)


def main() -> None:
    T.write_svg(T.repo_path("assets", "hero-terminal.svg"), build())


if __name__ == "__main__":
    main()
