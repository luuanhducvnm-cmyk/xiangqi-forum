// Bảng tàn cuộc "vét cạn" (retrograde) cho Vua+Hậu / Vua+Xe / Vua+Tốt đấu Vua, tính bằng ĐÚNG bộ luật của Chess 3D.
// Dùng để kiểm chứng mọi khẳng định về tàn cuộc trong bài viết (số nước chiếu hết tối đa, thế đối diện, ô chìa khoá…).
//   import { build, query } from './tablebase.mjs'   hoặc   node tools/tablebase.mjs  → in số liệu tổng hợp
import { ch } from './solver.mjs';
const { Position, sqName, sqFrom } = ch;
const N = 64, IDX = (wk, bk, p, stm) => ((wk * N + bk) * N + p) * 2 + stm;

function setup(pos, wk, bk, p, kind, stm) {
  pos.b.fill(0); pos.b[wk] = 6; pos.b[bk] = 14; pos.b[p] = kind;     // kind: 1 tốt, 4 xe, 5 hậu (trắng)
  pos.ksq = [wk, bk]; pos.side = stm; pos.castle = 0; pos.ep = -1; pos.half = 0; pos.undo = []; pos.keys1 = []; pos.keys2 = [];
}
const adj = (a, b) => Math.abs((a >> 3) - (b >> 3)) <= 1 && Math.abs((a & 7) - (b & 7)) <= 1;

/* trả về {dtm: Int16Array (-1 = không thắng), kind} ; dtm tính theo NỬA nước (ply) kể từ thế đó */
export function build(kind, queenTable) {
  const pos = new Position(), size = N * N * N * 2;
  const dtm = new Int16Array(size).fill(-1), legal = new Uint8Array(size), start = new Int32Array(size + 1), nextArr = [];
  const lo = kind === 1 ? 8 : 0, hi = kind === 1 ? 55 : 63;
  // 1) liệt kê thế hợp lệ + chuyển trạng thái
  for (let wk = 0; wk < 64; wk++) for (let bk = 0; bk < 64; bk++) {
    if (wk === bk || adj(wk, bk)) continue;
    for (let p = lo; p <= hi; p++) {
      if (p === wk || p === bk) continue;
      for (let stm = 0; stm < 2; stm++) {
        const id = IDX(wk, bk, p, stm);
        setup(pos, wk, bk, p, kind, stm);
        if (stm === 0 && pos.attacked(bk, 0)) continue;            // đen không thể đang bị chiếu khi đến lượt trắng
        if (stm === 1 && pos.attacked(wk, 1)) continue;
        legal[id] = 1;
      }
    }
  }
  const trans = new Array(size);   // mảng con; -1 = hoà (ăn quân), -2-… = phong cấp (giá trị dtm hậu cố định)
  for (let id = 0; id < size; id++) {
    if (!legal[id]) continue;
    const stm = id & 1, rest = id >> 1, p = rest % N, bk = ((rest / N) | 0) % N, wk = ((rest / N / N) | 0);
    setup(pos, wk, bk, p, kind, stm);
    const out = [];
    for (const m of pos.legalMoves()) {
      const f = m & 63, t = (m >> 6) & 63, pr = (m >> 12) & 7;
      let nwk = wk, nbk = bk, np = p;
      if (f === wk) nwk = t; else if (f === bk) { nbk = t; if (t === p) { out.push(-1); continue; } } else if (f === p) { np = t; }
      if (stm === 0 && f === p && pr) { // phong cấp: chỉ xét Hậu (theo lý thuyết, phong cấp thấp không đổi kết quả KPK) — tra bảng KQK
        if (pr === 5) out.push({ q: IDX(nwk, nbk, np, 1) }); else out.push(-9);
        continue;
      }
      out.push(IDX(nwk, nbk, np, stm ^ 1));
    }
    trans[id] = out;
  }
  // 2) retrograde
  let changed = true, ply = 0;
  const queenDtm = id => queenTable ? queenTable[id] : -1;
  for (let id = 0; id < size; id++) if (legal[id] && (id & 1) === 1 && trans[id].length === 0) {
    const rest = id >> 1, bk = ((rest / N) | 0) % N, wk = ((rest / N / N) | 0);
    setup(pos, wk, bk, rest % N, kind, 1); if (pos.inCheck()) dtm[id] = 0;
  }
  while (changed && ply < 400) {
    ply++; changed = false;
    for (let id = 0; id < size; id++) {
      if (!legal[id] || dtm[id] >= 0) continue;
      const tr = trans[id];
      if ((id & 1) === 0) {            // trắng đi: cần một nước dẫn tới thế đen thua với dtm = ply-1
        for (const t of tr) { const v = typeof t === 'object' ? queenDtm(t.q) : t >= 0 ? dtm[t] : -1; if (v === ply - 1) { dtm[id] = ply; changed = true; break; } }
      } else if (tr.length) {          // đen đi: mọi nước đều dẫn tới thế trắng thắng, tối đa = ply-1
        let mx = -1, ok = true;
        for (const t of tr) { const v = t >= 0 ? dtm[t] : -1; if (v < 0) { ok = false; break; } if (v > mx) mx = v; }
        if (ok && mx === ply - 1) { dtm[id] = ply; changed = true; }
      }
    }
    if (!changed && ply < 400) { // có thể còn thế thắng dài hơn sau 1 vòng không đổi (do phong cấp) – chạy thêm vài vòng
      let more = false; for (let id = 0; id < size && !more; id++) if (legal[id] && dtm[id] < 0 && (id & 1) === 0) for (const t of trans[id]) if (typeof t === 'object' && queenDtm(t.q) >= ply) more = true;
      if (more) changed = true;
    }
  }
  return { dtm, legal, kind };
}
export const sqs = { wk: s => sqFrom(s) };
/* tra một FEN dạng "K+X vs K" → {win:bool, dtm: số NƯỚC (không phải ply) trắng cần để chiếu hết nếu trắng đi trước} */
export function query(tb, fen) {
  const pos = Position.fromFEN(fen); let wk = -1, bk = -1, p = -1;
  for (let s = 0; s < 64; s++) { const v = pos.b[s]; if (!v) continue; if (v === 6) wk = s; else if (v === 14) bk = s; else p = s; }
  const id = IDX(wk, bk, p, pos.side), d = tb.dtm[id];
  return { legal: !!tb.legal[id], win: d >= 0, plies: d, moves: d < 0 ? null : Math.ceil(d / 2) };
}
export function worst(tb) { // thế (trắng đi) lâu nhất
  let best = -1, bid = -1;
  for (let id = 0; id < tb.dtm.length; id += 2) if (tb.dtm[id] > best) { best = tb.dtm[id]; bid = id; }
  return { plies: best, moves: Math.ceil(best / 2), fen: idFen(tb, bid) };
}
export function idFen(tb, id) {
  const stm = id & 1, rest = id >> 1, p = rest % N, bk = ((rest / N) | 0) % N, wk = ((rest / N / N) | 0);
  const g = Array(64).fill(''); g[wk] = 'K'; g[bk] = 'k'; g[p] = { 1: 'P', 4: 'R', 5: 'Q' }[tb.kind];
  let f = ''; for (let r = 7; r >= 0; r--) { let e = 0; for (let c = 0; c < 8; c++) { const x = g[r * 8 + c]; if (!x) e++; else { if (e) { f += e; e = 0; } f += x; } } if (e) f += e; if (r) f += '/'; }
  return `${f} ${stm ? 'b' : 'w'} - - 0 1`;
}

if (process.argv[1] && process.argv[1].endsWith('tablebase.mjs')) {
  const t0 = Date.now();
  const Q = build(5); const wq = worst(Q);
  console.log('KQK: số nước chiếu hết TỐI ĐA =', wq.moves, '| thế:', wq.fen, `(${Date.now() - t0} ms)`);
  const R = build(4); const wr = worst(R);
  console.log('KRK: số nước chiếu hết TỐI ĐA =', wr.moves, '| thế:', wr.fen);
  const P = build(1, Q.dtm); let wins = 0, tot = 0;
  for (let id = 0; id < P.dtm.length; id += 2) if (P.legal[id]) { tot++; if (P.dtm[id] >= 0) wins++; }
  console.log('KPK: trắng đi, thế hợp lệ =', tot, ', thắng =', wins, `(${Date.now() - t0} ms)`);
}
