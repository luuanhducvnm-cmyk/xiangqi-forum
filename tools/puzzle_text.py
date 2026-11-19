# -*- coding: utf-8 -*-
"""Phần chữ (hướng dẫn, FAQ) cho các trang bài tập. Đáp án do solver sinh, KHÔNG nằm ở đây."""

def faq3(a, b, c): return [a, b, c]

CHK_HOW_EN = """Work through the same short checklist each time:

1. List every check White has: queen and rook moves along lines, bishop and knight jumps, pawn captures.
2. For each check, count the king's escape squares. A square is not an escape if White attacks it, if a Black piece already stands on it, or if the king would still be in check there.
3. Ask whether the checking piece can be captured or blocked. A pinned piece cannot capture if that would expose its own king.
4. Drop the checks that fail and keep the one that passes all three tests.

This habit, *checks first*, is the most useful one in chess."""
CHK_HOW_VI = """Mỗi bài hãy đi qua cùng một danh sách kiểm tra ngắn:

1. Liệt kê mọi nước chiếu của Trắng: Hậu và Xe đi theo đường thẳng, Tượng và Mã nhảy, Tốt ăn chéo.
2. Với mỗi nước chiếu, đếm các ô thoát của Vua. Một ô không phải là lối thoát nếu Trắng đang tấn công ô đó, nếu quân Đen đã đứng trên ô đó, hoặc nếu Vua vẫn bị chiếu ở đó.
3. Hỏi xem quân đang chiếu có thể bị ăn hoặc bị chặn không. Quân bị ghim không được ăn nếu làm lộ Vua của mình.
4. Bỏ các nước chiếu thất bại và giữ lại nước vượt qua cả ba bước.

Thói quen *xét các nước chiếu trước* là thói quen hữu ích nhất trong cờ vua."""

XQ_RULES_EN = """Red is at the bottom of the diagram and moves first. Moves are written in WXF notation (see the [notation guide](/xiangqi/notation/)): for example `R9=4` is the chariot on file 9 moving sideways to file 4. When two identical pieces stand on the same file, `front` and `rear` replace the file number. Red counts files from the right-hand side of the bottom edge; Black counts from the right-hand side of the top edge."""
XQ_RULES_VI = """Đỏ ở phía dưới sơ đồ và đi trước. Nước đi ghi theo cách ghi của chuyên mục này (xem [cách ghi nước đi](/vi/co-tuong/ghi-nuoc-di/)): ví dụ "Xe 9 bình 4" là Xe ở đường 9 đi ngang sang đường 4. Khi hai quân cùng loại đứng trên một đường, dùng "tiền" (trước) và "hậu" (sau) thay cho số đường. Đỏ đếm đường dọc từ bên phải của mép dưới, Đen đếm từ bên phải của mép trên."""

TXT = {
 'hdr': {
  'en': dict(how='How to solve these puzzles', checked='How these puzzles were checked', sets='The puzzle sets', method='How we make sure the answers are right'),
  'vi': dict(how='Cách giải các bài này', checked='Các bài này được kiểm tra thế nào', sets='Các bộ bài tập', method='Cách đảm bảo đáp án đúng'),
 },
 'verify': {
  'en': {
   'ch': "Every position on this page was found by a computer and then checked with the rules engine of Chess 3D, the same code that runs the game. A puzzle is published only if White has exactly one first move that forces checkmate in {n}, and if every legal defence was searched to the end and checkmated. All {k} puzzles passed. No answer was copied from memory or from another site, and none of them is a quoted study, so you will not find them in a book.",
   'xq': "Every position on this page was found by a computer and then checked with the rules engine of Xiangqi 3D, the same code that runs the game, including the flying-general rule. A puzzle is published only if Red has exactly one first move that forces checkmate in {n}, and if every legal defence was searched to the end and ended in a real checkmate (a stalemated general, which also loses in xiangqi, is not counted as a solution here). All {k} puzzles passed. No answer was copied from memory or from another site.",
  },
  'vi': {
   'ch': "Mọi thế cờ trên trang này do máy tìm ra rồi được kiểm tra bằng bộ luật của Cờ vua 3D, chính là đoạn mã chạy game. Một bài chỉ được đăng nếu Trắng có đúng một nước đầu tiên ép chiếu hết sau {n} nước, và mọi cách phòng thủ hợp lệ của Đen đều được tìm đến cùng và đều bị chiếu hết. Cả {k} bài đều đạt. Không có đáp án nào chép theo trí nhớ hay từ trang khác, cũng không phải thế cờ nổi tiếng trích từ sách.",
   'xq': "Mọi thế cờ trên trang này do máy tìm ra rồi được kiểm tra bằng bộ luật của Cờ tướng 3D, chính là đoạn mã chạy game, kể cả luật hai tướng không được đối mặt. Một bài chỉ được đăng nếu Đỏ có đúng một nước đầu tiên ép chiếu bí sau {n} nước, và mọi cách phòng thủ hợp lệ của Đen đều được tìm đến cùng và kết thúc bằng chiếu bí thật (tướng hết nước đi mà không bị chiếu, vốn cũng thua trong cờ tướng, không được tính là đáp án ở đây). Cả {k} bài đều đạt. Không có đáp án nào chép theo trí nhớ hay từ trang khác.",
  },
 },
 'group': {'en': {}, 'vi': {}},
 'hub': {'en': {}, 'vi': {}},
}
G, H = TXT['group'], TXT['hub']

# ─────────── CỜ VUA · EN ───────────
G['en']['ch1'] = dict(
 title='Chess Puzzles: Mate in 1, Six Checkmate-in-One Puzzles with Solutions',
 crumb='Mate in 1', h1='Chess Mate in 1 Puzzles',
 description='Six verified chess mate-in-one puzzles with hints and solutions. Each position has exactly one checkmating move, confirmed by the Chess 3D rules engine.',
 blurb='Six one-move checkmates: find the only move that mates.',
 intro="In every position below it is **White's move**, and White can give checkmate **in one move**. There is exactly one such move in each puzzle, so you are looking for the single check that the Black king cannot escape. Cover the solution, take your time, and open the hint if you get stuck.",
 how=CHK_HOW_EN,
 next="Ready for something harder? Try the [mate in 2 puzzles](/chess/puzzles/mate-in-2/), review the [basic checkmate patterns](/chess/checkmates/), or practise on a real board with [Chess 3D](https://chess3d.online).",
 faq=[("What is a mate in 1 puzzle?", "A position where the side to move can deliver checkmate with a single move. In this set there is exactly one such move in every puzzle."),
      ("How do I find checkmate in one move?", "List all checks first, then test each one: can the king step away, can the checking piece be captured, can the check be blocked? The check for which every answer is no is the mate."),
      ("Are these puzzles from real games?", "No. They were generated by computer and verified by the Chess 3D rules engine, so each one is guaranteed to have exactly one solution. They are practice positions, not famous studies.")])
G['en']['ch2'] = dict(
 title='Chess Puzzles: Mate in 2, Eight Checkmate-in-Two Puzzles with Solutions',
 crumb='Mate in 2', h1='Chess Mate in 2 Puzzles',
 description='Eight verified chess mate-in-two puzzles with hints and full solutions. Each has one winning first move, and every Black defence is shown being checkmated.',
 blurb='Eight two-move checkmates, each with one key move and every defence refuted.',
 intro="In each puzzle **White moves, Black answers with anything, and White checkmates**. There is exactly one first move that makes this work whatever Black does, called the **key move**. It is often a quiet move: not a check, not a capture, but a move that takes away the last escape squares or creates a threat that cannot be parried.",
 how="""A mate in 2 is solved backwards. Use this routine:

1. Imagine the final position: which piece delivers mate, and which squares must be covered?
2. Look for a quiet move that **threatens** that mate. If Black cannot stop the threat, you are close.
3. Test every Black reply, including the awkward ones: moving the king, capturing the attacker, interposing, or counter-checking. The key move works only if **all** of them fail.
4. If one reply refutes your idea, discard it and try another candidate. Only one candidate survives.

Solutions list every legal Black reply with the checkmate that follows.""",
 next="Next level: [mate in 3 puzzles](/chess/puzzles/mate-in-3/). To see why these patterns recur, read the [chess tactics guide](/chess/tactics/).",
 faq=[("What is a key move in a chess puzzle?", "The one first move that wins by force. In a mate in 2 it is usually a quiet move that leaves Black with no defence."),
      ("Why is the first move often not a check?", "A check gives Black fewer options, but it lets the king run. A quiet move that removes the escape squares can leave Black in zugzwang-like trouble where every reply loses."),
      ("How do I get faster at mate in 2?", "Solve by pattern. After a few dozen puzzles you will recognise back-rank, smothered and ladder mates instantly, then only need to find the quiet move that prepares them.")])
G['en']['ch3'] = dict(
 title='Chess Puzzles: Mate in 3, Six Hard Checkmate-in-Three Puzzles',
 crumb='Mate in 3', h1='Chess Mate in 3 Puzzles',
 description='Six hard verified chess mate-in-three puzzles with hints and every defence solved to checkmate. Exactly one winning first move in each.',
 blurb='Six three-move checkmates: calculate deeper and find the single winning start.',
 intro="These are harder: **White moves, Black replies, White moves again, Black replies, and White checkmates**, three White moves in all. Each puzzle has exactly one first move that wins by force. Solutions show the full tree: every Black defence and the mating line that answers it.",
 how="""Three-move mates cannot be seen at a glance, so structure your calculation:

1. Write down the **candidate moves**: checks first, then moves that threaten a mate in 2.
2. For each candidate, find Black's most stubborn replies, not the obvious ones.
3. Aim for a **forcing sequence**: every move leaves Black few legal replies, so the tree stays small.
4. Verify the line to the end before you play it. One missed defence ruins the whole idea.

If you cannot find the key, look at the hint: it only names the piece that moves first.""",
 next="Return to [mate in 2](/chess/puzzles/mate-in-2/) to build pattern speed, or study [endgame technique](/chess/endgames/) so that the final mates feel automatic.",
 faq=[("How hard are mate in 3 puzzles?", "Much harder than mate in 2, because the tree is wider and the key move is often quiet. Beginners may need ten minutes or more per puzzle; that is normal."),
      ("Is there more than one solution?", "The first move is unique in every puzzle on this page. Later moves can sometimes be replaced by another mate, but only one line is shown per defence."),
      ("What should I do if I cannot solve one?", "Open the hint, then study the solution move by move. Setting the position up on a board and playing the key move yourself is the fastest way to remember the pattern.")])

# ─────────── CỜ VUA · VI ───────────
G['vi']['ch1'] = dict(
 title='Bài tập cờ vua: chiếu hết 1 nước, 6 thế cờ có đáp án',
 crumb='Chiếu hết 1 nước', h1='Bài tập cờ vua: chiếu hết sau 1 nước',
 description='Sáu bài tập cờ vua chiếu hết sau một nước có gợi ý và đáp án. Mỗi thế chỉ có đúng một nước chiếu hết, được kiểm chứng bằng bộ luật của Cờ vua 3D.',
 blurb='Sáu thế chiếu hết một nước: tìm nước chiếu duy nhất.',
 intro="Ở mọi thế cờ dưới đây **Trắng đi trước** và có thể chiếu hết **chỉ bằng một nước**. Mỗi bài có đúng một nước như vậy, nghĩa là bạn cần tìm nước chiếu duy nhất mà Vua Đen không thoát được. Hãy che đáp án lại, suy nghĩ thong thả và mở gợi ý nếu bị kẹt.",
 how=CHK_HOW_VI,
 next="Muốn khó hơn? Thử [bài tập chiếu hết 2 nước](/vi/co-vua/chieu-het-2-nuoc/), hoặc ôn lại [luật hết nước đi và chiếu hết](/vi/co-vua/het-nuoc-di/). Bạn cũng có thể luyện trên bàn cờ thật với [Cờ vua 3D](https://chess3d.online).",
 faq=[("Bài tập chiếu hết 1 nước là gì?", "Là thế cờ mà bên đến lượt có thể chiếu hết bằng đúng một nước. Ở mỗi bài trong bộ này chỉ có một nước như vậy."),
      ("Làm sao tìm nước chiếu hết trong một nước?", "Liệt kê mọi nước chiếu trước, rồi kiểm tra từng nước: Vua có chạy được không, quân chiếu có bị ăn được không, có chặn được không? Nước chiếu mà mọi câu trả lời đều là không chính là nước chiếu hết."),
      ("Các bài này có lấy từ ván thật không?", "Không. Chúng do máy sinh ra và được bộ luật của Cờ vua 3D kiểm chứng, nên mỗi bài chắc chắn chỉ có một đáp án. Đây là thế cờ luyện tập, không phải thế cờ nổi tiếng.")])
G['vi']['ch2'] = dict(
 title='Bài tập cờ vua: chiếu hết 2 nước, 8 thế cờ có đáp án',
 crumb='Chiếu hết 2 nước', h1='Bài tập cờ vua: chiếu hết sau 2 nước',
 description='Tám bài tập cờ vua chiếu hết sau hai nước có gợi ý và lời giải đầy đủ. Mỗi bài có một nước đầu tiên duy nhất, mọi cách đỡ của Đen đều được chỉ ra bị chiếu hết.',
 blurb='Tám thế chiếu hết hai nước, mỗi bài một nước then chốt và mọi cách đỡ đều bị phá.',
 intro="Ở mỗi bài **Trắng đi, Đen đáp bằng bất kỳ nước nào, rồi Trắng chiếu hết**. Chỉ có đúng một nước đầu tiên làm được điều đó dù Đen đáp thế nào, gọi là **nước then chốt**. Nước này thường là nước đi yên tĩnh: không chiếu, không ăn quân, nhưng lấy đi những ô thoát cuối cùng hoặc tạo ra một đe doạ không đỡ được.",
 how="""Bài chiếu hết hai nước nên giải theo hướng ngược lại. Hãy làm theo trình tự này:

1. Hình dung thế cờ cuối cùng: quân nào chiếu hết và những ô nào phải bị khống chế?
2. Tìm một nước yên tĩnh **đe doạ** nước chiếu hết đó. Nếu Đen không chặn được đe doạ thì bạn đã gần đến đáp án.
3. Thử mọi nước đáp của Đen, kể cả những nước khó chịu: chạy Vua, ăn quân tấn công, chặn đường, hoặc chiếu lại. Nước then chốt chỉ đúng khi **tất cả** đều thất bại.
4. Nếu một nước đáp bác bỏ ý tưởng của bạn, hãy bỏ nó và thử nước khác. Chỉ có một ứng viên sống sót.

Đáp án liệt kê mọi nước đáp hợp lệ của Đen cùng nước chiếu hết đi sau.""",
 next="Cấp độ tiếp theo: [bài tập chiếu hết 3 nước](/vi/co-vua/chieu-het-3-nuoc/). Muốn hiểu vì sao các thế này lặp lại, hãy xem [bài tập chiếu hết 1 nước](/vi/co-vua/chieu-het-1-nuoc/) và [cách chơi cờ vua](/vi/co-vua/cach-choi/).",
 faq=[("Nước then chốt trong bài tập cờ vua là gì?", "Là nước đi đầu tiên duy nhất thắng bằng cách ép buộc. Trong bài chiếu hết 2 nước, đó thường là một nước yên tĩnh khiến Đen không còn cách phòng thủ."),
      ("Vì sao nước đầu tiên thường không phải nước chiếu?", "Nước chiếu làm Đen có ít lựa chọn nhưng lại cho Vua chạy thoát. Một nước yên tĩnh lấy mất ô thoát có thể đẩy Đen vào thế mà nước nào cũng thua."),
      ("Làm sao giải nhanh hơn?", "Giải theo mẫu. Sau vài chục bài, bạn sẽ nhận ra ngay các thế chiếu hết hàng cuối, chiếu hết nghẹt và chiếu hết kiểu bậc thang, rồi chỉ cần tìm nước yên tĩnh chuẩn bị cho chúng.")])
G['vi']['ch3'] = dict(
 title='Bài tập cờ vua: chiếu hết 3 nước, 6 thế cờ khó có đáp án',
 crumb='Chiếu hết 3 nước', h1='Bài tập cờ vua: chiếu hết sau 3 nước',
 description='Sáu bài tập cờ vua chiếu hết sau ba nước (khó) có gợi ý và mọi cách đỡ của Đen đều được giải đến chiếu hết. Mỗi bài chỉ có một nước đầu tiên đúng.',
 blurb='Sáu thế chiếu hết ba nước: tính sâu hơn và tìm nước mở đầu duy nhất.',
 intro="Các bài này khó hơn: **Trắng đi, Đen đáp, Trắng đi tiếp, Đen đáp, rồi Trắng chiếu hết**, tổng cộng ba nước của Trắng. Mỗi bài có đúng một nước đầu tiên thắng bằng cách ép buộc. Đáp án trình bày đầy đủ cây nước đi: mọi cách phòng thủ của Đen và đường chiếu hết đáp lại.",
 how="""Chiếu hết ba nước không thể nhìn ra trong một cái liếc mắt, vì vậy hãy tính có cấu trúc:

1. Ghi ra các **nước ứng viên**: nước chiếu trước, rồi những nước đe doạ chiếu hết sau 2 nước.
2. Với mỗi ứng viên, tìm những nước đáp **ngoan cố nhất** của Đen chứ không chỉ nước hiển nhiên.
3. Nhắm tới **chuỗi ép buộc**: mỗi nước chỉ để Đen vài nước đáp hợp lệ, nên cây tính toán nhỏ lại.
4. Kiểm tra đường đi đến cùng trước khi chốt. Chỉ cần bỏ sót một cách phòng thủ là ý tưởng hỏng.

Nếu chưa tìm ra, hãy mở gợi ý: gợi ý chỉ nói quân nào đi trước.""",
 next="Quay lại [chiếu hết 2 nước](/vi/co-vua/chieu-het-2-nuoc/) để tăng tốc nhận mẫu, hoặc xem [bài tập chiếu hết 1 nước](/vi/co-vua/chieu-het-1-nuoc/) để ôn lại cách tìm nước chiếu.",
 faq=[("Bài chiếu hết 3 nước khó đến mức nào?", "Khó hơn nhiều so với 2 nước vì cây nước đi rộng hơn và nước then chốt thường yên tĩnh. Người mới có thể mất mười phút hoặc hơn cho mỗi bài, đó là bình thường."),
      ("Có nhiều hơn một đáp án không?", "Nước đầu tiên là duy nhất ở mọi bài trong trang này. Các nước sau đôi khi có thể thay bằng một nước chiếu hết khác, nhưng mỗi cách đỡ chỉ trình bày một đường."),
      ("Nếu giải không ra thì làm gì?", "Mở gợi ý rồi đọc đáp án từng nước. Đặt thế cờ lên bàn cờ và tự đi nước then chốt là cách nhanh nhất để nhớ mẫu này.")])

# ─────────── CỜ TƯỚNG · EN ───────────
G['en']['xq1'] = dict(
 title='Xiangqi Puzzles: Mate in 1, Six Checkmate-in-One Puzzles with Solutions',
 crumb='Mate in 1', h1='Xiangqi Mate in 1 Puzzles',
 description='Six verified xiangqi (Chinese chess) mate-in-one puzzles with hints and solutions. Each position has exactly one checkmating move, confirmed by the Xiangqi 3D rules engine.',
 blurb='Six one-move checkmates: find the only move that mates the general.',
 intro="In every position below it is **Red's move** and Red can checkmate the Black general **in one move**. Each puzzle has exactly one such move. " + XQ_RULES_EN,
 how="""Xiangqi checkmates are short because the general never leaves the palace. Use this checklist:

1. List Red's checks. Chariots check along files and ranks, cannons check by jumping exactly one screen, horses check with an L-jump, soldiers check from the front or side once across the river.
2. Count the general's flight squares inside the palace. Remember the **flying general** rule: the general cannot step onto a file that faces the other general with nothing in between.
3. Can the checking piece be captured, or the check blocked? A horse can be blocked by a piece next to it (the "horse leg"), and a cannon check needs exactly one screen that Black may be able to remove.
4. Pick the check that passes all three tests. Only one move does.""",
 next="Move on to [mate in 2](/xiangqi/puzzles/mate-in-2/), or review the [checkmate patterns](/xiangqi/checkmate-patterns/) and the [piece guides](/xiangqi/pieces/).",
 faq=[("What is a mate in 1 puzzle in xiangqi?", "A position where Red can checkmate the Black general with a single move. In this set each puzzle has exactly one such move."),
      ("Does stalemate count as a win in xiangqi?", "Yes: a player with no legal move loses, even without being in check. Every solution on this page, however, ends in a real checkmate."),
      ("How do I find the mating move?", "List the checks first, then count the general's exits, remembering the flying-general rule and the horse leg. The check that leaves no exit and cannot be captured or blocked is the answer.")])
G['en']['xq2'] = dict(
 title='Xiangqi Puzzles: Mate in 2, Eight Checkmate-in-Two Puzzles with Solutions',
 crumb='Mate in 2', h1='Xiangqi Mate in 2 Puzzles',
 description='Eight verified xiangqi mate-in-two puzzles with hints and full solutions: one winning first move each, every Black defence shown being checkmated.',
 blurb='Eight two-move checkmates, each with a single key move and every defence refuted.',
 intro="In each puzzle **Red moves, Black replies with anything, and Red checkmates**. Exactly one first move works against every defence: the **key move**. " + XQ_RULES_EN,
 how="""Solve a mate in 2 from the end:

1. Picture the mating position. Which piece gives the final check, and which flight squares must already be covered?
2. Look for a move that makes that mate a **threat**, often a quiet move that brings a chariot, horse or cannon into position.
3. Test every Black reply: moving the general, capturing, blocking, counter-checking. The key works only if all of them lose.
4. In xiangqi also test Black's blocks on the "horse leg" and the "elephant eye"; defenders often use them.

The solution shows every legal Black reply and the checkmate that follows.""",
 next="Next level: [mate in 3 puzzles](/xiangqi/puzzles/mate-in-3/). The ideas behind these mates are explained in the [xiangqi tactics guide](/xiangqi/tactics/).",
 faq=[("What is the key move?", "The only first move that wins by force. In many mate-in-2 puzzles it is a quiet move that does not give check."),
      ("Why can't I just check every move?", "A check forces a reply, but if Black answers with a capture or the general steps away, the attack fizzles. The key move must beat every legal answer."),
      ("Which pieces mate most often?", "In these puzzles the chariot and cannon do most of the work, with the horse closing the last square. The mating pieces differ in every position, so recognise patterns rather than memorising pieces.")])
G['en']['xq3'] = dict(
 title='Xiangqi Puzzles: Mate in 3, Hard Checkmate-in-Three Puzzles',
 crumb='Mate in 3', h1='Xiangqi Mate in 3 Puzzles',
 description='Hard verified xiangqi mate-in-three puzzles with hints and every Black defence solved to checkmate. Exactly one winning first move in each puzzle.',
 blurb='Hard three-move checkmates: calculate deeper and find the single winning start.',
 intro="These are harder: **Red moves, Black replies, Red moves again, Black replies, and Red checkmates**, three Red moves in all. Each puzzle has exactly one first move that wins by force. " + XQ_RULES_EN,
 how="""Three-move mates need structured calculation:

1. List **forcing candidates**: checks first, then moves that threaten checkmate in 2.
2. Against each candidate, look for Black's toughest replies rather than the obvious ones.
3. Prefer sequences where each Red move leaves Black one or two legal replies. The tree stays small enough to calculate.
4. Check the end of every line: a general that has no legal move wins for Red, but only a checkmate counts as a solution on this page.

If you are stuck, open the hint. It only names the piece that moves first.""",
 next="Go back to [mate in 2](/xiangqi/puzzles/mate-in-2/) to build speed, or learn how long attacks end in [perpetual check and repetition](/xiangqi/perpetual-check-and-repetition/).",
 faq=[("How hard are xiangqi mate in 3 puzzles?", "Much harder than mate in 2: the tree is wider and the key move may be quiet. Taking ten minutes or more is normal while you are learning."),
      ("Can there be two ways to mate at the last move?", "Sometimes. The first move is unique in every puzzle; at the last move another mating move may exist for some lines, and one is shown."),
      ("What should I do if I cannot solve one?", "Use the hint, then replay the solution on a board. Seeing the key move played is the fastest way to remember the pattern.")])

# ─────────── CỜ TƯỚNG · VI ───────────
G['vi']['xq1'] = dict(
 title='Bài tập cờ tướng: chiếu bí 1 nước, 6 thế cờ có đáp án',
 crumb='Chiếu bí 1 nước', h1='Bài tập cờ tướng: chiếu bí sau 1 nước',
 description='Sáu bài tập cờ tướng chiếu bí sau một nước có gợi ý và đáp án. Mỗi thế chỉ có đúng một nước chiếu bí, được kiểm chứng bằng bộ luật của Cờ tướng 3D.',
 blurb='Sáu thế chiếu bí một nước: tìm nước chiếu bí tướng duy nhất.',
 intro="Ở mọi thế cờ dưới đây **Đỏ đi trước** và có thể chiếu bí tướng Đen **chỉ bằng một nước**. Mỗi bài có đúng một nước như vậy. " + XQ_RULES_VI,
 how="""Chiếu bí trong cờ tướng ngắn gọn vì tướng không rời khỏi cung. Hãy dùng danh sách kiểm tra này:

1. Liệt kê các nước chiếu của Đỏ. Xe chiếu theo đường dọc và ngang, Pháo chiếu bằng cách nhảy qua đúng một quân làm ngòi, Mã chiếu bằng nước nhảy chữ L, Tốt chiếu từ phía trước hoặc bên cạnh khi đã qua sông.
2. Đếm các điểm tướng có thể chạy trong cung. Nhớ luật **hai tướng không được đối mặt**: tướng không được bước sang đường dọc mà hai tướng nhìn thẳng nhau không có quân chặn.
3. Quân chiếu có bị ăn được không, nước chiếu có chặn được không? Mã bị chặn khi có quân đứng ngay cạnh (cản chân Mã), còn nước chiếu bằng Pháo cần đúng một quân làm ngòi mà Đen có thể gỡ đi.
4. Chọn nước chiếu vượt qua cả ba bước. Chỉ có một nước như vậy.""",
 next="Tiếp theo là [chiếu bí 2 nước](/vi/co-tuong/chieu-bi-2-nuoc/), hoặc ôn lại [các thế chiếu bí](/vi/co-tuong/the-chieu-bi/) và [các quân cờ](/vi/co-tuong/cac-quan-co/).",
 faq=[("Bài tập chiếu bí 1 nước trong cờ tướng là gì?", "Là thế cờ mà Đỏ có thể chiếu bí tướng Đen chỉ bằng một nước. Mỗi bài trong bộ này có đúng một nước như vậy."),
      ("Tướng hết nước đi mà không bị chiếu có tính là thắng không?", "Có: bên không còn nước đi hợp lệ thì thua, dù không bị chiếu. Tuy nhiên mọi đáp án trong trang này đều kết thúc bằng một thế chiếu bí thật."),
      ("Làm sao tìm nước chiếu bí?", "Liệt kê các nước chiếu, rồi đếm lối thoát của tướng, nhớ luật hai tướng đối mặt và cản chân Mã. Nước chiếu không còn lối thoát và không thể bị ăn hay chặn chính là đáp án.")])
G['vi']['xq2'] = dict(
 title='Bài tập cờ tướng: chiếu bí 2 nước, 8 thế cờ có đáp án',
 crumb='Chiếu bí 2 nước', h1='Bài tập cờ tướng: chiếu bí sau 2 nước',
 description='Tám bài tập cờ tướng chiếu bí sau hai nước có gợi ý và lời giải đầy đủ: mỗi bài một nước đầu tiên duy nhất, mọi cách đỡ của Đen đều bị chiếu bí.',
 blurb='Tám thế chiếu bí hai nước, mỗi bài một nước then chốt và mọi cách đỡ đều bị phá.',
 intro="Ở mỗi bài **Đỏ đi, Đen đáp bằng bất kỳ nước nào, rồi Đỏ chiếu bí**. Chỉ có đúng một nước đầu tiên thắng được trước mọi cách đỡ: **nước then chốt**. " + XQ_RULES_VI,
 how="""Giải bài chiếu bí hai nước theo hướng từ cuối về đầu:

1. Hình dung thế chiếu bí cuối cùng. Quân nào chiếu lần cuối và những điểm thoát nào phải đã bị khống chế?
2. Tìm nước biến nước chiếu bí đó thành **đe doạ**, thường là một nước yên tĩnh đưa Xe, Mã hoặc Pháo vào vị trí.
3. Thử mọi nước đáp của Đen: tướng chạy, ăn quân, chặn, chiếu lại. Nước then chốt chỉ đúng khi tất cả đều thua.
4. Trong cờ tướng, hãy thử cả các cách chặn bằng "cản chân Mã" và "cản mắt Tượng", vì bên phòng thủ hay dùng chúng.

Đáp án liệt kê mọi nước đáp hợp lệ của Đen và nước chiếu bí đi sau.""",
 next="Cấp độ tiếp theo: [chiếu bí 3 nước](/vi/co-tuong/chieu-bi-3-nuoc/). Ý tưởng của các thế này được giải thích trong [các thế chiếu bí](/vi/co-tuong/the-chieu-bi/).",
 faq=[("Nước then chốt là gì?", "Là nước đi đầu tiên duy nhất thắng bằng cách ép buộc. Ở nhiều bài chiếu bí 2 nước đó là một nước yên tĩnh, không chiếu."),
      ("Sao không thử chiếu liên tục mọi nước?", "Nước chiếu buộc đối phương phải đáp, nhưng nếu Đen ăn quân hoặc tướng bước ra khỏi chỗ chiếu thì đòn tấn công tan. Nước then chốt phải thắng mọi nước đáp hợp lệ."),
      ("Quân nào hay chiếu bí nhất?", "Trong các bài này Xe và Pháo làm phần lớn công việc, còn Mã đóng nốt điểm thoát cuối. Quân chiếu bí khác nhau ở từng thế, nên hãy nhận ra mẫu thay vì học thuộc theo quân.")])
G['vi']['xq3'] = dict(
 title='Bài tập cờ tướng: chiếu bí 3 nước, thế cờ khó có đáp án',
 crumb='Chiếu bí 3 nước', h1='Bài tập cờ tướng: chiếu bí sau 3 nước',
 description='Các bài tập cờ tướng chiếu bí sau ba nước (khó) có gợi ý, mọi cách đỡ của Đen đều được giải đến chiếu bí. Mỗi bài chỉ có một nước đầu tiên đúng.',
 blurb='Thế chiếu bí ba nước khó: tính sâu hơn và tìm nước mở đầu duy nhất.',
 intro="Các bài này khó hơn: **Đỏ đi, Đen đáp, Đỏ đi tiếp, Đen đáp, rồi Đỏ chiếu bí**, tổng cộng ba nước của Đỏ. Mỗi bài có đúng một nước đầu tiên thắng bằng cách ép buộc. " + XQ_RULES_VI,
 how="""Chiếu bí ba nước cần tính toán có cấu trúc:

1. Liệt kê **nước ứng viên ép buộc**: nước chiếu trước, rồi những nước đe doạ chiếu bí sau 2 nước.
2. Với mỗi ứng viên, tìm những nước đáp khó chịu nhất của Đen chứ không chỉ nước hiển nhiên.
3. Ưu tiên chuỗi mà mỗi nước của Đỏ chỉ để Đen một hai nước đáp hợp lệ. Khi đó cây tính toán đủ nhỏ để tính hết.
4. Kiểm tra phần cuối của mọi đường: tướng hết nước đi cũng là Đỏ thắng, nhưng trang này chỉ tính đáp án là chiếu bí thật.

Nếu bí, hãy mở gợi ý. Gợi ý chỉ cho biết quân nào đi trước.""",
 next="Quay lại [chiếu bí 2 nước](/vi/co-tuong/chieu-bi-2-nuoc/) để tăng tốc, hoặc đọc về [chiếu dai và lặp thế](/vi/co-tuong/phao-dau/) và [các lỗi thường gặp](/vi/co-tuong/loi-thuong-gap/).",
 faq=[("Chiếu bí 3 nước trong cờ tướng khó đến đâu?", "Khó hơn nhiều so với 2 nước: cây nước đi rộng hơn và nước then chốt có thể là nước yên tĩnh. Mất mười phút hoặc hơn cho một bài là bình thường khi còn đang học."),
      ("Cuối đường có thể có hai cách chiếu bí không?", "Đôi khi có. Nước đầu tiên là duy nhất ở mọi bài; ở nước cuối của một số đường có thể có nước chiếu bí khác, và trang chỉ nêu một nước."),
      ("Nếu không giải được thì sao?", "Dùng gợi ý, rồi đi lại đáp án trên bàn cờ. Tự đi nước then chốt là cách nhanh nhất để nhớ mẫu.")])

# ─────────── HUB ───────────
H['en']['ch'] = dict(
 title='Chess Puzzles with Solutions: Mate in 1, 2 and 3', crumb='Puzzles', h1='Chess Puzzles with Solutions',
 description='Free chess checkmate puzzles: mate in 1, mate in 2 and mate in 3, each with a hint and a full solution. Every position is verified by a rules engine.',
 intro="Checkmate puzzles are the fastest way to improve at chess: they train you to see forcing lines, count escape squares and calculate every defence. These sets go from **mate in 1** to **mate in 3**, with a hint and a full solution for every position.",
 method="Each puzzle was generated by computer and proven with the Chess 3D rules engine: exactly one winning first move, and every defence solved to checkmate. Solutions are produced from the engine's search tree, not typed by hand, so they cannot contain a mistake in the notation or a missed defence.",
 more="To go from puzzles to games, learn the [basic checkmates](/chess/checkmates/), read about [tactics](/chess/tactics/), and play the Royal AI in [Chess 3D](https://chess3d.online).",
 faq=[("How should I practise chess puzzles?", "Start with mate in 1 until you find the answers in seconds, then move to mate in 2 and mate in 3. Cover the solution, spend a fixed time on each puzzle, and review the ones you missed."),
      ("Are these puzzles free?", "Yes. All puzzles, hints and solutions on this site are free, with no sign-up."),
      ("Why are the positions not from famous games?", "They are generated and verified so every solution is guaranteed correct. Nothing is copied from books or databases.")])
H['vi']['ch'] = dict(
 title='Bài tập cờ vua có đáp án: chiếu hết 1, 2 và 3 nước', crumb='Bài tập', h1='Bài tập cờ vua có đáp án',
 description='Bài tập chiếu hết cờ vua miễn phí: chiếu hết 1 nước, 2 nước và 3 nước, mỗi bài có gợi ý và đáp án đầy đủ. Mọi thế cờ đều được kiểm chứng bằng bộ luật.',
 intro="Giải thế chiếu hết là cách nhanh nhất để tiến bộ ở cờ vua: nó luyện bạn nhìn ra chuỗi nước ép buộc, đếm ô thoát của Vua và tính mọi cách phòng thủ. Các bộ bài dưới đây đi từ **chiếu hết 1 nước** đến **chiếu hết 3 nước**, mỗi thế đều có gợi ý và đáp án đầy đủ.",
 method="Mỗi bài do máy sinh ra và được bộ luật của Cờ vua 3D chứng minh: đúng một nước đầu tiên thắng, và mọi cách phòng thủ đều được giải đến chiếu hết. Đáp án được tạo từ cây tìm kiếm của engine, không gõ tay, nên không thể sai ký hiệu hay bỏ sót cách đỡ.",
 more="Để chuyển từ bài tập sang ván cờ, hãy học [nhập thành](/vi/co-vua/nhap-thanh/), [cách chơi](/vi/co-vua/cach-choi/) và đấu với máy Royal AI trong [Cờ vua 3D](https://chess3d.online).",
 faq=[("Nên luyện bài tập cờ vua thế nào?", "Bắt đầu với chiếu hết 1 nước đến khi giải trong vài giây, rồi sang 2 nước và 3 nước. Che đáp án, đặt giới hạn thời gian cho mỗi bài và xem lại những bài làm sai."),
      ("Các bài này có miễn phí không?", "Có. Mọi bài tập, gợi ý và đáp án trên trang đều miễn phí, không cần đăng ký."),
      ("Vì sao thế cờ không lấy từ ván nổi tiếng?", "Chúng do máy sinh ra và kiểm chứng để mọi đáp án đều chắc chắn đúng. Không có gì được chép từ sách hay cơ sở dữ liệu.")])
H['en']['xq'] = dict(
 title='Xiangqi Puzzles with Solutions: Mate in 1, 2 and 3', crumb='Puzzles', h1='Xiangqi Puzzles with Solutions',
 description='Free xiangqi (Chinese chess) checkmate puzzles: mate in 1, 2 and 3, each with a hint and full solution. Every position is verified by the game rules engine.',
 intro="Xiangqi puzzles teach you how chariots, cannons and horses combine to trap a general in the palace. These sets go from **mate in 1** to **mate in 3**, each with a hint and a full solution.",
 method="Each puzzle was generated by computer and proven with the Xiangqi 3D rules engine, flying-general rule included: exactly one winning first move, and every defence solved to a real checkmate. Solutions come from the engine's search tree, not from memory.",
 more="Learn the building blocks first: [checkmate patterns](/xiangqi/checkmate-patterns/), [how the pieces move](/xiangqi/pieces/) and [notation](/xiangqi/notation/). Then practise against the Royal AI in [Xiangqi 3D](https://xiangqi3d.online).",
 faq=[("How do I practise xiangqi puzzles?", "Start with mate in 1, then mate in 2 and 3. Cover the solution, set a time limit, and replay missed puzzles on a board."),
      ("Are the puzzles free?", "Yes, all puzzles, hints and solutions are free, with no sign-up."),
      ("Are these classic endgame positions?", "No. They are generated and verified positions, so every answer is guaranteed correct. For classic ideas, see the checkmate patterns page.")])
H['vi']['xq'] = dict(
 title='Bài tập cờ tướng có đáp án: chiếu bí 1, 2 và 3 nước', crumb='Bài tập', h1='Bài tập cờ tướng có đáp án',
 description='Bài tập chiếu bí cờ tướng miễn phí: chiếu bí 1 nước, 2 nước và 3 nước, mỗi bài có gợi ý và đáp án đầy đủ. Mọi thế cờ đều được kiểm chứng bằng bộ luật của game.',
 intro="Các bài tập cờ tướng giúp bạn hiểu Xe, Pháo và Mã phối hợp thế nào để nhốt tướng trong cung. Các bộ bài đi từ **chiếu bí 1 nước** đến **chiếu bí 3 nước**, mỗi bài đều có gợi ý và đáp án đầy đủ.",
 method="Mỗi bài do máy sinh ra và được bộ luật của Cờ tướng 3D chứng minh, kể cả luật hai tướng đối mặt: đúng một nước đầu tiên thắng, và mọi cách phòng thủ đều được giải đến chiếu bí thật. Đáp án lấy từ cây tìm kiếm của engine, không chép theo trí nhớ.",
 more="Hãy học nền tảng trước: [các thế chiếu bí](/vi/co-tuong/the-chieu-bi/), [cách đi của các quân](/vi/co-tuong/cac-quan-co/) và [cách ghi nước đi](/vi/co-tuong/ghi-nuoc-di/). Sau đó luyện với máy Royal AI trong [Cờ tướng 3D](https://xiangqi3d.online).",
 faq=[("Nên luyện bài tập cờ tướng thế nào?", "Bắt đầu với chiếu bí 1 nước, rồi sang 2 và 3 nước. Che đáp án, đặt giới hạn thời gian và đi lại những bài làm sai trên bàn cờ."),
      ("Các bài này có miễn phí không?", "Có. Mọi bài tập, gợi ý và đáp án đều miễn phí, không cần đăng ký."),
      ("Đây có phải các thế tàn cuộc kinh điển không?", "Không. Đây là thế do máy sinh và kiểm chứng, nên mọi đáp án đều chắc chắn đúng. Muốn xem ý tưởng kinh điển, hãy đọc trang các thế chiếu bí.")])

# ─────────── HUB: đoạn "vì sao nên luyện" (thêm sau, tránh trang mỏng) ───────────
H['en']['ch']['why_h'] = 'Why puzzles work'
H['en']['ch']['why'] = "A mate puzzle forces you to do three things every game needs: list the checking moves, count the squares the enemy king can use, and test each defence to the end. Do a few every day and these steps become automatic. Begin with mate in 1 to learn to recognise final patterns, then use mate in 2 and 3 to practise sacrifices and quiet moves, where the key is often not a check."
H['vi']['ch']['why_h'] = 'Vì sao nên luyện bài tập'
H['vi']['ch']['why'] = "Mỗi bài chiếu hết buộc bạn làm ba việc mà ván nào cũng cần: liệt kê các nước chiếu, đếm ô Vua đối phương còn đi được và thử từng cách đỡ đến cùng. Luyện vài bài mỗi ngày, các bước này sẽ thành phản xạ. Bắt đầu với chiếu hết 1 nước để nhận ra các mẫu kết thúc, rồi dùng chiếu hết 2 và 3 nước để tập hy sinh quân và nước đi yên lặng, vì khi đó nước đầu tiên thường không phải là nước chiếu."
H['en']['xq']['why_h'] = 'Why puzzles work'
H['en']['xq']['why'] = "In xiangqi the general is boxed into a small palace, so most wins come from a few repeating mating ideas: a chariot on an open file, a cannon needing a screen, a horse covering the escape squares, and the flying-general rule closing the last gap. Solving puzzles lets you see these ideas many times in a short period. Start with mate in 1 to learn how each piece delivers the final check, then work through mate in 2 and 3, where you must also find which defences exist and answer each of them."
H['vi']['xq']['why_h'] = 'Vì sao nên luyện bài tập'
H['vi']['xq']['why'] = "Trong cờ tướng, tướng bị nhốt trong cung nhỏ nên phần lớn các ván thắng đến từ vài ý tưởng chiếu bí lặp lại: Xe chiếm đường thông, Pháo cần có ngòi, Mã che các ô thoát, và luật hai tướng đối mặt đóng nốt khe hở cuối cùng. Giải bài tập giúp bạn gặp những ý tưởng này nhiều lần trong thời gian ngắn. Hãy bắt đầu với chiếu bí 1 nước để biết mỗi quân tung nước chiếu cuối thế nào, rồi sang 2 và 3 nước, nơi bạn còn phải tìm mọi cách đỡ của đối phương và có đòn đáp cho từng cách."
