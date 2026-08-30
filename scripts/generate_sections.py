"""
Content sections of the profile, rendered as terminal panels.

    assets/cmd-whoami.svg     command strip above the About text
    assets/modules.svg        AI SYSTEMS / BACKEND / PRODUCT / PLATFORM
    assets/projects.svg       FinAI / Tudu / Atharva as running processes
    assets/tech-stack.svg     the full stack, grouped
    assets/focus.svg          current focus areas
    assets/philosophy.svg     how the work is approached
    assets/connect.svg        closing panel

Every string a visitor reads lives in the DATA block below, so the profile is
edited here and regenerated, never hand-patched in SVG.

Run:  python scripts/generate_sections.py
"""

from __future__ import annotations

import os
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import theme as T  # noqa: E402

W = 1000
PAD = 24

# ==========================================================================
# DATA
# ==========================================================================
MODULES = (
    ("AI SYSTEMS", ("LLMs", "Agentic AI", "Hybrid RAG", "LangGraph",
                    "LangChain", "AI Evaluation")),
    ("BACKEND", ("Python", "FastAPI", "Django", "REST APIs", "PostgreSQL",
                 "System Design")),
    ("PRODUCT", ("React", "TypeScript", "Responsive UI", "API Integration",
                 "Product Engineering")),
    ("PLATFORM", ("AWS", "Azure", "Google Cloud", "Docker", "Kubernetes",
                  "CI/CD")),
)

PROJECTS = (
    dict(
        pid="001", name="FinAI", domain="Financial AI", status="ACTIVE",
        summary=("AI-powered financial intelligence platform that turns portfolio, "
                 "company, market and news data into actionable insights."),
        processes=(("portfolio_engine", "ONLINE"), ("fundamental_analysis", "ONLINE"),
                   ("technical_analysis", "ONLINE"), ("risk_model", "ONLINE"),
                   ("sentiment_engine", "ONLINE"), ("news_pipeline", "ONLINE"),
                   ("forecasting", "ONLINE")),
        capabilities=("Portfolio Intelligence", "Fundamental Analysis",
                      "Technical Analysis", "Risk Scoring", "AI Investment Insights",
                      "News Intelligence", "Sentiment Analysis", "Stock Forecasting",
                      "S&P 500 Benchmarking"),
        stack=("Python", "Django", "React", "PostgreSQL", "LLMs",
               "Financial APIs", "Docker", "Cloud"),
    ),
    dict(
        pid="002", name="Tudu", domain="Productivity AI", status="ACTIVE",
        summary=("AI productivity platform that reads natural-language tasks and "
                 "turns them into contextual, structured, actionable plans."),
        processes=(("nl_task_parser", "ONLINE"), ("date_extraction", "ONLINE"),
                   ("smart_scheduler", "ONLINE"), ("recommendation_engine", "ONLINE"),
                   ("context_planner", "ONLINE"), ("location_intel", "ONLINE"),
                   ("auth_service", "ONLINE")),
        capabilities=("Natural-Language Task Input", "Date Extraction",
                      "Smart Scheduling", "AI Recommendations",
                      "Context-Aware Planning", "Location Intelligence",
                      "Nearby Store Discovery", "Shared Tasks", "Authentication",
                      "Mobile-First Design"),
        stack=("AI Agents", "React", "Django", "PostgreSQL", "REST APIs",
               "Maps", "JWT", "Cloud"),
    ),
    dict(
        pid="003", name="Atharva", domain="AI + IoT / AgTech", status="BUILDING",
        summary=("AI and IoT agricultural intelligence ecosystem combining connected "
                 "devices, analytics, automation and digital market infrastructure."),
        processes=(("crop_intelligence", "BUILD"), ("soil_analysis", "BUILD"),
                   ("iot_monitor", "BUILD"), ("smart_irrigation", "BUILD"),
                   ("pest_detection", "BUILD"), ("weather_intel", "BUILD"),
                   ("marketplace", "BUILD")),
        capabilities=("Crop Intelligence", "Soil Analysis", "IoT Monitoring",
                      "Smart Irrigation", "Crop Health", "Pest Detection",
                      "Weather Intelligence", "Farmer Marketplace",
                      "AI Recommendations", "Agricultural Analytics"),
        stack=("Artificial Intelligence", "IoT", "Cloud", "Analytics",
               "Automation", "APIs"),
    ),
)

STACK = (
    ("AI / GENERATIVE AI", ("OpenAI", "LangChain", "LangGraph", "Hugging Face",
                            "Generative AI", "Agentic AI", "Hybrid RAG", "Embeddings",
                            "Vector Search", "Prompt Engineering", "Context Engineering",
                            "Tool Calling", "AI Evaluation", "Guardrails",
                            "Structured Outputs", "Function Calling")),
    ("LANGUAGES", ("Python", "JavaScript", "TypeScript", "SQL", "R", "Bash")),
    ("BACKEND", ("FastAPI", "Django", "Node.js", "REST APIs", "WebSockets", "JWT",
                 "OAuth 2.0", "Async APIs", "API Architecture", "Microservices")),
    ("FRONTEND", ("React", "Next.js", "HTML5", "CSS3", "Tailwind CSS",
                  "Responsive UI", "API Integration")),
    ("DATA STORES", ("PostgreSQL", "MySQL", "MongoDB", "Redis", "SQLite", "pgvector",
                     "Vector Databases", "Caching")),
    ("ML / DATA", ("Pandas", "NumPy", "scikit-learn", "TensorFlow", "PyTorch",
                   "OpenCV", "Time-Series Analysis", "Predictive Modeling",
                   "Statistical Analysis", "Feature Engineering")),
    ("CLOUD", ("AWS", "Microsoft Azure", "Google Cloud", "Cloud Run",
               "Azure App Service", "Cloud SQL", "Cloud-Native Architecture")),
    ("DEVOPS", ("Docker", "Kubernetes", "GitHub Actions", "Linux", "Git", "Nginx",
                "CI/CD", "Containers", "Production Deployment", "System Design")),
    ("SECURITY / OBS", ("Splunk", "OWASP", "Application Security", "AI Security",
                        "Authentication", "Authorization", "Monitoring", "Logging",
                        "Risk Scoring", "Data Validation")),
    ("ANALYTICS", ("Tableau", "Power BI", "Excel", "Plotly", "Data Visualization",
                   "Data Mining")),
    ("TOOLING", ("GitHub", "VS Code", "Postman", "Figma", "GitHub Copilot")),
)

FOCUS = (
    ("AI ENGINEERING", ("Production LLM Applications", "Context Engineering",
                        "Structured Generation", "Tool Calling", "AI Evaluation",
                        "Guardrails")),
    ("AGENTIC SYSTEMS", ("LangGraph", "Stateful Agents", "Multi-Step Workflows",
                         "Tool-Using Agents", "Human-in-the-Loop",
                         "Agent Monitoring")),
    ("RETRIEVAL", ("Hybrid RAG", "Semantic Search", "Keyword Search",
                   "Vector Retrieval", "Reranking", "Retrieval Evaluation")),
    ("AI SECURITY", ("Prompt Injection Defense", "Input Validation",
                     "Output Validation", "AI Monitoring", "Application Security",
                     "Trustworthy AI")),
    ("BACKEND / PLATFORM", ("API Architecture", "Distributed Systems",
                            "Authentication", "Authorization", "Database Design",
                            "Async Processing", "Containers", "Kubernetes",
                            "CI/CD", "Production Monitoring")),
)

PHILOSOPHY = (
    ("01", "SOLVE", "Understand the actual problem before choosing technology."),
    ("02", "DESIGN", "Treat AI as one part of a complete production system."),
    ("03", "MEASURE", "Measure quality, latency, reliability, security, impact."),
    ("04", "IMPROVE", "Feed production signal back into the system, continuously."),
)

QUOTE = ("AI becomes valuable when it moves beyond a model response and becomes "
         "part of a reliable product, workflow or decision system.")

CONNECT_DOMAINS = ("GENERATIVE AI", "AGENTIC SYSTEMS", "HYBRID RAG",
                   "FULL-STACK AI", "AI SAAS", "CLOUD ARCHITECTURE",
                   "INTELLIGENT AUTOMATION", "AI SECURITY")


# ==========================================================================
# SHARED PIECES
# ==========================================================================
def header(command: str, note: str = "", y: float = 34) -> str:
    """Terminal command line that opens a section, plus a hairline."""
    out = [T.prompt(PAD, y, command, size=15)]
    if note:
        out.append(T.text(W - PAD, y, note, size=10.5, cls="m", anchor="end",
                          letter_spacing=1.6))
    out.append(T.rule(PAD, y + 16, W - PAD * 2, opacity=0.7))
    return "".join(out)


def card(x: float, y: float, width: float, height: float, title: str, *,
         index: str = "", size: float = 13.5) -> str:
    """Panel with a title row and a hairline under it."""
    out = [T.panel(x, y, width, height, fill=T.PANEL, stroke=T.BORDER),
           f'<rect x="{x:g}" y="{y:g}" width="3" height="{height:g}" '
           f'fill="{T.GREEN_DARK}" opacity="0.85"/>',
           T.text(x + 16, y + 26, title, size=size, cls="g b", letter_spacing=1.5)]
    if index:
        out.append(T.text(x + width - 14, y + 26, index, size=11, cls="gd",
                          anchor="end", letter_spacing=1.2))
    out.append(T.rule(x + 16, y + 38, width - 30, opacity=0.6))
    return "".join(out)


def bullet_list(x: float, y: float, items, *, size: float = 12.5,
                step: float = 19.5, cls: str = "t") -> str:
    """Square-bulleted list; returns the SVG for all rows."""
    out = []
    for i, item in enumerate(items):
        iy = y + i * step
        out.append(f'<rect x="{x:g}" y="{iy - 6:g}" width="4" height="4" '
                   f'fill="{T.GREEN_DARK}"/>')
        out.append(T.text(x + 12, iy, item, size=size, cls=cls))
    return "".join(out)


# ==========================================================================
# SECTIONS
# ==========================================================================
def cmd_strip(command: str, note: str = "") -> str:
    height = 54
    svg = [T.open_svg(W, height, title=f"Terminal prompt: {command}")]
    svg.append(T.panel(0.5, 0.5, W - 1, height - 1, fill="none", stroke=T.BORDER,
                       rx=8))
    svg.append(f'<rect x="0.5" y="0.5" width="3" height="{height - 1:g}" '
               f'fill="{T.GREEN}" opacity="0.8"/>')
    svg.append(T.prompt(PAD, height / 2 + 5, command, size=15))
    if note:
        svg.append(T.text(W - PAD, height / 2 + 4, note, size=10.5, cls="m",
                          anchor="end", letter_spacing=1.6))
    svg.append(T.close_svg())
    return "".join(svg)


def modules_svg() -> str:
    cols, gap = 4, 18
    inner = W - PAD * 2
    card_w = (inner - gap * (cols - 1)) / cols
    rows_max = max(len(items) for _, items in MODULES)
    card_h = 52 + rows_max * 19.5 + 12
    height = card_h + 32

    svg = [T.open_svg(W, height,
                      title="Engineering areas: AI systems, backend, product, platform")]
    for i, (title, items) in enumerate(MODULES):
        x = PAD + i * (card_w + gap)
        svg.append(card(x, 16, card_w, card_h, title, index=f"0{i + 1}"))
        svg.append(bullet_list(x + 16, 16 + 58, items))
    svg.append(T.close_svg())
    return "".join(svg)


def projects_svg() -> str:
    card_h, gap, top = 292, 18, 66
    inner = W - PAD * 2
    height = top + len(PROJECTS) * card_h + (len(PROJECTS) - 1) * gap + PAD

    svg = [T.open_svg(W, height,
                      title="Project registry: FinAI, Tudu and Atharva shown as "
                            "running processes")]
    svg.append(header("ps --projects", "PROJECT REGISTRY"))

    for i, p in enumerate(PROJECTS):
        y = top + i * (card_h + gap)
        active = p["status"] == "ACTIVE"
        colour = T.GREEN if active else T.GREEN_2

        svg.append(T.panel(PAD, y, inner, card_h, fill=T.PANEL, stroke=T.BORDER))
        svg.append(f'<rect x="{PAD:g}" y="{y:g}" width="3" height="{card_h:g}" '
                   f'fill="{colour}" opacity="0.9"/>')

        name_size = 23
        svg.append(T.text(PAD + 22, y + 36, p["name"].upper(), size=name_size,
                          cls="t b", letter_spacing=2.4,
                          extra='filter="url(#glow-soft)"'))
        meta_x = PAD + 22 + T.w(p["name"], name_size) + len(p["name"]) * 2.4 + 24
        svg.append(T.text(meta_x, y + 36, f'PID: {p["pid"]}', size=11, cls="m",
                          letter_spacing=1.2))
        svg.append(T.text(meta_x + 86, y + 36, f'DOMAIN: {p["domain"].upper()}',
                          size=11, cls="gd", letter_spacing=1.2))

        pill, pw = T.status_pill(PAD + inner - 22 - (T.w(p["status"], 11) + 30),
                                 y + 22, p["status"], color=colour)
        svg.append(pill)
        svg.append(T.rule(PAD + 22, y + 50, inner - 44, opacity=0.6))

        # summary
        sy = y + 74
        for line in textwrap.wrap(p["summary"], 108):
            svg.append(T.text(PAD + 22, sy, line, size=12.5, cls="t2"))
            sy += 18

        # left column: processes with dotted leaders
        col_x, col_w = PAD + 22, 396
        py = y + 128
        svg.append(T.text(col_x, py - 16, "// MODULES", size=10, cls="m",
                          letter_spacing=1.6))
        for name, state in p["processes"]:
            svg.append(T.leader(col_x, py, name, state, col_w, size=12,
                                right_cls="g" if state == "ONLINE" else "g2"))
            py += 17

        # right column: capabilities
        cap_x = PAD + 22 + col_w + 34
        cap_w = inner - 44 - col_w - 34
        svg.append(T.text(cap_x, y + 112, "// CAPABILITIES", size=10, cls="m",
                          letter_spacing=1.6))
        chips, _ = T.chip_row(cap_x, y + 122, p["capabilities"], size=10.5,
                              height=20, gap=6, line_gap=6, max_width=cap_w)
        svg.append(chips)

        # footer: stack
        fy = y + card_h - 18
        svg.append(T.rule(PAD + 22, fy - 18, inner - 44, opacity=0.5))
        stack_line = "  /  ".join(p["stack"])
        svg.append(T.text(PAD + 22, fy, stack_line, size=11, cls="m",
                          letter_spacing=0.6))

    svg.append(T.close_svg())
    return "".join(svg)


def tech_stack_svg() -> str:
    """Category label on the left, chips flowing on the right - an `ls`
    listing rather than a wall of identical badges."""
    label_w, gap_y = 158, 16
    chip_x = PAD + label_w + 18
    chip_w = W - chip_x - PAD
    y = 78
    body = []
    for title, items in STACK:
        chips, used = T.chip_row(chip_x, y, items, size=11, height=21, gap=6,
                                 line_gap=6, max_width=chip_w)
        body.append(T.text(PAD + label_w, y + 14, title, size=11, cls="g2",
                           anchor="end", letter_spacing=1.4))
        body.append(f'<rect x="{PAD + label_w + 8:g}" y="{y:g}" width="2" '
                    f'height="{used:g}" fill="{T.BORDER}"/>')
        body.append(chips)
        y += used + gap_y

    height = y + 12
    svg = [T.open_svg(W, height, title="Technology stack grouped by discipline")]
    svg.append(header("ls ./stack", f"{sum(len(i) for _, i in STACK)} ENTRIES"))
    svg.append("".join(body))
    svg.append(T.close_svg())
    return "".join(svg)


def focus_svg() -> str:
    gap, top = 18, 70
    inner = W - PAD * 2
    small_w = (inner - gap * 2) / 3
    wide_w = small_w * 2 + gap
    row_h = 52 + 6 * 19.5 + 12

    svg = [T.open_svg(W, top + row_h * 2 + gap + PAD - 6,
                      title="Current focus: AI engineering, agentic systems, "
                            "retrieval, AI security, backend and platform")]
    svg.append(header("cat focus.log", "CURRENT FOCUS"))

    layout = ((0, top, small_w), (1, top, small_w), (2, top, small_w),
              (0, top + row_h + gap, small_w), (1, top + row_h + gap, wide_w))
    for (col, y, width), (title, items) in zip(layout, FOCUS):
        x = PAD + col * (small_w + gap)
        svg.append(card(x, y, width, row_h, title))
        columns = 2 if width > small_w else 1
        per = (len(items) + columns - 1) // columns
        for j, item in enumerate(items):
            cx = x + 16 + (j // per) * (width - 32) / columns
            iy = y + 58 + (j % per) * 19.5
            svg.append(f'<rect x="{cx:g}" y="{iy - 6:g}" width="4" height="4" '
                       f'fill="{T.GREEN_DARK}"/>')
            svg.append(T.text(cx + 12, iy, item, size=12.5, cls="t"))
    svg.append(T.close_svg())
    return "".join(svg)


def philosophy_svg() -> str:
    gap = 16
    inner = W - PAD * 2
    card_w = (inner - gap * 3) / 4
    card_h = 118
    quote_lines = textwrap.wrap(QUOTE, 92)
    height = 30 + card_h + 26 + len(quote_lines) * 22 + 34

    svg = [T.open_svg(W, height, title="Engineering philosophy: solve, design, "
                                       "measure, improve")]
    for i, (num, title, body) in enumerate(PHILOSOPHY):
        x = PAD + i * (card_w + gap)
        svg.append(T.panel(x, 22, card_w, card_h, fill=T.PANEL, stroke=T.BORDER))
        svg.append(T.text(x + 16, 52, num, size=21, cls="gd b", letter_spacing=1))
        svg.append(T.text(x + 58, 52, title, size=14, cls="g b", letter_spacing=1.8))
        svg.append(T.rule(x + 16, 64, card_w - 32, opacity=0.6))
        ty = 84
        for line in textwrap.wrap(body, 30):
            svg.append(T.text(x + 16, ty, line, size=11.5, cls="t2"))
            ty += 16

    qy = 22 + card_h + 26
    svg.append(T.panel(PAD, qy - 8, inner, len(quote_lines) * 22 + 26,
                       fill=T.BG_2, stroke=T.BORDER))
    svg.append(f'<rect x="{PAD:g}" y="{qy - 8:g}" width="3" '
               f'height="{len(quote_lines) * 22 + 26:g}" fill="{T.GREEN}" opacity="0.8"/>')
    ty = qy + 22
    for line in quote_lines:
        svg.append(T.text(PAD + 24, ty, line, size=13.5, cls="t"))
        ty += 22
    svg.append(T.close_svg())
    return "".join(svg)


def connect_svg() -> str:
    inner = W - PAD * 2
    chips, used = T.chip_row(PAD, 92, CONNECT_DOMAINS, size=11, height=26,
                             gap=8, line_gap=8, max_width=inner)
    height = 92 + used + 118

    svg = [T.open_svg(W, height, title="Connect: domains, and system status online")]
    svg.append(header("./connect", "NETWORK"))
    svg.append(T.text(PAD, 78, "// DOMAINS", size=10.5, cls="m", letter_spacing=1.8))
    svg.append(chips)

    y = 92 + used + 46
    svg.append(T.rule(PAD, y - 22, inner, opacity=0.6))
    svg.append(T.text(W / 2, y + 6, "BUILD SYSTEMS  /  SOLVE PROBLEMS  /  CREATE IMPACT",
                      size=15, cls="t b", anchor="middle", letter_spacing=2.4,
                      extra='filter="url(#glow-soft)"'))

    label = "SYSTEM STATUS: ONLINE"
    size = 12.5
    total = T.w(label, size) + len(label) * 1.6 + 16
    lx = W / 2 - total / 2
    svg.append(T.text(lx, y + 40, label, size=size, cls="g", letter_spacing=1.6))
    svg.append(f'<rect x="{lx + total - 12:g}" y="{y + 30:g}" width="7" height="12" '
               f'fill="{T.GREEN}" class="cursor"/>')
    svg.append(T.close_svg())
    return "".join(svg)


def main() -> None:
    out = T.repo_path("assets")
    T.write_svg(os.path.join(out, "cmd-whoami.svg"),
                cmd_strip("whoami", "IDENTITY"))
    T.write_svg(os.path.join(out, "modules.svg"), modules_svg())
    T.write_svg(os.path.join(out, "projects.svg"), projects_svg())
    T.write_svg(os.path.join(out, "tech-stack.svg"), tech_stack_svg())
    T.write_svg(os.path.join(out, "focus.svg"), focus_svg())
    T.write_svg(os.path.join(out, "philosophy.svg"), philosophy_svg())
    T.write_svg(os.path.join(out, "connect.svg"), connect_svg())


if __name__ == "__main__":
    main()
