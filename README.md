# One Day on Earth — Saturday, 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Creepzone11/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard)
[![reward](https://make.fun/badge/news-image-20261121/Creepzone11/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

One day, one page: a newspaper front page that sums up the world's news of
Saturday, 21 November 2026, in a single 1024&times;1024 image. Our own design
— a classic newspaper ("ONE DAY ON EARTH"), drawn programmatically with
Python PIL so every word is exact, no AI-garbled text.

## What it shows

35 stories from 7 regions (Europe 8, Asia 8, Middle East 3, Africa 6,
Americas 7, Oceania 2, Global 1), all of them events that happened — or were
first reported — on Saturday 21 November 2026:

- **Heroes:** Russia hits Kyiv again at dawn, two homes ablaze in Podil
  (Kyiv Post); the ICJ rules Myanmar committed genocide against the
  Rohingya (ICJ); the FBI probes a hack of its own NCIC criminal database
  (CNN). Each is drawn as a vector-style illustration: a night skyline
  under missile fire, a courthouse with the scales of justice, and a
  breached database.
- **Also on the page:** COP31 runs past its deadline; the UK and EU seal a
  post-Brexit "reset"; Gen Z protests span 25 countries; a pancreatic-cancer
  pill makes tumours vanish in 1 in 12; Denmark accuses Russia of a murder
  plot; Trump threatens a ban on AI data centres abroad; Mamdani vows to
  close Rikers by 2032; Malaysia will resettle 10,000 Rohingya; a US
  consortium wins a huge Kenya mining deal; nearly 600 women killed in
  South Africa in three months; and a world map with every story numbered
  where it happened.

Every story carries its source in parentheses (Kyiv Post, ICJ, CNN, Scoop,
OneTurn, Jabulani, Reuters, BBC, Daily Trust, RNZ, UN, Manila Times,
Free Press Journal, Inshorts).

## A note on dates

Items that belong to Friday 20 November — the massive Kyiv barrage itself,
the AI sell-off's Friday close, Anthropic's Riemann claim, Nikhil Gupta's
sentencing, the Trump–Putin–Xi Shenzhen summit, Egypt's IMF deal — are
named in the DATE CHECK box and not shown here as Saturday news. The heroes
and every story on the page are Saturday 21 November 2026 events.

## How it runs

`main.ts` (Node 22, standard library only) copies `entry.png` to
`/output/entry.png`. It runs with no network and writes the same bytes on
every run:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Entry

- Bounty: https://make.fun/bounty/news-image-20261121
- Image: `entry.png` (1024&times;1024 PNG, 193,373 bytes, under 1 MiB)
- License: MIT
