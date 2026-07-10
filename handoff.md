# 交接 · Ikarao V3 增长仪表盘

> 开工先读本文 + [架构契约](品牌分析/仪表盘/v3-build/q1-preview/dashboard-architecture.md) + [Q1需求清单](品牌分析/仪表盘/v3-build/q1-preview/q1-requirements-and-review-log.md)。设计源 [06蓝图](品牌分析/仪表盘/06_SQP趋势仪表盘V3蓝图.md)、结论 [08复盘](品牌分析/仪表盘/08_2026H1复盘与H2增量.md)、口径 [00总纲](品牌分析/00_三报告口径与边界总纲.md)、踩坑 [lessons](docs/lessons-learned.md)、开发史 [dev-log](docs/dev-log.md)。
> 更新：2026-07-10 傍晚（EDY 机收工）。git：`github.com/terryxming/nexgaios-amazon`（**public、装敏感数据、待转 private**）。


## 当前状态：Q1 仪表盘在按锁定架构重做

主线 = V3 六问题仪表盘（Q1–Q6）。本会话集中做 **Q1**，经多轮迭代 + Terry 批评，**已确认并锁定整体架构**，Q1 做成 **v8 样板**：

- **架构已锁（Terry 确认，见 dashboard-architecture.md）**：1440px 宽屏（不做手机）｜全局外壳（头+吸顶 Tab 导航 Q1–Q6，一次显一个问题）｜每问题固定 **6 层模板**（问题头/结论条/关键指标/图表/解读要点/审计）｜图表规范：**领星 1 图 12 月双线(2025/2026)+dataZoom 停 H1；SQP 需求(搜索)+成交 各 1 图双线**｜统一配色(我们=绿/市场=slate)、源标签 [SQP]/[领星]、间距/标题/标签一致。
- **Q1 v8 页面**：`品牌分析/仪表盘/07_Q1_稳定篮子预览.html`（自包含；生成器 `v3-build/q1-preview/gen_dash_v8.py` + 数据 `q1_v6_data.json`）。预览：`launch.json` 的 `ikarao-v3-dashboard`（8794 口 serve 仓库根）→ 开 `07_Q1_稳定篮子预览.html`。
- **口径已纠正并提交（`61f00f8`）**：SQP 头条改**稳定篮子**——市场搜索 −0.9%/成交 −7.6%、我方 SQP 归因 +13.6%、搜索侧份额 3.07→3.77%(+0.70pp)；**领星真实 +24.6% 不变（锚）**；撤"SQP≈领星双源互证"（巧合）。新词拆解：换血/长尾词搜索 +133% 但只搜不买（转化 0.9%）。（这坑是 Codex 审查发现、我复算确认，见 lessons"稳定篮子 vs 全榜"。）

**⚠️ 我这次最大教训（Terry 反复批评）**：别"顺手重构 / 整页重写"——每次从头写就丢上次要求，违反 CLAUDE.md §4/§3/§6。**架构已锁 → 之后只做定点手术改，每改对照 Q1 需求清单(R1–R10) + 4 常驻监工审。**


## 下一步

1. **派 4 常驻监工审 v8**（亚马逊业务专家/亚马逊新人/前端工程师+UI/UX/数据解读；这轮加"结构一致性"rubric）→ 定点修。（收工时中断在这一步。）
2. Q1 定稿后，**按同一 6 层模板 + 图表规范建 Q2–Q6**（数据绑定见架构契约§五）。
3. **reconcile 两条 Q1 轨道**：Codex 的构建管线（`build_all`→`07_V3_Q1切片.html`，当前是被否的"决策治理版"）vs 我的仪表盘（`07_Q1_稳定篮子预览.html`）——定用哪套或合并。
4. 处理**未提交的 Codex 大批**（见未决）。


## 未决问题

- **一大批 Codex 工程未提交**（`build_all.py`/`validate_build.py`/`build_q1_data.py`/`data/`/`q1-slice-template.html`/`09_商业级分析证据合同.md`/`ADR-0004`/`07_V3_Q1切片.html`重生成/`v3_data.json`重生成/`.claude/launch.json`）。Terry 已定：**保留有用工程；09 那套重合同"先别当定论"（N=1、过度设计、曾把 Codex 带偏）**。本 handoff/dev-log 之前被 Codex 改写过（数据链版），我这次按当前实况覆盖重写。
- **仓库 public 装敏感数据** → 待转 private 或脱敏（`gh repo edit ... --visibility private`）。
- **Codex 构建链有同一个稳定篮子口径错**（`build_q1_data.py`/`07_V3_Q1切片.html` 还是全榜）——若保留其工程须先修。
- Q4 增量口径 +24.6%(保守)/+29.1%(乐观) 待拍板。
- 数据包（sqp_digests/lingxing_snapshot/生成脚本）多在 scratchpad 未入仓（Q1 相关的已存 `v3-build/q1-preview/`）。


## 环境备忘

- 领星两店 SID：奥卡-US `7481`、无界-US `12137`。跑中文脚本用 `PYTHONUTF8=1`。
- **别重跑 Codex 的 `build_q1_slice.py`**（会生成被否的治理版 07_V3_Q1切片）；我的 Q1 页用 `q1-preview/gen_dash_v8.py`。
- 关键数字锁定见 `q1-preview/q1-requirements-and-review-log.md`（含 4 监工评审日志）。
- 4 常驻监工角色：亚马逊业务专家 / 亚马逊新人 / 前端工程师+UI/UX / 数据解读专家；每版都审、含结构一致性。


## 本次会话摘要（2026-07-10 · EDY 机）

Q1 仪表盘从 v1 迭代到 v8：起初零散、过度大白话，经 Terry 多轮批评（要 1440px 宽屏 / 专业但清晰 / 源标签 / 完整时间轴同比+环比 / 结构一致 / **别顺手重构**）逐步收敛；中途 Codex 审查发现 SQP 头条误用全榜、我复算确认并纠正为稳定篮子口径（提交 `61f00f8`）；答复了"稳定篮子会漏新需求"——拆出新词证明其只搜不买。最后 **Terry 拍板：先定架构再建**，我把整体架构写成契约、他确认锁定，Q1 重做为 v8（全局外壳+Tab+6 层模板+领星1图12月双线/SQP需求成交双线）。收工中断在"派 4 监工审 v8"前。核心教训：**先规划架构、只定点改、每改对照需求清单+监工**。
