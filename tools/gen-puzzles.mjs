// Sinh ứng viên thế cờ "chiếu bí trong N nước" rồi lọc bằng solver (key duy nhất, mọi nước đỡ đều bị chiếu bí).
//   node tools/gen-puzzles.mjs xq 2 <số_giây> <seed>   → in JSON-lines các ứng viên
import { xq, ch, xqBoard, solveXQ, solveCH, xqMate, xqWinAfter } from './solver.mjs';
const [game, N, secs, seed0] = [process.argv[2], +process.argv[3], +process.argv[4] || 60, +process.argv[5] || 1];
let seed = seed0 * 2654435761 >>> 0 || 1;
const rnd = () => { seed ^= seed << 13; seed >>>= 0; seed ^= seed >>> 17; seed ^= seed << 5; seed >>>= 0; return seed / 4294967296; };
const ri = n => Math.floor(rnd() * n), pick = a => a[ri(a.length)];
const shuffle = a => { for (let i = a.length - 1; i > 0; i--) { const j = ri(i + 1); [a[i], a[j]] = [a[j], a[i]]; } return a; };

/* ───── cờ tướng ───── */
const PAL = [[0, 3], [0, 5], [1, 4], [2, 3], [2, 5]], ELE_B = [[0, 2], [0, 6], [2, 0], [2, 4], [2, 8], [4, 2], [4, 6]];
const KB = [[0, 3], [0, 4], [0, 5], [1, 3], [1, 4], [1, 5], [2, 3], [2, 4], [2, 5]];
const flipR = ([r, c]) => [9 - r, c];
function xqRandom() {
  const g = Array.from({ length: 10 }, () => Array(9).fill(null)), used = new Set();
  const put = (p, [r, c]) => { if (used.has(r * 9 + c)) return false; used.add(r * 9 + c); g[r][c] = p; return true; };
  put('bK', pick(KB));
  for (const a of shuffle(PAL.slice()).slice(0, ri(3))) put('bA', a);
  for (const e of shuffle(ELE_B.slice()).slice(0, ri(3))) put('bE', e);
  if (rnd() < 0.5) for (let i = 0, n = 1 + ri(2); i < n; i++) put('bP', pick([[3, 0], [3, 2], [3, 4], [3, 6], [3, 8], [4, 0], [4, 2], [4, 4], [4, 6], [4, 8], [5, 1], [5, 4], [6, 3], [6, 7]]));
  if (rnd() < 0.35) put(pick(['bR', 'bC', 'bH']), [ri(10), ri(9)]);
  // đỏ
  let ok = false; for (let t = 0; t < 30 && !ok; t++) { const k = flipR(pick(KB)); ok = put('rK', k); }
  if (!ok) return null;
  const pool = shuffle(['rR', 'rR', 'rH', 'rH', 'rC', 'rC', 'rP', 'rP', 'rA', 'rE']).slice(0, N === 1 ? 2 + ri(3) : 3 + ri(3));
  for (const p of pool) {
    for (let t = 0; t < 20; t++) {
      let sq;
      if (p === 'rP') sq = pick([[0, 4], [1, 3], [1, 5], [2, 4], [3, 2], [3, 6], [4, 0], [4, 8], [4, 4], [3, 4], [2, 2], [2, 6], [1, 4], [3, 3], [3, 5], [5, 2], [5, 6], [6, 4], [4, 1], [4, 7]]);
      else if (p === 'rA') sq = pick([[7, 3], [7, 5], [8, 4], [9, 3], [9, 5]]);
      else if (p === 'rE') sq = pick([[9, 2], [9, 6], [7, 0], [7, 4], [7, 8], [5, 2], [5, 6]]);
      else sq = [ri(10), ri(9)];
      if (put(p, sq)) break;
    }
  }
  return g;
}
function gridFen(g) { return g.map(row => { let s = '', e = 0; for (const x of row) { if (!x) e++; else { if (e) { s += e; e = 0; } const l = { K: 'k', A: 'a', E: 'b', H: 'n', R: 'r', C: 'c', P: 'p' }[x[1]]; s += x[0] === 'r' ? l.toUpperCase() : l; } } return s + (e || ''); }).join('/') + ' w'; }
function xqOk(g) {
  if (xq.isKingInCheck(g, 'r') || xq.isKingInCheck(g, 'b')) return false;       // không bên nào đang bị chiếu (đỏ đi trước)
  if (xq.getAllLegalMoves(g, 'b').length === 0) return false;
  return true;
}

/* ───── cờ vua ───── */
function chRandom() {
  const g = Array(64).fill(''); const used = new Set();
  const put = (c, sq) => { if (used.has(sq)) return false; used.add(sq); g[sq] = c; return true; };
  const pawnSq = () => 8 + ri(48);
  let bk; do { bk = rnd() < 0.7 ? (7 * 8 + ri(8)) : ri(64); } while (!put('k', bk));
  let wk; for (let t = 0; t < 40; t++) { wk = ri(64); if (Math.abs((wk >> 3) - (bk >> 3)) > 1 || Math.abs((wk & 7) - (bk & 7)) > 1) if (put('K', wk)) break; }
  const wn = N === 1 ? 2 + ri(3) : 2 + ri(3), W = shuffle(['Q', 'R', 'R', 'B', 'B', 'N', 'N', 'P', 'P', 'P']).slice(0, wn);
  for (const p of W) for (let t = 0; t < 20; t++) if (put(p, p === 'P' ? pawnSq() : ri(64))) break;
  const bn = ri(5), B = shuffle(['q', 'r', 'r', 'b', 'n', 'p', 'p', 'p', 'p']).slice(0, bn);
  for (const p of B) for (let t = 0; t < 20; t++) if (put(p, p === 'p' ? pawnSq() : ri(64))) break;
  // vua đen thường có tốt che
  if (bk >> 3 === 7 && rnd() < 0.7) for (const f of [bk - 1, bk, bk + 1]) { const s = f - 8; if ((f >> 3) === 7 && (f & 7) === (f & 7) && s >= 0 && rnd() < 0.7) put('p', s); }
  let fen = ''; for (let r = 7; r >= 0; r--) { let e = 0; for (let f = 0; f < 8; f++) { const x = g[r * 8 + f]; if (!x) e++; else { if (e) { fen += e; e = 0; } fen += x; } } if (e) fen += e; if (r) fen += '/'; }
  return fen + ' w - - 0 1';
}

/* ───── vòng lặp ───── */
const t0 = Date.now(); let tried = 0, found = 0;
while (Date.now() - t0 < secs * 1000) {
  tried++;
  try {
    if (game === 'xq') {
      const g = xqRandom(); if (!g || !xqOk(g)) continue;
      const fen = gridFen(g);
      // tiền lọc: không có chiếu bí ≤ N-1 (solveXQ tự kiểm); với N=3 chỉ thử khi tồn tại chuỗi chiếu liên tục (rẻ)
      if (N === 3 && !checksOnly(g, 'r', 3)) continue;
      const r = solveXQ(fen, N);
      if (r.n !== N || !r.unique || !r.strictOk) continue;
      const k = r.keyMove, b2 = xq.boardAfter(g, k.from, k.to);
      found++; console.log(JSON.stringify({ game, fen, n: r.n, key: r.keys[0], legal: r.legal, check: xq.isKingInCheck(b2, 'b'), capture: !!g[k.to[0]][k.to[1]], replies: xq.getAllLegalMoves(b2, 'b').length, pieces: g.flat().filter(Boolean).length, tree: r.tree }));
    } else {
      const fen = chRandom(); let r;
      try { r = solveCH(fen, N); } catch (e) { continue; }
      if (r.illegal || r.n !== N || !r.unique) continue;
      const pos = ch.Position.fromFEN(fen); const k = r.keyMove; const cap = !!pos.b[(k >> 6) & 63]; pos.make(k);
      found++; console.log(JSON.stringify({ game, fen, n: r.n, key: r.keys[0], legal: r.legal, check: pos.inCheck(), capture: cap, replies: pos.legalMoves().length, pieces: fen.split(' ')[0].replace(/[\d/]/g, '').length, tree: r.tree }));
    }
  } catch (e) { /* vị trí lỗi → bỏ */ }
}
console.error(`thử ${tried}, nhận ${found}`);

/* chỉ xét các nước CHIẾU của bên tấn công (nhanh) để tiền lọc N=3 */
function checksOnly(b, att, n) {
  const def = att === 'r' ? 'b' : 'r';
  for (const m of xq.getAllLegalMoves(b, att)) {
    const b2 = xq.boardAfter(b, m.from, m.to);
    if (!xq.isKingInCheck(b2, def)) continue;
    const rep = xq.getAllLegalMoves(b2, def);
    if (!rep.length) return true;
    if (n === 1) continue;
    if (rep.every(r => checksOnly(xq.boardAfter(b2, r.from, r.to), att, n - 1))) return true;
  }
  return false;
}
