---
title: King and Pawn Endgames: Opposition, Key Squares and the Rook-Pawn Draw
crumb: King and pawn endgames
h1: King and Pawn Endgames: Opposition and Key Squares
description: Learn king and pawn endgames: how the opposition works, which squares win for the king in front of a pawn, why rook pawns draw and the stalemate trap, every claim checked by a tablebase.
path: /chess/king-and-pawn-endgames/
section: chess
order: 22
related: /chess/endgames/, /chess/stalemate/, /chess/queen-and-rook-checkmates/
faq:
- What is the opposition in chess? | Kings face each other with exactly one square between them, on the same file, rank or diagonal. The side that is NOT to move has the opposition, and the other king must give way.
- When does a king and pawn endgame win? | If the attacking king reaches a "key square" in front of the pawn, the pawn promotes even against best defence. If the defending king reaches the pawn's path first, or the pawn is a rook pawn with the defender in the corner, it is usually a draw.
- Why is a rook pawn so hard to win with? | The pawn on the a- or h-file has only one side, so the defending king can sit in the corner and the attacker runs out of squares. The stalemate trick makes the draw even easier.
---

King and pawn against king is the endgame every player must master. It decides games between much stronger positions, because trading down into it is often the way to win or save a game. This page explains the three ideas that matter most: **key squares**, **opposition** and the **rook-pawn draw**. **Every position was verified by a tablebase we built with the Chess 3D rules engine**, which checks every legal position of king and pawn against king exhaustively. Nothing here is quoted from memory.

## 1. Key squares: a king in front of the pawn wins

If the attacking king reaches a key square, the pawn will promote whatever the defender does. Our tablebase confirms these two cases for a pawn on the e-file:

- **Pawn on e5:** key squares are **d6, e6 and f6**.
- **Pawn on e6:** key squares are **d7, e7 and f7**.

For both, White wins **for every legal position of the black king, and whichever side is to move**. This was checked for all legal placements of the black king.

{{img:ch-kpk-key|White king on e6 (a key square for the pawn on e5). White wins whoever is to move.}}

The practical rule: **get your king in front of your pawn**. A king behind its own pawn can usually not win.

## 2. The opposition decides pawn on the fourth and lower ranks

When the key squares cannot be reached at once, the kings fight for the **opposition**: they stand on the same file with one square between them, and the side that has to move must give way. The tablebase gives exact answers for the position below:

{{img:ch-kpk-opp|White king e5, pawn e4, Black king e7. With White to move it is a draw; with Black to move White wins.}}

- **White to move: draw.** White cannot make progress without letting the black king in front of the pawn.
- **Black to move: White wins.** Black must move the king away, and White's king reaches a key square.

The same pattern holds one rank lower for a pawn on e3 with kings on e4 and e6, and for a pawn on e2 with kings on e3 and e5: White to move only draws, Black to move loses. So "who has the move" matters more than anything else.

## 3. The rook pawn: usually a draw

A pawn on the a- or h-file has only one side, so the defending king can hide in the corner. In the position below the pawn is on a6 with the white king on b6, Black to move, and the game is only a draw:

{{img:ch-kpk-rook|Rook pawn: a6 pawn and Kb6 against Ka8 with Black to move is a draw because of stalemate tricks.}}

The tablebase confirms that White cannot force a win here: the defender keeps the king in the corner, and White's winning attempts run into stalemate or lose the pawn. In general, **a rook pawn plus a king cannot win if the defending king reaches the corner in front of the pawn**. Our tablebase confirms draws for these positions with either side to move: the king on b6, pawn on a5, and the black king on a8.

## 4. The stalemate trap

Even with a pawn on the seventh rank White does not always win. Look at this position with White to move:

{{img:ch-kpk-trap|White king f6, pawn e7, Black king e8, White to move: only a draw, because Kf7 stalemates.}}

The natural move 1.Kf7 is **stalemate**, and the tablebase confirms that no other move wins either, so the position is a draw. If the white king stood on e6 instead (pawn on e7, black king on e8, White to move), White would win. See [stalemate](/chess/stalemate/) for the rule.

## What this means in practice

- Aim for positions where your king stands in front of your pawn.
- Count who has the opposition before you push a pawn.
- Avoid rook-pawn endings where the defender's king reaches the corner.
- Always check for stalemate before you move.

To practise, read the other [endgame basics](/chess/endgames/) and learn [how to checkmate with queen or rook](/chess/queen-and-rook-checkmates/). Then play your own endgames on [Chess 3D](https://chess3d.online).

{{cta:chess}}
