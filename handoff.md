# 交接 · Ikarao SQP 仪表盘项目

> 开工先读本文 + [docs/decisions/](docs/decisions/)。耐用事实见 [docs/project-context.md](docs/project-context.md)，踩坑见 [docs/lessons-learned.md](docs/lessons-learned.md)，工作约定见 [docs/working-agreements.md](docs/working-agreements.md)，开发史见 [docs/dev-log.md](docs/dev-log.md)，三报告口径见 [品牌分析/00_三报告口径与边界总纲.md](品牌分析/00_三报告口径与边界总纲.md)，**V3 设计见 [品牌分析/仪表盘/06 蓝图](品牌分析/仪表盘/06_SQP趋势仪表盘V3蓝图.md)，H1 复盘/H2 增量结论见 [品牌分析/仪表盘/08](品牌分析/仪表盘/08_2026H1复盘与H2增量.md)**。
> 更新时间：2026-07-10（公司机 EDY 收工）。


## ⚠️ 开工先看：仓库是 PUBLIC、装敏感数据

**git 已就绪**：仓库已推到 `https://github.com/terryxming/nexgaios-amazon`（`main`，gh 已登录 terryxming），开工照常 `git pull`。

**但仓库是 PUBLIC，装着利润率/提成/运营姓名/销售额 + 全部会话原档**。Terry 决定"先跑通、跑通后再处理"；**跑通已经跑通了，转 private 或脱敏该处理了**（已挂后台卡；public 期间内容可能已被缓存/索引）。转 private 一条命令：`gh repo edit terryxming/nexgaios-amazon --visibility private --accept-visibility-change-consequences`。


## 当前状态

**主线**：V2 仪表盘 → V3 重建，SQP 情报是主干、利润是薄护栏。**2026 H1 已复盘、H2 增量已研究、V3 蓝图已全面重写**，下一步是照蓝图建 V3 或深挖。

**本会话（2026-07-10）产出（详见 dev-log）**：

- **item 1 闭环**：git init + 首推；v3-build 三脚本迁仓路径修为仓库相对（跑通验证）；补 `AGENTS.md` + `tools/check-discipline-drift.py` 漂移校验（绿）。
- **00 §七（联网核实后落盘）**：三报告的订单/销量/销售额/价格 **≠ 领星、不可对账**，讲清为什么；纠正旧"24 小时归因"（官方无此说法，是"经搜索结果页"归因）。
- **24 子代理对抗核验研究**：V3 六问题 + H1 复盘 + H2 增量，每单元 正/反/中立整合，原档存 [子代理研究_2026H1_20260710/](品牌分析/仪表盘/存档/子代理研究_2026H1_20260710/)。
- **08 复盘报告**：H1 复盘 + 六问题诊断 + H2 增量 + Q4 框架（两层白话+审计）。
- **Q4 目标框架**：领星绝对量主锚（2025 Q4=35,298 台）× 今年 H1 vs 去年 H1 同比增量，SQP 份额只作风险提示；补拉 2025-01 领星、诚实披露局限。
- **V3 蓝图 06 全面重写**：去补丁化、单一现行设计源（§一–§八 + Q1–Q6 + 新增 §五 联动深挖）。

**已定（拍板/研究裁决）**：7% 提成 = **月度**考核（同 ADR-0003）；Q1 参照系别锚"市场扩张"/低基×1.25；Q4 = 领星绝对量主锚 × H1 同比；废单 Hero → 5-ASIN 角色矩阵；集中度风险挂 X 父体（非 S2）；全部口径纠正落定（见 06 §二 / 08 §四）。


## 下一步（候选，待 Terry 定序）

1. **建 V3**：照 [06 蓝图](品牌分析/仪表盘/06_SQP趋势仪表盘V3蓝图.md) §七实施顺序（先重建 DATA 结构承载 5 ASIN+父体+领星两店 → 接线 → 护栏 → Q1–Q6 → UX）。**注意：先重建数据包**（见环境备忘）。
2. **§五 联动深挖**：挑一个点开干（SQP vs 领星 gap / 竞品 ASIN 全景 / 自家漏斗逐 ASIN / 弃单暖池 / 组合 P&L / 价格带 / S3 渠道迁移）。
3. **转 private / 脱敏**（见开头，越早越好）。
4. **作战表固化**：是否把词级作战卡并入 V3 的 Q4/Q5（decisions/0002 已定"作为增强"，时机未定）。


## 未决问题

- **仓库 public 装敏感数据** → 待转 private 或脱敏（已挂后台卡；含 08 报告 + 24 份会话原档 + 全部数据）。
- **Q4 增量口径待拍板**：保守 +24.6%（干净 5 月）还是乐观 +29.1%（完整 H1，含 1 月退货虚高）——取决于 Terry 判断 2025 Q4 份额压缩是每年规律还是去年特殊。
- **跨期默认呈现形态**（单篮子线 / 三轨带）、**ECharts vs 手写 SVG**（建议先原型对比）——见 06 §八。
- **git/public 决策未留 ADR**：转 private/脱敏拍板后补一条 ADR-0004 留痕（后台卡里已记）。
- **数据包未入仓、跨设备不同步**（见环境备忘）。


## 环境备忘

- **跨设备**：家用机(terry)/公司机(EDY)接力，git/GitHub 唯一同步通道 = `github.com/terryxming/nexgaios-amazon`。开工 `git pull`、收工 commit+push。
- **⚠️ 分析数据包在 scratchpad、未入仓、跨设备会丢**：SQP 紧凑表 `sqp_digests/`、领星两店快照 `lingxing_snapshot/`、生成脚本 `build_sqp_digests.py`/`make_agents.py` 都在临时区。**换机器要重建**：重跑领星两店取数（`lingxing_store_sales` + `lingxing_product_performance`，sid 7481+12137，2025-01~2026-06）+ 重切 SQP digests（从仓库内 `v3_data.json`）。→ 待办：考虑把这些脚本 + 快照固化进 `v3-build/`，让分析可跨设备复现。
- **领星 MCP**：`nexgaios-lingxing`（`lingxing_profit_report`）+ `lingxing_mcp`（`store_sales`/`product_performance`/`profit_op`）。两店 sid：**奥卡-US 7481、无界未来-US 12137**（无界=单品店卖 S3、占 0.68%）。利润准确窗口 2025-08~2026-05（DD+7）。
- **终端**：Windows，跑领星/中文脚本用 `PYTHONUTF8=1` 避 gbk print 崩；CSV utf-8-sig、2 行表头 skiprows=1。领星大响应会存文件（用 jq/python 或子代理处理，别灌主上下文）。
- **⚠️ `build_q1_slice.py` 过时**：重跑会用旧模板覆盖定稿 `07_V3_Q1切片.html`（丢 dataZoom + 修正诊断）；07 HTML 手工维护、构建管线非其事实源（见 lessons）。
- **多代理对抗核验**（正/反/中立整合）很好用：本项目反复靠它抓真错（8 文档、Q1 诊断、24 单元 H1 研究）。用 Workflow 编排、transcript 存档进仓库供核查。


## 上次会话摘要（2026-07-10 · 公司机 EDY）

一整段大活：**① git 打通**（EDY 机首次 init + 推到 public 仓库，Terry 两次确认 public）→ **② item 1 闭环**（修 v3-build 迁仓路径、跑通验证、发现 build_q1_slice 过时坑并还原定稿；补 AGENTS.md + 漂移校验）→ **③ 00 §七**（先派子代理联网核实"三报告 vs 领星不可对账 + 为什么"，纠正旧 24 小时归因说法，再落盘）→ **④ 24 子代理对抗核验**（V3 六问题+H1 复盘+H2 增量，正/反/中立整合 × 8 单元，原档存仓库）→ **⑤ 08 复盘报告**落盘 + 回写蓝图/00/lessons 口径纠正 → **⑥ Q4 框架**（领星绝对量主锚 × H1 同比，补拉 2025-01、诚实披露局限）→ **⑦ V3 蓝图 06 全面重写**（去补丁化、单一现行设计源、新增 §五联动深挖）。收工：刷新本交接 + 记 dev-log。**核心结论**：H1 量+份额真升但利润没过 7% 线（1 月退货潮）、增长偏低端；H2 增量靠免费 CRO + S3 放量 + 守功能词 + Q4 旺季（扣退货、过月度闸）。
