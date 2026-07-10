# 交接 · Ikarao SQP 仪表盘项目

> 开工先读本文 + [docs/decisions/](docs/decisions/)。耐用事实见 [docs/project-context.md](docs/project-context.md)，踩坑经验见 [docs/lessons-learned.md](docs/lessons-learned.md)，工作约定见 [docs/working-agreements.md](docs/working-agreements.md)，三报告口径边界见 [品牌分析/00_三报告口径与边界总纲.md](品牌分析/00_三报告口径与边界总纲.md)。
> 更新时间：2026-07-10（公司机 EDY，item 1 闭环 checkpoint）。上次收工：2026-07-10 凌晨（家里机 terry）。


## ✅ git 已就绪（跨设备同步通道已打通）

**仓库已 `git init` 并推到 `https://github.com/terryxming/nexgaios-amazon`（`main` 分支）**，2026-07-10 于公司机（EDY）完成。开工照常 `git pull`；`.claude/settings.local.json` 按机器私有已 `.gitignore`。

**⚠️ 仓库当前是 PUBLIC，装着敏感商业数据（利润率/提成/运营姓名/销售额 + 全量会话存档）。** Terry 决定"先跑通、跑通后再处理"。**待办：转 private 或脱敏**（public 期间内容可能已被缓存/索引，越早越好）——已挂后台任务卡，见下方未决问题。


## 当前状态

**主线**：给 V2 仪表盘挑业务/UX 问题、重建为 V3（Q1–Q6），SQP 情报是主干、利润是薄护栏。

**已完成**：

- **三报告地基（今晚重点，已扎实）**：SQP + 热门搜索词 + 搜索目录绩效，三份各有 01/02 字段/用法文档 + SQP 有 03 分类文档 + 跨报告 `品牌分析/00_总纲`。**8 份文档经"正方+反方+中立整合"多代理对抗核验（联网核官方 + 真实数据复算），逐条修正约 35 处**（含 2 处我之前造成的错：SQP-01"得分排序"、00 列号基准）。核内核（公式/份额/CVR/CTR 定义）复算全对；补齐了防下游踩坑的护栏（样本量闸、换血、营收别反推、前3品牌≠点击第1商品等）。详见 `docs/lessons-learned.md`。
- **词级作战表·定版**：`品牌分析/仪表盘/词级作战表_定版.csv`（运营底稿）+ `_老板决策版.csv`（8列白话）。两轮子代理审查修 4 项定稿。
- **V3 Q1 切片定稿** `品牌分析/仪表盘/07_V3_Q1切片.html`：两层结构（白话卡 + ▸展开审计）、数据绑定、ECharts 时间轴缩放（治强季节性、默认停上半年可拖出看旺季）、Q1 诊断已按三报告审查修正（背离=早春灌水非萎缩、我们健康、CTR 是真警报）。定下 Q2–Q6 基调。
- **知识/目录进仓库**：项目知识从用户级 memory 迁入仓库 `docs/`；数据+产物按"报告 vs 仪表盘"归类进 `品牌分析/`。见 `docs/decisions/0001`。
- **item 1 闭环（2026-07-10 公司机 EDY）**：① `git init` + 首推 GitHub（见上）；② 修 v3-build 三脚本迁仓路径为仓库相对、跑通验证（`v3_data.json`/`q1_slice_data.json` 字节级复现、口径数字全对）；③ 补 `AGENTS.md`（共享段与 CLAUDE.md 逐字节一致）+ `tools/check-discipline-drift.py` 校验（绿）。**注**：蓝图内其实无硬编码路径（原交接说法不准），只脚本有、已全修。踩坑见 `docs/lessons-learned.md`：build_q1_slice 过时、重跑会覆盖定稿。


## 下一步（候选，待 Terry 定序）

1. **Phase 3**：按蓝图做 Q2（份额 2×2 小多图）+ Q3（5-ASIN 角色矩阵 + 指数化对比），复用 Q1 的缩放画法与两层结构。
2. **蓝图 §六 4 个待拍板项**（Terry 定）：Q1 参照系 / 跨期形态 / ECharts 与否 / S2·S3 走量力度 + 提成考核周期。
3. **作战表固化**：是否把词级作战卡并入 V3 的 Q4/Q5。
4. **（可选）** build_q1_slice.py 模板同步到定稿，或明确"它只产数据、07 HTML 手工维护"。


## 未决问题

- **仓库是 PUBLIC、装敏感数据**（利润/提成/姓名/存档）——待转 private 或脱敏（Terry"跑通后处理"，已挂后台卡）；public 期间或已被缓存/索引。
- **`build_q1_slice.py` 过时**：重跑会用旧模板覆盖定稿 07 HTML（丢 dataZoom + 修正诊断）；构建管线非 Q1 切片事实源、定稿 HTML 手工维护；缺 v3_data→q1_slice 基座构建一步。
- 作战表要不要现在固化进 Q4/Q5（decisions/0002 已定"作为增强、不另起炉灶"，但时机未定）。
- **无 CI**：`tools/check-discipline-drift.py` 目前手动跑，CI 门禁作为后续项。


## 环境备忘

- **跨设备**：家用机(terry)/公司机(EDY)接力，git/GitHub 唯一同步通道 = `github.com/terryxming/nexgaios-amazon`（gh 已登录 terryxming、`main` 分支）。开工 `git pull`、收工 commit+push。
- **终端**：Windows，中文路径在 gbk 终端 print 会乱码——用 python 写 UTF-8 文件再 Read，别直接 print 中文。CSV 编码 utf-8-sig、2 行表头 skiprows=1。
- **领星 MCP**：`nexgaios-lingxing` 的 `lingxing_profit_report`（sids=[7481]，逐月拉，准确窗口 2025-08~2026-05）。见 `docs/project-context.md`。
- **预览**：Q1 切片是自包含离线 HTML（echarts.min.js 同目录），双击即开；本地验证用 `.claude/launch.json` 起 python http.server（截图对 ECharts 偶超时，用 preview_eval/inspect 更稳）。
- **会话原档**：`品牌分析/仪表盘/存档/`——今晚 3 段（`e01e5f80`/`bb179777`/`1c12c92e`），加更早的 07-09（a/b）与家里 V2 阶段（0600a961）。
- **多代理核验很好用**：本项目反复靠"正方+反方+中立整合"对抗核验抓真错（作战表方法、Q1 诊断、8 份文档），重要结论落地前先派子代理证伪、再自己复算把关（`docs/working-agreements.md`）。


## 上次会话摘要（2026-07-09 晚 ~ 07-10 凌晨）

接着 07-09 的活：三报告联动探索（做词级作战表，两轮审查揪出单月/价尺/品牌名漂移等错→定版）→ Q1 诊断经三报告审查修正（背离=早春灌水、我们健康、CTR 警报）→ Q1 图加时间轴缩放治季节性 → **打地基**：先建三报告边界总纲（00）→ **归类**：文件迁入仓库 `品牌分析/` → **知识进仓库**：memory 迁入 `docs/` + ADR → **文档核验**：8 份地基文档多代理对抗核验 + 逐条修正约 35 处（含我自己 2 处错）。收工：复制 3 段会话原档进存档 + 刷新本交接。
