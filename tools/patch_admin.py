import re, sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
subs = [
    ('<meta name="theme-color" content="#19191b">', '<meta name="theme-color" content="#9e2512">'),
    ('<title>Controle — Votação ao vivo</title>', '<title>Controle — Tribunal do Amor</title>'),
    ('.chip.voting { background: var(--yellow); color: var(--bg); }', '.chip.voting { background: var(--wine); color: var(--paper); }'),
    ('.chip.offline { background: var(--orange); color: var(--bg); }', '.chip.offline { background: #d86a3a; color: #fff; }'),
    ('.btn.go { background: var(--yellow); color: var(--bg); }', '.btn.go { background: var(--go); color: #fff; }'),
    ('.btn.stop { background: var(--red); color: var(--bg); }', '.btn.stop { background: var(--ink); color: var(--paper); }'),
    ("'Pergunta ' + (cur.index + 1) + ' de ' + cur.total", "'Caso ' + (cur.index + 1) + ' de ' + cur.total"),
    ("cur.total + ' perguntas prontas'", "cur.total + ' casos prontos'"),
    ("'Todas as perguntas foram votadas.'", "'Todos os casos foram votados.'"),
    ("ready: 'Pergunta na tela'", "ready: 'Caso na tela'"),
]
for a, b in subs:
    if a not in s:
        sys.exit('não encontrado: ' + a)
    s = s.replace(a, b)
res = [
    (r'(\.mini \.r i \{[^}]*?)color: var\(--bg\);', r'\1color: var(--paper);'),
    (r'(\.mini \.bar u \{[^}]*?)opacity: \.85;', r'\1opacity: .3;'),
    (r'(\.mini \.bar span \{[^}]*?) text-shadow: [^;]*;', r'\1'),
    (r'(\.btn \{[^}]*?)color: var\(--fg\);', r'\1color: var(--paper);'),
    (r'(body \{ font-family: var\(--font\);)', r'\1 background: var(--cream);'),
]
for a, b in res:
    s, n = re.subn(a, b, s, count=1)
    if n != 1:
        sys.exit('regex sem efeito: ' + a)
open(p, 'w', encoding='utf-8').write(s)
print('admin.html ajustado')
