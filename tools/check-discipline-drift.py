# -*- coding: utf-8 -*-
"""校验 CLAUDE.md 与 AGENTS.md 的 DISCIPLINE:SHARED 共享段逐字节一致（CLAUDE.md §13）。

两个平台各读各的文件、AGENTS.md 无 import 机制，故共享纪律必须两地各存一份且完全一致；
本脚本抽取两文件中 `DISCIPLINE:SHARED:START` 与 `:END` 之间的内容逐字节比对。

用法：python tools/check-discipline-drift.py
      一致 → 打印 OK、退出码 0；漂移 → 打印首个差异位置、退出码 1。
"""
import io, os, sys

START = '<!-- DISCIPLINE:SHARED:START -->'
END   = '<!-- DISCIPLINE:SHARED:END -->'

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)


def shared(path):
    t = io.open(path, encoding='utf-8', newline='').read()
    i, j = t.find(START), t.find(END)
    if i < 0 or j < 0:
        sys.exit('缺少 DISCIPLINE:SHARED 标记: %s' % path)
    return t[i + len(START):j]


a = shared(os.path.join(REPO, 'CLAUDE.md'))
b = shared(os.path.join(REPO, 'AGENTS.md'))

if a == b:
    print('OK: CLAUDE.md 与 AGENTS.md 共享段逐字节一致 (%d 字符)' % len(a))
    sys.exit(0)

n = min(len(a), len(b))
k = next((i for i in range(n) if a[i] != b[i]), n)
print('DRIFT: 共享段不一致，首个差异在第 %d 字符（共 CLAUDE %d / AGENTS %d）' % (k, len(a), len(b)))
print('  CLAUDE.md 附近: %r' % a[max(0, k - 30):k + 30])
print('  AGENTS.md 附近: %r' % b[max(0, k - 30):k + 30])
sys.exit(1)
