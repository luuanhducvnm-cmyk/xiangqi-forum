"""Danh sách sơ đồ. 'from' = ô quân cần hiện nước đi (engine tự tính); 'expect' = engine phải xác nhận (mate/check/stalemate).
Cờ tướng: FEN chuẩn (chữ HOA = Đỏ ở dưới, thường = Đen ở trên); toạ độ (hàng,cột) hàng 0 = đỉnh bàn."""
XQ_START = 'rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w'
CH_START = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
PAL = [(r, c) for r in (0, 1, 2, 7, 8, 9) for c in (3, 4, 5)]

def xq(fen, alt, **k): return dict(game='xq', fen=fen, alt=alt, **k)
def ch(fen, alt, **k): return dict(game='ch', fen=fen, alt=alt, **k)

SPECS = {
    # ───── cờ tướng ─────
    'xq-start': xq(XQ_START, 'Xiangqi starting position: Red pieces on the bottom ranks, Black on the top, with the river between them.'),
    'xq-board': xq('9/9/9/9/9/9/9/9/9/9 w', 'Empty xiangqi board: 9 files by 10 ranks, two palaces highlighted, the river in the middle.', hl=PAL),
    'xq-king': xq('3k5/9/9/9/9/9/9/9/4K4/9 w', 'A Red general in the middle of its palace can step one point in any of four directions.', **{'from': '8,4'}),
    'xq-flying': xq('4k4/9/9/9/9/4R4/9/9/9/4K4 b', 'The two generals face each other down the same file with only a Red chariot between them — the chariot is pinned to the file.', hl=[(0, 4), (9, 4)]),
    'xq-advisor': xq('3k5/9/9/9/9/9/9/9/4A4/4K4 w', 'A Red advisor on the palace centre moves one point diagonally to the four corners of the palace.', **{'from': '8,4'}),
    'xq-elephant': xq('3k5/9/9/9/9/9/5p3/4B4/9/4K4 w', 'A Red elephant on the middle point can reach three diagonal points; the fourth is blocked by a piece on the "elephant eye".', **{'from': '7,4'}),
    'xq-horse': xq('4k4/9/9/9/9/4N4/9/9/9/3K5 w', 'A Red horse in open space can jump to eight points: one step straight then one step diagonally outward.', **{'from': '5,4'}),
    'xq-horse-block': xq('4k4/9/9/9/9/9/4P4/4NP3/9/4K4 w', 'A Red horse hobbled by its own pawns: the pieces directly above and to the right block four of its jumps.', **{'from': '7,4'}),
    'xq-chariot': xq('4k4/9/9/3P5/9/9/3R3p1/9/9/5K3 w', 'A Red chariot slides along ranks and files, stopped by its own pawn and able to capture the Black pawn on its rank.', **{'from': '6,3'}),
    'xq-cannon': xq('1n2k4/9/9/1p7/9/9/9/1C2P1p2/9/3K5 w', 'A Red cannon slides like a chariot but captures only by jumping exactly one screen piece, here to take a pawn on its rank or the horse on its file.', **{'from': '7,1'}),
    'xq-soldier-before': xq('4k4/9/9/9/9/9/4P4/9/9/3K5 w', 'A Red soldier that has not crossed the river can only step one point forward.', **{'from': '6,4'}),
    'xq-soldier-after': xq('4k4/9/9/9/4P4/9/9/9/9/3K5 w', 'A Red soldier that has crossed the river can step forward or one point sideways.', **{'from': '4,4'}),
    'xq-central-cannon': xq('rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C2C4/9/RNBAKABNR b', 'Central Cannon opening: Red’s cannon on file 2 has moved to the central file (C2=5), aiming at the Black general’s file.', arrows=[((7, 7), (7, 4))]),
    'xq-screen-horse': xq('r1bakab1r/9/1cn3nc1/p1p1p1p1p/9/9/P1P1P1P1P/1C2C1N2/9/RNBAKAB1R w', 'Central Cannon versus the Screen Horse defence: Black’s two horses guard the centre while the soldiers on files 3 and 7 support them.'),
    'xq-mate-chariots': xq('R3k4/8R/9/9/9/9/9/9/9/3K5 b', 'Double-chariot checkmate: one chariot checks along the back rank while the other seals the rank in front of the general.', expect='mate', arrows=[((0, 0), (0, 3))]),
    'xq-mate-horse-chariot': xq('R3k4/9/9/3N5/9/9/9/9/9/3K5 b', 'Chariot and horse checkmate: the chariot checks along the back rank, the horse covers the only escape square in front of the general.', expect='mate'),
    'xq-mate-cannon-horse': xq('3aka3/C1N6/2b3b2/9/9/9/9/9/9/3K5 b', 'Horse and cannon checkmate: the horse gives check, and the cannon behind it covers the general’s last flight square on the second rank.', expect='mate'),
    'xq-stalemate': xq('4k4/3P1P3/9/9/9/9/9/9/9/3K5 b', 'Stalemate in xiangqi: Black’s general is not in check, but both flight squares beside it and the square below are attacked by the two Red soldiers, so Black has no legal move and loses.', expect='stalemate'),
    'xq-cc-same': xq('rnbakabnr/9/1c2c4/p1p1p1p1p/9/9/P1P1P1P1P/1C2C4/9/RNBAKABNR w', 'Same-direction cannons: after 1.C2=5 Black answers C8=5, so both cannons stand on the central file.'),
    'xq-cc-opposite': xq('rnbakabnr/9/4c2c1/p1p1p1p1p/9/9/P1P1P1P1P/1C2C4/9/RNBAKABNR w', 'Opposite cannons: after 1.C2=5 Black answers C2=5 with the cannon from the other side of the board.'),
    'xq-cc-target': xq('rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C2C4/9/RNBAKABNR w', 'After 1.C2=5 the Red cannon uses its own soldier as a screen and attacks the Black soldier on the central file.', **{'from': '7,4'}),
    'xq-elephant-river': xq('4k4/9/9/9/9/2B6/9/9/9/3K5 w', 'A Red elephant on the river bank can only retreat: its two forward jumps would cross the river, which is not allowed.', **{'from': '5,2'}),
    # ───── cờ vua ─────
    'ch-start': ch(CH_START, 'Chess starting position: White on ranks 1 and 2, Black on ranks 7 and 8.'),
    'ch-king': ch('8/8/8/8/4K3/8/8/k7 w - - 0 1', 'A king on e4 can move one square in any direction.', **{'from': 'e4'}),
    'ch-queen': ch('7k/8/8/3p4/3Q4/8/8/K7 w - - 0 1', 'A queen on d4 slides along ranks, files and diagonals, and may capture the pawn on d5.', **{'from': 'd4'}),
    'ch-rook': ch('7k/8/8/8/3R2p1/8/8/K7 w - - 0 1', 'A rook on d4 slides along its rank and file; here it can capture the pawn on g4.', **{'from': 'd4'}),
    'ch-bishop': ch('7k/8/8/8/3B4/8/8/K7 w - - 0 1', 'A bishop on d4 slides along its diagonals and always stays on the same colour of square.', **{'from': 'd4'}),
    'ch-knight': ch('7k/8/8/8/3N4/8/8/K7 w - - 0 1', 'A knight on d4 jumps in an L-shape to eight squares and may leap over other pieces.', **{'from': 'd4'}),
    'ch-pawn-start': ch('7k/8/8/8/8/3p4/4P3/K7 w - - 0 1', 'A pawn on its starting square e2 can advance one or two squares; it captures diagonally, here the pawn on d3.', **{'from': 'e2'}),
    'ch-castle': ch('r3k2r/pppqbppp/2n1bn2/3pp3/3PP3/2N1BN2/PPPQBPPP/R3K2R w KQkq - 0 1', 'White can castle kingside (king to g1, rook to f1) or queenside (king to c1, rook to d1) because the squares between are empty.', arrows=[('e1', 'g1'), ('e1', 'c1')]),
    'ch-enpassant': ch('7k/8/8/3pP3/8/8/8/K7 w - - 0 1', 'En passant: after Black plays d7–d5 past the white pawn on e5, White may capture it as if it had moved only one square, landing on d6.', arrows=[('e5', 'd6')], hl=['d5']),
    'ch-promotion': ch('8/4P1k1/8/8/8/8/8/K7 w - - 0 1', 'A pawn on the seventh rank is one step from promotion to a queen, rook, bishop or knight.', arrows=[('e7', 'e8')]),
    'ch-fools-mate': ch('rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3', 'Fool’s mate: 1.f3 e5 2.g4 Qh4# — the fastest possible checkmate.', expect='mate', hl=['h4']),
    'ch-scholars-mate': ch('r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4', 'Scholar’s mate: the queen on f7, protected by the bishop on c4, checkmates the king on e8.', expect='mate', hl=['f7']),
    'ch-back-rank': ch('R5k1/5ppp/8/8/8/8/5PPP/6K1 b - - 0 1', 'Back-rank mate: the rook on a8 checks the king, which is boxed in by its own pawns.', expect='mate', hl=['a8']),
    'ch-smothered': ch('6rk/5Npp/8/8/8/8/8/7K b - - 0 1', 'Smothered mate: the knight on f7 checks a king that is surrounded by its own rook and pawns.', expect='mate', hl=['f7']),
    'ch-queen-mate': ch('7k/6Q1/6K1/8/8/8/8/8 b - - 0 1', 'King and queen versus king: the queen on g7, protected by the king, delivers checkmate.', expect='mate'),
    'ch-fork': ch('r3k3/8/8/1N6/8/8/8/4K3 w - - 0 1', 'A knight fork: Nc7+ attacks the king on e8 and the rook on a8 at the same time.', arrows=[('b5', 'c7')]),
    'ch-pin': ch('4k3/8/2n5/1B6/8/8/8/4K3 b - - 0 1', 'A pin: the knight on c6 cannot move because it would expose its king on e8 to the bishop on b5.', **{'from': 'c6'}, hl=['c6']),
    'ch-opp': ch('8/8/4k3/8/4K3/8/8/8 w - - 0 1', 'Opposition: the kings face each other with one square between them; the side NOT to move holds the opposition.'),
    'ch-italian': ch('r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3', 'Italian Game: 1.e4 e5 2.Nf3 Nc6 3.Bc4.'),
    'ch-ruy-lopez': ch('r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3', 'Ruy Lopez: 1.e4 e5 2.Nf3 Nc6 3.Bb5.'),
    'ch-sicilian': ch('rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2', 'Sicilian Defence: 1.e4 c5.'),
    'ch-queens-gambit': ch('rnbqkbnr/ppp1pppp/8/3p4/2PP4/8/PP2PPPP/RNBQKBNR b KQkq - 0 2', 'Queen’s Gambit: 1.d4 d5 2.c4.'),
    'ch-london': ch('rnbqkbnr/ppp1pppp/8/3p4/3P1B2/8/PPP1PPPP/RN1QKBNR b KQkq - 1 2', 'London System: 1.d4 d5 2.Bf4.'),
    'ch-french': ch('rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2', 'French Defence: 1.e4 e6.'),
    'ch-caro-kann': ch('rnbqkbnr/pp1ppppp/2p5/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2', 'Caro-Kann Defence: 1.e4 c6.'),
    'ch-kings-indian': ch('rnbqkb1r/pppppp1p/5np1/8/2PP4/8/PP2PPPP/RNBQKBNR w KQkq - 0 3', 'King’s Indian Defence setup: 1.d4 Nf6 2.c4 g6.'),
    'ch-castle-through': ch('4kr2/8/8/8/8/8/8/R3K2R w KQ - 0 1', 'White cannot castle kingside here: the black rook on f8 attacks f1, a square the king would pass over. Queenside castling is still legal.', **{'from': 'e1'}),
    'ch-stalemate': ch('7k/5Q2/6K1/8/8/8/8/8 b - - 0 1', 'Stalemate: Black is not in check but has no legal move, so the game is a draw.', expect='stalemate'),
}

# ───── bài tập chiếu bí (tools/puzzles.json; đáp án do tools/solver.mjs chứng minh) ─────
import json as _json, os as _os
for _p in _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'puzzles.json'))):
    _side = 'White' if _p['game'] == 'ch' else 'Red'
    _f = ch if _p['game'] == 'ch' else xq
    SPECS['pz-' + _p['id']] = _f(_p['fen'], f"{'Chess' if _p['game'] == 'ch' else 'Xiangqi'} puzzle: {_side} to move and checkmate in {_p['n']}.")

# ───── tàn cuộc: thế cờ do tools/tablebase.mjs vét cạn (retrograde) xác nhận ─────
SPECS.update({
    'ch-kpk-key': ch('4k3/8/4K3/4P3/8/8/8/8 w - - 0 1', 'King on e6 in front of the pawn on e5 against the king on e8: a won position for White whoever is to move.', hl=['e6']),
    'ch-kpk-opp': ch('8/4k3/8/4K3/4P3/8/8/8 w - - 0 1', 'Opposition: White king on e5 behind the pawn on e4, Black king on e7. With White to move it is only a draw; with Black to move White wins.'),
    'ch-kpk-rook': ch('k7/8/PK6/8/8/8/8/8 b - - 0 1', 'Rook pawn draw: the pawn on a6 and king on b6 cannot make progress because the black king on a8 is stalemated at the right moment.'),
    'ch-kpk-trap': ch('4k3/4P3/5K2/8/8/8/8/8 w - - 0 1', 'A stalemate trap: with White to move, the natural 1.Kf7 is stalemate and the game is drawn; the position is only a draw against best play.'),
    'ch-kqk-worst': ch('8/8/8/5k2/8/8/1Q6/K7 w - - 0 1', 'A position from which king and queen need the maximum, 10 moves, to checkmate a lone king.'),
    'ch-krk-worst': ch('8/8/8/8/8/2k5/1R6/K7 w - - 0 1', 'A position from which king and rook need the maximum, 16 moves, to checkmate a lone king.'),
})

# ───── thế cờ dựng từ danh sách nước đi (tools/lines.json): mọi nước được kiểm hợp lệ bằng bộ luật thật khi build ─────
import subprocess as _sp
_L = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'lines.json')))
_r = _json.loads(_sp.run(['node', _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'lines.mjs')], input=_json.dumps(_L), capture_output=True, text=True, check=True).stdout)
for _l in _L:
    _o = _r[_l['id']]
    assert _o['ok'], f"đường nước đi {_l['id']} KHÔNG hợp lệ: {_o.get('error')}"
    _kw = {'expect': 'mate'} if _l['id'] in ('ln-legal', 'ln-shilling') else {}
    SPECS[_l['id']] = (ch if _l['game'] == 'ch' else xq)(_o['fen'], _l['alt'], **_kw)
