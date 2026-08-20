# -*- coding: utf-8 -*-
import base64, re, os, sys

FOLDER = r"C:\Users\user\manual-shots"
SCRATCH = r"C:\Users\user\AppData\Local\Temp\claude\C--Users-user-claude-code\57fd9647-d2a9-4df0-a53b-9b30bf93a77d\scratchpad"

MIME = {'.png':'image/png', '.webp':'image/webp', '.jpg':'image/jpeg', '.jpeg':'image/jpeg'}

def datauri(basename):
    for ext in ('.png', '.webp', '.jpg', '.jpeg'):
        p = os.path.join(FOLDER, basename + ext)
        if os.path.exists(p):
            with open(p, 'rb') as f:
                b = base64.b64encode(f.read()).decode('ascii')
            return "data:%s;base64,%s" % (MIME[ext], b)
    return None

# marker substring (found inside the .shot div) -> image basename
MAPS = {
    'student-manual.html': {
        'shot.s1': 's-login',
        'shot.s2': 's-mic',
        'shot.s3': 's-intro',
        'shot.s5': 's-done',
        'shot.s6': 's-result',
    },
    'teacher-manual.html': {
        't-list \u00b7': 't-list',
        't-write \u00b7': 't-write',
        't-speak \u00b7': 't-speak',
        't-band \u00b7': 't-band',
        't-history \u00b7': 't-history',
    },
    'admin-manual.html': {
        'a-list \u00b7': 'a-list',
        'a-settings \u00b7': 'a-settings',
        'a-students \u00b7': 'a-students',
        'a-teachers \u00b7': 'a-teachers',
        'a-monitor \u00b7': 'a-monitor',
        'a-results \u00b7': 'a-results',
        'a-difficulty \u00b7': 'a-difficulty',
        'a-bands \u00b7': 'a-bands',
        'a-divisions \u00b7': 'a-divisions',
        'a-compare \u00b7': 'a-compare',
        'a-scoreedit \u00b7': 'a-scoreedit',
    },
}

SHOT_RE = re.compile(r'<div class="shot([^"]*)"([^>]*)>(.*?)</div>', re.S)

for fname, mapping in MAPS.items():
    path = os.path.join(SCRATCH, fname)
    if not os.path.exists(path):
        print("skip (missing):", fname); continue
    html = open(path, encoding='utf-8').read()
    filled = []
    def repl(m):
        cls, attrs, inner = m.group(1), m.group(2), m.group(3)
        if 'filled' in cls:
            return m.group(0)
        for marker, base in mapping.items():
            if marker in inner:
                uri = datauri(base)
                if uri:
                    filled.append(base)
                    return '<div class="shot%s filled"%s><img src="%s" alt="%s" loading="lazy"></div>' % (cls, attrs, uri, base)
                return m.group(0)  # slot known but no file yet -> keep placeholder
        return m.group(0)
    new = SHOT_RE.sub(repl, html)
    open(path, 'w', encoding='utf-8').write(new)
    print("%s -> filled %d shots: %s" % (fname, len(filled), ", ".join(filled) if filled else "(none)"))
