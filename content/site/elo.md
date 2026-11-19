---
title: ELO Rating Explained: How Chess and Xiangqi Ratings Work
crumb: ELO ratings
h1: ELO Ratings Explained
description: How the Elo rating system works for chess and xiangqi: the expected-score formula, K-factor, worked examples and how ratings work in Chess 3D and Xiangqi 3D.
path: /elo-rating-explained/
section: site
order: 5
faq:
- What does ELO stand for? | It is not an acronym: it is named after Arpad Elo, the Hungarian-American physicist who developed the system for the US Chess Federation in the 1960s. It is written "Elo" in his honour, but "ELO" is common usage.
- What is a good ELO rating? | It depends on the pool of players. In the games here everyone starts at 1000; 1500 is a strong club-level player, and 1900 and above is expert level. Ratings from different websites are not directly comparable.
- Why did I lose points for a draw? | If you draw with a higher-rated player you gain points; if you draw with a lower-rated player you lose a few. The system expects the stronger player to score more than half.
- Does a draw by agreement change ratings in Chess 3D and Xiangqi 3D? | No. A draw agreed by both players does not change either player's rating in the two games. Draws that arise from the rules (repetition, stalemate in chess, and so on) still count as drawn results.
---

The **Elo rating system** gives every player a number that estimates their strength. It is used in chess, xiangqi, Go, many video games and sports. A higher number means a stronger player; the difference between two ratings predicts the result of a game between them.

## The idea in one sentence

If a player wins more often than the system expects, their rating goes up; if they do worse than expected, it goes down — and the amount depends on how surprising the result was.

## The formula

**Expected score** of player A against player B:

`E_A = 1 / (1 + 10^((R_B − R_A) / 400))`

The result is a number between 0 and 1: the share of points A is expected to score (a win is 1, a draw ½, a loss 0).

**New rating** after a game:

`R_A' = R_A + K × (S_A − E_A)`

where `S_A` is the actual score (1, ½ or 0) and **K** is the maximum change per game.

## Worked examples

| Rating difference | Expected score of the stronger player |
|---|---|
| 0 | 50% |
| 100 | about 64% |
| 200 | about 76% |
| 400 | about 91% |

Example: you are 1500 and your opponent is 1700. Your expected score is about 0.24. With K = 20:

- If you **win**: 20 × (1 − 0.24) ≈ **+15**.
- If you **draw**: 20 × (0.5 − 0.24) ≈ **+5**.
- If you **lose**: 20 × (0 − 0.24) ≈ **−5**.

Beating a stronger player gives many points; losing to one costs few. The reverse holds when you play someone weaker.

## The K-factor

K controls how fast ratings move. A big K reacts quickly (good for new players whose strength is unknown); a small K is stable. In [Chess 3D](https://chess3d.online) and [Xiangqi 3D](https://xiangqi3d.online) K starts high for your first games and becomes smaller as you play more and as your rating rises.

## How ratings work in Chess 3D and Xiangqi 3D

- **Everyone starts at 1000.** You can start playing as a guest and choose a name when you want to be on the leaderboard.
- **Rated games** are played with a 10 minutes + 5 seconds per move clock and count only if at least 10 moves have been played, so quitting early does not change ratings.
- **Matchmaking** pairs you with players of similar rating when possible.
- **Games against the Royal AI count for half** and stop adding points above 1500: to rise further you must beat people.
- **Invite links**: a game with a friend is a normal rated game, with limits on how many games the same two players can have in an hour and a day, to prevent rating farming.
- **A draw by agreement** changes nobody's rating.
- **Leaderboard**: after ten rated games you appear on the leaderboard.
- **Rank tiers** give you a title as your number grows: in Chess 3D from Pawn through Knight, Bishop, Rook, Queen and King to Grandmaster; in Xiangqi 3D from Soldier through Advisor, Elephant, Horse, Cannon and Chariot to General.

## Reading your rating

| Rating | Rough level |
|---|---|
| Below 900 | Just learning the rules |
| 900–1300 | Beginner to casual player |
| 1300–1500 | Improving club player |
| 1500–1900 | Strong player with good tactics |
| 1900+ | Expert level |

These are rules of thumb. Ratings in one pool (a website, a country, a game) do not translate to another.

## How to improve your rating

- Play regularly with a clock ([chess time controls](/chess/time-controls/)).
- Review your losses and look for the first mistake.
- Learn tactics: [chess tactics](/chess/tactics/) or [xiangqi tactics](/xiangqi/tactics/).
- Learn endgames: [chess endgames](/chess/endgames/) or [xiangqi endgames](/xiangqi/endgames/).

{{cta:both}}
