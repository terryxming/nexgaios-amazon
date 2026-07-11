# -*- coding: utf-8 -*-
"""按路由把 CLAUDE.md 的纪律章节重新注入上下文，对冲长会话的位置衰减（见 ADR-0005）。

单一事实源：只读 CLAUDE.md 的 DISCIPLINE:SHARED 区块，按 `## N.` 章节切片，
按触发点（gate）分发对应维度的全文——不 fork、不摘要，改 CLAUDE.md 四个 gate 自动跟随。

gate 与维度映射（合起来正好覆盖 §1–§14，无遗漏无重复）：
  session  开工        §14                    -> SessionStart（纯 stdout 注入）
  prompt   动手前+交付前 §1 §2 §5 §6 §7 §9 §10 §11 -> UserPromptSubmit（纯 stdout 注入）
  write    落盘前       §3 §4 §8 §12 §13         -> PreToolUse（走 additionalContext，不阻断）

注：原打算把"交付前"挂 Stop，但 Stop hook 返回 additionalContext 会触发再入
（continuation）——每轮收尾都被拉回、且有循环风险（Claude Code 为此设 stop_hook_active
防护位）。故把交付前并入 UserPromptSubmit 每轮注入，不用 Stop。

铁律：任何异常都 fail-open（退出码 0、空输出），绝不阻断 prompt 提交或工具调用。
"""
import io, os, re, sys, json

START = '<!-- DISCIPLINE:SHARED:START -->'
END = '<!-- DISCIPLINE:SHARED:END -->'

GATES = {
    'session': {'sections': [14], 'event': 'SessionStart', 'mode': 'stdout', 'label': '开工巡检'},
    'prompt': {'sections': [1, 2, 5, 6, 7, 9, 10, 11], 'event': 'UserPromptSubmit', 'mode': 'stdout', 'label': '动手前与交付前'},
    'write': {'sections': [3, 4, 8, 12, 13], 'event': 'PreToolUse', 'mode': 'json', 'label': '落盘前'},
}


def repo_root():
    env = os.environ.get('CLAUDE_PROJECT_DIR')
    if env and os.path.isdir(env):
        return env
    # <repo>/.claude/hooks/discipline-hook.py -> <repo>
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(os.path.dirname(here))


def load_sections():
    """返回 {章节号: 全文}——只取 DISCIPLINE:SHARED 区块内的编号章节。"""
    path = os.path.join(repo_root(), 'CLAUDE.md')
    t = io.open(path, encoding='utf-8', newline='').read()
    i, j = t.find(START), t.find(END)
    if i < 0 or j < 0:
        return {}
    shared = t[i + len(START):j]
    out = {}
    # 按行首二级标题 `## ` 切片；`###/####` 子节因非 `## ` 而自然留在父节内
    for part in re.split(r'(?m)^(?=## )', shared):
        m = re.match(r'## (\d+)\. ', part)
        if m:
            out[int(m.group(1))] = part.strip('\n')
    return out


def build(gate):
    spec = GATES[gate]
    sections = load_sections()
    picked = [sections[n] for n in spec['sections'] if n in sections]
    if not picked:
        return ''
    header = '【纪律复诵 · %s维度 · 来源 CLAUDE.md（单一事实源）】' % spec['label']
    return header + '\n\n' + '\n\n\n'.join(picked)


def main():
    gate = sys.argv[1] if len(sys.argv) > 1 else ''
    if gate not in GATES:
        return  # 未知 gate：静默，不打扰
    text = build(gate)
    if not text:
        return
    spec = GATES[gate]
    if spec['mode'] == 'json':
        # ensure_ascii 默认 True -> 纯 ASCII，不受 Windows 控制台编码影响
        sys.stdout.write(json.dumps({
            'hookSpecificOutput': {
                'hookEventName': spec['event'],
                'additionalContext': text,
            }
        }))
    else:
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass
        sys.stdout.write(text + '\n')


if __name__ == '__main__':
    try:
        main()
    except Exception:
        pass  # fail-open：任何异常都不得阻断会话
    sys.exit(0)
