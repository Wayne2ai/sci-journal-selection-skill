# SCI Journal Selection · Agent Skill

[中文说明](README.zh-CN.md)

Recommend **SCI/SCIE** target journals from a manuscript brief: verify **CAS** and **XinRui** zones, **LetPub** IF/reviews, and same-topic **precedents by year**. Defaults: **prefer XinRui** for ranking; **skip TypeSafe Jev** (no API key).

Compatible with [Agent Skills](https://agentskills.io/specification) on **Cursor**, **Codex**, and **Claude**.

## Do / Do not

| Do | Do not |
| --- | --- |
| Candidate pool + evidenced metrics/precedents | Predict acceptance or “good enough for X” |
| List CAS and XinRui in **separate** year-stamped columns | Invent IF, zones, reviews, or papers |
| Heuristic rank by default; optional Jev | Submit, create publisher accounts, or pay APC |
| Label sprint / solid / safe as **strategy** only | Treat Jev/IF/CAS as P(accept) |

## Defaults (ask once; silent → these)

1. **Zones: prefer XinRui** — rank by **2026 XinRui 大类** when it conflicts with CAS; still show **both** columns.
2. **Ranking: no API key / skip Jev** — heuristic unless the user opts in **and** `TYPESAFE_API_KEY` is set.

## How it runs (text)

1. Normalize brief (title, abstract, methods, contribution, constraints). Keep an English brief for finders / optional Jev.
2. Preference gate (above).
3. Build a 15–40 journal pool from ≥2 sources (Journal Finders, MJL, LetPub, OpenAlex, …). Offline CAS lookup uses the bundled CSV (see **Bundled data**).
4. Verify: SCIE, CAS, XinRui (else `新锐未核实`), JCR Q, LetPub page fields (secondary). Conflict: Clarivate/MJL > publisher > LetPub.
5. Precedents for final-table journals: same topic/type + **year**; last 3y > 4–7y > older/none. No hits → `近作先例：待核验` (never invent).
6. Rank: heuristic (scope → precedent recency → zone preference → metrics → risk) or optional Jev (`scope_fit` / `precedent_fit` / `zone_fit` …). Scores ≠ acceptance odds.
7. Deliver paste-ready table + **no-acceptance** line. No submission by this skill.

### Optional illustrations

Pixar-style sketches ([illustration-style-samples](https://github.com/preangelleo/illustration-style-samples)); decorative only.

| Language | File |
| --- | --- |
| English | [`skills/sci-journal-selection/assets/selection-pipeline-pixar.jpg`](skills/sci-journal-selection/assets/selection-pipeline-pixar.jpg) |
| 中文 | [`skills/sci-journal-selection/assets/selection-pipeline-pixar-zh.jpg`](skills/sci-journal-selection/assets/selection-pipeline-pixar-zh.jpg) |

![Pipeline sketch (EN)](skills/sci-journal-selection/assets/selection-pipeline-pixar.jpg)

## Bundled data

`skills/sci-journal-selection/data/FQBJCR2025-UTF8.csv` — CAS **2025** upgrade table (UTF-8).

| CAS 大类 zone | Count | Role |
| --- | ---: | --- |
| 1 | **1451** | Sprint pool |
| 2 | **2844** | Solid pool |
| 3 | **4583** | Safe / expand |
| **1–3 total** | **8878** | Default candidate coverage |
| 4 | 12894 | Lookup only |
| Full table | 21772 | Offline CAS match |

XinRui is **not** fully bundled — look up live or mark `新锐未核实`. See `skills/sci-journal-selection/data/README.md`.

## Install (Cursor / Codex / Claude)

```bash
SKILL_SRC="$(pwd)/skills/sci-journal-selection"
# Codex / Agent Skills
mkdir -p .agents/skills && ln -sfn "$SKILL_SRC" .agents/skills/sci-journal-selection
# Cursor
mkdir -p .cursor/skills && ln -sfn "$SKILL_SRC" .cursor/skills/sci-journal-selection
# Claude
mkdir -p .claude/skills && ln -sfn "$SKILL_SRC" .claude/skills/sci-journal-selection
# optional: ./install.sh --project .   or   ./install.sh --user
```

| Scope | Cursor | Codex | Claude |
| --- | --- | --- | --- |
| Project | `.cursor/skills/…` | `.agents/skills/…` | `.claude/skills/…` |
| User | `~/.cursor/skills/…` | `~/.agents/skills/…` | `~/.claude/skills/…` |

## Environment (optional)

Only if the user chooses **有apikey / use Jev**:

```bash
export TYPESAFE_API_KEY="your-key"   # placeholder — never commit a real key
```

Details: `skills/sci-journal-selection/references/typesafe-jev.md`. `.gitignore` ignores `.env`.

## Quick start

1. Install (symlink above).
2. Chat: `Use $sci-journal-selection` / “按选刊 skill 推荐期刊”.
3. Answer the two preference questions (or accept defaults).
4. Paste title + abstract.
5. Expect CAS / XinRui / LetPub / precedent years + the no-acceptance disclaimer.

```bash
python3 skills/sci-journal-selection/scripts/openalex_precedents.py \
  --issn 0888-3270 --query "bearing PHM" --years 3 --mailto you@example.com
```

## Layout

```
sci-journal-selection-skill/
├── README.md / README.zh-CN.md
├── LICENSE · install.sh · .env.example
├── examples/acm-phm-brief.md
└── skills/sci-journal-selection/
    ├── SKILL.md
    ├── data/FQBJCR2025-UTF8.csv
    ├── assets/selection-pipeline-pixar{,-zh}.jpg
    ├── references/ · scripts/ · agents/
```

## Spec & version

- Spec: https://agentskills.io/specification
- Skill version: **1.2.0** (`SKILL.md` metadata)

## Disclaimer

Academic reference only. Not a submission promise or acceptance forecast. Zones/IF follow official or clearly labeled secondary sources; LetPub is third-party page display. Authors must follow their unit’s rules.
