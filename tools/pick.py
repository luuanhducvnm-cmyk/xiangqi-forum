#!/usr/bin/env python3
"""Chọn thế cờ từ ứng viên (đã được solver chứng minh) → tools/puzzles.json. Chọn xác định (không ngẫu nhiên) theo độ đa dạng quân chiếu."""
import json, sys, re
C = sys.argv[1] if len(sys.argv) > 1 else '/tmp/t/c'
def load(f):
    out = []
    for l in open(f'{C}/{f}.jsonl'):
        try: out.append(json.loads(l))
        except Exception: pass
    return out
def walk(t):
    yield t
    for r in t.get('replies', []):
        yield r; yield from walk(r['next'])
def amb3(x):
    return any(n.get('note', {}).get('amb3') or n.get('next', {}).get('note', {}).get('amb3') for n in walk(x['tree']) if isinstance(n, dict)) if x['game'] == 'xq' else False
def kind(x):
    k = x['key']
    if x['game'] == 'ch': return k[0] if k[0] in 'KQRBN' else 'P'
    return k.split()[-1][0]
def pick(items, want, flt, count):
    out, seen = [], set(); items = [x for x in items if flt(x)]
    seen_fen = set()
    for w in want:
        for x in items:
            if x['fen'] in seen_fen: continue
            if w == '*' or kind(x) == w:
                out.append(x); seen_fen.add(x['fen']); break
        if len(out) >= count: break
    for x in items:
        if len(out) >= count: break
        if x['fen'] not in seen_fen: out.append(x); seen_fen.add(x['fen'])
    return out
res = []
def add(group, game, n, xs):
    for i, x in enumerate(xs, 1): res.append(dict(id=f'{group}-{i}', game=game, n=n, fen=x['fen'], group=group))
rank8 = lambda x: 'k' in x['fen'].split('/')[0]
add('ch1', 'ch', 1, pick(load('ch1'), ['Q', 'R', 'B', 'N', 'P', 'R'], lambda x: 6 <= x['pieces'] <= 10 and rank8(x) and x['legal'] >= 12, 6))
add('ch2', 'ch', 2, pick(load('ch2'), ['R', 'Q', 'K', 'B', 'N', 'P', 'R', 'Q'], lambda x: not x['check'] and not x['capture'] and x['replies'] >= 2 and 6 <= x['pieces'] <= 11, 8))
add('ch3', 'ch', 3, pick(load('ch3'), ['Q', 'R', 'K', 'B', 'N', 'P'], lambda x: not x['check'] and x['replies'] >= 2 and 6 <= x['pieces'] <= 12, 6))
add('xq1', 'xq', 1, pick(load('xq1'), ['R', 'C', 'H', 'P', 'R', 'C'], lambda x: x['pieces'] >= 8 and not amb3(x), 6))
add('xq2', 'xq', 2, pick(load('xq2'), ['R', 'H', 'C', 'P', 'K', 'R', 'H', 'C'], lambda x: not x['check'] and x['replies'] >= 2 and not amb3(x), 8))
add('xq3', 'xq', 3, pick(load('xq3'), ['R', 'H', 'C', 'P', 'K', 'R'], lambda x: x['replies'] >= 2 and not amb3(x), 6))
json.dump(res, open('puzzles.json', 'w'), indent=1)
import collections; print(collections.Counter(r['group'] for r in res))
