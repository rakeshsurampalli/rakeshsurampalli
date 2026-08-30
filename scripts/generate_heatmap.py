"""
assets/contribution-stream.svg - the GitHub activity heatmap, Matrix edition.

Reads the cache written by fetch_contributions.py and renders a terminal
contribution stream: 53 week columns, month markers, a legend and headline
figures that are all derived from the fetched data. Nothing here invents a
number; with no cache present the panel says so instead.

Run:  python scripts/generate_heatmap.py
"""

from __future__ import annotations

import json
import os
import sys
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import theme as T  # noqa: E402

W = 1000
PAD = 24
CELL, GAP = 13, 3.4        # heatmap cell size and spacing
GRID_X, GRID_Y = 74, 176   # top-left of the grid

CACHE = T.repo_path("assets", "contributions.json")
OUT = T.repo_path("assets", "contribution-stream.svg")

# empty cells keep a hairline so the grid stays legible at level 0
EMPTY_OUTLINE = f' stroke="{T.BORDER}" stroke-width="0.6"'

MONTHS = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN",
          "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")

CSS = """
    @keyframes cellin { from { opacity: 0; } to { opacity: 1; } }
    .wk { animation: cellin .5s ease-out both; }
    @keyframes sweep { 0%% { opacity: 0; } 6%% { opacity: .5; }
                       92%% { opacity: .12; } 100%% { opacity: 0; } }
    .sweep { opacity: 0; animation: sweep 3.4s ease-out 1 both; }""" % {}


# --------------------------------------------------------------------------
# STATS - every figure below is computed from the fetched calendar
# --------------------------------------------------------------------------
def stats(days: list[dict]) -> dict:
    counts = [d["count"] for d in days]
    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    current = 0
    for d in reversed(days):
        if not d["count"]:
            break
        current += 1
    busiest = max(days, key=lambda d: d["count"])
    return {
        "total": sum(counts),
        "active": sum(1 for c in counts if c),
        "current": current,
        "longest": longest,
        "busiest": busiest["count"],
        "busiest_date": busiest["date"],
        "span": f'{days[0]["date"]} -> {days[-1]["date"]}',
    }


def stat_block(x: float, y: float, width: float, value: str, label: str) -> str:
    return (T.panel(x, y, width, 54, fill=T.PANEL, stroke=T.BORDER) +
            f'<rect x="{x:g}" y="{y:g}" width="3" height="54" '
            f'fill="{T.GREEN_DARK}" opacity="0.9"/>' +
            T.text(x + 16, y + 26, value, size=19, cls="g b", letter_spacing=1) +
            T.text(x + 16, y + 44, label, size=9.5, cls="m", letter_spacing=1.4))


# --------------------------------------------------------------------------
# GRID
# --------------------------------------------------------------------------
def grid(days: list[dict]) -> tuple[str, float]:
    """53 columns of 7 cells, anchored so the last column holds the latest day."""
    first = date.fromisoformat(days[0]["date"])
    by_date = {d["date"]: d for d in days}
    start = first - timedelta(days=(first.weekday() + 1) % 7)   # back to Sunday
    last = date.fromisoformat(days[-1]["date"])
    weeks = (last - start).days // 7 + 1

    out, months = [], []
    seen = set()
    for wk in range(weeks):
        x = GRID_X + wk * (CELL + GAP)
        cells = []
        for dow in range(7):
            day = start + timedelta(days=wk * 7 + dow)
            record = by_date.get(day.isoformat())
            if record is None:
                continue
            y = GRID_Y + dow * (CELL + GAP)
            level = record["level"]
            outline = EMPTY_OUTLINE if level == 0 else ""
            glow = ' filter="url(#glow)"' if record["count"] >= 8 else ""
            tip = f'{record["count"]} on {record["date"]}'
            cells.append(f'<rect x="{x:g}" y="{y:g}" width="{CELL:g}" '
                         f'height="{CELL:g}" rx="2.5" fill="{T.HEAT[level]}"'
                         f'{outline}{glow}><title>{tip}</title></rect>')
            if day.day <= 7 and day.month not in seen and dow == 0:
                seen.add(day.month)
                months.append((x, MONTHS[day.month - 1]))
        if cells:
            out.append(f'<g class="wk" style="animation-delay:{wk * 0.022:.3f}s">'
                       + "".join(cells) + "</g>")

    labels = [T.text(x, GRID_Y - 10, name, size=9.5, cls="m", letter_spacing=1.2)
              for x, name in months]
    for i, name in ((1, "MON"), (3, "WED"), (5, "FRI")):
        labels.append(T.text(GRID_X - 12, GRID_Y + i * (CELL + GAP) + 10, name,
                             size=9, cls="m", anchor="end", letter_spacing=1))
    width = weeks * (CELL + GAP) - GAP
    return "".join(labels) + "".join(out), width


def legend(x: float, y: float) -> str:
    out = [T.text(x, y + 10, "LESS", size=9.5, cls="m", letter_spacing=1.2)]
    bx = x + 36
    for level, colour in enumerate(T.HEAT):
        outline = EMPTY_OUTLINE if level == 0 else ""
        out.append(f'<rect x="{bx:g}" y="{y:g}" width="12" height="12" rx="2.5" '
                   f'fill="{colour}"{outline}/>')
        bx += 16
    out.append(T.text(bx + 4, y + 10, "MORE", size=9.5, cls="m", letter_spacing=1.2))
    return "".join(out)


# --------------------------------------------------------------------------
# DOCUMENT
# --------------------------------------------------------------------------
def offline_panel() -> str:
    """No cache yet: say so plainly rather than draw invented activity."""
    height = 200
    svg = [T.open_svg(W, height, css=CSS,
                      title="GitHub contribution stream: awaiting first sync")]
    svg.append(T.prompt(PAD, 34, "./activity_stream", size=15))
    svg.append(T.rule(PAD, 50, W - PAD * 2, opacity=0.7))
    svg.append(T.panel(PAD, 74, W - PAD * 2, 96, fill=T.PANEL, stroke=T.BORDER))
    svg.append(T.text(W / 2, 118, "CONTRIBUTION STREAM: AWAITING SYNC", size=14,
                      cls="g2", anchor="middle", letter_spacing=1.8))
    svg.append(T.text(W / 2, 142, "run  python scripts/fetch_contributions.py",
                      size=11, cls="m", anchor="middle"))
    svg.append(T.close_svg())
    return "".join(svg)


def build(data: dict) -> str:
    days = data["days"]
    s = stats(days)
    cells, grid_w = grid(days)
    height = GRID_Y + 7 * (CELL + GAP) + 86

    svg = [T.open_svg(W, height, css=CSS,
                      title=(f"GitHub contribution stream for {data['login']}: "
                             f"{s['total']} contributions across {s['active']} "
                             f"active days in the last year"))]
    svg.append(T.prompt(PAD, 34, "./activity_stream", size=15))
    svg.append(T.text(W - PAD, 34, "CONTRIBUTION STREAM // LIVE", size=10.5,
                      cls="m", anchor="end", letter_spacing=1.6))
    svg.append(T.rule(PAD, 50, W - PAD * 2, opacity=0.7))

    blocks = ((str(s["total"]), "CONTRIBUTIONS / 365 DAYS"),
              (str(s["active"]), "ACTIVE DAYS"),
              (str(s["current"]), "CURRENT STREAK / DAYS"),
              (str(s["longest"]), "LONGEST STREAK / DAYS"),
              (str(s["busiest"]), "BUSIEST DAY"))
    inner = W - PAD * 2
    bw = (inner - 14 * (len(blocks) - 1)) / len(blocks)
    for i, (value, label) in enumerate(blocks):
        svg.append(stat_block(PAD + i * (bw + 14), 72, bw, value, label))

    svg.append(cells)

    # single slow scan line, then gone
    svg.append(f'<rect x="{GRID_X:g}" y="{GRID_Y - 4:g}" width="26" '
               f'height="{7 * (CELL + GAP) + 4:g}" fill="{T.GREEN}" class="sweep">'
               f'<animate attributeName="x" from="{GRID_X:g}" '
               f'to="{GRID_X + grid_w:g}" dur="3.4s" fill="freeze"/></rect>')

    svg.append(legend(GRID_X, GRID_Y + 7 * (CELL + GAP) + 10))

    foot = height - PAD - 4
    svg.append(T.rule(PAD, foot - 20, inner, opacity=0.6))
    svg.append(T.text(PAD, foot, "CONTRIBUTION STREAM", size=11, cls="g2",
                      letter_spacing=1.6))
    svg.append(T.text(PAD + 200, foot, s["span"], size=10.5, cls="m"))
    pill_w = T.w("ONLINE", 11) + 30
    pill, _ = T.status_pill(W - PAD - pill_w, foot - 14, "ONLINE")
    svg.append(T.text(W - PAD - pill_w - 18, foot, f"SYNCED {data['fetched_at']}",
                      size=10.5, cls="m", anchor="end", letter_spacing=1.2))
    svg.append(pill)
    svg.append(T.close_svg())
    return "".join(svg)


def main() -> None:
    if not os.path.exists(CACHE):
        print("  no assets/contributions.json - rendering awaiting-sync panel")
        T.write_svg(OUT, offline_panel())
        return
    with open(CACHE, encoding="utf-8") as fh:
        data = json.load(fh)
    T.write_svg(OUT, build(data))


if __name__ == "__main__":
    main()
