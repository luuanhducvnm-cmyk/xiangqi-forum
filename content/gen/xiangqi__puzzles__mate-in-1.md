---
title: Xiangqi Puzzles: Mate in 1, Six Checkmate-in-One Puzzles with Solutions
crumb: Mate in 1
h1: Xiangqi Mate in 1 Puzzles
description: Six verified xiangqi (Chinese chess) mate-in-one puzzles with hints and solutions. Each position has exactly one checkmating move, confirmed by the Xiangqi 3D rules engine.
path: /xiangqi/puzzles/mate-in-1/
section: xiangqi
order: 31
alt: vi=/vi/co-tuong/chieu-bi-1-nuoc/
related: /xiangqi/puzzles/, /xiangqi/puzzles/mate-in-2/, /xiangqi/puzzles/mate-in-3/
faq:
- What is a mate in 1 puzzle in xiangqi? | A position where Red can checkmate the Black general with a single move. In this set each puzzle has exactly one such move.
- Does stalemate count as a win in xiangqi? | Yes: a player with no legal move loses, even without being in check. Every solution on this page, however, ends in a real checkmate.
- How do I find the mating move? | List the checks first, then count the general's exits, remembering the flying-general rule and the horse leg. The check that leaves no exit and cannot be captured or blocked is the answer.
---

In every position below it is **Red's move** and Red can checkmate the Black general **in one move**. Each puzzle has exactly one such move. Red is at the bottom of the diagram and moves first. Moves are written in WXF notation (see the [notation guide](/xiangqi/notation/)): for example `R9=4` is the chariot on file 9 moving sideways to file 4. When two identical pieces stand on the same file, `front` and `rear` replace the file number. Red counts files from the right-hand side of the bottom edge; Black counts from the right-hand side of the top edge.

## How to solve these puzzles

Xiangqi checkmates are short because the general never leaves the palace. Use this checklist:

1. List Red's checks. Chariots check along files and ranks, cannons check by jumping exactly one screen, horses check with an L-jump, soldiers check from the front or side once across the river.
2. Count the general's flight squares inside the palace. Remember the **flying general** rule: the general cannot step onto a file that faces the other general with nothing in between.
3. Can the checking piece be captured, or the check blocked? A horse can be blocked by a piece next to it (the "horse leg"), and a cannon check needs exactly one screen that Black may be able to remove.
4. Pick the check that passes all three tests. Only one move does.

## Puzzle 1

{{img:pz-xq1-1|Puzzle 1: Red to move, mate in 1.}}

<details><summary>Hint</summary><p>The first move is made by the chariot and it gives check.</p></details>

<details><summary>Show the solution</summary><p><strong>Solution: 1. R1+4</strong> Only 1 of the 32 legal moves delivers checkmate.</p></details>

## Puzzle 2

{{img:pz-xq1-2|Puzzle 2: Red to move, mate in 1.}}

<details><summary>Hint</summary><p>The first move is made by the cannon and it gives check.</p></details>

<details><summary>Show the solution</summary><p><strong>Solution: 1. C7=6</strong> Only 1 of the 27 legal moves delivers checkmate.</p></details>

## Puzzle 3

{{img:pz-xq1-3|Puzzle 3: Red to move, mate in 1.}}

<details><summary>Hint</summary><p>The first move is made by the horse and it gives check.</p></details>

<details><summary>Show the solution</summary><p><strong>Solution: 1. H7+8</strong> Only 1 of the 13 legal moves delivers checkmate.</p></details>

## Puzzle 4

{{img:pz-xq1-4|Puzzle 4: Red to move, mate in 1.}}

<details><summary>Hint</summary><p>The first move is made by the soldier and it gives check.</p></details>

<details><summary>Show the solution</summary><p><strong>Solution: 1. P7+1</strong> Only 1 of the 26 legal moves delivers checkmate.</p></details>

## Puzzle 5

{{img:pz-xq1-5|Puzzle 5: Red to move, mate in 1.}}

<details><summary>Hint</summary><p>The first move is made by the chariot and it gives check.</p></details>

<details><summary>Show the solution</summary><p><strong>Solution: 1. R2+4</strong> Only 1 of the 51 legal moves delivers checkmate.</p></details>

## Puzzle 6

{{img:pz-xq1-6|Puzzle 6: Red to move, mate in 1.}}

<details><summary>Hint</summary><p>The first move is made by the cannon and it gives check.</p></details>

<details><summary>Show the solution</summary><p><strong>Solution: 1. C8+3</strong> Only 1 of the 24 legal moves delivers checkmate.</p></details>

## How these puzzles were checked

Every position on this page was found by a computer and then checked with the rules engine of Xiangqi 3D, the same code that runs the game, including the flying-general rule. A puzzle is published only if Red has exactly one first move that forces checkmate in 1, and if every legal defence was searched to the end and ended in a real checkmate (a stalemated general, which also loses in xiangqi, is not counted as a solution here). All 6 puzzles passed. No answer was copied from memory or from another site.

{{cta:xiangqi}}

Move on to [mate in 2](/xiangqi/puzzles/mate-in-2/), or review the [checkmate patterns](/xiangqi/checkmate-patterns/) and the [piece guides](/xiangqi/pieces/).
