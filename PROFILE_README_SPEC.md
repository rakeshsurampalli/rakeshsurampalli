# Profile README — Implementation Spec

The specification this repository is built to. If a change contradicts something
here, change this file in the same commit.

---

## 1. Intent

A black terminal, Matrix green, and a developer profile that behaves like a running
system: boot sequence, identity load, project processes, architecture, stack, focus,
live activity stream. It must not read as the output of a README generator — no
capsule banners, no wave headers, no trophy strips, no rainbow shields, no emoji.

---

## 2. Colour system

| token | value | use |
| --- | --- | --- |
| background | `#020604` | page ground |
| secondary background | `#050B07` | raised ground, chips |
| panel | `#07110A` | cards |
| panel light | `#0A160D` | inner panels |
| matrix green | `#00FF41` | primary accent |
| bright green | `#39FF14` | print head, brightest ink only |
| secondary green | `#00C832` | secondary accent |
| dark green | `#008F2F` | tertiary accent, bullets |
| border green | `#0B5F27` | all 1px borders |
| muted green | `#548C61` | labels, dotted leaders |
| primary text | `#D7FFE0` | body |
| secondary text | `#8BB596` | supporting body |

Heatmap levels 0–4: `#07110A`, `#0A3D18`, `#008F2F`, `#00C832`, `#00FF41`.

No blue, purple, pink, orange or brand colours anywhere, including technology labels.
Glow is `filter: drop-shadow`/`feGaussianBlur` used sparingly — headline text, the
print head, and the densest heatmap cells only.

## 3. Typography

`"JetBrains Mono", "Fira Code", "IBM Plex Mono", "DejaVu Sans Mono", "Courier New", monospace`.

No font files are bundled and no webfont is fetched — GitHub renders these SVGs inside
`<img>`, where external resources do not load. Monospace advance is assumed to be
`0.6em` and pinned with `textLength` + `lengthAdjust="spacing"` so columns align in
whichever face the viewer actually has.

---

## 4. Structure

```
README.md                     composes generated assets only
PROFILE_README_SPEC.md        this file
requirements.txt              Pillow, numpy, requests
assets/                       generated SVGs + profile-photo.jpg + contributions.json
scripts/                      generators (the only place content is edited)
.github/workflows/            daily activity refresh
```

README order: hero → navigation → about → projects → architecture → stack → focus →
philosophy → activity → connect → build notes.

Section anchors come from markdown headings (`## PROJECTS` → `#projects`), so the
custom SVG navigation buttons keep working without any raw-HTML `id` attributes.

---

## 5. Asset rules

- **SVG only.** No JavaScript, no iframes, no canvas, no external images, no
  third-party stat cards or badge services.
- **Animation is additive.** Every element's static state is its final state.
  Transient elements (the `PRINTING n%` readout, the scan line, the flow dashes)
  carry `opacity="0"` statically and are only made visible by animation. If CSS
  animation and SMIL both fail, the page still reads correctly.
- `@media (prefers-reduced-motion: reduce)` disables all animation.
- Total intro motion settles in roughly 3 seconds; only the cursor, the status dot
  and the architecture flow dashes loop.
- Assets are ≤ 1000 units wide with `width="100%"` and a `viewBox`, so they scale to
  the README column on any screen.
- Every asset carries `role="img"`, `<title>` and an `aria-label`; status is always
  spelled out in words (`ONLINE`, `ACTIVE`, `BUILDING`) and never by colour alone.
- Budget: no asset over 500 KB. Portraits emit one `<text>` per colour tier per row,
  not one per character.

---

## 6. Portrait

Source: `assets/profile-photo.jpg` — the only personal image input.

```
crop → backdrop flood-removal → local contrast → subject-only stretch →
brightness mapping (inverted) → density ramp → SVG rows → line-printer reveal
```

Tuning constants sit at the top of `scripts/make_ascii_portrait.py`. The backdrop is
flooded away only from *light* border pixels, so a dark suit is never mistaken for
background. Reveal is a SMIL clip that steps down one row at a time behind a bright
print head; without SMIL the portrait is simply complete from the first frame.

If the photograph is absent, both the portrait and the hero render a labelled
placeholder that names the missing file. A face is never fabricated.

---

## 7. Activity

Real data only. `scripts/fetch_contributions.py` reads the public contribution
calendar — GraphQL when `GITHUB_TOKEN` is present, otherwise the public
`github.com/users/<login>/contributions` fragment — and caches it to
`assets/contributions.json`. The heatmap renders from that cache.

- A failed fetch prints a warning, leaves the cache and the SVG untouched, and exits 0.
- With no cache at all, the panel says `AWAITING SYNC`; it never draws invented cells.
- Every figure shown (total, active days, current streak, longest streak, busiest day)
  is computed from the fetched calendar. No metric is estimated, rounded up or invented.

The workflow commits only when `git diff` shows the generated assets actually changed.

---

## 8. Claims

No invented years of experience, revenue, users, latency, accuracy, stars, downloads
or company metrics. Technologies appear under stack categories that reflect genuine
engineering background; nothing is presented as professional expertise beyond that.

---

## 9. Acceptance

- [x] black + Matrix-green throughout, no blue theme, no emoji, no wave banner
- [x] custom hero with boot sequence and ASCII portrait printing animation
- [x] FinAI, Tudu and Atharva as process modules
- [x] AI architecture diagram in Matrix green
- [x] comprehensive, visually organised technology stack
- [x] current focus and engineering philosophy
- [x] custom activity stream built from real GitHub data, refreshed by Actions
- [x] workflow avoids empty commits
- [x] works with no JavaScript; readable when animation is disabled
- [x] mobile-friendly scaling; no fake metrics; no broken widgets
- [x] regenerating from `scripts/` reproduces every asset
