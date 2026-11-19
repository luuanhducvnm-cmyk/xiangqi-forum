// Dùng chính bộ luật của 2 game để tính nước đi hợp lệ / kiểm tra chiếu hết cho sơ đồ.
// Vào: JSON trên stdin  [{id, game:'xq'|'ch', fen, sq:'r,c'|'e4', want:'moves'|'status'}]  → ra JSON {id: ...}
import { readFileSync } from 'node:fs';
const root = new URL('../vendor/royal-games/', import.meta.url).pathname;
const xq = await import(root + 'xiangqi/public/js/rules.js');
const ch = await import(root + 'chess/public/js/chess.js');
const XQ = { r: 'R', n: 'H', b: 'E', a: 'A', k: 'K', c: 'C', p: 'P' };
function xqBoard(fen) {
  const rows = fen.split(' ')[0].split('/'), b = [];
  for (const row of rows) { const line = []; for (const ch of row) { if (/\d/.test(ch)) for (let i = 0; i < +ch; i++) line.push(null); else line.push((ch === ch.toUpperCase() ? 'r' : 'b') + XQ[ch.toLowerCase()]); } b.push(line); }
  return b; // hàng 0 = phía đen (trên), như FEN cờ tướng chuẩn
}
const input = JSON.parse(readFileSync(0, 'utf8')), out = {};
for (const q of input) {
  try {
    if (q.game === 'xq') {
      const b = xqBoard(q.fen), turn = (q.fen.split(' ')[1] || 'w') === 'w' ? 'r' : 'b';
      if (q.want === 'moves') { const [r, c] = q.sq.split(',').map(Number); out[q.id] = xq.getLegalMovesForSquare(b, r, c); }
      else { const n = xq.getAllLegalMoves(b, turn).length; out[q.id] = { legal: n, check: xq.isKingInCheck(b, turn), mate: n === 0 && xq.isKingInCheck(b, turn), stalemate: n === 0 && !xq.isKingInCheck(b, turn), turn }; }
    } else {
      const pos = ch.Position.fromFEN(q.fen);
      if (q.want === 'moves') { const f = ch.sqFrom(q.sq); out[q.id] = pos.legalMoves().filter(m => ch.mFrom(m) === f).map(m => ch.sqName(ch.mTo(m))); }
      else if (q.want === 'san') { const m = pos.parseUci(q.uci); out[q.id] = m ? pos.san(m) : null; }
      else { const ms = pos.legalMoves(); out[q.id] = { legal: ms.length, check: pos.inCheck(), status: pos.status(ms) }; }
    }
  } catch (e) { out[q.id] = { error: String(e) }; }
}
process.stdout.write(JSON.stringify(out));
