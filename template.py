"""HTML khung trang: nhẹ, không JS, CSS nhúng sẵn (không chặn hiển thị)."""
import os, re, json, html as _h

GAMES = {
    'xiangqi': dict(name='Xiangqi 3D', url='https://xiangqi3d.online', cta='Play Xiangqi 3D', blurb='Practice what you just read: play xiangqi in 3D against real players or the Royal AI, with a real two-button clock and an ELO rating.'),
    'chess': dict(name='Chess 3D', url='https://chess3d.online', cta='Play Chess 3D', blurb='Practice what you just read: play chess in 3D against real players or the Royal AI, with a real two-button clock and an ELO rating.'),
}
SECTIONS = {'xiangqi': 'Xiangqi', 'chess': 'Chess', 'news': 'News', 'play': 'Play online', 'site': 'About'}
BRAND = 'Xiangqi Forum'

# Chuỗi giao diện theo ngôn ngữ (en mặc định; trang dưới /vi/ dùng tiếng Việt)
T = {
 'en': dict(skip='Skip to content', tag='Chinese chess &amp; chess guides', nav=[('Xiangqi', '/xiangqi/'), ('Chess', '/chess/'), ('News', '/news/'), ('Play online', '/play/'), ('ELO ratings', '/elo-rating-explained/')],
            home='Home', allg='All guides in this section', faq='Frequently asked questions', keep='Keep learning', toc='On this page', upd='Updated', rd='min read',
            side='Play it in 3D', sidep='Free in your browser — no download.', ready='Ready to play?', real='Try it on a real board', locale='en_US', html='en',
            both='Both games are 3D, run in your browser (and install like an app on your phone), and use a real two-button clock — pick one:'),
 'vi': dict(skip='Bỏ qua, tới nội dung', tag='Cờ tướng &amp; cờ vua: hướng dẫn', nav=[('Cờ tướng', '/vi/co-tuong/'), ('Cờ vua', '/vi/co-vua/'), ('Tin tức', '/vi/tin-tuc/'), ('English', '/')],
            home='Trang chủ', allg='Tất cả bài hướng dẫn trong mục này', faq='Câu hỏi thường gặp', keep='Đọc tiếp', toc='Trong bài này', upd='Cập nhật', rd='phút đọc',
            side='Chơi thử trên bàn cờ 3D', sidep='Miễn phí ngay trên trình duyệt, không cần tải về.', ready='Sẵn sàng chơi chưa?', real='Thử ngay trên bàn cờ thật', locale='vi_VN', html='vi',
            both='Cả hai game đều là 3D, chạy ngay trên trình duyệt (cài lên điện thoại như một ứng dụng) và có đồng hồ hai nút như thật. Chọn một:'),
}
GAMES_VI = {
    'xiangqi': dict(cta='Chơi Cờ tướng 3D', blurb='Thực hành những gì bạn vừa đọc: chơi cờ tướng 3D với người thật hoặc với máy Royal AI, có đồng hồ hai nút như thật và bảng xếp hạng ELO.'),
    'chess': dict(cta='Chơi Cờ vua 3D', blurb='Thực hành những gì bạn vừa đọc: chơi cờ vua 3D với người thật hoặc với máy Royal AI, có đồng hồ hai nút như thật và bảng xếp hạng ELO.'),
}
def lang_of(p): return 'vi' if p['path'].startswith('/vi/') else 'en'
def game_of(p):
    """Game gắn với trang: front matter `game:` (trang /vi/), nếu không thì theo mục."""
    sec = p['section']
    if p.get('game') in GAMES: return p['game']
    return 'xiangqi' if sec in ('xiangqi', 'vi') else 'chess' if sec == 'chess' else None

def vurl(k): return GAMES[k]['url'] + '?lang=vi'  # trang tiếng Việt mở game ở giao diện tiếng Việt (người đọc đã chọn đọc tiếng Việt)

LOGO_SVG = '<svg class="logo" viewBox="0 0 40 40" width="34" height="34" aria-hidden="true"><circle cx="20" cy="20" r="18" fill="#f8ecd0" stroke="#b3261e" stroke-width="2.6"/><circle cx="20" cy="20" r="14.2" fill="none" stroke="#b3261e" stroke-width="1"/><text x="20" y="27.5" font-size="19" font-weight="700" text-anchor="middle" fill="#b3261e" font-family="\'Noto Serif CJK SC\',\'PingFang SC\',\'Microsoft YaHei\',serif">帥</text></svg>'
FAVICON_SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><circle cx="20" cy="20" r="19" fill="#f8ecd0" stroke="#b3261e" stroke-width="2.6"/><circle cx="20" cy="20" r="14.8" fill="none" stroke="#b3261e" stroke-width="1"/><text x="20" y="27.5" font-size="20" font-weight="700" text-anchor="middle" fill="#b3261e" font-family="\'Noto Serif CJK SC\',\'PingFang SC\',\'Microsoft YaHei\',serif">帥</text></svg>'

CSS = """
:root{--bg:#fbf7ef;--fg:#2a2017;--mut:#6d5b49;--line:#e6d9c5;--card:#fffdf8;--acc:#b3261e;--acc-fg:#fff;--jade:#1f6f4a;--note:#fff4dc;--code:#f3e9d7}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#17120d;--fg:#eee4d4;--mut:#b5a48f;--line:#3a2e22;--card:#201a13;--acc:#ef6b5f;--acc-fg:#1b0f0c;--jade:#5fc790;--note:#2c2214;--code:#2a2117}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.7 system-ui,-apple-system,"Segoe UI",Roboto,"Noto Sans",sans-serif}
a{color:var(--acc);text-underline-offset:3px}a:hover{text-decoration-thickness:2px}
.skip{position:absolute;left:-999px}.skip:focus{left:8px;top:8px;background:var(--card);padding:8px 12px;z-index:9}
.w{max-width:1120px;margin:0 auto;padding:0 18px}
.hd{border-bottom:1px solid var(--line);background:var(--card)}
.hd .w{display:flex;align-items:center;gap:18px;min-height:60px;flex-wrap:wrap;padding-top:6px;padding-bottom:6px}
.brand{display:flex;align-items:center;gap:10px;font:700 19px Georgia,"Iowan Old Style",serif;color:var(--fg);text-decoration:none}
.brand small{display:block;font:500 12px system-ui,sans-serif;color:var(--mut);letter-spacing:.02em}
nav{margin-left:auto;display:flex;gap:4px;flex-wrap:wrap}
nav a{color:var(--fg);text-decoration:none;padding:7px 12px;border-radius:8px;font-weight:600;font-size:15px}
nav a:hover,nav a[aria-current]{background:var(--code)}
.layout{display:grid;grid-template-columns:minmax(0,1fr);gap:36px;padding-top:26px;padding-bottom:50px}
@media(min-width:1020px){.layout{grid-template-columns:minmax(0,760px) 280px;justify-content:center}}
.crumbs{font-size:14px;color:var(--mut);margin-bottom:6px}.crumbs a{color:var(--mut)}
h1,h2,h3{font-family:Georgia,"Iowan Old Style","Noto Serif",serif;line-height:1.25;letter-spacing:-.01em}
h1{font-size:clamp(30px,5vw,42px);margin:.2em 0 .3em}
h2{font-size:28px;margin:1.9em 0 .5em;padding-top:.2em}h3{font-size:21px;margin:1.5em 0 .3em}
.meta{color:var(--mut);font-size:14px;margin:0 0 22px}
article p,article li{max-width:68ch}
article li{margin:.3em 0}
article>p:first-of-type{font-size:19px;color:var(--fg)}
code{background:var(--code);padding:1px 6px;border-radius:5px;font-size:.92em}
.note{background:var(--note);border-left:4px solid var(--acc);padding:12px 16px;border-radius:0 10px 10px 0;margin:1.3em 0;max-width:68ch}
.tw{overflow-x:auto;margin:1.2em 0}table{border-collapse:collapse;width:100%;font-size:15.5px}
th,td{border:1px solid var(--line);padding:8px 11px;text-align:left;vertical-align:top}th{background:var(--code)}
.dg{margin:1.4em 0;text-align:center}.dg img{max-width:100%;height:auto;border-radius:10px;box-shadow:0 2px 10px rgba(60,35,10,.18)}
.dg figcaption{font-size:14.5px;color:var(--mut);margin-top:8px}
.cta{background:linear-gradient(135deg,#3a1d12,#1c110b);color:#f6e8d4;border-radius:16px;padding:22px 22px 20px;margin:2.2em 0;border:1px solid #6a3a1f}
.cta h3{margin:.1em 0 .3em;color:#ffd98a;font-size:22px}.cta p{margin:.2em 0 .9em;color:#ecd9bd;max-width:60ch}
.btn{display:inline-block;background:#e0402f;color:#fff;font-weight:700;text-decoration:none;padding:11px 20px;border-radius:10px;margin:0 8px 8px 0}
.btn:hover{background:#c93223}.btn.alt{background:#f3dfb4;color:#2b1608}
.side{align-self:start}@media(min-width:1020px){.side{position:sticky;top:18px}}
.toc,.sidecta{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px;margin-bottom:16px;font-size:15px}
.toc b,.sidecta b{display:block;margin-bottom:6px;font-family:Georgia,serif;font-size:16px}
.toc ol{margin:0;padding-left:18px}.toc a{color:var(--fg);text-decoration:none}.toc a:hover{color:var(--acc)}
.toc li{margin:.25em 0}
.sidecta p{margin:.2em 0 .7em;color:var(--mut);font-size:14.5px}.sidecta .btn{margin:0 0 6px;padding:9px 14px;font-size:15px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px;margin:1.2em 0}
.card{display:block;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px;text-decoration:none;color:var(--fg)}
.card:hover{border-color:var(--acc);transform:translateY(-1px)}.card b{display:block;font-family:Georgia,serif;font-size:17px;margin-bottom:3px;color:var(--acc)}
.card span{font-size:14.5px;color:var(--mut);line-height:1.45;display:block}
details{border:1px solid var(--line);background:var(--card);border-radius:12px;padding:10px 16px;margin:.7em 0}
summary{cursor:pointer;font-weight:700}details p{margin:.6em 0 .2em}
.hero{padding:44px 0 22px}.hero h1{font-size:clamp(32px,6vw,52px);max-width:22ch}.hero p{font-size:20px;max-width:56ch;color:var(--mut)}
.two{display:grid;gap:16px;grid-template-columns:1fr}@media(min-width:760px){.two{grid-template-columns:1fr 1fr}}
.game{border-radius:18px;padding:24px;color:#f6e8d4;background:linear-gradient(140deg,#3a1d12,#150d08);border:1px solid #6a3a1f}
.game h2{margin:0 0 .2em;color:#ffd98a;font-size:26px;padding:0}.game p{color:#ecd9bd;margin:.3em 0 1em}
footer{border-top:1px solid var(--line);background:var(--card);padding:30px 0 40px;font-size:15px;color:var(--mut)}
footer .cols{display:grid;gap:22px;grid-template-columns:repeat(auto-fit,minmax(180px,1fr))}
footer b{color:var(--fg);display:block;margin-bottom:6px}footer a{color:var(--mut);display:block;padding:2px 0}
@media(max-width:560px){nav a{padding:6px 9px;font-size:14px}.hd .w{gap:6px}h2{font-size:25px}}
@media print{.hd,.side,footer,.cta{display:none}}
"""

def short(p): return p.get('crumb') or p['title']

def children(p, pages):
    base = p['path']; n = base.strip('/').count('/') + 2 if base != '/' else 1
    out = [c for c in pages if c['path'].startswith(base) and c['path'] != base and c['path'].strip('/').count('/') + 1 == n]
    return sorted(out, key=lambda c: (int(c['order']), c['path']))

def crumbs(p, pages):
    byp = {x['path']: x for x in pages}; segs = p['path'].strip('/').split('/'); out = [] if lang_of(p) == 'vi' else [(T['en']['home'], '/')]
    for i in range(1, len(segs)):
        pp = '/' + '/'.join(segs[:i]) + '/'
        if pp in byp: out.append((short(byp[pp]), pp))
    out.append((short(p), p['path'])); return out

def alt_links(p, site):
    return ''.join(f'<link rel="alternate" hreflang="{l}" href="{site}{u}">' for l, u in p.get('alts', []))

def og_for(p, site):
    slug = p['path'].strip('/').replace('/', '-') or 'home'
    f = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'og-cache', slug + '.png')
    return f'{site}/og/{slug}.png' if os.path.exists(f) else f'{site}/og/default.png' if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'og-cache', 'default.png')) else None

def head(title, desc, url, site, esc, og=None, typ='article', extra='', noindex=False, locale='en_US'):
    full = title if (title.endswith(BRAND) or len(title) + len(BRAND) + 3 > 62) else f'{title} | {BRAND}'
    h = ['<meta charset="utf-8">', '<meta name="viewport" content="width=device-width,initial-scale=1">',
         f'<title>{esc(full)}</title>', f'<meta name="description" content="{esc(desc)}">',
         f'<link rel="canonical" href="{url}">',
         '<meta name="robots" content="noindex,follow">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">',
         '<meta name="theme-color" content="#b3261e">', '<link rel="icon" href="/favicon-96.png" sizes="96x96" type="image/png">', '<link rel="icon" href="/favicon.svg" type="image/svg+xml">', '<link rel="apple-touch-icon" href="/apple-touch-icon.png">',
         '<link rel="alternate" type="application/atom+xml" href="/feed.xml" title="Xiangqi Forum">',
         f'<meta property="og:type" content="{typ}">', f'<meta property="og:site_name" content="{BRAND}">', f'<meta property="og:title" content="{esc(full)}">',
         f'<meta property="og:description" content="{esc(desc)}">', f'<meta property="og:url" content="{url}">', f'<meta property="og:locale" content="{locale}">']
    if og: h += [f'<meta property="og:image" content="{og}">', '<meta property="og:image:width" content="1200">', '<meta property="og:image:height" content="630">', '<meta name="twitter:card" content="summary_large_image">', f'<meta name="twitter:image" content="{og}">']
    else: h.append('<meta name="twitter:card" content="summary">')
    h += [f'<meta name="twitter:title" content="{esc(full)}">', f'<meta name="twitter:description" content="{esc(desc)}">', f'<style>{CSS}</style>', extra]
    return '\n'.join(h)

def ld(obj): return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + '</script>'

def header(cur=None, lang='en'):
    t = T[lang]; items = t['nav']
    nav = ''.join(f'<a href="{u}"' + (' aria-current="page"' if cur and u == cur else '') + f'>{n}</a>' for n, u in items)
    return f'<a class="skip" href="#main">{t["skip"]}</a><header class="hd"><div class="w"><a class="brand" href="/">{LOGO_SVG}<span>{BRAND}<small>{t["tag"]}</small></span></a><nav aria-label="Main">{nav}</nav></div></header>'

def footer(pages, lang='en'):
    if lang == 'vi': return footer_vi(pages)
    def col(title, sec, extra=()):
        ps = sorted([x for x in pages if x['section'] == sec and x['path'].strip('/').count('/') <= 1 and x.get('footer', '1') != '0'], key=lambda x: (int(x['order']), x['path']))
        return f'<div><b>{title}</b>' + ''.join(f'<a href="{x["path"]}">{_h.escape(short(x))}</a>' for x in ps) + ''.join(extra) + '</div>'
    g = ''.join(f'<a href="{v["url"]}">{v["name"]} ↗</a>' for v in GAMES.values())
    return (f'<footer><div class="w"><div class="cols">{col("Xiangqi guides", "xiangqi")}{col("Chess guides", "chess")}'
            f'<div><b>Play in 3D</b>{g}<a href="/play/">How the games work</a><a href="/elo-rating-explained/">ELO ratings explained</a></div>'
            f'<div><b>{BRAND}</b><a href="/news/">News</a><a href="/about/">About</a><a href="/privacy/">Privacy</a><a href="/sitemap/">Site map</a><a href="/vi/co-tuong/" hreflang="vi" lang="vi">Tiếng Việt</a><a href="/feed.xml">Atom feed</a></div></div>'
            f'<p style="margin-top:22px">© {BRAND} — independent learning resources for xiangqi and chess. Companion site to {GAMES["xiangqi"]["name"]} and {GAMES["chess"]["name"]}.</p></div></footer>')

def footer_vi(pages):
    def col(title, prefix):
        ps = sorted([x for x in pages if x['section'] == 'vi' and x['path'].startswith(prefix) and x['path'].strip('/').count('/') == 2 and x.get('footer', '1') != '0'], key=lambda x: (int(x['order']), x['path']))
        return f'<div><b>{title}</b>' + ''.join(f'<a href="{x["path"]}">{_h.escape(short(x))}</a>' for x in ps) + '</div>'
    g = ''.join(f'<a href="{vurl(k)}">{GAMES[k]["name"]} ↗</a>' for k in GAMES)
    return (f'<footer><div class="w"><div class="cols">{col("Học cờ tướng", "/vi/co-tuong/")}{col("Học cờ vua", "/vi/co-vua/")}'
            f'<div><b>Chơi game 3D</b>{g}<a href="/vi/choi-co-tuong-online/">Chơi cờ tướng online</a><a href="/vi/choi-co-vua-online/">Chơi cờ vua online</a><a href="/vi/tin-tuc/">Tin tức</a></div>'
            f'<div><b>{BRAND}</b><a href="/" hreflang="en" lang="en">English guides</a><a href="/about/" hreflang="en" lang="en">About</a><a href="/privacy/" hreflang="en" lang="en">Privacy</a></div></div>'
            f'<p style="margin-top:22px">© {BRAND}: tài liệu học cờ tướng và cờ vua độc lập, đồng hành cùng {GAMES["xiangqi"]["name"]} và {GAMES["chess"]["name"]}.</p></div></footer>')

def cta_box(which, h3=None, lang='en'):
    if lang == 'vi':
        t = T['vi']; keys = [which] if which in GAMES else list(GAMES)
        if len(keys) == 1:
            g = GAMES_VI[keys[0]]
            return f'<aside class="cta"><h3>{h3 or t["ready"]}</h3><p>{g["blurb"]}</p><a class="btn" href="{vurl(keys[0])}">{g["cta"]} →</a></aside>'
        return f'<aside class="cta"><h3>{h3 or t["ready"]}</h3><p>{t["both"]}</p>' + ''.join(f'<a class="btn{" alt" if i else ""}" href="{vurl(k)}">{GAMES_VI[k]["cta"]} →</a>' for i, k in enumerate(keys)) + '</aside>'
    keys = [which] if which in GAMES else list(GAMES)
    if len(keys) == 1:
        g = GAMES[keys[0]]
        return f'<aside class="cta"><h3>{h3 or "Ready to play?"}</h3><p>{g["blurb"]}</p><a class="btn" href="{g["url"]}">{g["cta"]} →</a></aside>'
    return ('<aside class="cta"><h3>' + (h3 or 'Ready to play?') + '</h3><p>Both games are 3D, run in your browser (and install like an app on your phone), and use a real two-button clock — pick one:</p>'
            + ''.join(f'<a class="btn{" alt" if i else ""}" href="{GAMES[k]["url"]}">{GAMES[k]["cta"]} →</a>' for i, k in enumerate(keys)) + '</aside>')

def sitemap_html(pages, esc):
    out = []
    for sec, label in (('xiangqi', 'Xiangqi'), ('chess', 'Chess'), ('news', 'News'), ('play', 'Play online'), ('site', 'About & reference')):
        ps = sorted([x for x in pages if x['section'] == sec and x['path'] != '/sitemap/'], key=lambda x: (x['path'].count('/'), int(x['order']), x['path']))
        out.append(f'<h2>{label}</h2><ul>' + ''.join(f'<li><a href="{x["path"]}">{esc(x["h1"])}</a></li>' for x in ps) + '</ul>')
    return ''.join(out)

def page_html(p, pages, site, today, esc, inline):
    url = site + p['path']; sec = p['section']; byp = {x['path']: x for x in pages}; lang = lang_of(p); t = T[lang]; vi = lang == 'vi'
    parts = []
    for x in p['parts']:
        if isinstance(x, tuple) and x[0] == 'SITEMAP': parts.append(sitemap_html(pages, esc))
        elif isinstance(x, tuple): parts.append(cta_box(x[1] or game_of(p) or 'both', t['real'], lang))
        else: parts.append(x)
    body = '\n'.join(parts)
    if p.get('hub') != '0':
        kids = children(p, pages)
        if kids and p.get('hub', '1') != '0':
            body += f'<h2 id="all-guides">{t["allg"]}</h2><div class="grid">' + ''.join(f'<a class="card" href="{k["path"]}"><b>{esc(short(k))}</b><span>{esc(k["description"])}</span></a>' for k in kids) + '</div>'
    faq_html = ''
    if p['faq']:
        faq_html = f'<h2 id="faq">{t["faq"]}</h2>' + ''.join(f'<details><summary>{esc(q)}</summary><p>{inline(a)}</p></details>' for q, a in p['faq'])
    rel = p['related'] or [x['path'] for x in sorted([x for x in pages if x['section'] == sec and x['path'] != p['path'] and x['path'].strip('/').count('/') >= 1], key=lambda x: (abs(int(x['order']) - int(p['order'])), x['path']))[:4]]
    rel_html = ''
    if rel and sec in ('xiangqi', 'chess', 'play', 'vi', 'news'):
        rel_html = f'<h2 id="keep-learning">{t["keep"]}</h2><div class="grid">' + ''.join(f'<a class="card" href="{r}"><b>{esc(short(byp[r]))}</b><span>{esc(byp[r]["description"])}</span></a>' for r in rel if r in byp) + '</div>'
    cta_end = '' if sec == 'site' else cta_box(game_of(p) or 'both', None, lang)
    toc_items = list(p['heads']) + ([('faq', t['faq'])] if p['faq'] else [])
    toc = ''
    if len(toc_items) >= 3:
        toc = f'<nav class="toc" aria-label="{t["toc"]}"><b>{t["toc"]}</b><ol>' + ''.join(f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in toc_items) + '</ol></nav>'
    key = game_of(p)
    side_cta = ''
    if sec != 'site':
        ks = [key] if key else list(GAMES)
        side_cta = f'<div class="sidecta"><b>{t["side"]}</b><p>{t["sidep"]}</p>' + ''.join(f'<a class="btn{" alt" if i else ""}" href="{vurl(k) if vi else GAMES[k]["url"]}">{(GAMES_VI if vi else GAMES)[k]["cta"]} →</a>' for i, k in enumerate(ks)) + '</div>'
    cr = crumbs(p, pages)
    crumb_html = '<div class="crumbs">' + ' › '.join(f'<a href="{u}">{esc(n)}</a>' if i < len(cr) - 1 else esc(n) for i, (n, u) in enumerate(cr)) + '</div>'
    mins = max(1, round(p['words'] / 210))
    other = dict(p.get('alts', [])).get('en' if vi else 'vi')
    langsw = (f' · <a href="{other}" hreflang="{"en" if vi else "vi"}" lang="{"en" if vi else "vi"}">{"Read in English" if vi else "Đọc bằng tiếng Việt"}</a>') if other else ''
    og = og_for(p, site)
    graph = [{'@type': 'NewsArticle' if (p['path'].startswith('/news/') or p['path'].startswith('/vi/tin-tuc/')) and p['path'] not in ('/news/', '/vi/tin-tuc/') else 'Article', 'headline': p['h1'], 'description': p['description'], 'mainEntityOfPage': url, 'inLanguage': t['html'],
              'datePublished': p.get('published', p['updated']), 'dateModified': p['updated'],
              'author': {'@type': 'Organization', 'name': BRAND, 'url': site + '/'}, 'publisher': {'@type': 'Organization', 'name': BRAND, 'url': site + '/'}}]
    if og: graph[0]['image'] = [og]
    graph.append({'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': site + u} for i, (n, u) in enumerate(cr)]})
    if p['faq']: graph.append({'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', a)}} for q, a in p['faq']]})
    if p.get('app') in GAMES:
        g = GAMES[p['app']]
        graph.append({'@type': 'SoftwareApplication', 'name': g['name'], 'url': g['url'], 'applicationCategory': 'GameApplication', 'operatingSystem': 'Any (web browser)', 'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'USD'}})
    ldj = ld({'@context': 'https://schema.org', '@graph': graph})
    return (f'<!doctype html><html lang="{t["html"]}"><head>{head(p["title"], p["description"], url, site, esc, og, "article", ldj + alt_links(p, site), locale=t["locale"])}</head><body>{header(("/" + "/".join(p["path"].strip("/").split("/")[:2]) + "/") if vi else ("/" + p["path"].strip("/").split("/")[0] + "/"), lang)}'
            f'<div class="w layout"><article id="main">{crumb_html}<h1>{esc(p["h1"])}</h1><p class="meta">{t["upd"]} {p["updated"]} · {mins} {t["rd"]}{langsw}</p>{body}{faq_html}{cta_end}{rel_html}</article>'
            f'<aside class="side">{toc}{side_cta}</aside></div>{footer(pages, lang)}</body></html>')

def home_html(pages, site, today, esc):
    byp = {x['path']: x for x in pages}
    def cards(paths): return '<div class="grid">' + ''.join(f'<a class="card" href="{r}"><b>{esc(short(byp[r]))}</b><span>{esc(byp[r]["description"])}</span></a>' for r in paths if r in byp) + '</div>'
    title = 'Xiangqi & Chess Guides: Rules, Openings, Tactics & ELO'
    desc = 'Free, plain-English guides to xiangqi (Chinese chess) and chess: rules, pieces, openings, tactics, checkmates, endgames and ELO — then play in 3D online.'
    og = og_for({'path': '/'}, site)
    graph = [{'@type': 'WebSite', 'name': BRAND, 'url': site + '/', 'description': desc, 'inLanguage': 'en'},
             {'@type': 'Organization', 'name': BRAND, 'url': site + '/'}]
    ldj = ld({'@context': 'https://schema.org', '@graph': graph})
    xq = ['/xiangqi/how-to-play/', '/xiangqi/rules/', '/xiangqi/pieces/', '/xiangqi/openings/', '/xiangqi/vs-chess/', '/xiangqi/checkmate-patterns/']
    ch = ['/chess/how-to-play/', '/chess/rules/', '/chess/openings/', '/chess/checkmates/', '/chess/time-controls/', '/chess/special-moves/']
    return (f'<!doctype html><html lang="en"><head>{head(title, desc, site + "/", site, esc, og, "website", ldj)}</head><body>{header()}'
            '<div class="w"><section class="hero"><h1>Learn xiangqi and chess — then play them in 3D.</h1><p>Clear rules, pieces, openings, tactics and checkmate patterns for <strong>xiangqi (Chinese chess)</strong> and <strong>chess</strong>, with diagrams checked by a real rules engine.</p>'
            f'<a class="btn" href="/xiangqi/how-to-play/">Learn xiangqi</a><a class="btn alt" href="/chess/how-to-play/">Learn chess</a></section>'
            '<div class="two">'
            f'<div class="game"><h2>{GAMES["xiangqi"]["name"]}</h2><p>Xiangqi on a real 3D board with a two-button clock, Royal AI, invite links and an ELO ladder.</p><a class="btn" href="{GAMES["xiangqi"]["url"]}">Play xiangqi online →</a></div>'
            f'<div class="game"><h2>{GAMES["chess"]["name"]}</h2><p>Chess in 3D with a real two-button clock, Royal AI, draw offers and rated matchmaking.</p><a class="btn" href="{GAMES["chess"]["url"]}">Play chess online →</a></div></div>'
            f'<h2 style="margin-top:1.6em">Xiangqi (Chinese chess) guides</h2>{cards(xq)}'
            f'<h2>Chess guides</h2>{cards(ch)}'
            f'<h2>News and puzzles</h2>{cards(["/news/world-chess-championship-2026/", "/news/lai-ly-huynh-world-xiangqi-champion/", "/chess/puzzles/", "/xiangqi/puzzles/"])}'
            f'<h2>Ratings and online play</h2>{cards(["/elo-rating-explained/", "/play/", "/play/with-friends/", "/play/vs-computer/"])}'
            '<h2>What is this site?</h2><p style="max-width:68ch">Xiangqi Forum is a free learning companion for two browser games, <a href="'
            f'{GAMES["xiangqi"]["url"]}">Xiangqi 3D</a> and <a href="{GAMES["chess"]["url"]}">Chess 3D</a>. Every guide is written to be useful on its own: if you only want to learn the rules, you never have to play. If you want to practise, one click puts you on a 3D board.</p></div>'
            f'{footer(pages)}</body></html>')

def notfound_html(site, esc):
    return (f'<!doctype html><html lang="en"><head>{head("Page not found", "This page does not exist.", site + "/", site, esc, None, "website", "", True)}</head><body>{header()}'
            '<div class="w"><section class="hero"><h1>That page doesn’t exist.</h1><p>Try one of the guides below.</p>'
            '<a class="btn" href="/xiangqi/">Xiangqi guides</a><a class="btn alt" href="/chess/">Chess guides</a></section></div></body></html>')
