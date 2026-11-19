#!/usr/bin/env python3
"""Trình tạo site tĩnh cho xiangqi.forum — không phụ thuộc thư viện ngoài (chỉ Python 3 + node để chạy engine kiểm chứng sơ đồ).
Chạy:  python3 build.py   →  dist/  (triển khai thư mục này lên Cloudflare)"""
import os, re, sys, json, html, shutil, datetime, hashlib
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools'))
import diagrams, specs, gen_pages
from template import page_html, home_html, notfound_html, CSS, LOGO_SVG, FAVICON_SVG

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT, DIST = os.path.join(ROOT, 'content'), os.path.join(ROOT, 'dist')
SITE = 'https://xiangqi.forum'
TODAY = os.environ.get('BUILD_DATE') or datetime.date.today().isoformat()
CJK_RE = re.compile(r'([㐀-鿿豈-﫿]+)')

def esc(s): return html.escape(s, quote=True)
def slugify(s):
    s = re.sub(r'<[^>]+>', '', s).lower(); s = re.sub(r'[^a-z0-9]+', '-', s).strip('-'); return s or 'section'

# ───────────── front matter ─────────────
def parse_file(path):
    raw = open(path, encoding='utf-8').read()
    m = re.match(r'---\n(.*?)\n---\n(.*)', raw, re.S)
    if not m: raise SystemExit(f'{path}: thiếu front matter')
    meta, faq, in_faq = {}, [], False
    for line in m.group(1).split('\n'):
        if in_faq and line.startswith('- '):
            q, _, a = line[2:].partition(' | ')
            if not a: raise SystemExit(f'{path}: faq phải có dạng "- hỏi | đáp"')
            faq.append((q.strip(), a.strip())); continue
        k, _, v = line.partition(':'); k = k.strip(); v = v.strip()
        if k == 'faq': in_faq = True; continue
        in_faq = False; meta[k] = v
    meta['faq'] = faq; meta['body'] = m.group(2).strip() + '\n'; meta['src'] = path
    for k in ('title', 'description', 'path', 'section'):
        if k not in meta: raise SystemExit(f'{path}: thiếu "{k}"')
    meta.setdefault('h1', meta['title']); meta.setdefault('order', '50'); meta.setdefault('updated', TODAY)
    meta['related'] = [x.strip() for x in meta.get('related', '').split(',') if x.strip()]
    return meta

# ───────────── markdown mini ─────────────
def inline(t):
    t = esc(t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<em>\1</em>', t)
    def link(m):
        txt, url = m.group(1), m.group(2).replace('&amp;', '&')
        ext = url.startswith('http')
        return f'<a href="{esc(url)}"' + (' rel="noopener"' if ext else '') + f'>{txt}</a>'
    t = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', link, t)
    parts = re.split(r'(<[^>]+>)', t)
    return ''.join(p if p.startswith('<') else CJK_RE.sub(r'<span lang="zh-Hans">\1</span>', p) for p in parts)

def render_body(md, ctx):
    out, heads, blocks = [], [], re.split(r'\n\s*\n', md.strip())
    for b in blocks:
        b = b.strip('\n')
        if not b: continue
        if b.startswith('## ') or b.startswith('### '):
            lvl = 2 if b.startswith('## ') else 3; txt = b[lvl + 1:].strip(); sid = slugify(txt)
            if lvl == 2: heads.append((sid, re.sub(r'\*', '', txt)))
            out.append(f'<h{lvl} id="{sid}">{inline(txt)}</h{lvl}>')
        elif b.startswith('{{img:'):
            m = re.match(r'\{\{img:([\w-]+)(?:\|(.*))?\}\}$', b)
            if not m: raise SystemExit(f'{ctx["src"]}: sai cú pháp {b[:40]}')
            k, cap = m.group(1), m.group(2)
            if k not in ctx['diag']: raise SystemExit(f'{ctx["src"]}: không có sơ đồ "{k}"')
            w, h, alt = ctx['diag'][k]; ctx['used'].add(k)
            if ctx.get('lang') == 'vi' and cap: alt = re.sub(r'[*`]', '', cap)
            lazy = ' loading="lazy" decoding="async"' if ctx['imgs'] else ''
            ctx['imgs'] += 1
            out.append(f'<figure class="dg"><img src="/img/{k}.svg" width="{w}" height="{h}" alt="{esc(alt)}"{lazy}>' + (f'<figcaption>{inline(cap)}</figcaption>' if cap else '') + '</figure>')
        elif b == '{{sitemap}}':
            out.append(('SITEMAP', None))
        elif b.startswith('{{cta'):
            m = re.match(r'\{\{cta(?::(\w+))?\}\}$', b); out.append(('CTA', m.group(1) if m else None))
        elif b.startswith('|'):
            rows = [r.strip() for r in b.split('\n') if r.strip().startswith('|')]
            cells = lambda r: [c.strip() for c in r.strip('|').split('|')]
            head = cells(rows[0]); body = [cells(r) for r in rows[2:]]
            t = '<div class="tw"><table><thead><tr>' + ''.join(f'<th>{inline(c)}</th>' for c in head) + '</tr></thead><tbody>'
            for r in body: t += '<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>'
            out.append(t + '</tbody></table></div>')
        elif re.match(r'(- |\d+\. )', b):
            ordered = bool(re.match(r'\d+\. ', b)); items = re.split(r'\n(?=(?:- |\d+\. ))', b)
            tag = 'ol' if ordered else 'ul'
            out.append(f'<{tag}>' + ''.join('<li>' + inline(re.sub(r'^(- |\d+\. )', '', i).replace('\n', ' ')) + '</li>' for i in items) + f'</{tag}>')
        elif b.startswith('> '):
            out.append('<aside class="note">' + inline(' '.join(l[2:] if l.startswith('> ') else l for l in b.split('\n'))) + '</aside>')
        elif b.startswith('<'):
            out.append(b)
        else:
            out.append('<p>' + inline(b.replace('\n', ' ')) + '</p>')
    return out, heads

def words(htmlstr): return len(re.findall(r'\w+', re.sub(r'<[^>]+>', ' ', htmlstr)))

# ───────────── build ─────────────
def main():
    gen_pages.run()   # trang bài tập: giải + kiểm chứng bằng solver (có cache), ghi content/gen/
    if os.path.exists(DIST): shutil.rmtree(DIST)
    os.makedirs(DIST)
    pages = []
    for dp, _, fs in os.walk(CONTENT):
        for f in sorted(fs):
            if f.endswith('.md'): pages.append(parse_file(os.path.join(dp, f)))
    paths = [p['path'] for p in pages]
    assert len(paths) == len(set(paths)), 'trùng path'
    diag = diagrams.build(specs.SPECS, os.path.join(DIST, 'img'))
    byp = {p['path']: p for p in pages}
    used_all, problems = set(), []
    for p in pages:
        ctx = {'src': p['src'], 'diag': diag, 'used': set(), 'imgs': 0, 'lang': 'vi' if p['path'].startswith('/vi/') else 'en'}
        parts, heads = render_body(p['body'], ctx)
        used_all |= ctx['used']
        p['parts'], p['heads'] = parts, heads
        p['words'] = sum(words(x) for x in parts if isinstance(x, str)) + sum(words(q + ' ' + a) for q, a in p['faq'])
        p['first_img'] = next((k for k in re.findall(r'\{\{img:([\w-]+)', p['body'])), None)
        for r in p['related']:
            if r not in byp: problems.append(f'{p["path"]}: related không tồn tại {r}')
    # hreflang: trang khai báo alt: en=/duong-dan/ → hai chiều tự động
    pairs = {}
    for p in pages:
        for item in [x.strip() for x in p.get('alt', '').split(',') if x.strip()]:
            l, _, u = item.partition('=')
            if u not in byp: problems.append(f'{p["path"]}: alt không tồn tại {u}')
            else: pairs.setdefault(p['path'], {})[l] = u; pairs.setdefault(u, {})['vi' if p['path'].startswith('/vi/') else 'en'] = p['path']
    for p in pages:
        if p['path'] in pairs:
            own = 'vi' if p['path'].startswith('/vi/') else 'en'
            al = [(own, p['path'])] + sorted(pairs[p['path']].items())
            p['alts'] = al + [('x-default', next(u for l, u in al if l == 'en'))] if any(l == 'en' for l, _ in al) else al
    # ghi trang
    for p in pages:
        d = os.path.join(DIST, p['path'].strip('/')); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(page_html(p, pages, SITE, TODAY, esc, inline))
    open(os.path.join(DIST, 'index.html'), 'w', encoding='utf-8').write(home_html(pages, SITE, TODAY, esc))
    open(os.path.join(DIST, '404.html'), 'w', encoding='utf-8').write(notfound_html(SITE, esc))
    # kiểm tra liên kết nội bộ
    valid = set(paths) | {'/'}
    for p in pages + [{'path': '/', 'body': '', 'parts': []}]:
        txt = p['body'] + ''.join(x for x in p['parts'] if isinstance(x, str))
        for u in re.findall(r'\]\((/[^)\s#]*)', p['body']) + re.findall(r'href="(/[^"#]*)"', ''.join(x for x in p['parts'] if isinstance(x, str))):
            if u not in valid and not u.startswith(('/img/', '/og/')) and not re.search(r'\.\w+$', u): problems.append(f'{p["path"]}: liên kết nội bộ hỏng {u}')
    # sơ đồ chưa dùng
    for k in diag:
        if k not in used_all and not k.startswith('og-'): problems.append(f'sơ đồ không dùng: {k}')
    # static files
    open(os.path.join(DIST, 'favicon.svg'), 'w').write(FAVICON_SVG)
    sm = ['<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    sm.append(f'<url><loc>{SITE}/</loc><lastmod>{TODAY}</lastmod></url>')
    for p in sorted(pages, key=lambda x: x['path']):
        sm.append(f'<url><loc>{SITE}{p["path"]}</loc><lastmod>{p["updated"]}</lastmod>' + ''.join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{SITE}{u}"/>' for l, u in p.get('alts', [])) + '</url>')
    sm.append('</urlset>\n'); open(os.path.join(DIST, 'sitemap.xml'), 'w').write('\n'.join(sm))
    open(os.path.join(DIST, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
    # feed
    ent = ''.join(f'<entry><title>{esc(p["title"])}</title><link href="{SITE}{p["path"]}"/><id>{SITE}{p["path"]}</id><updated>{p["updated"]}T00:00:00Z</updated><summary>{esc(p["description"])}</summary></entry>' for p in sorted(pages, key=lambda x: x['updated'], reverse=True)[:30])
    open(os.path.join(DIST, 'feed.xml'), 'w', encoding='utf-8').write(f'<?xml version="1.0" encoding="utf-8"?><feed xmlns="http://www.w3.org/2005/Atom"><title>Xiangqi Forum</title><link href="{SITE}/"/><link rel="self" href="{SITE}/feed.xml"/><id>{SITE}/</id><updated>{TODAY}T00:00:00Z</updated>{ent}</feed>')
    lt = ['# Xiangqi Forum', '', '> Free, plain-English guides to xiangqi (Chinese chess) and chess: rules, pieces, openings, tactics, checkmates, endgames and ELO ratings. Companion site to the 3D games Xiangqi 3D (https://xiangqi3d.online) and Chess 3D (https://chess3d.online).', '']
    for sec in ('xiangqi', 'chess', 'news', 'play', 'vi', 'site'):
        lt.append('## ' + {'vi': 'Tiếng Việt: cờ tướng & cờ vua'}.get(sec, sec.capitalize()))
        for p in sorted([x for x in pages if x['section'] == sec], key=lambda x: (int(x['order']), x['path'])): lt.append(f'- [{p["title"]}]({SITE}{p["path"]}): {p["description"]}')
        lt.append('')
    open(os.path.join(DIST, 'llms.txt'), 'w', encoding='utf-8').write('\n'.join(lt))
    for f in os.listdir(os.path.join(ROOT, 'static')): shutil.copy(os.path.join(ROOT, 'static', f), os.path.join(DIST, f))
    # ảnh OG (nếu đã sinh)
    ogdir = os.path.join(ROOT, 'og-cache')
    if os.path.isdir(ogdir):
        shutil.copytree(ogdir, os.path.join(DIST, 'og'))
        for f in ('apple-touch-icon.png', 'favicon-96.png'):
            if os.path.exists(os.path.join(ogdir, f)): shutil.move(os.path.join(DIST, 'og', f), os.path.join(DIST, f))
    tw = sum(p['words'] for p in pages)
    thin = [f'{p["path"]} ({p["words"]} từ)' for p in pages if p['words'] < 250 and p['section'] != 'site' and 'hub' not in p]
    print(f'OK: {len(pages)+1} trang, {tw} từ nội dung, {len(diag)} sơ đồ')
    if thin: print('CẢNH BÁO trang mỏng:', *thin, sep='\n  ')
    if problems: print('VẤN ĐỀ:', *problems, sep='\n  '); sys.exit(1)

if __name__ == '__main__':
    main()
