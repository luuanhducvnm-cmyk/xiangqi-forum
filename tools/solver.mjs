// Bộ giải "chiếu bí trong N nước" dùng ĐÚNG bộ luật của 2 game (vendor/royal-games/…/rules.js, chess.js — bản sao từ repo game).
// Mọi đáp án trên forum đều do file này chứng minh: key đầu tiên có DUY NHẤT hay không, và MỌI nước đỡ của đối phương đều bị chiếu bí.
//   node tools/solver.mjs  < [{id, game:'xq'|'ch', fen, maxN}]   →  JSON {id: {n, keys:[…], unique, tree…}}
import { readFileSync } from 'node:fs';
const root = new URL('../vendor/royal-games/', import.meta.url).pathname;
export const xq = await import(root + 'xiangqi/public/js/rules.js');
export const ch = await import(root + 'chess/public/js/chess.js');

/* ───────────────────────── cờ tướng ───────────────────────── */
const XQ = { r: 'R', n: 'H', b: 'E', a: 'A', k: 'K', c: 'C', p: 'P' };
export function xqBoard(fen) {
  return fen.split(' ')[0].split('/').map(row => { const l = []; for (const c of row) { if (/\d/.test(c)) for (let i = 0; i < +c; i++) l.push(null); else l.push((c === c.toUpperCase() ? 'r' : 'b') + XQ[c.toLowerCase()]); } return l; });
}
export const xqTurn = fen => (fen.split(' ')[1] || 'w') === 'w' ? 'r' : 'b';
const opp = s => s === 'r' ? 'b' : 'r';
const xqAfter = (b, m) => xq.boardAfter(b, m.from, m.to);

/* bên `att` (đang đến lượt) ép thắng trong ≤ n nước? strict=true: nước cuối PHẢI là chiếu bí (không tính hết nước đi mà không bị chiếu) */
export function xqMate(b, att, n, strict) {
  for (const m of xq.getAllLegalMoves(b, att)) if (xqWinAfter(b, att, m, n, strict)) return true;
  return false;
}
export function xqWinAfter(b, att, m, n, strict) {
  const def = opp(att), b2 = xqAfter(b, m);
  if (n === 1 || strict) { const chk = xq.isKingInCheck(b2, def); if (n === 1 && strict && !chk) return false; }
  const rep = xq.getAllLegalMoves(b2, def);
  if (!rep.length) return strict ? xq.isKingInCheck(b2, def) : true;
  if (n === 1) return false;
  for (const r of rep) if (!xqMate(xqAfter(b2, r), att, n - 1, strict)) return false;
  return true;
}
/* ký hiệu WXF (K A E H R C P; + tiến, - thoái, = bình). amb=true nếu có quân cùng loại cùng đường (cần "trước/sau") */
export function xqNote(b, m, side) {
  const [r, c] = m.from, [tr, tc] = m.to, t = b[r][c][1];
  const file = (cc) => side === 'r' ? 9 - cc : cc + 1;
  let amb = false, others = 0, front = true;
  for (let rr = 0; rr < 10; rr++) if (rr !== r && b[rr][c] === b[r][c]) { others++; amb = true; if (side === 'r' ? rr < r : rr > r) front = false; }
  const dr = tr - r, fwd = side === 'r' ? dr < 0 : dr > 0;
  const dir = dr === 0 ? '=' : fwd ? '+' : '-';
  const num = 'RCPK'.includes(t) ? (dr === 0 ? file(tc) : Math.abs(dr)) : file(tc);
  // hai quân cùng loại cùng đường: dùng "trước/sau" thay số đường (ghi 'front'/'rear'); từ 3 quân trở lên → amb3 (loại khỏi bài)
  const fr = amb ? (front ? 'front' : 'rear') : null;
  return { t, file: file(c), dir, num, amb, amb3: others > 1, fr, wxf: amb ? `${fr} ${t}${dir}${num}` : `${t}${file(c)}${dir}${num}` };
}
const xqKey = m => `${m.from}>${m.to}`;
export function xqTree(b, att, m, n) {
  const node = { note: xqNote(b, m, att), key: xqKey(m), replies: [], mate: false };
  const def = opp(att), b2 = xqAfter(b, m), rep = xq.getAllLegalMoves(b2, def);
  node.check = xq.isKingInCheck(b2, def);
  if (!rep.length) { node.mate = true; return node; }
  for (const r of rep) {
    const b3 = xqAfter(b2, r); let found = null, k = 0;
    for (k = 1; k <= n - 1 && !found; k++) {
      const ws = xq.getAllLegalMoves(b3, att).filter(w => xqWinAfter(b3, att, w, k, true));
      if (ws.length) found = { ws, k };
    }
    if (!found) throw new Error('cây lỗi: một nước đỡ không bị chiếu bí');
    const sub = xqTree(b3, att, found.ws[0], found.k);
    sub.alts = found.ws.length - 1;
    node.replies.push({ note: xqNote(b2, r, def), key: xqKey(r), len: found.k, next: sub, hitsFirst: !!(b2[r.to[0]][r.to[1]]) });
  }
  node.replies.sort((x, y) => y.len - x.len || x.note.wxf.localeCompare(y.note.wxf));
  return node;
}
export function solveXQ(fen, maxN) {
  const b = xqBoard(fen), att = xqTurn(fen), all = xq.getAllLegalMoves(b, att);
  if (xq.isKingInCheck(b, opp(att))) return { illegal: 'bên chờ đã bị chiếu' };
  for (let n = 1; n <= maxN; n++) {
    const keys = all.filter(m => xqWinAfter(b, att, m, n, false));
    if (!keys.length) continue;
    const strictKeys = keys.filter(m => xqWinAfter(b, att, m, n, true));
    return { n, keys: keys.map(m => xqNote(b, m, att).wxf), strictOk: strictKeys.length === keys.length, unique: keys.length === 1, tree: keys.length === 1 ? xqTree(b, att, keys[0], n) : null, legal: all.length, keyMove: keys[0] };
  }
  return { n: 0, keys: [] };
}

/* ───────────────────────── cờ vua ───────────────────────── */
export function chMate(pos, n) { for (const m of pos.legalMoves()) if (chWinAfter(pos, m, n)) return true; return false; }
export function chWinAfter(pos, m, n) {
  pos.make(m); let res;
  const rep = pos.legalMoves();
  if (!rep.length) res = pos.inCheck();
  else if (n === 1) res = false;
  else { res = true; for (const r of rep) { pos.make(r); const ok = chMate(pos, n - 1); pos.unmake(); if (!ok) { res = false; break; } } }
  pos.unmake(); return res;
}
export function chTree(pos, m, n) {
  const node = { san: pos.san(m), uci: pos.uci(m), replies: [], mate: false };
  pos.make(m); const rep = pos.legalMoves();
  if (!rep.length) { pos.unmake(); node.mate = true; return node; }
  for (const r of rep) {
    const rsan = pos.san(r), ruci = pos.uci(r); pos.make(r);
    let found = null;
    for (let k = 1; k <= n - 1 && !found; k++) { const ws = pos.legalMoves().filter(w => chWinAfter(pos, w, k)); if (ws.length) found = { ws, k }; }
    if (!found) throw new Error('cây lỗi');
    const sub = chTree(pos, found.ws[0], found.k); sub.alts = found.ws.length - 1;
    pos.unmake();
    node.replies.push({ san: rsan, uci: ruci, len: found.k, next: sub });
  }
  pos.unmake();
  node.replies.sort((x, y) => y.len - x.len || x.san.localeCompare(y.san));
  return node;
}
export function solveCH(fen, maxN) {
  const pos = ch.Position.fromFEN(fen);
  if (pos.attacked(pos.ksq[pos.side ^ 1], pos.side)) return { illegal: 'bên chờ đã bị chiếu' };
  const all = pos.legalMoves();
  for (let n = 1; n <= maxN; n++) {
    const keys = all.filter(m => chWinAfter(pos, m, n));
    if (!keys.length) continue;
    return { n, keys: keys.map(m => pos.san(m)), unique: keys.length === 1, strictOk: true, tree: keys.length === 1 ? chTree(pos, keys[0], n) : null, legal: all.length, keyMove: keys[0] };
  }
  return { n: 0, keys: [] };
}

/* ───────────────────────── CLI ───────────────────────── */
if (process.argv[1] && process.argv[1].endsWith('solver.mjs')) {
  const input = JSON.parse(readFileSync(0, 'utf8')), out = {};
  for (const q of input) {
    const t0 = Date.now(); const r = (q.game === 'xq' ? solveXQ : solveCH)(q.fen, q.maxN || 3);
    delete r.keyMove; r.ms = Date.now() - t0; out[q.id] = r;
  }
  process.stdout.write(JSON.stringify(out));
}
