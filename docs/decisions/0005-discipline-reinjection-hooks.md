# 0005 · 纪律复诵 hook：按维度路由重新注入，对冲长会话衰减

- 状态：已采纳（2026-07-11）
- 相关：[../../CLAUDE.md](../../CLAUDE.md) §11/§12/§13、[0002](0002-report-linkage-scope-guardrail.md)（同为门禁类决策）、`tools/check-discipline-drift.py`


## 背景

CLAUDE.md 全部工程纪律在会话开局被注入上下文顶部。随着上下文变长，模型对顶部指令的注意力下降（位置衰减），纪律触发概率随之走低。CLAUDE.md 是"注入一次、放在顶部"，缺一个让纪律在会话中持续在场、且落到注意力更强的近端的确定性机制。hook 的价值正是确定性执行——它一定会跑，不像 CLAUDE.md 只是概率性被遵守。


## 决策

新增 `.claude/hooks/discipline-hook.py` 与 `.claude/settings.json` 的三个 hook，把 CLAUDE.md 的纪律**全文**（不摘要）按维度路由到各自触发点重新注入：

- `SessionStart` → §14 开工巡检（纯 stdout 注入）
- `UserPromptSubmit` → §1/§2/§6/§10 动手前 + §5/§7/§9/§11 交付前，每轮注入（纯 stdout 注入）
- `PreToolUse`（`matcher: Write|Edit|NotebookEdit`）→ §3/§4/§8/§12/§13 落盘前（走 `hookSpecificOutput.additionalContext`，不阻断工具）

三个 gate 合起来正好覆盖 §1–§14，无遗漏无重复。hook 只读 CLAUDE.md 的 `DISCIPLINE:SHARED` 区块并按 `## N.` 章节切片，不 fork 任何副本。


## 理由

- **路由而非每轮全量**：每个 gate 只注入本维度全文，避免每轮重复整份 27 KB 把上下文烧穿、提前触发压缩；且更贴合"每条纪律在它真正起作用的时刻出现"。
- **只读 CLAUDE.md 本体**：改纪律无需改 hook，不产生第二事实源（§13 单一事实源）。这是 Claude 平台专属机制，不复制纪律内容，故不影响 `check-discipline-drift.py` 的 SHARED 逐字节比对。
- **全文不摘要**：保留每条纪律的"为什么 + 例子"，避免摘要丢掉可执行性（§11 祈使要配理由）。
- **fail-open**：hook 任何异常都退出码 0、空输出，绝不阻断 prompt 提交或工具调用。


## 后果

- `.claude/settings.json` 首次入仓、随 git 同步，两台机器 pull 后自动生效（§14 跨设备）。
- 常驻成本（粗估 0.75 token/字符）：`prompt` 维度每轮 `UserPromptSubmit` 约 **5.0k token**（动手前+交付前）；`write` 约 3.0k 为**按需触发**（落盘时）；`session` 约 0.6k 每会话一次。
- 交付前原设计挂 `Stop`，实测发现 `Stop` hook 返回 `additionalContext` 会触发再入（continuation）——每轮收尾被拉回、且有循环风险（Claude Code 为此设 `stop_hook_active` 防护位）；故并入 `UserPromptSubmit` 每轮注入，不用 `Stop`。若日后要"收尾前强制自检"的硬门禁，须用 `Stop` 带 `decision: block` + `stop_hook_active` 防循环，另行评估。
- 依赖 `python` 在 PATH（与 `.claude/launch.json` 用法一致）。
- 回退：删除 `.claude/settings.json` 的 `hooks` 段即整体停用，无外部依赖、无数据迁移。
