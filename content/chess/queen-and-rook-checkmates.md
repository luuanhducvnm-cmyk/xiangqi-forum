---
title: How to Checkmate with King and Queen or King and Rook (Longest Mates Verified)
crumb: Queen and rook mates
h1: How to Checkmate with a Queen or a Rook
description: Learn the basic checkmates: king and queen versus king takes at most 10 moves, king and rook at most 16. Full optimal lines from the worst positions, verified by a tablebase.
path: /chess/queen-and-rook-checkmates/
section: chess
order: 23
related: /chess/endgames/, /chess/king-and-pawn-endgames/, /chess/checkmates/
faq:
- How many moves does it take to checkmate with king and queen against king? | At most 10 moves with best play, from the worst starting position. Most positions are much faster.
- How many moves does king and rook take? | At most 16 moves with best play from the worst position.
- What is the biggest danger when mating with a queen? | Stalemate. If you take away every square from the lone king while it is not in check, the game is drawn. Always leave the king one legal move until you give checkmate.
---

You must be able to checkmate with a queen or a rook against a bare king. Both are forced wins, and they teach the idea you will use in many other endgames: **shrink the box**, bring your king, then deliver mate. This page gives the technique and the longest possible mates. **All numbers and lines were computed by a tablebase built with the Chess 3D rules engine**, which solves every position of king and queen (or rook) against king exhaustively. It reproduces the well-known maxima: 10 moves for the queen, 16 for the rook.

## King and queen against king

The queen takes away many squares at once, so the technique is to restrict the king with a queen's "knight's-move" distance and then bring your own king close. The longest possible mate takes **10 moves**:

{{img:ch-kqk-worst|White to move; with best play from this position White needs 10 moves to checkmate.}}

One optimal line from the tablebase (Black plays the longest resistance):

1. Kb1 Ke6 2. Kc2 Kf5 3. Qb4 Kg5 4. Kd3 Kf5 5. Qd6 Kg4 6. Ke3 Kg5 7. Ke4 Kg4 8. Qg6+ Kh4 9. Kf4 Kh3 10. Qg3#

Notice that the winning side first brings the king and uses queen moves that keep the black king boxed in, and that the black king is never left without a move (that would be stalemate).

**Rule of thumb:** never give a check unless it improves the box, and before each queen move ask "does the lone king still have a legal move?"

## King and rook against king

The rook is slower: it needs the king's help to build a "box" and then pushes the lone king to the edge. The longest mate with a rook takes **16 moves**:

{{img:ch-krk-worst|White to move; with best play from this position White needs 16 moves to checkmate.}}

An optimal line from the tablebase:

1. Kb1 Kd4 2. Kc2 Ke4 3. Rb4+ Ke5 4. Kd3 Ke6 5. Kd4 Kd6 6. Rb6+ Kc7 7. Kc5 Kd7 8. Rd6+ Ke7 9. Kc6 Ke8 10. Rd7 Kf8 11. Kd6 Kg8 12. Ke6 Kf8 13. Kf6 Kg8 14. Rc7 Kh8 15. Kg6 Kg8 16. Rc8#

The pattern is a "ladder": the rook checks, the king steps up, and the lone king is pushed to the edge, where the opposition and a rook check give mate.

## How to practise

- Set up the two positions above and mate from them in the fewest moves you can.
- Do the mate with a time limit (under 10 moves for queen, under 20 for rook).
- Read [basic checkmates](/chess/checkmates/) to see the final patterns, and the [endgames overview](/chess/endgames/) for the next step.
- Practise against the Royal AI on [Chess 3D](https://chess3d.online).

For king and pawn endings, see the companion page on [opposition and key squares](/chess/king-and-pawn-endgames/).

{{cta:chess}}
