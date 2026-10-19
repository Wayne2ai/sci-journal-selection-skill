# SCI 选刊 · Agent Skill

[English](README.md)

从稿件摘要推荐 **SCI/SCIE** 目标期刊：核验 **中科院(CAS)** 与 **新锐(XinRui)**、**LetPub** IF/评价，并按**近作年份**收集同主题先例。默认：**认新锐**排序；**无 API Key / 跳过 TypeSafe Jev**。

遵循 [Agent Skills](https://agentskills.io/specification)，可装到 **Cursor**、**Codex**、**Claude**。

## 做什么 / 不做什么

| 做 | 不做 |
| --- | --- |
| 候选池 + 有来源的指标与近作证据 | **不预测录用** / 不评判“够不够发” |
| CAS 与新锐**分列**并标注年份 | 不伪造 IF、分区、评论、先例 |
| 默认启发式；可选 Jev | 不代投、不开账号、不付 APC |
| 冲刺/稳妥/保底 = **策略分档** | 不把 Jev/IF/分区当成录用概率 |

## 默认偏好（问一次；沉默则用此）

1. **分区：认新锐** — 排序优先 **2026新锐大类**（与 CAS 冲突时提示）；表中仍同时列出两者。
2. **排序：无apikey / 跳过 Jev** — 走启发式；仅当用户选 **有apikey** 且已设置 `TYPESAFE_API_KEY` 才调用 Jev。

## 选刊怎么做（文字）

1. **整理 brief**：题名、摘要、方法、贡献、约束；保留英文 brief。
2. **偏好闸门**：见上。
3. **候选池 15–40 刊**：≥2 个来源（Journal Finder、MJL、LetPub、OpenAlex…）。离线 CAS 用包内 CSV（见 **附带数据**）。
4. **核验**：SCIE、中科院、新锐（缺则 `新锐未核实`）、JCR Q、LetPub 页示字段。冲突：Clarivate/MJL > 出版社 > LetPub。
5. **近作先例**（进终表必做）：同主题/类型 + **年份**；近3年 > 4–7年 > 更早/无。无则 `近作先例：待核验`，禁止编造。
6. **排序**：启发式（scope → 近作新旧 → zone 偏好 → 指标 → 风险）或可选 Jev。**分数 ≠ 录用概率**。
7. **交付**：可粘贴表 + **不预测录用**声明。本 skill 不投稿。

### 配图（可选）

风格参考 [illustration-style-samples · Pixar Style](https://github.com/preangelleo/illustration-style-samples)，仅示意。

| 语言 | 文件 |
| --- | --- |
| 中文 | [`skills/sci-journal-selection/assets/selection-pipeline-pixar-zh.jpg`](skills/sci-journal-selection/assets/selection-pipeline-pixar-zh.jpg) |
| English | [`skills/sci-journal-selection/assets/selection-pipeline-pixar.jpg`](skills/sci-journal-selection/assets/selection-pipeline-pixar.jpg) |

![SCI选刊流程示意（中文）](skills/sci-journal-selection/assets/selection-pipeline-pixar-zh.jpg)

## 附带数据

`skills/sci-journal-selection/data/FQBJCR2025-UTF8.csv` — 中科院 **2025** 升级版（UTF-8）。

| 大类分区 | 刊数 | 用法 |
| --- | ---: | --- |
| 1区 | **1451** | 冲刺主池 |
| 2区 | **2844** | 稳妥主池 |
| 3区 | **4583** | 保底/扩展 |
| **1–3 合计** | **8878** | **默认候选覆盖** |
| 4区 | 12894 | 可查，不优先 |
| 全表 | 21772 | 离线 CAS 匹配 |

新锐全表未打包：在线查，否则 `新锐未核实`。详见 `skills/sci-journal-selection/data/README.md`。

## 安装（Cursor / Codex / Claude）

```bash
SKILL_SRC="$(pwd)/skills/sci-journal-selection"
mkdir -p .agents/skills && ln -sfn "$SKILL_SRC" .agents/skills/sci-journal-selection
mkdir -p .cursor/skills && ln -sfn "$SKILL_SRC" .cursor/skills/sci-journal-selection
mkdir -p .claude/skills && ln -sfn "$SKILL_SRC" .claude/skills/sci-journal-selection
# 或 ./install.sh --project .  /  ./install.sh --user
```

| 范围 | Cursor | Codex | Claude |
| --- | --- | --- | --- |
| 项目 | `.cursor/skills/…` | `.agents/skills/…` | `.claude/skills/…` |
| 用户 | `~/.cursor/skills/…` | `~/.agents/skills/…` | `~/.claude/skills/…` |

## 环境变量（可选）

仅当选择 **有apikey / 用 Jev**：

```bash
export TYPESAFE_API_KEY="your-key"   # 占位符 — 切勿提交真实 Key
```

说明见 `skills/sci-journal-selection/references/typesafe-jev.md`。`.gitignore` 已忽略 `.env`。

## 快速开始

1. 安装（上节 symlink）。
2. 对话：`Use $sci-journal-selection` / 「按选刊 skill 推荐期刊」。
3. 回答两项偏好（或默认）。
4. 粘贴题名 + 摘要。
5. 得到含中科院/新锐/LetPub/近作年份与不预测录用声明的表。

## 规范与版本

- Spec: https://agentskills.io/specification
- Skill 版本：**1.2.0**

## 免责声明

仅供学术选刊参考，不构成投稿承诺或录用预测。分区与 IF 以官方或明确标注的二次来源为准；LetPub 为第三方页示。请自行核对单位认定规则。
