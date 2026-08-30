<!--
  RAKESH SURAMPALLI - GITHUB PROFILE
  Every image below is generated from the scripts in ./scripts.
  Edit the data at the top of those scripts, then run:
      python scripts/generate_profile_assets.py
  Do not hand-edit the SVGs in ./assets - they are build output.

  Two GitHub rendering rules shape the markup below:
  1. an image that is not already inside a link gets auto-wrapped in a link to
     its raw blob, opened in a new tab - so every image here carries its own
     same-page anchor instead;
  2. target="_blank" is stripped from author-supplied anchors, so external
     links open in the same tab (ctrl/cmd+click still opens a new one).
-->

<div align="center">

<a href="#about"><img src="assets/hero-terminal.svg" width="100%" alt="Rakesh Surampalli - Full-Stack AI Engineer and AI Product Builder. Terminal boot screen with ASCII portrait. System status: online."></a>

<br><br>

<a href="#about"><img src="assets/nav-about.svg" height="30" alt="About"></a>
<a href="#projects"><img src="assets/nav-projects.svg" height="30" alt="Projects"></a>
<a href="#architecture"><img src="assets/nav-architecture.svg" height="30" alt="Architecture"></a>
<a href="#stack"><img src="assets/nav-stack.svg" height="30" alt="Stack"></a>
<a href="#focus"><img src="assets/nav-focus.svg" height="30" alt="Focus"></a>
<a href="#activity"><img src="assets/nav-activity.svg" height="30" alt="Activity"></a>
<a href="#connect"><img src="assets/nav-connect.svg" height="30" alt="Connect"></a>

<br><br>

<a href="https://www.linkedin.com/in/rakeshsurampalli27/"><img src="assets/btn-linkedin.svg" height="40" alt="LinkedIn"></a>
<a href="https://rakeshsurampalli.github.io/Rakesh_portfolio/"><img src="assets/btn-portfolio.svg" height="40" alt="Portfolio"></a>
<a href="https://medium.com/@rakeshsurampalli"><img src="assets/btn-medium.svg" height="40" alt="Medium"></a>
<a href="mailto:rakeshsurampalli@gmail.com"><img src="assets/btn-email.svg" height="40" alt="Email"></a>

</div>

<br>

## ABOUT

<a href="#about"><img src="assets/cmd-whoami.svg" width="100%" alt="rakesh@github:~$ whoami"></a>

Full-Stack AI Engineer focused on building production-grade AI applications across
generative AI, agentic systems, retrieval, backend engineering, modern web platforms
and cloud infrastructure.

I work across the complete engineering lifecycle — translating ambiguous problems into
architecture, AI workflows, APIs, product experiences and production cloud systems.

My focus is not simply connecting software to an LLM.

I build systems where AI becomes part of a reliable product, workflow or decision process.

<a href="#about"><img src="assets/modules.svg" width="100%" alt="Engineering areas: AI systems, backend, product, platform."></a>

<br>

## PROJECTS

<a href="#projects"><img src="assets/projects.svg" width="100%" alt="Project registry. 001 FinAI, financial AI, active. 002 Tudu, productivity AI, active. 003 Atharva, AI and IoT agriculture, building."></a>

<br>

## ARCHITECTURE

<a href="#architecture"><img src="assets/architecture.svg" width="100%" alt="Reference AI system architecture: user, React or Next.js client, FastAPI or Django API, LangGraph and LangChain orchestration, LLM agents and hybrid RAG, tools, Redis, vector database and PostgreSQL, cloud infrastructure, observability."></a>

<br>

## STACK

<a href="#stack"><img src="assets/tech-stack.svg" width="100%" alt="Technology stack grouped by discipline: AI and generative AI, languages, backend, frontend, data stores, ML and data, cloud, DevOps, security and observability, analytics, tooling."></a>

<br>

## FOCUS

<a href="#focus"><img src="assets/focus.svg" width="100%" alt="Current focus: AI engineering, agentic systems, retrieval, AI security, backend and platform."></a>

<a href="#focus"><img src="assets/philosophy.svg" width="100%" alt="Engineering philosophy: 01 solve, 02 design, 03 measure, 04 improve. AI becomes valuable when it moves beyond a model response and becomes part of a reliable product, workflow or decision system."></a>

<br>

## ACTIVITY

<a href="#activity"><img src="assets/contribution-stream.svg" width="100%" alt="GitHub contribution stream: a Matrix-green heatmap of the last 365 days of public contributions, refreshed daily by GitHub Actions."></a>

<br>

## CONNECT

<a href="#connect"><img src="assets/connect.svg" width="100%" alt="Domains: generative AI, agentic systems, hybrid RAG, full-stack AI, AI SaaS, cloud architecture, intelligent automation, AI security. Build systems, solve problems, create impact. System status: online."></a>

<div align="center">

<a href="https://www.linkedin.com/in/rakeshsurampalli27/"><img src="assets/btn-linkedin.svg" height="40" alt="LinkedIn"></a>
<a href="https://rakeshsurampalli.github.io/Rakesh_portfolio/"><img src="assets/btn-portfolio.svg" height="40" alt="Portfolio"></a>
<a href="https://medium.com/@rakeshsurampalli"><img src="assets/btn-medium.svg" height="40" alt="Medium"></a>
<a href="mailto:rakeshsurampalli@gmail.com"><img src="assets/btn-email.svg" height="40" alt="Email"></a>

</div>

<br>

<details>
<summary><sub><b>BUILD / REGENERATE THIS PROFILE</b></sub></summary>

<br>

Everything visible above is a generated SVG. Content lives in the scripts, not in the
markup — edit the data block at the top of a generator and rebuild.

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS / Linux

pip install -r requirements.txt

python scripts/generate_profile_assets.py   # all static assets, offline
python scripts/fetch_contributions.py       # activity stream (needs network)
```

| path | what it builds |
| --- | --- |
| `scripts/theme.py` | palette, typography and the shared SVG primitives |
| `scripts/make_ascii_portrait.py` | `assets/ascii-portrait.svg` from `assets/profile-photo.jpg` |
| `scripts/generate_hero.py` | `assets/hero-terminal.svg` |
| `scripts/generate_sections.py` | about / projects / stack / focus / philosophy / connect |
| `scripts/generate_architecture.py` | `assets/architecture.svg` |
| `scripts/generate_buttons.py` | navigation and social buttons |
| `scripts/fetch_contributions.py` | `assets/contributions.json` from public GitHub data |
| `scripts/generate_heatmap.py` | `assets/contribution-stream.svg` from that cache |

**Replacing the portrait.** Drop a new photograph at `assets/profile-photo.jpg` and run
`python scripts/make_ascii_portrait.py && python scripts/generate_hero.py`. Framing and
tone are controlled by the constants at the top of `make_ascii_portrait.py`
(`CROP`, `ASCII_WIDTH`, `CONTRAST`, `GAMMA`, `FLOOR`, `FADE_BOTTOM`). With no photograph
present, both assets render a labelled placeholder instead.

**Activity.** `.github/workflows/update-profile.yml` runs daily at 05:17 UTC, re-fetches
the public contribution calendar and commits only when the generated SVG actually
changed. A failed fetch leaves the previous asset in place rather than blanking it.

</details>

<div align="center">
<sub>generated with python · no javascript · no third-party stat cards</sub>
</div>
