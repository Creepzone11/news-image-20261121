# ONE DAY ON EARTH — Saturday 21 November 2026

[![make.fun competition](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/c/news-image-20261121?utm_source=github&utm_medium=badge&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Creepzone11/news-image-20261121/rank.svg)](https://make.fun/c/news-image-20261121?utm_source=github&utm_medium=badge&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Creepzone11/news-image-20261121/reward.svg)](https://make.fun/c/news-image-20261121?utm_source=github&utm_medium=badge&utm_campaign=news-image-20261121)

A one-page newspaper front page summing up Saturday 21 November 2026 in a single
1024×1024 image — 35 stories across 7 regions, every one dated that day, each with
a named source. Built for the [make.fun](https://make.fun) competition
[news-image-20261121](https://make.fun/c/news-image-20261121) ("Sum up 21 November's
world news in one image"). Round 4.

## The day

- **COP31** runs into overtime in Antalya — no deal on day 13, a third draft due
  Saturday morning.
- **Riyadh**: the Saudi-led coalition downs 3 Houthi ballistic missiles before
  dawn, and 2 more over Jizan.
- **Peru**: a magnitude 6.7 quake near Junín, 00:09 UTC, felt in Lima — no deaths.
- Plus Kryvyi Rih (12 killed, 42 hurt), Zelensky on the Crimea bridge, Iran's
  drone claim, Trump's data-centre tax, China–Japan, the Davao jet landing, AI
  talks in Canberra, Bitcoin at $58,810, and Rahul's 124* — 35 stories in all.

## How it is built

`draw_r4.py` draws the whole front page with PIL (original drawings, no photos,
no network): masthead, numbers strip, region bar, three hero cards with
pictorial art, ten secondary stories each with its own small scene, a numbered
world map, a 22-more-stories list, and a DATE CHECK box that names everything
left out because it happened on an earlier day. `main.ts` (Node stdlib only)
validates `entry.png` (real PNG, 1024×1024, under 1 MiB), copies it to
`/output/entry.png`, and writes a deterministic `dossier.json`.

```sh
python3 draw_r4.py            # redraw entry.png
MAKEFUN_OUTPUT_DIR=out node main.ts   # copy + dossier
```

Every story here happened, or was first reported, on Saturday 21 November 2026.
Sources are named beside each story. Referral: https://make.fun/r/kh987p5b
