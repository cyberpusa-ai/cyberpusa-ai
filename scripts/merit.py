"""Render the merit ledger (功德簿) card from public GitHub data."""
import json, os, urllib.parse, urllib.request
from datetime import datetime, timezone

USER = "cyberpusa-ai"
TOKEN = os.environ.get("GITHUB_TOKEN", "")


def api(path):
    req = urllib.request.Request("https://api.github.com" + path, headers={"Accept": "application/vnd.github+json"})
    if TOKEN:
        req.add_header("Authorization", "Bearer " + TOKEN)
    return json.load(urllib.request.urlopen(req))


def count(q, kind="issues"):
    return api(f"/search/{kind}?per_page=1&q=" + urllib.parse.quote(q))["total_count"]


repos = [r for r in api(f"/users/{USER}/repos?per_page=100") if r["name"] != USER]
rows = [
    ("渡化 Repos adopted", sum(r["fork"] for r in repos)),
    ("功德 PRs merged", count(f"author:{USER} type:pr is:merged")),
    ("随喜 Issues opened", count(f"author:{USER} type:issue")),
    ("经文 Commits", count(f"author:{USER}", "commits")),
    ("香火 Stars received", sum(r["stargazers_count"] for r in repos)),
]

W, H = 495, 60 + 34 * len(rows)
lines = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
    '<style>.t{font:600 18px Georgia,serif;fill:#f3ead8}.l{font:14px -apple-system,Segoe UI,sans-serif;fill:#b9b4aa}'
    '.v{font:600 16px ui-monospace,Menlo,monospace;fill:#e8c98a}.f{font:11px ui-monospace,Menlo,monospace;fill:#6f6a62}</style>',
    f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="10" fill="#131316" stroke="#3a352c"/>',
    '<circle cx="32" cy="30" r="9" fill="none" stroke="#e8c98a" stroke-width="1.5"/>',
    '<text x="50" y="36" class="t">Merit Ledger · 功德簿</text>',
]
for i, (label, value) in enumerate(rows):
    y = 76 + 34 * i
    lines.append(f'<text x="28" y="{y}" class="l">{label}</text>')
    lines.append(f'<text x="{W-28}" y="{y}" class="v" text-anchor="end">{value:,}</text>')
stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
lines.append(f'<text x="{W-28}" y="36" class="f" text-anchor="end">updated {stamp}</text></svg>')
open("assets/merit.svg", "w").write("\n".join(lines))
