# 交接 · Ikarao SQP 仪表盘

> 开工先读本文 + [00 三报告口径总纲](品牌分析/00_三报告口径与边界总纲.md) + [耐用事实 project-context](docs/project-context.md) + [工作约定 working-agreements](docs/working-agreements.md)。设计源 [06 蓝图](品牌分析/仪表盘/06_SQP趋势仪表盘V3蓝图.md)、Q1 样板 [07 稳定篮子预览](品牌分析/仪表盘/07_Q1_稳定篮子预览.html)（生成器/规格在 `v3-build/q1-preview/`）。
>
> 更新：2026-07-11。git：`github.com/terryxming/nexgaios-amazon`（public、装敏感数据、待转 private）。


## 当前状态：仓库已重置到可信基线

本会话末尾做了一次**清库重置**：Terry 对堆积的派生/历史/争议内容失去信任，只保留可信基座，其余删除、从头重建。

保留下来的可信基座：

- **三报告原始数据 + 字典**：`搜索查询绩效报告/`(01/02/03)、`搜索目录绩效/`(01/02)、`热门搜索词/`(01/02)。
- **口径**：`00_三报告口径与边界总纲.md`。
- **设计 + Q1 样板**：`06` 蓝图、`07_Q1_稳定篮子预览.html`（已定稿 v8）+ `echarts.min.js` + `v3-build/q1-preview/`（生成器 `gen_dash_v8.py`、数据 `q1_v6_data.json`、规格 `dashboard-architecture.md`/`q1-requirements-and-review-log.md`）。
- **纪律 + 知识**：`CLAUDE.md`/`AGENTS.md` + `.claude/hooks/` + `tools/check-discipline-drift.py`；`docs/project-context.md`/`working-agreements.md`/`decisions/{0001,0005}`。

已删（Codex 原子层数据管线、`08` 复盘、`09` 证据合同、旧仪表盘 `04/05`、ADR-0002/0003/0004、`存档/`、会话 jsonl、dev-log、lessons 等）。**回滚锚点**：重置前 commit = `44f2318`（已提交内容可从 git 历史找回；未跟踪部分——Codex 管线 `data/`、部分脚本、`09`、ADR-0004——已永久删除，需从原始报告重建）。

Q1 仪表盘 `07` 已定稿：口径统一到 **strict_10of10**（份额 3.03→3.75%/+0.71pp、市场可比搜索 −0.9%/成交 −7.6%、我方 SQP 归因 +14.1%、领星真实 +24.6% 为锚）。


## 下一步

1. **从保留的三报告原始数据重建权威"原子层"**（不复用被删的 Codex 管线，从零写、配 validator）：SQP 品牌/大盘/5ASIN 四阶(曝光/点击/加购/成交)×逐月×两年(2025-02~2026-06，YoY 仅 Feb–Jun 可对齐)、稳定篮子三口径(strict_10of10 171词 / paired_4of5 240词 / 全榜)；catalog 自家漏斗(ASIN×月)；热门词(前三 ASIN 量化 + 前三品牌仅名)。数字唯一事实源 = build+validator（见 working-agreements「数字只有一个事实源」）。
2. **建 Q2「我们在赢份额吗」**：SQP 四阶份额 YoY + 份额升幅分解(我方真涨 vs 大盘塌，约六成/四成) + 领星 ASP(结构下沉非旗舰降价)。套 06 蓝图 + 07 的 6 层模板。
3. 之后 Q3–Q6 按同模板。


## 未决问题

- **Q2 边界与派生指标**未锁（四阶完整 vs 聚焦、Q2/Q3 的 ASP 分界）。
- **ASIN 级毛利拿不到**：领星快照只到运营组合级 → Q3/Q6 的 ASIN 毛利需补领星成本数据。
- **热门词新词/长尾竞品盲区**：报告只给前三、且原 Codex 只 join 了 strict 词；新词竞品格局要直接读原始热门词 CSV。
- **仓库 public 装敏感数据** → 待转 private 或脱敏。


## 环境备忘

- 领星两店 SID：奥卡-US `7481`、无界-US `12137`。跑中文脚本用 `PYTHONUTF8=1`。
- 预览 07：`.claude/launch.json` 的 `ikarao-v3-dashboard`（8794 口 serve 仓库根）→ 开 `品牌分析/仪表盘/07_Q1_稳定篮子预览.html`。07 靠同目录 `echarts.min.js` 渲染。
- **strict 稳定篮子定义** = 同一词两年 Feb–Jun 全 5 月都在榜（171 词，覆盖搜索侧成交约 90%）；protected facts：搜索 2,872,374→2,845,191、成交 73,556→67,973、我方 2,231→2,546。
- 三报告联动红线（00 总纲）：SQP↔领星只比增速不对账；catalog↔领星禁求精确占比（毛额vs净额）；热门词竞品 ASIN 仅展示、认 ASIN 不认品牌名。


## 上次会话摘要（2026-07-11）

先给 Q1 v8 加三处（问题区改「结论+证据」、KPI 补量级、市场成交图叠品牌 YoY 双线），并把口径从 paired 统一到 strict（份额 3.07→3.77 改 3.03→3.75、归因 +13.6→+14.1），审计份额分解 ¾/¼ 复算修正为约六成/四成，并立「数字单一事实源」防漂移规矩、把 06/08 的过时 paired 数覆盖为 strict。随后 Terry 要进 Q2，先查清三报告口径与联动（派子代理：SQP 三层四阶已全、catalog 自家漏斗算法复算无误、热门词确认「前三 ASIN 量化 / 前三品牌仅名」两套独立体系）；核验 Codex 数据层其实正确（validator protected facts = 独立复算值），但 Terry 决定弃用、从零重建。最后对整仓失去信任，执行「重置到可信基线」清库（删派生/历史/争议，修所有保留文档的死链，重写本 handoff）。核心教训：数字只留 build+validator 一处、prose 不自持；派生数据不轻信、要能自己重建才算可信。
