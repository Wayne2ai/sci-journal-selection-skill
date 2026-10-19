#!/usr/bin/env python3
"""Fetch recent OpenAlex works for a journal ISSN + topic query.

Optional helper for sci-journal-selection. Stdlib only (urllib).
Not required to run the skill.

Example:
  python3 openalex_precedents.py --issn 0888-3270 --query "bearing PHM residual" --years 3
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone


OPENALEX = "https://api.openalex.org/works"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--issn", required=True, help="Journal ISSN (with or without hyphen)")
    p.add_argument("--query", required=True, help="Topic / method keywords")
    p.add_argument("--mailto", default="", help="Polite pool email for OpenAlex")
    p.add_argument("--years", type=int, default=3, help="Look back N years (default 3)")
    p.add_argument("--per-page", type=int, default=10, help="Max results (default 10)")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    issn = args.issn.strip().replace(" ", "")
    now = datetime.now(timezone.utc).year
    from_year = now - max(1, args.years) + 1

    filt = f"primary_location.source.issn:{issn},from_publication_date:{from_year}-01-01"
    params = {
        "filter": filt,
        "search": args.query,
        "sort": "publication_date:desc",
        "per_page": str(max(1, min(args.per_page, 50))),
    }
    if args.mailto:
        params["mailto"] = args.mailto

    url = OPENALEX + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "sci-journal-selection/1.1 (OpenAlex helper)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:  # noqa: BLE001 — surface to agent/user
        print(json.dumps({"error": str(exc), "url": url}, ensure_ascii=False), file=sys.stderr)
        return 1

    out = []
    for w in payload.get("results") or []:
        year = w.get("publication_year")
        title = (w.get("display_name") or "").strip()
        doi = None
        ids = w.get("ids") or {}
        if ids.get("doi"):
            doi = ids["doi"]
        elif w.get("doi"):
            doi = w["doi"]
        out.append(
            {
                "year": year,
                "title": title,
                "doi": doi,
                "id": w.get("id"),
            }
        )

    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
