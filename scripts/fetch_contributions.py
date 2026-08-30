"""
Fetch the public contribution calendar for a GitHub user.

Two sources, in order:
  1. the GraphQL API, when GITHUB_TOKEN is set (as it is inside Actions)
  2. the public contributions fragment at github.com/users/<login>/contributions

Only public data is read; no private repository access is required.

The result is cached in assets/contributions.json so the heatmap can be
regenerated offline. On any network or parse failure the cache and the
existing SVG are left exactly as they are - a bad fetch must never blank the
README - and the script still exits 0 so scheduled runs stay green.

Run:  python scripts/fetch_contributions.py
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import generate_heatmap  # noqa: E402
import theme as T  # noqa: E402

LOGIN = os.environ.get("PROFILE_LOGIN", "rakeshsurampalli")
CACHE = T.repo_path("assets", "contributions.json")

GRAPHQL = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount contributionLevel } }
      }
    }
  }
}
"""

LEVELS = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2,
          "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}

UA = {"User-Agent": f"{LOGIN}-profile-readme (github actions)"}


def from_graphql(token: str) -> list[dict]:
    import requests

    r = requests.post("https://api.github.com/graphql",
                      json={"query": GRAPHQL, "variables": {"login": LOGIN}},
                      headers={"Authorization": f"bearer {token}", **UA},
                      timeout=30)
    r.raise_for_status()
    payload = r.json()
    if "errors" in payload:
        raise RuntimeError(payload["errors"])
    calendar = (payload["data"]["user"]["contributionsCollection"]
                       ["contributionCalendar"])
    days = []
    for week in calendar["weeks"]:
        for day in week["contributionDays"]:
            days.append({"date": day["date"],
                         "count": day["contributionCount"],
                         "level": LEVELS.get(day["contributionLevel"], 0)})
    return days


DAY_TAG = re.compile(r"<td[^>]*ContributionCalendar-day[^>]*>")
ATTR = re.compile(r'([a-z-]+)="([^"]*)"')
TOOLTIP = re.compile(r'<tool-tip[^>]*for="([^"]+)"[^>]*>([^<]*)</tool-tip>')
COUNT = re.compile(r"^(\d+|No)\s+contributions?")


def from_html() -> list[dict]:
    """Parse the public calendar fragment: one <td> per day, with the exact
    count carried by the matching <tool-tip>."""
    import requests

    r = requests.get(f"https://github.com/users/{LOGIN}/contributions",
                     headers=UA, timeout=30)
    r.raise_for_status()
    html = r.text

    counts = {}
    for target, label in TOOLTIP.findall(html):
        m = COUNT.match(label.strip())
        if m:
            counts[target] = 0 if m.group(1) == "No" else int(m.group(1))

    days = []
    for tag in DAY_TAG.findall(html):
        attrs = dict(ATTR.findall(tag))
        date = attrs.get("data-date")
        if not date:
            continue
        days.append({"date": date,
                     "count": counts.get(attrs.get("id", ""), 0),
                     "level": int(attrs.get("data-level", 0))})
    if len(days) < 300:
        raise RuntimeError(f"only {len(days)} days parsed - layout changed?")
    return days


def fetch() -> list[dict]:
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        try:
            return from_graphql(token)
        except Exception as exc:                       # noqa: BLE001
            print(f"  graphql fetch failed ({exc}); falling back to public page")
    return from_html()


def main() -> int:
    try:
        days = sorted(fetch(), key=lambda d: d["date"])
    except Exception as exc:                           # noqa: BLE001
        print(f"  contribution fetch failed: {exc}")
        print("  keeping the existing contribution-stream.svg unchanged")
        return 0

    data = {
        "login": LOGIN,
        "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "total": sum(d["count"] for d in days),
        "days": days,
    }
    with open(CACHE, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, indent=1)
        fh.write("\n")
    print(f"  assets/contributions.json               "
          f"{len(days)} days, {data['total']} contributions")

    generate_heatmap.main()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
