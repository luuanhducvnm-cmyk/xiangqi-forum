// Dựng thế cờ từ một danh sách nước đi (SAN cờ vua / WXF cờ tướng), KIỂM TRA từng nước hợp lệ bằng bộ luật thật, trả về FEN.
//   vào: [{id, game:'ch'|'xq', moves:['e4','e5',…]}]   ra: {id:{fen, ok, status?, material?}}  (nước sai → ok:false + lý do, build sẽ dừng)
import { readFileSync } from 'node:fs';
import { xq, ch, xqBoard, xqNote } from './solver.mjs';
const out = {};
const XL = { K: 'k', A: 'a', E: 'b', H: 'n', R: 'r', C: 'c', P: 'p' };
const xqFen = (b, turn) => b.map(row => { let s = '', e = 0; for (const x of row) { if (!x) e++; else { if (e) { s += e; e = 0; } const l = XL[x[1]]; s += x[0] === 'r' ? l.toUpperCase() : l; } } return s + (e || ''); }).join('/') + ' ' + (turn === 'r' ? 'w' : 'b');
for (const q of JSON.parse(readFileSync(0, 'utf8'))) {
  try {
    if (q.game === 'ch') {
      const pos = ch.Position.fromFEN(q.start || ch.START_FEN);
      for (const tok of q.moves) {
        const bare = tok.replace(/[+#!?]/g, '');
        const m = pos.legalMoves().find(x => pos.san(x).replace(/[+#]/g, '') === bare);
        if (!m) throw new Error(`nước không hợp lệ: ${tok} (tại ${pos.toFEN()})`);
        if (/[+#]$/.test(tok.replace(/[!?]+$/, '')) && !pos.san(m).endsWith(tok.replace(/[!?]+$/, '').slice(-1))) throw new Error(`dấu chiếu/chiếu hết sai: ${tok} → ${pos.san(m)}`);
        pos.make(m);
      }
      const val = { 1: 1, 2: 3, 3: 3, 4: 5, 5: 9 }; const mat = [0, 0];
      for (let s = 0; s < 64; s++) { const v = pos.b[s]; if (v && (v & 7) !== 6) mat[v >> 3] += val[v & 7]; }
      out[q.id] = { ok: true, fen: pos.toFEN(), status: pos.status(), material: { white: mat[0], black: mat[1] } };
    } else {
      let b = xqBoard(q.start || 'rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w'), turn = 'r';
      for (const tok of q.moves) {
        const m = xq.getAllLegalMoves(b, turn).find(x => xqNote(b, x, turn).wxf === tok);
        if (!m) throw new Error(`nước không hợp lệ: ${tok}`);
        b = xq.boardAfter(b, m.from, m.to); turn = turn === 'r' ? 'b' : 'r';
      }
      out[q.id] = { ok: true, fen: xqFen(b, turn), check: xq.isKingInCheck(b, turn) };
    }
  } catch (e) { out[q.id] = { ok: false, error: String(e.message || e) }; }
}
process.stdout.write(JSON.stringify(out));
