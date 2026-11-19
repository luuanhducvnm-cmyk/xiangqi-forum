/* Royal Chess — bộ luật cờ vua đầy đủ (dùng chung: trình duyệt, Web Worker AI, Cloudflare Worker).
 *
 * Quy ước:
 *  · Ô: sq = rank*8 + file, a1 = 0 … h8 = 63. Rank 0 = hàng 1 (Trắng).
 *  · Quân: 0 trống; Trắng 1..6 = P N B R Q K; Đen 9..14 (bit 8 = màu).
 *  · Nước đi: số nguyên  from | to<<6 | promo<<12   (promo = loại quân 2..5, 0 = không).
 *  · Trắng = màu 0, Đen = màu 1.
 */
export const P = 1, N = 2, B = 3, R = 4, Q = 5, K = 6;
export const WHITE = 0, BLACK = 1;
export const START_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1';
export const typeOf = p => p & 7;
export const colorOf = p => p >> 3;
export const mkPiece = (color, type) => (color << 3) | type;
export const sqName = s => 'abcdefgh'[s & 7] + ((s >> 3) + 1);
export const sqFrom = n => (n.charCodeAt(0) - 97) + (n.charCodeAt(1) - 49) * 8;
export const mFrom = m => m & 63, mTo = m => (m >> 6) & 63, mPromo = m => (m >> 12) & 7;
export const mkMove = (f, t, pr = 0) => f | (t << 6) | (pr << 12);
export const moveUci = m => sqName(mFrom(m)) + sqName(mTo(m)) + (mPromo(m) ? 'nbrq'[mPromo(m) - 2] : '');
const PCH = '.PNBRQK..pnbrqk';

/* ── bảng tra trước ── */
const KN = [], KG = [], RAYS = [];       // RAYS[sq] = [[các ô theo hướng],…] (8 hướng: 0-3 thẳng, 4-7 chéo)
const DIRS = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]];
for (let s = 0; s < 64; s++) {
  const f = s & 7, r = s >> 3; KN[s] = []; KG[s] = []; RAYS[s] = [];
  for (const [df, dr] of [[1, 2], [2, 1], [-1, 2], [-2, 1], [1, -2], [2, -1], [-1, -2], [-2, -1]]) { const nf = f + df, nr = r + dr; if (nf >= 0 && nf < 8 && nr >= 0 && nr < 8) KN[s].push(nr * 8 + nf); }
  for (const [df, dr] of DIRS) {
    const nf = f + df, nr = r + dr; if (nf >= 0 && nf < 8 && nr >= 0 && nr < 8) KG[s].push(nr * 8 + nf);
    const ray = []; let a = f + df, b = r + dr; while (a >= 0 && a < 8 && b >= 0 && b < 8) { ray.push(b * 8 + a); a += df; b += dr; } RAYS[s].push(ray);
  }
}
/* quyền nhập thành mất khi quân đi/bị ăn tại các ô này */
const CASTLE_MASK = new Int8Array(64).fill(15);
CASTLE_MASK[0] = 15 & ~2; CASTLE_MASK[7] = 15 & ~1; CASTLE_MASK[4] = 15 & ~3;
CASTLE_MASK[56] = 15 & ~8; CASTLE_MASK[63] = 15 & ~4; CASTLE_MASK[60] = 15 & ~12;

/* ── Zobrist 2×32 bit (PRNG xác định để các bản Swift/Kotlin cho đúng cùng giá trị) ── */
let seed = 0x9E3779B9 | 0;
const rnd = () => { seed ^= seed << 13; seed ^= seed >>> 17; seed ^= seed << 5; return seed | 0; };
const ZP1 = new Int32Array(16 * 64), ZP2 = new Int32Array(16 * 64), ZC1 = new Int32Array(16), ZC2 = new Int32Array(16), ZE1 = new Int32Array(8), ZE2 = new Int32Array(8);
for (let i = 0; i < ZP1.length; i++) { ZP1[i] = rnd(); ZP2[i] = rnd(); }
for (let i = 0; i < 16; i++) { ZC1[i] = rnd(); ZC2[i] = rnd(); }
for (let i = 0; i < 8; i++) { ZE1[i] = rnd(); ZE2[i] = rnd(); }
const ZS1 = rnd(), ZS2 = rnd();

export class Position {
  constructor() {
    this.b = new Int8Array(64); this.side = 0; this.castle = 0; this.ep = -1; this.half = 0; this.full = 1;
    this.ksq = [4, 60]; this.h1 = 0; this.h2 = 0; this.undo = []; this.keys1 = []; this.keys2 = [];
  }
  static start() { return Position.fromFEN(START_FEN); }
  static fromFEN(fen) {
    const p = new Position(), parts = fen.trim().split(/\s+/);
    let r = 7, f = 0;
    for (const ch of parts[0]) {
      if (ch === '/') { r--; f = 0; } else if (ch >= '1' && ch <= '8') f += +ch;
      else { const i = PCH.indexOf(ch); if (i < 1) throw new Error('FEN lỗi'); p.b[r * 8 + f] = i; if ((i & 7) === K) p.ksq[i >> 3] = r * 8 + f; f++; }
    }
    p.side = parts[1] === 'b' ? 1 : 0;
    for (const ch of parts[2] || '-') p.castle |= ch === 'K' ? 1 : ch === 'Q' ? 2 : ch === 'k' ? 4 : ch === 'q' ? 8 : 0;
    p.ep = parts[3] && parts[3] !== '-' ? sqFrom(parts[3]) : -1;
    p.half = +parts[4] || 0; p.full = +parts[5] || 1;
    p.computeHash(); p.keys1.push(p.h1); p.keys2.push(p.h2);
    return p;
  }
  toFEN() {
    let s = '';
    for (let r = 7; r >= 0; r--) { let e = 0; for (let f = 0; f < 8; f++) { const v = this.b[r * 8 + f]; if (!v) e++; else { if (e) { s += e; e = 0; } s += PCH[v]; } } if (e) s += e; if (r) s += '/'; }
    const c = (this.castle & 1 ? 'K' : '') + (this.castle & 2 ? 'Q' : '') + (this.castle & 4 ? 'k' : '') + (this.castle & 8 ? 'q' : '');
    return `${s} ${this.side ? 'b' : 'w'} ${c || '-'} ${this.ep >= 0 ? sqName(this.ep) : '-'} ${this.half} ${this.full}`;
  }
  clone() { const p = Position.fromFEN(this.toFEN()); return p; }
  /* ep chỉ tính vào băm khi bên đi có thể bắt (đúng luật lặp thế) */
  epHashFile() {
    if (this.ep < 0) return -1;
    const me = this.side, f = this.ep & 7, rr = me ? 3 : 4, pawn = mkPiece(me, P);
    return ((f > 0 && this.b[rr * 8 + f - 1] === pawn) || (f < 7 && this.b[rr * 8 + f + 1] === pawn)) ? f : -1;
  }
  computeHash() {
    let a = 0, b = 0;
    for (let s = 0; s < 64; s++) { const v = this.b[s]; if (v) { a ^= ZP1[v * 64 + s]; b ^= ZP2[v * 64 + s]; } }
    if (this.side) { a ^= ZS1; b ^= ZS2; }
    a ^= ZC1[this.castle]; b ^= ZC2[this.castle];
    const ef = this.epHashFile(); if (ef >= 0) { a ^= ZE1[ef]; b ^= ZE2[ef]; }
    this.h1 = a; this.h2 = b;
  }

  /* ô `sq` có bị bên `by` tấn công không */
  attacked(sq, by) {
    const b = this.b, f = sq & 7, r = sq >> 3, o = by << 3;
    // tốt
    if (by === 0) { if (r > 0) { if (f > 0 && b[sq - 9] === (o | P)) return true; if (f < 7 && b[sq - 7] === (o | P)) return true; } }
    else if (r < 7) { if (f > 0 && b[sq + 7] === (o | P)) return true; if (f < 7 && b[sq + 9] === (o | P)) return true; }
    for (const t of KN[sq]) if (b[t] === (o | N)) return true;
    for (const t of KG[sq]) if (b[t] === (o | K)) return true;
    const rays = RAYS[sq];
    for (let d = 0; d < 8; d++) {
      const ray = rays[d];
      for (let i = 0; i < ray.length; i++) {
        const v = b[ray[i]]; if (!v) continue;
        if ((v >> 3) === by) { const t = v & 7; if (t === Q || (d < 4 ? t === R : t === B)) return true; }
        break;
      }
    }
    return false;
  }
  inCheck(side = this.side) { return this.attacked(this.ksq[side], side ^ 1); }

  /* sinh nước giả-hợp lệ (chưa kiểm tra vua có bị chiếu sau nước đi); capsOnly = chỉ nước ăn quân/phong cấp */
  gen(capsOnly = false) {
    const out = [], b = this.b, me = this.side, o = me << 3, enemy = me ^ 1;
    const pushPromo = (f, t) => { out.push(f | (t << 6) | (5 << 12), f | (t << 6) | (4 << 12), f | (t << 6) | (3 << 12), f | (t << 6) | (2 << 12)); };
    for (let s = 0; s < 64; s++) {
      const v = b[s]; if (!v || (v >> 3) !== me) continue;
      const t = v & 7;
      if (t === P) {
        const dir = me ? -8 : 8, startR = me ? 6 : 1, promoR = me ? 1 : 6, f = s & 7, r = s >> 3;
        const one = s + dir;
        if (!b[one]) {
          if (r === promoR) pushPromo(s, one);
          else if (!capsOnly) { out.push(s | (one << 6)); if (r === startR && !b[one + dir]) out.push(s | ((one + dir) << 6)); }
        }
        for (const df of [-1, 1]) {
          const nf = f + df; if (nf < 0 || nf > 7) continue;
          const to = one + df, tv = b[to];
          if (tv && (tv >> 3) === enemy) { if (r === promoR) pushPromo(s, to); else out.push(s | (to << 6)); }
          else if (to === this.ep && !tv) out.push(s | (to << 6));
        }
      } else if (t === N || t === K) {
        for (const to of (t === N ? KN[s] : KG[s])) { const tv = b[to]; if (tv ? (tv >> 3) === enemy : !capsOnly) out.push(s | (to << 6)); }
        if (t === K && !capsOnly) {
          const base = me ? 56 : 0, rights = me ? this.castle >> 2 : this.castle & 3;
          if (s === base + 4 && rights) {
            if ((rights & 1) && !b[base + 5] && !b[base + 6] && b[base + 7] === (o | R) && !this.attacked(s, enemy) && !this.attacked(base + 5, enemy) && !this.attacked(base + 6, enemy)) out.push(s | ((base + 6) << 6));
            if ((rights & 2) && !b[base + 3] && !b[base + 2] && !b[base + 1] && b[base] === (o | R) && !this.attacked(s, enemy) && !this.attacked(base + 3, enemy) && !this.attacked(base + 2, enemy)) out.push(s | ((base + 2) << 6));
          }
        }
      } else {
        const d0 = t === B ? 4 : 0, d1 = t === R ? 4 : 8, rays = RAYS[s];
        for (let d = d0; d < d1; d++) {
          const ray = rays[d];
          for (let i = 0; i < ray.length; i++) {
            const to = ray[i], tv = b[to];
            if (!tv) { if (!capsOnly) out.push(s | (to << 6)); continue; }
            if ((tv >> 3) === enemy) out.push(s | (to << 6));
            break;
          }
        }
      }
    }
    return out;
  }

  /* đi nước m; trả về false (và tự hoàn tác) nếu vua mình bị chiếu sau nước đi */
  make(m) {
    const b = this.b, from = m & 63, to = (m >> 6) & 63, promo = (m >> 12) & 7, v = b[from], me = v >> 3, t = v & 7;
    let cap = b[to], capSq = to, isEp = false, a = this.h1, c = this.h2;
    const u = { m, cap: 0, capSq: to, isEp: false, castle: this.castle, ep: this.ep, half: this.half, h1: this.h1, h2: this.h2, ksq: this.ksq[me], full: this.full };
    const oef = this.epHashFile(); if (oef >= 0) { a ^= ZE1[oef]; c ^= ZE2[oef]; }
    a ^= ZC1[this.castle]; c ^= ZC2[this.castle];
    if (t === P && to === this.ep && !cap) { isEp = true; capSq = to + (me ? 8 : -8); cap = b[capSq]; b[capSq] = 0; }
    if (cap) { a ^= ZP1[cap * 64 + capSq]; c ^= ZP2[cap * 64 + capSq]; }
    u.cap = cap; u.capSq = capSq; u.isEp = isEp;
    b[from] = 0; a ^= ZP1[v * 64 + from]; c ^= ZP2[v * 64 + from];
    const nv = promo ? ((me << 3) | promo) : v;
    b[to] = nv; a ^= ZP1[nv * 64 + to]; c ^= ZP2[nv * 64 + to];
    if (t === K) {
      this.ksq[me] = to;
      if (to - from === 2) { const rf = from + 3, rt = from + 1, rv = b[rf]; b[rf] = 0; b[rt] = rv; a ^= ZP1[rv * 64 + rf] ^ ZP1[rv * 64 + rt]; c ^= ZP2[rv * 64 + rf] ^ ZP2[rv * 64 + rt]; }
      else if (from - to === 2) { const rf = from - 4, rt = from - 1, rv = b[rf]; b[rf] = 0; b[rt] = rv; a ^= ZP1[rv * 64 + rf] ^ ZP1[rv * 64 + rt]; c ^= ZP2[rv * 64 + rf] ^ ZP2[rv * 64 + rt]; }
    }
    this.castle &= CASTLE_MASK[from] & CASTLE_MASK[to];
    this.ep = (t === P && Math.abs(to - from) === 16) ? (from + to) >> 1 : -1;
    this.half = (t === P || cap) ? 0 : this.half + 1;
    if (me) this.full++;
    this.side ^= 1; a ^= ZS1; c ^= ZS2;
    a ^= ZC1[this.castle]; c ^= ZC2[this.castle];
    this.h1 = a; this.h2 = c;
    const nef = this.epHashFile(); if (nef >= 0) { this.h1 ^= ZE1[nef]; this.h2 ^= ZE2[nef]; }
    this.undo.push(u);
    if (this.attacked(this.ksq[me], me ^ 1)) { this._back(this.undo.pop()); return false; }
    this.keys1.push(this.h1); this.keys2.push(this.h2);
    return true;
  }
  _back(u) {
    const m = u.m, from = m & 63, to = (m >> 6) & 63, promo = (m >> 12) & 7, b = this.b, mover = this.side ^ 1;
    const piece = promo ? ((mover << 3) | P) : b[to];
    b[to] = 0; b[from] = piece;
    if (u.cap) b[u.capSq] = u.cap;
    if ((piece & 7) === K) {
      if (to - from === 2) { b[from + 3] = b[from + 1]; b[from + 1] = 0; }
      else if (from - to === 2) { b[from - 4] = b[from - 1]; b[from - 1] = 0; }
    }
    this.side = mover; this.castle = u.castle; this.ep = u.ep; this.half = u.half; this.full = u.full; this.h1 = u.h1; this.h2 = u.h2; this.ksq[mover] = u.ksq;
  }
  unmake() { this.keys1.pop(); this.keys2.pop(); this._back(this.undo.pop()); }

  /* nước "bỏ lượt" cho null-move pruning của AI */
  makeNull() {
    const u = { ep: this.ep, h1: this.h1, h2: this.h2, half: this.half };
    const oef = this.epHashFile(); if (oef >= 0) { this.h1 ^= ZE1[oef]; this.h2 ^= ZE2[oef]; }
    this.ep = -1; this.side ^= 1; this.h1 ^= ZS1; this.h2 ^= ZS2; this.half++;
    this.nullStack = this.nullStack || []; this.nullStack.push(u);
    this.keys1.push(this.h1); this.keys2.push(this.h2);
  }
  unmakeNull() { const u = this.nullStack.pop(); this.keys1.pop(); this.keys2.pop(); this.side ^= 1; this.ep = u.ep; this.h1 = u.h1; this.h2 = u.h2; this.half = u.half; }

  legalMoves() { const out = []; for (const m of this.gen()) if (this.make(m)) { this.unmake(); out.push(m); } return out; }
  /* nước hợp lệ từ ô `from` (dùng khi người chơi chạm vào quân) */
  legalFrom(from) { return this.legalMoves().filter(m => (m & 63) === from); }
  /* tìm nước hợp lệ theo UCI ('e2e4', 'e7e8q'); không thấy → null */
  parseUci(s) {
    if (!/^[a-h][1-8][a-h][1-8][nbrq]?$/.test(s)) return null;
    const f = sqFrom(s.slice(0, 2)), t = sqFrom(s.slice(2, 4)), pr = s[4] ? 'nbrq'.indexOf(s[4]) + 2 : 0;
    return this.legalMoves().find(m => (m & 63) === f && ((m >> 6) & 63) === t && ((m >> 12) & 7) === pr) ?? null;
  }
  uci(m) { return sqName(m & 63) + sqName((m >> 6) & 63) + (((m >> 12) & 7) ? 'nbrq'[((m >> 12) & 7) - 2] : ''); }

  /* ── kết thúc ván ── */
  repetitions() { // số lần thế hiện tại đã xuất hiện (tính cả lần này), chỉ xét trong đoạn từ nước không thể đảo ngược cuối
    const n = this.keys1.length - 1; let c = 1;
    for (let i = n - 2, lim = Math.max(0, n - this.half); i >= lim; i -= 2) if (this.keys1[i] === this.h1 && this.keys2[i] === this.h2) c++;
    return c;
  }
  insufficientSide(side) { // bên `side` không thể chiếu hết dù đối phương đi sai
    let n = 0, bi = 0, sq0 = -1, bc = 0, oppOther = 0, oppKnight = 0, oppPawn = 0;
    for (let s = 0; s < 64; s++) {
      const v = this.b[s]; if (!v) continue; const t = v & 7, c = v >> 3;
      if (c === side) { if (t === P || t === R || t === Q) return false; if (t === N) n++; else if (t === B) { bi++; bc |= 1 << ((s + (s >> 3)) & 1); } }
      else if (t !== K) { oppOther++; if (t === N) oppKnight++; if (t === P) oppPawn++; }
    }
    if (n + bi === 0) return true;
    if (n === 1 && bi === 0) return oppOther === 0;
    if (n === 0 && bi >= 1) return (bc === 1 || bc === 2) && oppKnight === 0 && oppPawn === 0;
    return false;
  }
  insufficientMaterial() { return this.insufficientSide(0) && this.insufficientSide(1); }
  /* trả null nếu ván tiếp tục; ngược lại { result: '1-0'|'0-1'|'1/2-1/2', winner: 0|1|null, reason } */
  status(movesCache) {
    const moves = movesCache || this.legalMoves();
    if (!moves.length) return this.inCheck() ? { result: this.side ? '1-0' : '0-1', winner: this.side ^ 1, reason: 'checkmate' } : { result: '1/2-1/2', winner: null, reason: 'stalemate' };
    if (this.insufficientMaterial()) return { result: '1/2-1/2', winner: null, reason: 'insufficient' };
    if (this.half >= 100) return { result: '1/2-1/2', winner: null, reason: 'fifty' };
    if (this.repetitions() >= 3) return { result: '1/2-1/2', winner: null, reason: 'repetition' };
    return null;
  }

  /* ── ký hiệu đại số (SAN): gọi TRƯỚC khi đi nước m ── */
  san(m) {
    const from = m & 63, to = (m >> 6) & 63, promo = (m >> 12) & 7, v = this.b[from], t = v & 7;
    let s;
    if (t === K && Math.abs(to - from) === 2) s = to > from ? 'O-O' : 'O-O-O';
    else {
      const capture = this.b[to] || (t === P && to === this.ep);
      if (t === P) s = (capture ? 'abcdefgh'[from & 7] + 'x' : '') + sqName(to) + (promo ? '=' + ' NBRQ'[promo - 1] : '');
      else {
        let dis = '';
        const others = this.legalMoves().filter(x => x !== m && ((x >> 6) & 63) === to && (x & 63) !== from && (this.b[x & 63] & 7) === t);
        if (others.length) {
          const sameFile = others.some(x => (x & 7) === (from & 7)), sameRank = others.some(x => ((x & 63) >> 3) === (from >> 3));
          dis = !sameFile ? 'abcdefgh'[from & 7] : !sameRank ? String((from >> 3) + 1) : sqName(from);
        }
        s = ' PNBRQK'[t] + dis + (capture ? 'x' : '') + sqName(to);
      }
    }
    if (this.make(m)) { const chk = this.inCheck(); if (chk) s += this.legalMoves().length ? '+' : '#'; this.unmake(); }
    return s;
  }
}

/* đếm số nút đi (kiểm thử bộ luật) */
export function perft(pos, depth) {
  if (depth === 0) return 1;
  let n = 0;
  for (const m of pos.gen()) { if (!pos.make(m)) continue; n += depth === 1 ? 1 : perft(pos, depth - 1); pos.unmake(); }
  return n;
}
export const PIECE_CHARS = PCH;
