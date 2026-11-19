#!/usr/bin/env python3
"""Sinh ảnh chia sẻ 1200×630 (Open Graph) cho từng trang + favicon PNG. Cần Playwright/Chromium. Kết quả → og-cache/ (build.py sẽ copy vào dist/og)."""
import os, sys, re, asyncio, html, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT); sys.path.insert(0, HERE)
from playwright.async_api import async_playwright
import build
OUT = os.path.join(ROOT, 'og-cache'); os.makedirs(OUT, exist_ok=True)
THEME = {'xiangqi': ('#b3261e', '#3a1d12', '帥', 'XIANGQI · CHINESE CHESS'), 'chess': ('#1f6f4a', '#12261c', '♞', 'CHESS'), 'play': ('#e0402f', '#2a140c', '3D', 'PLAY ONLINE'), 'news': ('#1d4f8a', '#101c2e', 'N', 'NEWS'), 'site': ('#8a5a1c', '#2a1d0c', '帥', 'XIANGQI FORUM'), 'vi': ('#b3261e', '#3a1d12', '象', 'CỜ TƯỚNG · XIANGQI')}
def card(title, sec, sub):
    acc, bg, glyph, label = THEME[sec]
    size = 74 if len(title) < 34 else 62 if len(title) < 52 else 52
    return f'''<!doctype html><meta charset=utf-8><style>
*{{box-sizing:border-box}}body{{margin:0;width:1200px;height:630px;background:linear-gradient(135deg,{bg},#0e0805);color:#f6e8d4;font-family:"Noto Serif CJK SC",Georgia,serif;position:relative;overflow:hidden}}
.bar{{position:absolute;left:0;top:0;bottom:0;width:18px;background:{acc}}}
.lab{{position:absolute;left:80px;top:64px;font:700 26px system-ui,sans-serif;letter-spacing:.14em;color:#ffd98a}}
h1{{position:absolute;left:80px;top:150px;width:760px;margin:0;font-size:{size}px;line-height:1.12;font-weight:800}}
.sub{{position:absolute;left:80px;bottom:64px;width:760px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font:500 30px system-ui,sans-serif;color:#d9c3a3}}
.g{{position:absolute;right:70px;top:120px;width:300px;height:300px;border-radius:50%;background:#f8ecd0;border:12px solid {acc};display:flex;align-items:center;justify-content:center;font-size:{190 if len(glyph)==1 else 120}px;font-weight:800;color:{acc};box-shadow:0 18px 60px rgba(0,0,0,.5)}}
.dom{{position:absolute;right:70px;top:60px;font:700 34px system-ui,sans-serif;color:#ffd98a}}
</style><div class=bar></div><div class=lab>{html.escape(label)}</div><h1>{html.escape(title)}</h1><div class=sub>{html.escape(sub)}</div><div class=g>{glyph}</div><div class=dom>xiangqi.forum</div>'''
async def main():
    pages = []
    for dp, _, fs in os.walk(build.CONTENT):
        for f in sorted(fs):
            if f.endswith('.md'): pages.append(build.parse_file(os.path.join(dp, f)))
    items = [('home', 'Learn xiangqi & chess — then play in 3D', 'site', 'Rules · openings · tactics · ELO')] + [(p['path'].strip('/').replace('/', '-'), p['h1'], p['section'], p['description'][:70].rsplit(' ', 1)[0] + '…') for p in pages]
    items.append(('default', 'Xiangqi & Chess Guides', 'site', 'Free guides · play in 3D'))
    async with async_playwright() as pw:
        b = await pw.chromium.launch(); pg = await b.new_page(viewport={'width': 1200, 'height': 630})
        for slug, title, sec, sub in items:
            await pg.set_content(card(title, sec, sub)); await pg.wait_for_timeout(60)
            await pg.screenshot(path=os.path.join(OUT, slug + '.png'), type='png')
        # favicon PNG
        pg2 = await b.new_page(viewport={'width': 180, 'height': 180})
        from template import FAVICON_SVG
        await pg2.set_content(f'<body style="margin:0;background:transparent">{FAVICON_SVG.replace("<svg ", "<svg width=180 height=180 ")}</body>')
        await pg2.screenshot(path=os.path.join(OUT, 'apple-touch-icon.png'), omit_background=True)
        pg3 = await b.new_page(viewport={'width': 96, 'height': 96})
        await pg3.set_content(f'<body style="margin:0;background:transparent">{FAVICON_SVG.replace("<svg ", "<svg width=96 height=96 ")}</body>')
        await pg3.screenshot(path=os.path.join(OUT, 'favicon-96.png'), omit_background=True)
        await b.close()
    print(len(items), 'ảnh OG →', OUT)
asyncio.run(main())
