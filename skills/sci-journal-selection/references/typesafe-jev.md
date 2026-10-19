# TypeSafe Jev (optional)

Call Jev **only** when the user chose **有apikey / use Jev** and `TYPESAFE_API_KEY` is non-empty. Otherwise skip and use heuristic 4b.

## Product links

- Product: [TypeSafe AI](https://typesafe.ai) **Jev** (`jev-latest` / versioned ids)
- Docs: [Quick start](https://docs.typesafe.ai/introduction/quickstart), [API](https://docs.typesafe.ai/api), [Primitives](https://docs.typesafe.ai/primitives)
- Vendor skill (API patterns, not 选刊): https://github.com/typesafe-ai/skills

## Request shape

- `POST https://api.typesafe.ai/v1/systemone`
- Header: `Authorization: Bearer $TYPESAFE_API_KEY`
- Primitives: Choice / Score / Noul

Example (illustrative):

```json
{
  "model": "jev-latest",
  "state": {
    "manuscript_brief": "...",
    "journal": {
      "name": "...",
      "issn": "...",
      "cas": "2025中科院大类…",
      "xinrui": "2026新锐…",
      "letpub_if": "页示…",
      "precedents": [{"year": 2026, "title": "...", "why": "..."}]
    },
    "zone_policy": "prefer_xinrui"
  },
  "primitives": [
    {"id": "scope_fit", "type": "Score", "min": 0, "max": 3},
    {"id": "precedent_fit", "type": "Score", "min": 0, "max": 3},
    {"id": "zone_fit", "type": "Noul"},
    {"id": "indexing_ok", "type": "Noul"},
    {"id": "risk_flag", "type": "Noul"},
    {"id": "tier", "type": "Choice", "options": ["sprint", "solid", "safe", "skip"]}
  ]
}
```

Adapt field names to the current TypeSafe API docs if they differ. Report the model id used.

## Safety

- Never invent Jev scores.
- Never treat scores as P(accept).
- Do not write the API key into reports, commits, or examples.
