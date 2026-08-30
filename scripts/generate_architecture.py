"""
assets/architecture.svg - the reference AI system architecture.

A compact layered diagram: client -> API -> orchestration -> agents and
retrieval -> tools and data -> cloud -> observability. Thin Matrix-green
connectors, green node titles, off-white labels.

Signal flow is suggested by a dashed overlay that only exists while the
animation runs; the solid connectors underneath carry the diagram on their
own when it does not.

Run:  python scripts/generate_architecture.py
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import theme as T  # noqa: E402

W = 1000
PAD = 24
CX = W / 2

CSS = """
    @keyframes flow { to { stroke-dashoffset: -22; } }
    .flow { animation: flow 1.6s linear infinite; opacity: 0; }
    .node { animation: fin .5s ease-out both; }"""


def node(cx: float, y: float, width: float, height: float, title: str,
         sub: str = "", *, accent: str = T.BORDER, title_size: float = 13.5,
         delay: float = 0.0) -> str:
    x = cx - width / 2
    out = [f'<g class="node" style="animation-delay:{delay:.2f}s">',
           T.panel(x, y, width, height, fill=T.PANEL, stroke=accent),
           f'<rect x="{x:g}" y="{y:g}" width="{width:g}" height="2" '
           f'fill="{accent}" opacity="0.85"/>']
    ty = y + (height / 2 + title_size * 0.36) - (9 if sub else 0)
    out.append(T.text(cx, ty, title, size=title_size, cls="g b",
                      anchor="middle", letter_spacing=1.5))
    if sub:
        out.append(T.text(cx, ty + 18, sub, size=10.5, cls="t2",
                          anchor="middle", letter_spacing=1.1))
    out.append("</g>")
    return "".join(out)


def arrow(x: float, y: float) -> str:
    return (f'<path d="M{x - 4:g} {y - 5:g} L{x + 4:g} {y - 5:g} L{x:g} {y:g} Z" '
            f'fill="{T.GREEN_2}"/>')


def link_v(x: float, y1: float, y2: float) -> str:
    """Straight vertical connector with an arrow head and a flow overlay."""
    return (f'<line x1="{x:g}" y1="{y1:g}" x2="{x:g}" y2="{y2 - 5:g}" '
            f'stroke="{T.BORDER}" stroke-width="1.2"/>'
            f'<line x1="{x:g}" y1="{y1:g}" x2="{x:g}" y2="{y2 - 5:g}" '
            f'stroke="{T.GREEN}" stroke-width="1.2" stroke-dasharray="6 16" '
            f'class="flow"/>' + arrow(x, y2))


def link_elbow(x1: float, y1: float, x2: float, y2: float,
               drop: float = 26) -> str:
    """Vertical, across, vertical - the classic architecture elbow."""
    d = (f"M{x1:g} {y1:g} V{y1 + drop:g} H{x2:g} V{y2 - 5:g}")
    return (f'<path d="{d}" fill="none" stroke="{T.BORDER}" stroke-width="1.2"/>'
            f'<path d="{d}" fill="none" stroke="{T.GREEN}" stroke-width="1.2" '
            f'stroke-dasharray="6 16" class="flow"/>' + arrow(x2, y2))


def band(y: float, height: float, title: str, items, *,
         accent: str = T.BORDER) -> str:
    x, width = PAD, W - PAD * 2
    out = [T.panel(x, y, width, height, fill=T.BG_2, stroke=accent),
           f'<rect x="{x:g}" y="{y:g}" width="3" height="{height:g}" '
           f'fill="{accent}" opacity="0.9"/>',
           T.text(x + 20, y + height / 2 + 5, title, size=12.5, cls="g b",
                  letter_spacing=1.8)]
    label = "   /   ".join(items)
    out.append(T.text(W - PAD - 20, y + height / 2 + 5, label, size=11,
                      cls="t2", anchor="end", letter_spacing=1))
    return "".join(out)


def build() -> str:
    top = 76
    rows = {
        "user": top,
        "client": top + 74,
        "api": top + 148,
        "orch": top + 226,
        "split": top + 330,
        "leaf": top + 428,
    }
    node_h, wide_h = 44, 56
    height = rows["leaf"] + node_h + 34 + 60 + 14 + 60 + PAD

    svg = [T.open_svg(W, height, css=CSS,
                      title="Reference AI system architecture: client, API, "
                            "LangGraph orchestration, agents, hybrid RAG, data "
                            "stores, cloud and observability")]
    svg.append(f'<g transform="translate(0,0)">')
    svg.append(T.prompt(PAD, 34, "./architecture.sh", size=15))
    svg.append(T.text(W - PAD, 34, "REFERENCE AI SYSTEM", size=10.5, cls="m",
                      anchor="end", letter_spacing=1.6))
    svg.append(T.rule(PAD, 50, W - PAD * 2, opacity=0.7))

    left, right = CX - 208, CX + 208
    leaves = (CX - 330, CX - 110, CX + 110, CX + 330)

    # connectors first so nodes sit on top
    svg.append(link_v(CX, rows["user"] + node_h, rows["client"]))
    svg.append(link_v(CX, rows["client"] + node_h, rows["api"]))
    svg.append(link_v(CX, rows["api"] + node_h, rows["orch"]))
    svg.append(link_elbow(CX, rows["orch"] + wide_h, left, rows["split"]))
    svg.append(link_elbow(CX, rows["orch"] + wide_h, right, rows["split"]))
    svg.append(link_elbow(left, rows["split"] + wide_h, leaves[0], rows["leaf"]))
    svg.append(link_elbow(left, rows["split"] + wide_h, leaves[1], rows["leaf"]))
    svg.append(link_elbow(right, rows["split"] + wide_h, leaves[2], rows["leaf"]))
    svg.append(link_elbow(right, rows["split"] + wide_h, leaves[3], rows["leaf"]))

    svg.append(node(CX, rows["user"], 168, node_h, "USER", delay=0.0))
    svg.append(node(CX, rows["client"], 330, node_h, "REACT  /  NEXT.JS",
                    delay=0.12))
    svg.append(node(CX, rows["api"], 330, node_h, "FASTAPI  /  DJANGO",
                    delay=0.24))
    svg.append(node(CX, rows["orch"], 470, wide_h, "AI ORCHESTRATION",
                    "LANGGRAPH  /  LANGCHAIN", accent=T.GREEN, delay=0.36))
    svg.append(node(left, rows["split"], 260, wide_h, "LLM AGENTS",
                    "PLANNING / TOOL CALLING / STATE", accent=T.GREEN_DARK,
                    delay=0.48))
    svg.append(node(right, rows["split"], 260, wide_h, "HYBRID RAG",
                    "SEMANTIC + KEYWORD + RERANK", accent=T.GREEN_DARK,
                    delay=0.48))

    leaf_labels = (("TOOLS / APIs", "EXTERNAL SERVICES"),
                   ("REDIS", "CACHE / QUEUE"),
                   ("VECTOR DB", "EMBEDDINGS / pgvector"),
                   ("POSTGRESQL", "RELATIONAL STATE"))
    for cx, (title, sub) in zip(leaves, leaf_labels):
        svg.append(node(cx, rows["leaf"], 206, node_h + 10, title, sub,
                        title_size=12.5, delay=0.6))

    y = rows["leaf"] + node_h + 44
    svg.append(band(y, 60, "CLOUD INFRASTRUCTURE",
                    ("AWS", "AZURE", "GCP", "DOCKER", "KUBERNETES", "CI/CD"),
                    accent=T.BORDER))
    svg.append(band(y + 74, 60, "OBSERVABILITY",
                    ("LOGGING", "TRACING", "EVALUATION", "GUARDRAILS",
                     "MONITORING"), accent=T.BORDER))
    # every leaf drops onto a shared bus that feeds the cloud band
    bus_y = rows["leaf"] + node_h + 10 + 22
    for cx in leaves:
        svg.append(f'<line x1="{cx:g}" y1="{rows["leaf"] + node_h + 10:g}" '
                   f'x2="{cx:g}" y2="{bus_y:g}" stroke="{T.BORDER}" stroke-width="1.2"/>')
    svg.append(f'<line x1="{leaves[0]:g}" y1="{bus_y:g}" x2="{leaves[-1]:g}" '
               f'y2="{bus_y:g}" stroke="{T.BORDER}" stroke-width="1.2"/>')
    svg.append(f'<line x1="{leaves[0]:g}" y1="{bus_y:g}" x2="{leaves[-1]:g}" '
               f'y2="{bus_y:g}" stroke="{T.GREEN}" stroke-width="1.2" '
               f'stroke-dasharray="6 16" class="flow"/>')
    svg.append(link_v(CX, bus_y, y))
    svg.append(link_v(CX, y + 60, y + 74))
    svg.append("</g>")
    svg.append(T.close_svg())
    return "".join(svg)


def main() -> None:
    T.write_svg(T.repo_path("assets", "architecture.svg"), build())


if __name__ == "__main__":
    main()
