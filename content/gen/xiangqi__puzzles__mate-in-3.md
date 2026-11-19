---
title: Xiangqi Puzzles: Mate in 3, Hard Checkmate-in-Three Puzzles
crumb: Mate in 3
h1: Xiangqi Mate in 3 Puzzles
description: Hard verified xiangqi mate-in-three puzzles with hints and every Black defence solved to checkmate. Exactly one winning first move in each puzzle.
path: /xiangqi/puzzles/mate-in-3/
section: xiangqi
order: 33
alt: vi=/vi/co-tuong/chieu-bi-3-nuoc/
related: /xiangqi/puzzles/, /xiangqi/puzzles/mate-in-1/, /xiangqi/puzzles/mate-in-2/
faq:
- How hard are xiangqi mate in 3 puzzles? | Much harder than mate in 2: the tree is wider and the key move may be quiet. Taking ten minutes or more is normal while you are learning.
- Can there be two ways to mate at the last move? | Sometimes. The first move is unique in every puzzle; at the last move another mating move may exist for some lines, and one is shown.
- What should I do if I cannot solve one? | Use the hint, then replay the solution on a board. Seeing the key move played is the fastest way to remember the pattern.
---

These are harder: **Red moves, Black replies, Red moves again, Black replies, and Red checkmates**, three Red moves in all. Each puzzle has exactly one first move that wins by force. Red is at the bottom of the diagram and moves first. Moves are written in WXF notation (see the [notation guide](/xiangqi/notation/)): for example `R9=4` is the chariot on file 9 moving sideways to file 4. When two identical pieces stand on the same file, `front` and `rear` replace the file number. Red counts files from the right-hand side of the bottom edge; Black counts from the right-hand side of the top edge.

## How to solve these puzzles

Three-move mates need structured calculation:

1. List **forcing candidates**: checks first, then moves that threaten checkmate in 2.
2. Against each candidate, look for Black's toughest replies rather than the obvious ones.
3. Prefer sequences where each Red move leaves Black one or two legal replies. The tree stays small enough to calculate.
4. Check the end of every line: a general that has no legal move wins for Red, but only a checkmate counts as a solution on this page.

If you are stuck, open the hint. It only names the piece that moves first.

## Puzzle 1

{{img:pz-xq3-1|Puzzle 1: Red to move, mate in 3.}}

<details><summary>Hint</summary><p>The first move is made by the chariot and it gives check.</p></details>

<details><summary>Show the solution</summary><p><strong>Key move: 1. R1+2</strong> Only 1 of the 46 legal first moves forces mate; every other move lets Black escape or defend.</p><p>Black has 2 legal replies, and each one is checkmated:</p><ul><li>1… E5-7 2. R1=3 2… K6+1 3. H4+3</li><li>1… K6+1 2. H4+3</li></ul></details>

## Puzzle 2

{{img:pz-xq3-2|Puzzle 2: Red to move, mate in 3.}}

<details><summary>Hint</summary><p>The first move is made by the horse and it gives check.</p></details>

<details><summary>Show the solution</summary><p><strong>Key move: 1. H5+4</strong> Only 1 of the 41 legal first moves forces mate; every other move lets Black escape or defend.</p><p>Black has 3 legal replies, and each one is checkmated:</p><ul><li>1… K4+1 2. R9-2 2… E3+1 3. C1-1</li><li>1… K4=5 2. R9-1 2… K5+1 3. C1-1</li><li>1… K4-1 2. R9=7</li></ul></details>

## Puzzle 3

{{img:pz-xq3-3|Puzzle 3: Red to move, mate in 3.}}

<details><summary>Hint</summary><p>The first move is made by the cannon and it gives check.</p></details>

<details><summary>Show the solution</summary><p><strong>Key move: 1. C8=5</strong> Only 1 of the 58 legal first moves forces mate; every other move lets Black escape or defend.</p><p>Black has 2 legal replies, and each one is checkmated:</p><ul><li>1… K5=4 2. R1=6 2… H5+4 3. R6+2</li><li>1… K5=6 2. R1=4 2… H5+6 3. R4+2</li></ul></details>

## Puzzle 4

{{img:pz-xq3-4|Puzzle 4: Red to move, mate in 3.}}

<details><summary>Hint</summary><p>The first move is made by the soldier and it gives check.</p></details>

<details><summary>Show the solution</summary><p><strong>Key move: 1. P5+1</strong> Only 1 of the 49 legal first moves forces mate; every other move lets Black escape or defend.</p><p>Black has 2 legal replies, and each one is checkmated:</p><ul><li>1… K5=4 2. P5=6 2… K4+1 3. R7=6</li><li>1… K5=6 2. C7=4</li></ul></details>

## Puzzle 5

{{img:pz-xq3-5|Puzzle 5: Red to move, mate in 3.}}

<details><summary>Hint</summary><p>The first move is made by the chariot and it gives check.</p></details>

<details><summary>Show the solution</summary><p><strong>Key move: 1. R7+5</strong> Only 1 of the 35 legal first moves forces mate; every other move lets Black escape or defend.</p><p>Black has 3 legal replies, and each one is checkmated:</p><ul><li>1… K6-1 2. H2-3 2… K6=5 3. R7+1</li><li>1… A4-5 2. C8=4</li><li>1… K6+1 2. C8=4</li></ul></details>

## Puzzle 6

{{img:pz-xq3-6|Puzzle 6: Red to move, mate in 3.}}

<details><summary>Hint</summary><p>The first move is made by the horse and it gives check.</p></details>

<details><summary>Show the solution</summary><p><strong>Key move: 1. H5-7</strong> Only 1 of the 20 legal first moves forces mate; every other move lets Black escape or defend.</p><p>Black has 2 legal replies, and each one is checkmated:</p><ul><li>1… K4-1 2. H7+8 2… K4+1 3. rear H+7</li><li>1… K4+1 2. H7+8 2… K4-1 3. rear H+7</li></ul></details>

## How these puzzles were checked

Every position on this page was found by a computer and then checked with the rules engine of Xiangqi 3D, the same code that runs the game, including the flying-general rule. A puzzle is published only if Red has exactly one first move that forces checkmate in 3, and if every legal defence was searched to the end and ended in a real checkmate (a stalemated general, which also loses in xiangqi, is not counted as a solution here). All 6 puzzles passed. No answer was copied from memory or from another site.

{{cta:xiangqi}}

Go back to [mate in 2](/xiangqi/puzzles/mate-in-2/) to build speed, or learn how long attacks end in [perpetual check and repetition](/xiangqi/perpetual-check-and-repetition/).
