---
name: sci-journal-selection
description: >-
  Recommend SCI/SCIE target journals from a manuscript brief. Verify CAS and
  XinRui zones, LetPub IF/reviews, and same-topic precedents by year; rank with
  TypeSafe Jev only when user opts in and TYPESAFE_API_KEY is set, else heuristic.
  Use when the user asks for 选刊, journal selection, CAS/XinRui zones, or LetPub.
license: MIT
compatibility: Cursor Agent Skills, Codex (.agents/skills), Claude Code/Claude.ai Skills; network access for OpenAlex/LetPub/publisher pages; optional TYPESAFE_API_KEY
metadata:
  version: "1.2.0"
  author: SCI选刊
  defaults: "xinrui=prefer; jev=off"
---

# SCI journal selection

Recommend target journals for a research manuscript. Verify sourced metrics, cite recent same-topic precedents by year, and rank with an explicit preference gate.

**Defaults (if the user is silent):** prefer **2026新锐** for zone ranking; **skip TypeSafe Jev** (heuristic 4b).

## Academic boundary (non-negotiable)

- Provide candidates, sourced metrics, scope/precedent **evidence**, and uncertainty—not a verdict on manuscript quality or **acceptance probability**.
- Do not say a paper is “good enough” for a journal, do not forecast desk-reject/accept rates, and do not treat Jev scores, IF, or CAS/XinRui as acceptance odds.
- Final submission choice stays with the author (and supervisor / unit rules). This skill does not submit, create publisher accounts, or pay APC unless separately and explicitly asked.
- Never fabricate IF, CiteScore, CAS, XinRui, JCR quartile, LetPub ratings, or precedent papers. Unverified → **未核实** / **待核验**.

## Preference gate (ask once per session)

Before building the shortlist, ask (widgets, numbered choices, or plain text). If the user already stated both, skip the ask.

**1. 分区口径怎么认？**

| Choice | Meaning |
| --- | --- |
| **认新锐** (default) | When ranking `zone_fit`, prefer **2026新锐大类** over CAS alone if they conflict; still show **both** columns |
| 不认新锐 | Rank primarily by CAS (e.g. 2025中科院大类); still show XinRui when available |

If silent → **认新锐**.

**2. 是否调用 TypeSafe Jev（需要 API Key）？**

| Choice | Meaning |
| --- | --- |
| **无apikey / skip Jev** (default) | Do **not** call Jev; use Step **4b** heuristic |
| 有apikey / use Jev | Call Jev only if `TYPESAFE_API_KEY` is non-empty; else fall back to 4b and say why |

If silent → **无apikey / skip Jev**.

### Key gate for Jev

1. User chose **有apikey** **and** `TYPESAFE_API_KEY` is set → Step 4; report model id.
2. Otherwise → skip Step 4; say `Jev skipped (no key / user opted out)`; use Step 4b.
3. Do not solicit or invent an API key. See [references/typesafe-jev.md](references/typesafe-jev.md) for API details.

## Inputs

- Title + abstract (required); keywords optional
- Methods / study type; contribution one-liner
- Target: CAS 大类 and/or JCR Q; SCIE; OA/APC; other unit rules

## Terminology

| Term | Meaning |
| --- | --- |
| **CAS** | 中科院《期刊分区表》升级版（大类/小类 + **year**）. Prefer e.g. `2025中科院大类`. |
| **XinRui / 新锐** | 《新锐期刊分区表》（e.g. **2026新锐**）. **Not** the same as CAS; always a separate column. |
| **JCR Quartile** | Clarivate JIF Quartile in a **named category** (+ year). |
| **LetPub** | letpub.com.cn journal card: IF display, review-speed, author ratings—label as LetPub secondary, not Clarivate official. |
| **Precedent evidence** | Recent papers in that journal on a **similar topic/type**, with **publication year**. |

Zone source notes: [references/zone-sources.md](references/zone-sources.md).

## Steps

### 1. Normalize the manuscript brief

Compact: title, abstract, methods, contribution, target_zones, constraints, and the two preference answers. Keep an English brief for finders/Jev.

### 2. Build a candidate pool

Gather 15–40 from ≥2 sources when possible:

- Elsevier / Springer Nature / Wiley / T&F Journal Finders
- Clarivate MJL / Manuscript Matcher — https://mjl.clarivate.com/
- LetPub AI selector — https://www.letpub.com.cn/index.php?page=aitools_journal_selector
- OpenAlex (or similar) works → journal aggregation
- JANE when bio/med

Record name, ISSN, publisher, short scope snip. Optional helper: `scripts/openalex_precedents.py`.

### 3. Verify metrics + LetPub + XinRui

For each shortlisted journal, collect and **date-stamp** sources:

1. **Indexing**: SCIE/SSCI/…; On Hold / removed — Master Journal List when possible
2. **CAS**: 大类 + 小类 + year (e.g. 2025) Prefer bundled [data/FQBJCR2025-UTF8.csv](data/FQBJCR2025-UTF8.csv); cite path + year.
3. **XinRui**: 大类/小类 + year (e.g. 2026新锐); if missing → `新锐未核实`
4. **JCR**: JIF + Quartile + category + year
5. **LetPub** journal page (search by title/ISSN):
   - IF as shown + as-of date
   - 审稿周期 / 录用比等 **页面明示**字段（作者反馈 → 标注“作者反馈，非官方”）
   - Scores if shown; copy and cite
   - 近期作者评价：摘 1–3 条可核对要点；勿编造
6. CiteScore / OA / APC when useful
7. Risk: 预警名单, mega-journal, predatory signals, special-issue-only, WoS 异常
8. Official aims & scope + article types (publisher URL)

Conflict rule: Clarivate/MJL > publisher page > LetPub display > other aggregators; always show what you used.

### 3b. Precedent evidence (required for top candidates)

For every journal that may enter the **final table** (typically top 8–12):

- Prefer **object + problem** matches, then method-class matches
- Record: **year**, short title, why similar (1 line), URL/DOI
- Aim for **2–3** precedents; if none → `近作先例：待核验` (do not invent)
- **Recency weighting:** last **3 years** strong; **4–7** moderate; older/none weak → down-rank unless scope is excellent
- Sources: OpenAlex, Scholar, publisher recent articles, WoS if available—cite which

### 4. Rank with TypeSafe Jev (only if opted in + key)

Per candidate, `model: "jev-latest"`. Put brief + journal card (CAS/XinRui/LetPub + **precedent years**) into `state`.

| id | type | purpose |
| --- | --- | --- |
| `scope_fit` | Score | 0–3 topical/method fit |
| `precedent_fit` | Score | 0–3 recent same-type support (0=none/old-only; 3=multiple last-3y close matches) |
| `zone_fit` | Noul | Meets user’s zone target under **preference gate** (认新锐 → XinRui大类 primary) |
| `indexing_ok` | Noul | Indexing OK |
| `risk_flag` | Noul | Material risk (high = bad) |
| `tier` | Choice | `sprint` / `solid` / `safe` / `skip` |

Aggregate: high `scope_fit` + `precedent_fit` + `zone_fit`; penalize `risk_flag`. **Never interpret as P(accept).** Full API notes: [references/typesafe-jev.md](references/typesafe-jev.md).

### 4b. Heuristic rank (Jev skipped — default)

Same shortlist **without** Jev columns. Rank by:

1. Scope (aims vs manuscript)
2. **Precedent recency** (last-3y same-type > older > none)
3. Zone vs user target under preference gate (**认新锐** → prefer XinRui大类; still show CAS)
4. LetPub/JCR metrics only after evidence; SCIE + risk filters
5. Bands: 冲刺 / 稳妥 / 保底 — **strategy bands only**, not quality/acceptance claims
6. Label mode: `heuristic (Jev skipped)`

### 5. Deliverable

Lead with one-sentence pick + ranking mode (`Jev` or `heuristic`) + preference summary (`认新锐` / `不认新锐`).

Add: **本报告不预测录用；分区/IF/Jev 仅作匹配与策略参考。**

Table columns and evidence block: [references/deliverable-template.md](references/deliverable-template.md). Blank skeleton: [assets/recommendation-table.md](assets/recommendation-table.md).

### 6. Hard rules

- No fabricated metrics, reviews, or precedents
- CAS vs XinRui vs JCR always separate + year
- Default skip Jev unless user opted in **and** key is set
- No acceptance prediction; no submission unless separately asked

## Maintenance

On annual CAS / XinRui / JCR releases, refresh zone column years and [references/zone-sources.md](references/zone-sources.md). Prefer `jev-latest` unless pinning a version.
