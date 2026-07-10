# 0001 · 项目知识与目录布局进仓库

- 状态：已采纳（2026-07-10）
- 相关：[../project-context.md](../project-context.md)、仓库根 CLAUDE.md §14


## 背景

Terry 家用机（私人电脑，晚/周末）与公司机（工作日）跨设备接力，**git/GitHub 是唯一同步通道**。此前项目知识（决策/记忆/经验）存在**用户级** `C:\Users\<user>\.claude\projects\D--nexgaios-amazon\memory\`——不进 git，换台电脑 pull 下来即丢，无法跨设备接力。数据文件也曾散在 `Downloads\`、靠手动拷贝。


## 决策

1. **一切需要跨设备延续的项目知识都放进仓库**（`D:\nexgaios-amazon\`）：
   - `docs/project-context.md`（耐用事实）、`docs/lessons-learned.md`（踩坑经验）、`docs/working-agreements.md`（工作约定）、`docs/decisions/`（本目录，难逆转决策 ADR，零填充编号）。
   - `handoff.md` 放**仓库根**（开工先读的"上次到哪"）。
2. **数据 + 产物归入 `品牌分析/`** 并按"报告 vs 产物"分类：三份报告文件夹各只装本报告（原始 CSV + 该报告 01/02/03 文档）；跨报告的 `00_三报告口径与边界总纲.md` 置于 `品牌分析/` 顶层；一切基于报告产出的东西（仪表盘 HTML、蓝图、构建代码 `v3-build/`、作战表、会话存档）归入 `品牌分析/仪表盘/`。
3. **用户级 memory 瘦成指针**：只留一行指向仓库 `docs/` + `handoff.md`，避免同一信息两地存、日后漂移（单一事实源）。


## 理由

- 跨设备接力靠 git；仓库外的东西不同步。
- 单一事实源（CLAUDE.md §13）：知识只存一处（仓库），本机 harness 自动加载的指针 + CLAUDE.md §14 的"开工读 docs/handoff"两条路都落到仓库。


## 后果

- 换机器 pull 仓库即得全部项目知识。
- 目录布局难逆转，故留此 ADR。
- **连带待办**：`v3-build/` 脚本、蓝图内仍硬编码旧 `Downloads\` 路径，需改为仓库相对路径（见 handoff 未决项）。
- **另需补**：CLAUDE.md §13 要求 `AGENTS.md` 与 `CLAUDE.md` 并存，当前仓库只有 CLAUDE.md，待补。
