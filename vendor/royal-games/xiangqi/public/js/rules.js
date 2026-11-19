// Tự động trích từ public/index.html — luật cờ dùng chung để server kiểm tra nước đi.
export const INITIAL_BOARD = [
  ["bR", "bH", "bE", "bA", "bK", "bA", "bE", "bH", "bR"],
  [null, null, null, null, null, null, null, null, null],
  [null, "bC", null, null, null, null, null, "bC", null],
  ["bP", null, "bP", null, "bP", null, "bP", null, "bP"],
  [null, null, null, null, null, null, null, null, null],
  [null, null, null, null, null, null, null, null, null],
  ["rP", null, "rP", null, "rP", null, "rP", null, "rP"],
  [null, "rC", null, null, null, null, null, "rC", null],
  [null, null, null, null, null, null, null, null, null],
  ["rR", "rH", "rE", "rA", "rK", "rA", "rE", "rH", "rR"]
];

export function cloneBoard(b) { return b.map(row => row.slice()); }
export function isInside(r, c) { return r >= 0 && r < 10 && c >= 0 && c < 9; }
export function inPalace(r, c, side) {
  if (c < 3 || c > 5) return false;
  return side === 'r' ? (r >= 7 && r <= 9) : (r >= 0 && r <= 2);
}

export function getPseudoMovesForPiece(b, r, c) {
  const piece = b[r][c];
  if (!piece) return [];
  const side = piece[0];
  const type = piece[1];
  const moves = [];

  const tryAdd = (nr, nc) => {
    if (!isInside(nr, nc)) return;
    const target = b[nr][nc];
    if (!target || target[0] !== side) moves.push([nr, nc]);
  };

  if (type === 'K') {
    [[1, 0], [-1, 0], [0, 1], [0, -1]].forEach(([dr, dc]) => {
      const nr = r + dr, nc = c + dc;
      if (inPalace(nr, nc, side)) tryAdd(nr, nc);
    });
  } else if (type === 'A') {
    [[1, 1], [1, -1], [-1, 1], [-1, -1]].forEach(([dr, dc]) => {
      const nr = r + dr, nc = c + dc;
      if (inPalace(nr, nc, side)) tryAdd(nr, nc);
    });
  } else if (type === 'E') {
    [[2, 2], [2, -2], [-2, 2], [-2, -2]].forEach(([dr, dc]) => {
      const nr = r + dr, nc = c + dc;
      const er = r + dr / 2, ec = c + dc / 2;
      const ownHalf = side === 'r' ? nr >= 5 : nr <= 4;
      if (isInside(nr, nc) && ownHalf && !b[er][ec]) tryAdd(nr, nc);
    });
  } else if (type === 'H') {
    const horseSteps = [
      [-2, -1, -1, 0], [-2, 1, -1, 0],
      [2, -1, 1, 0],   [2, 1, 1, 0],
      [-1, -2, 0, -1], [1, -2, 0, -1],
      [-1, 2, 0, 1],   [1, 2, 0, 1]
    ];
    horseSteps.forEach(([dr, dc, lr, lc]) => {
      const nr = r + dr, nc = c + dc;
      if (isInside(nr, nc) && !b[r + lr][c + lc]) tryAdd(nr, nc);
    });
  } else if (type === 'R') {
    [[1, 0], [-1, 0], [0, 1], [0, -1]].forEach(([dr, dc]) => {
      let nr = r + dr, nc = c + dc;
      while (isInside(nr, nc)) {
        if (!b[nr][nc]) {
          moves.push([nr, nc]);
        } else {
          if (b[nr][nc][0] !== side) moves.push([nr, nc]);
          break;
        }
        nr += dr; nc += dc;
      }
    });
  } else if (type === 'C') {
    [[1, 0], [-1, 0], [0, 1], [0, -1]].forEach(([dr, dc]) => {
      let nr = r + dr, nc = c + dc;
      let jumped = false;
      while (isInside(nr, nc)) {
        if (!jumped) {
          if (!b[nr][nc]) { moves.push([nr, nc]); }
          else { jumped = true; }
        } else if (b[nr][nc]) {
          if (b[nr][nc][0] !== side) moves.push([nr, nc]);
          break;
        }
        nr += dr; nc += dc;
      }
    });
  } else if (type === 'P') {
    const forward = side === 'r' ? -1 : 1;
    tryAdd(r + forward, c);
    const crossedRiver = side === 'r' ? r <= 4 : r >= 5;
    if (crossedRiver) { tryAdd(r, c - 1); tryAdd(r, c + 1); }
  }
  return moves;
}

export function isKingInCheck(b, side) {
  let kr = -1, kc = -1, okr = -1, okc = -1;
  const opp = side === 'r' ? 'b' : 'r';

  for (let r = 0; r < 10; r++) {
    for (let c = 0; c < 9; c++) {
      if (b[r][c] === side + 'K') { kr = r; kc = c; }
      if (b[r][c] === opp + 'K') { okr = r; okc = c; }
    }
  }
  if (kr === -1) return true;

  if (kc === okc && okr !== -1) {
    let blocked = false;
    for (let r = Math.min(kr, okr) + 1; r < Math.max(kr, okr); r++) {
      if (b[r][kc]) { blocked = true; break; }
    }
    if (!blocked) return true;
  }

  for (let r = 0; r < 10; r++) {
    for (let c = 0; c < 9; c++) {
      const p = b[r][c];
      if (p && p[0] === opp) {
        const pMoves = getPseudoMovesForPiece(b, r, c);
        if (pMoves.some(([mr, mc]) => mr === kr && mc === kc)) return true;
      }
    }
  }
  return false;
}

export function getLegalMovesForSquare(b, r, c) {
  const piece = b[r][c];
  if (!piece) return [];
  const side = piece[0];
  const pseudo = getPseudoMovesForPiece(b, r, c);
  return pseudo.filter(([nr, nc]) => {
    const sim = cloneBoard(b);
    sim[nr][nc] = piece;
    sim[r][c] = null;
    return !isKingInCheck(sim, side);
  });
}

export function getAllLegalMoves(b, side) {
  const all = [];
  for (let r = 0; r < 10; r++) {
    for (let c = 0; c < 9; c++) {
      if (b[r][c] && b[r][c][0] === side) {
        const list = getLegalMovesForSquare(b, r, c);
        list.forEach(([tr, tc]) => all.push({ from: [r, c], to: [tr, tc], piece: b[r][c] }));
      }
    }
  }
  return all;
}

/* ===== Luật lặp thế · chiếu liên tục · đuổi quân liên tục · 60 nước không ăn quân ===== */
export const NO_CAPTURE_PLIES = 120;                                   // 60 nước mỗi bên không ai ăn quân → hòa
const CHASE_VAL = { R: 9, C: 4, H: 4, A: 2, E: 2, P: 1, K: 100 };

export function positionKey(board, turn) {
  let s = turn;
  for (let r = 0; r < 10; r++) for (let c = 0; c < 9; c++) s += board[r][c] || '--';
  return s;
}
export function boardAfter(board, f, t) {
  const b = cloneBoard(board);
  b[t[0]][t[1]] = b[f[0]][f[1]]; b[f[0]][f[1]] = null;
  return b;
}
/* Các ô có quân Xe/Pháo/Mã của đối phương đang bị `side` đe dọa ăn "có lợi"
   (quân bị đe dọa không được bảo vệ, hoặc có giá trị lớn hơn quân tấn công; Mã–Pháo coi như ngang nhau) */
export function chaseTargets(board, side) {
  const enemy = side === 'r' ? 'b' : 'r', out = new Set();
  for (let r = 0; r < 10; r++) for (let c = 0; c < 9; c++) {
    const p = board[r][c];
    if (!p || p[0] !== side) continue;
    for (const [tr, tc] of getLegalMovesForSquare(board, r, c)) {
      const t = board[tr][tc];
      if (!t || t[0] !== enemy || 'RHC'.indexOf(t[1]) < 0 || out.has(tr * 9 + tc)) continue;
      let profit = CHASE_VAL[t[1]] > CHASE_VAL[p[1]];
      if (!profit) {
        const b2 = boardAfter(board, [r, c], [tr, tc]);
        profit = !getAllLegalMoves(b2, enemy).some(m => m.to[0] === tr && m.to[1] === tc);
      }
      if (profit) out.add(tr * 9 + tc);
    }
  }
  return out;
}
/* Phân xử theo danh sách nước đi [[from,to],...] tính từ thế khai cuộc (hoặc `start` = {board, turn} để thử nghiệm).
   Trả về { count: số lần thế cờ hiện tại đã xuất hiện, since: số nước kể từ lần ăn quân cuối,
            over: null | { winner: 'r'|'b'|null, reason: 'perpetual'|'repetition'|'nocapture', kind?: 'check'|'chase' } } */
export function analyzeGame(moves, start) {
  const t0 = (start && start.turn) || 'r', flip = s => s === 'r' ? 'b' : 'r';
  const sideAt = i => i % 2 === 0 ? t0 : flip(t0);
  const init = () => cloneBoard((start && start.board) || INITIAL_BOARD);
  let board = init(), since = 0;
  const keys = [positionKey(board, t0)];
  for (let i = 0; i < moves.length; i++) {
    const [f, t] = moves[i];
    since = board[t[0]][t[1]] ? 0 : since + 1;
    board[t[0]][t[1]] = board[f[0]][f[1]]; board[f[0]][f[1]] = null;
    keys.push(positionKey(board, flip(sideAt(i))));
  }
  const n = moves.length, occ = [];
  for (let i = 0; i <= n; i++) if (keys[i] === keys[n]) occ.push(i);
  const out = { count: occ.length, since, over: null };

  if (occ.length >= 3) {                                        // lặp lần thứ 3 → phân xử
    const a = occ[occ.length - 3];
    let bd = init();
    for (let i = 0; i < a; i++) bd = boardAfter(bd, moves[i][0], moves[i][1]);
    const viol = { r: true, b: true }, had = { r: false, b: false }, chased = { r: false, b: false };
    for (let i = a; i < n; i++) {
      const side = sideAt(i), after = boardAfter(bd, moves[i][0], moves[i][1]);
      had[side] = true;
      let attack = isKingInCheck(after, flip(side));
      if (!attack) {
        const before = chaseTargets(bd, side);
        for (const s of chaseTargets(after, side)) if (!before.has(s)) { attack = true; chased[side] = true; break; }
      }
      if (!attack) viol[side] = false;
      bd = after;
    }
    const rv = had.r && viol.r, bv = had.b && viol.b;           // chỉ một bên phạm luật → bên đó thua
    if (rv !== bv) {
      const v = rv ? 'r' : 'b';
      out.over = { winner: flip(v), reason: 'perpetual', kind: chased[v] ? 'chase' : 'check' };
    } else out.over = { winner: null, reason: 'repetition' };    // cả hai cùng phạm, hoặc không ai phạm → hòa
  } else if (since >= NO_CAPTURE_PLIES) out.over = { winner: null, reason: 'nocapture' };
  return out;
}
