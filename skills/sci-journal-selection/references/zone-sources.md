# Zone / metric sources

## Bundled offline data

- **CAS 2025:** [`../data/FQBJCR2025-UTF8.csv`](../data/FQBJCR2025-UTF8.csv)  
  - Columns include Journal, 年份, ISSN/EISSN, 大类, 大类分区, Top, 小类…  
  - Match by exact journal title (uppercase common) or ISSN.  
  - In deliverables cite: `FQBJCR2025-UTF8.csv (CAS 2025 升级版, bundled)`.

## Live / secondary sources (still required for XinRui & IF)

| Signal | Preferred source | Notes |
| --- | --- | --- |
| CAS | Bundled CSV + official 中科院分区表 | Separate column `2025中科院大类` |
| XinRui / 新锐 | LetPub journal card or official 新锐表 | Separate column `2026新锐`; else `新锐未核实` |
| JCR Q / JIF | Clarivate / MJL | Label secondary if not Clarivate login |
| LetPub IF / 周期 / 评分 | https://www.letpub.com.cn/ | Page-shown; not Clarivate official |
| Indexing | Master Journal List | SCIE / On Hold |

Conflict rule: Clarivate/MJL > publisher page > LetPub display > other aggregators > this CSV for IF (CSV is for **CAS zones**, not IF).
