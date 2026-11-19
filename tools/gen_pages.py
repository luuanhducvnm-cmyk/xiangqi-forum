#!/usr/bin/env python3
"""Sinh các trang BÀI TẬP (chiếu bí 1/2/3 nước) cho cờ vua + cờ tướng, tiếng Anh và tiếng Việt, từ tools/puzzles.json.
Đáp án KHÔNG gõ tay: cây nước đi do tools/solver.mjs chứng minh bằng đúng bộ luật của 2 game (key duy nhất, mọi nước đỡ đều bị chiếu bí).
Kết quả giải được cache trong tools/puzzle-cache.json, khoá bằng hash của solver + bộ luật → đổi luật/solver thì tự giải lại."""
import json, os, subprocess, hashlib, html, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
RG = os.path.join(ROOT, 'vendor', 'royal-games')
SRC = [os.path.join(HERE, 'solver.mjs'), os.path.join(RG, 'xiangqi/public/js/rules.js'), os.path.join(RG, 'chess/public/js/chess.js')]
CACHE = os.path.join(HERE, 'puzzle-cache.json')
def salt():
    h = hashlib.sha256()
    for f in SRC: h.update(open(f, 'rb').read())
    return h.hexdigest()[:16]
def puzzles(): return json.load(open(os.path.join(HERE, 'puzzles.json')))

def solve_all():
    ps = puzzles(); s = salt()
    c = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    if c.get('salt') != s: c = {'salt': s, 'res': {}}
    todo = [p for p in ps if p['game'] + ' ' + p['fen'] not in c['res']]
    if todo:
        print(f'  giải {len(todo)} thế cờ bằng solver…', file=sys.stderr)
        q = [dict(id=p['id'], game=p['game'], fen=p['fen'], maxN=p['n']) for p in todo]
        out = subprocess.run(['node', os.path.join(HERE, 'solver.mjs')], input=json.dumps(q), capture_output=True, text=True, timeout=3600)
        if out.returncode: raise SystemExit('solver lỗi: ' + out.stderr[:400])
        res = json.loads(out.stdout)
        for p in todo: c['res'][p['game'] + ' ' + p['fen']] = res[p['id']]
        json.dump(c, open(CACHE, 'w'))
    for p in ps:   # CỔNG KIỂM TRA: mỗi thế phải đúng độ sâu, key duy nhất, mọi đường là chiếu bí thật
        r = c['res'][p['game'] + ' ' + p['fen']]
        assert r.get('n') == p['n'] and r.get('unique') and r.get('strictOk'), f'thế {p["id"]} KHÔNG đạt: {r.get("n")} {r.get("keys")}'
    return {p['id']: c['res'][p['game'] + ' ' + p['fen']] for p in p_list(ps)}
def p_list(ps): return ps
esc = html.escape

# ───────────── ngôn ngữ ─────────────
PN = {  # tên quân khi gợi ý
 'en': {'ch': dict(K='king', Q='queen', R='rook', B='bishop', N='knight', P='pawn'), 'xq': dict(K='general', A='advisor', E='elephant', H='horse', R='chariot', C='cannon', P='soldier')},
 'vi': {'ch': dict(K='Vua', Q='Hậu', R='Xe', B='Tượng', N='Mã', P='Tốt'), 'xq': dict(K='Tướng', A='Sĩ', E='Tượng', H='Mã', R='Xe', C='Pháo', P='Tốt')},
}
DIRV = {'+': 'tiến', '-': 'thoái', '=': 'bình'}
def xq_text(note, lang):
    if lang == 'en': return note['wxf']
    t = PN['vi']['xq'][note['t']]
    if note['amb']: return f"{t} {'tiền' if note['fr'] == 'front' else 'hậu'} {DIRV[note['dir']]} {note['num']}"
    return f"{t} {note['file']} {DIRV[note['dir']]} {note['num']}"
def mv(node, game, lang): return node['san'] if game == 'ch' else xq_text(node['note'], lang)

def cont(node, num, game, lang, red='1'):
    """HTML phần còn lại của đường chiếu bí sau nước `node` (nước thứ `num`)."""
    if node['mate']: return ''
    reps = node['replies']
    if len(reps) == 1:
        r = reps[0]; nx = r['next']
        return f" {num}… {mv(r, game, lang)} {num+1}. {mv(nx, game, lang)}" + cont(nx, num + 1, game, lang)
    items = ''.join(f"<li>{num}… {mv(r, game, lang)} {num+1}. {mv(r['next'], game, lang)}{cont(r['next'], num + 1, game, lang)}</li>" for r in reps)
    return f'<ul>{items}</ul>'

def hint(game, tree, lang):
    if game == 'ch':
        k = tree['san']; t = k[0] if k[0] in 'KQRBN' else 'P'
        quiet = not (k.endswith('+') or k.endswith('#') or 'x' in k)
        if lang == 'en': return f"The first move is made by the {PN['en']['ch'][t]}" + (" and it is a quiet move: not a check, not a capture." if quiet else " and it is forcing: a check or a capture.")
        return f"Nước đầu tiên do quân {PN['vi']['ch'][t]} đi" + (", và đó là một nước đi yên tĩnh: không chiếu, không ăn quân." if quiet else ", và nó là nước ép buộc: chiếu hoặc ăn quân.")
    t = tree['note']['t']; chk = tree['check']
    if lang == 'en': return f"The first move is made by the {PN['en']['xq'][t]}" + (" and it gives check." if chk else " and it is a quiet move: it does not give check.")
    return f"Nước đầu tiên do quân {PN['vi']['xq'][t]} đi" + (" và đó là nước chiếu." if chk else ", và đó là nước đi yên tĩnh: chưa chiếu tướng.")

def puzzle_md(p, r, idx, lang):
    g, n, tree = p['game'], p['n'], r['tree']
    side = {'en': ('White', 'Red'), 'vi': ('Trắng', 'Đỏ')}[lang][0 if g == 'ch' else 1]
    other = {'en': ('Black', 'Black'), 'vi': ('Đen', 'Đen')}[lang][0]
    key = mv(tree, g, lang); mark = '#' if (g == 'ch' and tree['mate']) else '!' if g == 'ch' else ''
    legal = r['legal']
    if lang == 'en':
        cap = f"Puzzle {idx}: {side} to move, mate in {n}."; head = f"## Puzzle {idx}"
        hsum = 'Hint'; ssum = 'Show the solution'
        first = f"<p><strong>Key move: 1. {esc(key)}{mark}</strong> Only 1 of the {legal} legal first moves forces mate; every other move lets {other} escape or defend.</p>"
        rep = f"<p>{other} has {len(tree['replies'])} legal repl{'y' if len(tree['replies']) == 1 else 'ies'}, and each one is checkmated:</p>"
        tail = ''
    else:
        cap = f"Bài {idx}: {side} đi trước, chiếu {'hết' if g == 'ch' else 'bí'} sau {n} nước."; head = f"## Bài {idx}"
        hsum = 'Gợi ý'; ssum = 'Xem đáp án'
        first = f"<p><strong>Nước then chốt: 1. {esc(key)}{mark}</strong> Chỉ có 1 trong {legal} nước đi hợp lệ đầu tiên ép được chiếu {'hết' if g == 'ch' else 'bí'}; mọi nước khác đều để {other} thoát hoặc kịp phòng thủ.</p>"
        rep = f"<p>{other} có {len(tree['replies'])} nước đáp hợp lệ, và nước nào cũng bị chiếu {'hết' if g == 'ch' else 'bí'}:</p>"
        tail = ''
    if n == 1:
        sol = (f"<p><strong>{'Solution' if lang == 'en' else 'Đáp án'}: 1. {esc(key)}{mark}</strong> " +
               (f"Only 1 of the {legal} legal moves delivers checkmate." if lang == 'en' else f"Chỉ có 1 trong {legal} nước đi hợp lệ chiếu {'hết' if g == 'ch' else 'bí'} ngay.") + '</p>')
    else:
        sol = first + rep + '<ul>' + ''.join(f"<li>1… {esc(mv(x, g, lang))} 2. {esc(mv(x['next'], g, lang))}{cont(x['next'], 2, g, lang)}</li>" for x in tree['replies']) + '</ul>'
    return (f"{head}\n\n{{{{img:pz-{p['id']}|{cap}}}}}\n\n"
            f"<details><summary>{hsum}</summary><p>{esc(hint(g, tree, lang))}</p></details>\n\n"
            f"<details><summary>{ssum}</summary>{sol}</details>\n")

# ───────────── trang ─────────────
G = {  # group → cấu hình
 'ch1': dict(game='ch', n=1, en='/chess/puzzles/mate-in-1/', vi='/vi/co-vua/chieu-het-1-nuoc/', order=31),
 'ch2': dict(game='ch', n=2, en='/chess/puzzles/mate-in-2/', vi='/vi/co-vua/chieu-het-2-nuoc/', order=32),
 'ch3': dict(game='ch', n=3, en='/chess/puzzles/mate-in-3/', vi='/vi/co-vua/chieu-het-3-nuoc/', order=33),
 'xq1': dict(game='xq', n=1, en='/xiangqi/puzzles/mate-in-1/', vi='/vi/co-tuong/chieu-bi-1-nuoc/', order=31),
 'xq2': dict(game='xq', n=2, en='/xiangqi/puzzles/mate-in-2/', vi='/vi/co-tuong/chieu-bi-2-nuoc/', order=32),
 'xq3': dict(game='xq', n=3, en='/xiangqi/puzzles/mate-in-3/', vi='/vi/co-tuong/chieu-bi-3-nuoc/', order=33),
}
HUB = {'ch': dict(en='/chess/puzzles/', vi='/vi/co-vua/bai-tap/'), 'xq': dict(en='/xiangqi/puzzles/', vi='/vi/co-tuong/bai-tap/')}

sys.path.insert(0, HERE)
from puzzle_text import TXT

def verify_para(g, lang, k, n):
    return TXT['verify'][lang][g].format(k=k, n=n)

def group_page(grp, res, lang):
    cfg = G[grp]; g, n = cfg['game'], cfg['n']
    ps = [p for p in puzzles() if p['group'] == grp]; k = len(ps)
    t = TXT['group'][lang][grp]
    other = 'vi' if lang == 'en' else 'en'
    side = 'game'
    fm = ['---', f"title: {t['title']}", f"crumb: {t['crumb']}", f"h1: {t['h1']}", f"description: {t['description']}", f"path: {cfg[lang]}",
          f"section: {'vi' if lang == 'vi' else ('chess' if g == 'ch' else 'xiangqi')}", f"order: {cfg['order'] + (0 if lang == 'en' else 20)}", f"alt: {other}={cfg[other]}"]
    if lang == 'vi' and g == 'ch': fm.append('game: chess')
    nxt = [G[x][lang] for x in G if G[x]['game'] == g and x != grp]
    fm.append('related: ' + ', '.join([HUB[g][lang]] + nxt[:2]))
    fm.append('faq:'); fm += [f"- {q} | {a}" for q, a in t['faq']]; fm.append('---')
    body = [t['intro'], '', '## ' + TXT['hdr'][lang]['how'], '', t['how'], '']
    for i, p in enumerate(ps, 1): body.append(puzzle_md(p, res[p['id']], i, lang))
    body += ['## ' + TXT['hdr'][lang]['checked'], '', verify_para(g, lang, k, n), '', '{{cta:%s}}' % ('chess' if g == 'ch' else 'xiangqi'), '', t['next']]
    return '\n'.join(fm) + '\n\n' + '\n'.join(body) + '\n'

def hub_page(g, lang):
    t = TXT['hub'][lang][g]; other = 'vi' if lang == 'en' else 'en'
    grps = [x for x in G if G[x]['game'] == g]
    fm = ['---', f"title: {t['title']}", f"crumb: {t['crumb']}", f"h1: {t['h1']}", f"description: {t['description']}", f"path: {HUB[g][lang]}",
          f"section: {'vi' if lang == 'vi' else ('chess' if g == 'ch' else 'xiangqi')}", f"order: {30 + (0 if lang == 'en' else 20)}", f"alt: {other}={HUB[g][other]}"]
    if lang == 'vi' and g == 'ch': fm.append('game: chess')
    fm.append('related: ' + ', '.join(G[x][lang] for x in grps))
    fm.append('faq:'); fm += [f"- {q} | {a}" for q, a in t['faq']]; fm.append('---')
    body = [t['intro'], '', '## ' + t['why_h'], '', t['why'], '', '## ' + TXT['hdr'][lang]['sets'], '']
    body += [f"- [{TXT['group'][lang][x]['h1']}]({G[x][lang]}): {TXT['group'][lang][x]['blurb']}" for x in grps]
    body += ['', '## ' + TXT['hdr'][lang]['method'], '', t['method'], '', '{{cta:%s}}' % ('chess' if g == 'ch' else 'xiangqi'), '', t['more']]
    return '\n'.join(fm) + '\n\n' + '\n'.join(body) + '\n'

def run():
    res = solve_all()
    out = {}
    for grp in G:
        for lang in ('en', 'vi'):
            out[G[grp][lang]] = group_page(grp, res, lang)
    for g in HUB:
        for lang in ('en', 'vi'): out[HUB[g][lang]] = hub_page(g, lang)
    for path, md in out.items():
        f = os.path.join(ROOT, 'content', 'gen', path.strip('/').replace('/', '__') + '.md')
        os.makedirs(os.path.dirname(f), exist_ok=True)
        if not os.path.exists(f) or open(f, encoding='utf-8').read() != md: open(f, 'w', encoding='utf-8').write(md)
    return out

if __name__ == '__main__':
    o = run(); print(f'OK: {len(o)} trang bài tập sinh từ solver')
