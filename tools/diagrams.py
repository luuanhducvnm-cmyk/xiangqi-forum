"""Sơ đồ bàn cờ SVG (cờ tướng + cờ vua) cho bài viết.
Nước đi 'chấm xanh' được TÍNH BẰNG ĐÚNG ENGINE LUẬT CỦA 2 GAME (tools/engine.mjs) — không vẽ tay,
và mọi thế chiếu hết / hết nước đi được engine xác nhận khi build (assert)."""
import json, subprocess, os, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# ───────────────────────── gọi engine ─────────────────────────
def run_engine(queries):
    if not queries: return {}
    p = subprocess.run(['node', os.path.join(HERE, 'engine.mjs')], input=json.dumps(queries), capture_output=True, text=True, timeout=120)
    if p.returncode: raise SystemExit('engine lỗi: ' + p.stderr[:500])
    return json.loads(p.stdout)

# ───────────────────────── cờ tướng ─────────────────────────
XQ_RED = {'r': '俥', 'n': '傌', 'b': '相', 'a': '仕', 'k': '帥', 'c': '炮', 'p': '兵'}
XQ_BLK = {'r': '車', 'n': '馬', 'b': '象', 'a': '士', 'k': '將', 'c': '砲', 'p': '卒'}
CJK = "'Noto Serif CJK SC','Noto Sans CJK SC','PingFang SC','Microsoft YaHei','SimSun',serif"
CN_NUM = '九八七六五四三二一'

def xq_parse(fen):
    rows = fen.split(' ')[0].split('/'); out = {}
    for r, row in enumerate(rows):
        c = 0
        for ch in row:
            if ch.isdigit(): c += int(ch)
            else: out[(r, c)] = ch; c += 1
    return out

def xq_svg(spec, marks):
    S, M, MT, MB = 52, 36, 48, 48
    W, H = 8 * S + 2 * M, 9 * S + MT + MB
    X = lambda c: M + c * S
    Y = lambda r: MT + r * S
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" font-family="{CJK}">',
         f'<title>{html.escape(spec["alt"])}</title>',
         f'<rect width="{W}" height="{H}" rx="10" fill="#ecc98a"/>',
         f'<rect x="{M-10}" y="{MT-10}" width="{8*S+20}" height="{9*S+20}" fill="none" stroke="#7a4a1d" stroke-width="3"/>',
         '<g stroke="#5a3514" stroke-width="1.6" fill="none">']
    for r in range(10): o.append(f'<path d="M{X(0)} {Y(r)}H{X(8)}"/>')
    o.append(f'<path d="M{X(0)} {Y(0)}V{Y(9)}M{X(8)} {Y(0)}V{Y(9)}"/>')
    for c in range(1, 8): o.append(f'<path d="M{X(c)} {Y(0)}V{Y(4)}M{X(c)} {Y(5)}V{Y(9)}"/>')
    for r0 in (0, 7):
        o.append(f'<path d="M{X(3)} {Y(r0)}L{X(5)} {Y(r0+2)}M{X(5)} {Y(r0)}L{X(3)} {Y(r0+2)}"/>')
    o.append('</g>')
    o.append(f'<text x="{X(2)}" y="{(Y(4)+Y(5))/2+9}" font-size="24" text-anchor="middle" fill="#5a3514" opacity=".75" letter-spacing="6">楚河</text>')
    o.append(f'<text x="{X(6)}" y="{(Y(4)+Y(5))/2+9}" font-size="24" text-anchor="middle" fill="#5a3514" opacity=".75" letter-spacing="6">漢界</text>')
    if spec.get('files', True):
        for c in range(9):
            o.append(f'<text x="{X(c)}" y="{MT-31}" font-size="14" text-anchor="middle" fill="#5a3514">{c+1}</text>')
            o.append(f'<text x="{X(c)}" y="{H-12}" font-size="15" text-anchor="middle" fill="#8a1f16">{CN_NUM[c]}</text>')
    for (r, c) in spec.get('hl', []):
        o.append(f'<rect x="{X(c)-S/2+3}" y="{Y(r)-S/2+3}" width="{S-6}" height="{S-6}" rx="6" fill="#ffd54a" opacity=".45"/>')
    pcs = xq_parse(spec['fen'])
    for (r, c), ch in pcs.items():
        red = ch.isupper(); g = (XQ_RED if red else XQ_BLK)[ch.lower()]; col = '#b3261e' if red else '#1c1c1c'
        o.append(f'<g><circle cx="{X(c)}" cy="{Y(r)}" r="22.5" fill="#f8ecd0" stroke="{col}" stroke-width="2.4"/><circle cx="{X(c)}" cy="{Y(r)}" r="18" fill="none" stroke="{col}" stroke-width="1"/>'
                 f'<text x="{X(c)}" y="{Y(r)+9.5}" font-size="27" font-weight="700" text-anchor="middle" fill="{col}">{g}</text></g>')
    for (r, c, kind) in marks:
        if kind == 'cap': o.append(f'<circle cx="{X(c)}" cy="{Y(r)}" r="26" fill="none" stroke="#d6281c" stroke-width="3.5" stroke-dasharray="5 3"/>')
        else: o.append(f'<circle cx="{X(c)}" cy="{Y(r)}" r="8" fill="#1f8f55" opacity=".85"/>')
    for (a, b) in spec.get('arrows', []): o.append(arrow(X(a[1]), Y(a[0]), X(b[1]), Y(b[0])))
    o.append('</svg>')
    return W, H, ''.join(o)

# ───────────────────────── cờ vua ─────────────────────────
CH_GLYPH = {'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'}
SYM = "'Segoe UI Symbol','Noto Sans Symbols 2','DejaVu Sans','Apple Symbols',sans-serif"

def ch_parse(fen):
    out = {}
    for r, row in enumerate(fen.split(' ')[0].split('/')):   # r=0 là hạng 8
        c = 0
        for ch in row:
            if ch.isdigit(): c += int(ch)
            else: out[(r, c)] = ch; c += 1
    return out

def sq_rc(sq): return (8 - int(sq[1]), ord(sq[0]) - 97)

def ch_svg(spec, marks):
    S, ML, MT = 56, 30, 12
    W, H = 8 * S + ML + MT, 8 * S + ML + MT
    X = lambda c: ML + c * S
    Y = lambda r: MT + r * S
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" font-family="{SYM}">',
         f'<title>{html.escape(spec["alt"])}</title>', f'<rect width="{W}" height="{H}" rx="10" fill="#3b2a1a"/>']
    for r in range(8):
        for c in range(8):
            o.append(f'<rect x="{X(c)}" y="{Y(r)}" width="{S}" height="{S}" fill="{"#f0d9b5" if (r+c)%2==0 else "#b58863"}"/>')
    for (r, c) in [sq_rc(s) for s in spec.get('hl', [])]:
        o.append(f'<rect x="{X(c)}" y="{Y(r)}" width="{S}" height="{S}" fill="#ffd54a" opacity=".5"/>')
    for i in range(8):
        o.append(f'<text x="{X(i)+S/2}" y="{H-10}" font-size="14" text-anchor="middle" fill="#e8d3b0" font-family="sans-serif">{"abcdefgh"[i]}</text>')
        o.append(f'<text x="{ML-12}" y="{Y(i)+S/2+5}" font-size="14" text-anchor="middle" fill="#e8d3b0" font-family="sans-serif">{8-i}</text>')
    for (r, c), ch in ch_parse(spec['fen']).items():
        white = ch.isupper(); g = CH_GLYPH[ch.lower()] + '︎'
        if white: st = 'fill="#fffdf6" stroke="#1a1209" stroke-width="2.2" paint-order="stroke" stroke-linejoin="round"'
        else: st = 'fill="#17110b" stroke="#17110b"'
        o.append(f'<text x="{X(c)+S/2}" y="{Y(r)+S/2+17}" font-size="50" text-anchor="middle" {st}>{g}</text>')
    for (r, c, kind) in marks:
        if kind == 'cap': o.append(f'<circle cx="{X(c)+S/2}" cy="{Y(r)+S/2}" r="24" fill="none" stroke="#d6281c" stroke-width="4"/>')
        else: o.append(f'<circle cx="{X(c)+S/2}" cy="{Y(r)+S/2}" r="9" fill="#1f8f55" opacity=".8"/>')
    for (a, b) in spec.get('arrows', []):
        (ra, ca), (rb, cb) = sq_rc(a), sq_rc(b)
        o.append(arrow(X(ca) + S/2, Y(ra) + S/2, X(cb) + S/2, Y(rb) + S/2))
    o.append('</svg>')
    return W, H, ''.join(o)

def arrow(x1, y1, x2, y2):
    import math
    dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy) or 1; ux, uy = dx / L, dy / L
    ex, ey = x2 - ux * 18, y2 - uy * 18
    hx1, hy1 = x2 - ux * 18 - uy * 9, y2 - uy * 18 + ux * 9
    hx2, hy2 = x2 - ux * 18 + uy * 9, y2 - uy * 18 - ux * 9
    return (f'<g opacity=".9" stroke="#e07b00" fill="#e07b00"><path d="M{x1+ux*14:.1f} {y1+uy*14:.1f}L{ex:.1f} {ey:.1f}" stroke-width="6" stroke-linecap="round"/>'
            f'<path d="M{x2:.1f} {y2:.1f}L{hx1:.1f} {hy1:.1f}L{hx2:.1f} {hy2:.1f}Z" stroke="none"/></g>')

# ───────────────────────── dựng tất cả ─────────────────────────
def build(specs, outdir):
    """specs: {id: {game, fen, alt, from?, hl?, arrows?, expect?}} → ghi svg, trả {id: (w,h,alt)}"""
    q = []
    for k, s in specs.items():
        if s.get('from'): q.append({'id': k + ':m', 'game': s['game'], 'fen': s['fen'], 'sq': s['from'], 'want': 'moves'})
        if s.get('expect'): q.append({'id': k + ':s', 'game': s['game'], 'fen': s['fen'], 'want': 'status'})
    res = run_engine(q)
    os.makedirs(outdir, exist_ok=True); meta = {}
    for k, s in specs.items():
        marks = []
        if s.get('from'):
            dest = res[k + ':m']
            if s['game'] == 'xq':
                pcs = xq_parse(s['fen'])
                for r, c in dest: marks.append((r, c, 'cap' if (r, c) in pcs else 'dot'))
            else:
                pcs = ch_parse(s['fen'])
                for sq in dest:
                    r, c = sq_rc(sq); marks.append((r, c, 'cap' if (r, c) in pcs else 'dot'))
        if s.get('expect'):
            st = res[k + ':s']; e = s['expect']
            if e == 'mate': ok = (st.get('mate') if s['game'] == 'xq' else (st['status'] or {}).get('reason') == 'checkmate')
            elif e == 'check': ok = st['check']
            elif e == 'stalemate': ok = (st.get('stalemate') if s['game'] == 'xq' else (st['status'] or {}).get('reason') == 'stalemate')
            else: ok = True
            assert ok, f'sơ đồ {k}: engine KHÔNG xác nhận "{e}": {st}'
        w, h, svg = (xq_svg if s['game'] == 'xq' else ch_svg)(s, marks)
        open(os.path.join(outdir, k + '.svg'), 'w', encoding='utf-8').write(svg)
        meta[k] = (w, h, s['alt'])
    return meta
