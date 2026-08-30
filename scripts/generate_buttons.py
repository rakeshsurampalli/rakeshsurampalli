"""
Custom SVG navigation and social buttons.

GitHub cannot make regions of one image clickable, so every button is its own
small SVG wrapped in its own <a> in the README. That keeps the terminal look
without shields.io badges and without blue link text.

Run:  python scripts/generate_buttons.py
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import theme as T  # noqa: E402

# section anchor buttons
NAV = ("ABOUT", "PROJECTS", "ARCHITECTURE", "STACK", "FOCUS", "ACTIVITY",
       "CONNECT")

# social buttons: (file suffix, label)
SOCIAL = (("linkedin", "LINKEDIN"), ("portfolio", "PORTFOLIO"),
          ("medium", "MEDIUM"), ("email", "EMAIL"))


def nav_button(label: str) -> str:
    size, height, pad = 11.5, 30, 15
    tw = T.w(label, size) + (len(label) - 1) * 1.4
    width = tw + pad * 2 + 10
    svg = [T.open_svg(width, height, title=f"{label} section", background=False,
                      full_width=False)]
    svg.append(T.panel(0.5, 0.5, width - 1, height - 1, fill=T.PANEL,
                       stroke=T.BORDER, rx=3))
    svg.append(f'<rect x="0.5" y="0.5" width="2.5" height="{height - 1:g}" '
               f'fill="{T.GREEN_DARK}"/>')
    svg.append(T.text(pad + 5, height / 2 + size * 0.36, label, size=size,
                      cls="g2", letter_spacing=1.4))
    svg.append(T.close_svg())
    return "".join(svg)


def social_button(label: str) -> str:
    size, height, pad = 12.5, 40, 20
    tw = T.w(label, size) + (len(label) - 1) * 1.6
    width = tw + pad * 2 + 18
    svg = [T.open_svg(width, height, title=f"{label} link", background=False,
                      full_width=False)]
    svg.append(T.panel(0.5, 0.5, width - 1, height - 1, fill=T.BG_2,
                       stroke=T.BORDER, rx=4))
    svg.append(f'<rect x="{pad:g}" y="{height / 2 - 3:g}" width="6" height="6" '
               f'fill="{T.GREEN}" filter="url(#glow)"/>')
    svg.append(T.text(pad + 18, height / 2 + size * 0.36, label, size=size,
                      cls="g b", letter_spacing=1.6))
    svg.append(T.close_svg())
    return "".join(svg)


def main() -> None:
    for label in NAV:
        T.write_svg(T.repo_path("assets", f"nav-{label.lower()}.svg"),
                    nav_button(label))
    for name, label in SOCIAL:
        T.write_svg(T.repo_path("assets", f"btn-{name}.svg"),
                    social_button(label))


if __name__ == "__main__":
    main()
