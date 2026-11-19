---
title: Chess Notation: How to Read and Write Moves
crumb: Notation
h1: Chess Notation: Reading and Writing Moves
description: Learn algebraic chess notation: squares, piece letters, captures, check, checkmate, castling and promotion — plus a short introduction to FEN and PGN.
path: /chess/notation/
section: chess
order: 6
related: /chess/openings/, /chess/special-moves/, /chess/glossary/
faq:
- What does Nf3 mean? | A knight (N) moves to the square f3. Pieces are written with a capital letter (K, Q, R, B, N); pawns have no letter.
- What is the difference between + and #? | A plus sign (+) means the move gives check. A hash sign (#) means checkmate.
- What is PGN? | Portable Game Notation: a plain-text format that stores the moves and information about a chess game. Most chess software can open it.
---

Notation is the shorthand that lets you read books, follow annotated games and write down your own. Modern chess uses **algebraic notation**.

## The squares

Files (columns) are lettered **a–h** from left to right as seen from White. Ranks (rows) are numbered **1–8** from White's side. Every square has a name: the bottom-left corner is a1, the top-right h8, and the king starts on e1 (White) or e8 (Black).

## Pieces

| Letter | Piece |
|---|---|
| K | King |
| Q | Queen |
| R | Rook |
| B | Bishop |
| N | Knight (K is taken by the king) |
| (none) | Pawn |

## Writing a move

- A **piece move**: letter + destination: `Nf3` (knight to f3), `Bc4`, `Qd1`.
- A **pawn move**: destination only: `e4`, `d5`.
- **Captures** add `x`: `Bxc6` (bishop captures on c6); for pawn captures write the starting file: `exd5`.
- **Check** adds `+`: `Qh5+`; **checkmate** adds `#`: `Qh4#`.
- **Castling**: `O-O` (kingside), `O-O-O` (queenside).
- **Promotion**: `e8=Q` (pawn promotes to a queen on e8).
- **Two identical pieces can move to the same square**: add the file or rank: `Nbd2` or `R1e2`.

## Examples

| Notation | Meaning |
|---|---|
| `e4` | The pawn on e-file goes to e4 |
| `Nf3` | A knight moves to f3 |
| `Bxc6` | A bishop captures a piece on c6 |
| `exd5` | The pawn on the e-file captures on d5 |
| `O-O` | Castles kingside |
| `Qxf7#` | The queen captures on f7 and it is checkmate |
| `e8=Q+` | A pawn promotes to a queen on e8 with check |

Moves are numbered: `1. e4 e5 2. Nf3 Nc6` means White plays e4, Black e5, White Nf3, Black Nc6.

## FEN: describing a position

**FEN** (Forsyth–Edwards Notation) is a single line of text that describes one position. The starting position is:

`rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1`

It lists the ranks from 8 to 1; capital letters are White pieces, lower case Black; digits are empty squares; then whose turn, castling rights, the en passant square and move counters.

## PGN: recording a game

**PGN** (Portable Game Notation) is the standard text format for whole games: a header with names and result, then the moves. Almost every chess program can import and export it.

## Practise

Write down your own games (many apps do this for you), then replay them to find your mistakes. When you are comfortable, read the [opening guide](/chess/openings/): every opening is shown with its moves in this notation.
