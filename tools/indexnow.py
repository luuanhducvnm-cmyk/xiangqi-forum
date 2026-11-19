#!/usr/bin/env python3
"""Báo cho Bing/Yandex/Seznam... (IndexNow) biết URL mới/đổi ngay lập tức. Chạy SAU khi deploy:  python3 tools/indexnow.py
(Google không dùng IndexNow — với Google hãy gửi sitemap trong Search Console.)"""
import os, glob, json, re, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = 'xiangqi.forum'
keyfile = [f for f in glob.glob(os.path.join(ROOT, 'static', '*.txt')) if re.fullmatch(r'[0-9a-f]{32}', os.path.basename(f)[:-4])][0]
key = os.path.basename(keyfile)[:-4]
urls = re.findall(r'<loc>(.*?)</loc>', open(os.path.join(ROOT, 'dist', 'sitemap.xml')).read())
body = json.dumps({'host': HOST, 'key': key, 'keyLocation': f'https://{HOST}/{key}.txt', 'urlList': urls}).encode()
req = urllib.request.Request('https://api.indexnow.org/IndexNow', body, {'Content-Type': 'application/json; charset=utf-8'})
try:
    with urllib.request.urlopen(req, timeout=30) as r: print('IndexNow:', r.status, f'({len(urls)} URL)')
except Exception as e: print('Lỗi IndexNow (đã deploy chưa? domain đã trỏ đúng chưa?):', e)
