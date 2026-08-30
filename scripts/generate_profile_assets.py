"""
Regenerate every static profile asset.

    python scripts/generate_profile_assets.py

Runs offline. The contribution stream needs the network, so it is refreshed
separately (and by the scheduled workflow):

    python scripts/fetch_contributions.py
"""

from __future__ import annotations

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import generate_architecture  # noqa: E402
import generate_buttons  # noqa: E402
import generate_heatmap  # noqa: E402
import generate_hero  # noqa: E402
import generate_sections  # noqa: E402
import make_ascii_portrait  # noqa: E402

STEPS = (
    ("ascii portrait", make_ascii_portrait.main),
    ("hero terminal", generate_hero.main),
    ("architecture", generate_architecture.main),
    ("sections", generate_sections.main),
    ("buttons", generate_buttons.main),
    ("contribution stream (from cache)", generate_heatmap.main),
)


def main() -> None:
    started = time.time()
    for name, step in STEPS:
        print(f"\n[ {name} ]")
        step()
    print(f"\ndone in {time.time() - started:.1f}s")


if __name__ == "__main__":
    main()
