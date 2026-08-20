# -*- coding: utf-8 -*-
import re, os

SCRATCH = r"C:\Users\user\AppData\Local\Temp\claude\C--Users-user-claude-code\57fd9647-d2a9-4df0-a53b-9b30bf93a77d\scratchpad"

LABELS = {
    't-list': '채점 대기', 't-write': '쓰기 채점', 't-speak': '말하기 채점', 't-band': '급 배정 참조',
    'a-list': '평가 목록', 'a-settings': '평가 설정', 'a-students': '학생 계정', 'a-teachers': '강사 계정',
    'a-monitor': '응시 현황', 'a-results': '결과·분포', 'a-difficulty': '난이도 흐름',
    'a-bands': '급수 확정', 'a-divisions': '반배정 확정', 'a-compare': '채점 비교', 'a-scoreedit': '점수 수정',
}

# match a filled shot's <img ...> that is immediately followed by </div> (no caption yet)
PAT = re.compile(r'(<img src="[^"]*" alt="([^"]*)"[^>]*>)\s*</div>')

for fname in ('admin-manual.html', 'teacher-manual.html'):
    path = os.path.join(SCRATCH, fname)
    html = open(path, encoding='utf-8').read()
    n = [0]
    def repl(m):
        alt = m.group(2)
        label = LABELS.get(alt)
        if not label:
            return m.group(0)
        n[0] += 1
        return '%s<figcaption class="shotcap">%s</figcaption></div>' % (m.group(1), label)
    new = PAT.sub(repl, html)
    open(path, 'w', encoding='utf-8').write(new)
    print("%s -> added %d captions" % (fname, n[0]))
