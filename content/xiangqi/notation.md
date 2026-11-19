---
title: Xiangqi Notation: How to Read and Write Moves (WXF & Chinese)
crumb: Notation
h1: Xiangqi Notation: Reading and Writing Moves
description: Learn xiangqi notation: how files are numbered, what + − = mean, and how to read moves like C2=5 and H8+7 in WXF and traditional Chinese notation.
path: /xiangqi/notation/
section: xiangqi
order: 7
related: /xiangqi/board-setup/, /xiangqi/openings/, /xiangqi/glossary/
faq:
- What does C2=5 mean in xiangqi? | The cannon (C) on file 2 moves horizontally (=) to file 5, the central file. It is the famous "central cannon" opening move.
- Why do both players count files from their own right? | It keeps notation symmetric: each side describes the same move in the same way, as if the board were turned around. The general always starts on file 5.
- Is there a standard computer format for xiangqi games? | Yes. Games are commonly stored in the same kinds of record formats as chess, and the World Xiangqi Federation (WXF) notation is the usual way to write moves in English.
---

Xiangqi moves are written in a compact notation that you can learn in ten minutes. Once you know it, you can read opening books, game records and the examples on this site.

## Step 1: files are numbered from your own right

Files are numbered 1–9 **from each player's right-hand side**. Red counts from the right edge of the board as Red sees it; Black counts from his own right edge, which is the left edge in a normal diagram. See [the board page](/xiangqi/board-setup/). Both generals start on file 5.

## Step 2: write the move in four parts

In the World Xiangqi Federation (WXF) system a move has four parts:

1. The **piece**: K general, A advisor, E elephant, H horse, R chariot, C cannon, P soldier.
2. The **file** it stands on (1–9).
3. The **direction**: `+` forward, `-` backward, `=` sideways (horizontal).
4. A **number** that depends on the piece:
   - For pieces that move **in a straight line** (R, C, P, K): the number of points moved when going forward or backward, or the **destination file** when moving sideways.
   - For pieces that move **diagonally or in an L** (H, E, A): always the **destination file**.

## Examples

| Notation | Meaning |
|---|---|
| `C2=5` | The cannon on file 2 moves sideways to the centre file (Central Cannon). |
| `H2+3` | The horse on file 2 moves forward and lands on file 3. |
| `E3+5` | The elephant on file 3 moves forward to file 5 (the "elephant opening"). |
| `R1+1` | The chariot on file 1 advances one point. |
| `P7+1` | The soldier on file 7 advances one point. |
| `H8+7` | (Black) the horse on file 8 moves forward to file 7. |

Here is the start of a very common game, with both sides' moves:

{{img:xq-screen-horse|After 1. C2=5 H8+7 2. H2+3 H2+3 — Central Cannon against Screen Horse.}}

1. `C2=5 H8+7` — Red plays the central cannon, Black develops the horse on file 8.
2. `H2+3 H2+3` — both sides develop their second horse. Black's two horses and the soldiers on files 3 and 7 now form the "screen" in front of the general.

## Traditional Chinese notation

Chinese players write the same move with characters:

- **Red** uses Chinese numerals: 炮二平五 (cannon on file 2 moves sideways to 5).
- **Black** uses Arabic digits: 馬8進7 (horse on file 8 moves forward to 7).
- 進 (*jìn*) is forward, 退 (*tuì*) backward, 平 (*píng*) horizontal.

The structure is identical to WXF: piece, file, direction, number.

## Two identical pieces on the same file

If two pieces of the same type stand on the same file, the file number is replaced by "front" and "rear" (Chinese: 前 and 後). For example 前車平四 means "the front chariot moves sideways to file 4". WXF writes the same idea with `+` for the front and `-` for the rear.

## Why bother?

- You can follow annotated games and opening books.
- You can write down your own games to review them.
- When you read the [opening guide](/xiangqi/openings/), every line uses this system.

Next, put it to use: [xiangqi openings](/xiangqi/openings/).
