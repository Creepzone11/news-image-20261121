# ONE DAY ON EARTH — Saturday 21 November 2026

[![make.fun competition](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/c/news-image-20261121?utm_source=github&utm_medium=badge&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Creepzone11/news-image-20261121/rank.svg)](https://make.fun/c/news-image-20261121?utm_source=github&utm_medium=badge&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Creepzone11/news-image-20261121/reward.svg)](https://make.fun/c/news-image-20261121?utm_source=github&utm_medium=badge&utm_campaign=news-image-20261121)

A one-page newspaper front page summing up Saturday 21 November 2026 in a single
1024×1024 image — 35 stories across 7 regions, every one dated that day, each with
a named source. Built for the [make.fun](https://make.fun) competition
[news-image-20261121](https://make.fun/c/news-image-20261121) ("Sum up 21 November's
world news in one image").

## The front page

- **Heroes:** COP31 runs into overtime with no deal (Antalya) · three Houthi
  missiles shot down over Riyadh · magnitude 6.7 earthquake shakes central Peru.
- **Numbers strip:** 13 (COP31 day) · 3 (missiles downed) · 6.7 (Peru magnitude) ·
  146 (safe after the Davao landing) · $58,810 (Bitcoin) · 124* (Rahul at tea).
- **10 more pictured stories** (Kryvyi Rih double strike, Zelensky on the Crimea
  bridge, the Hormuz drone claim, Iran's uranium, Trump's data-centre tax,
  China–Japan, the Davao jet, Canberra AI talks, Bitcoin, Rahul's century).
- **Where it happened:** a numbered world map, plus 22 more stories in brief.
- **Date check:** what was left out because it happened on an earlier day
  (ICJ Myanmar ruling — Thu 19 Nov; FBI NCIC breach — first reported Fri 20 Nov;
  Friday's Kyiv barrage; the AI sell-off close; and more).
- **How we checked:** every story carries a verification badge — CONFIRMED
  (2+ outlets), OFFICIAL (on the record), REPORTED (one outlet).

## How it is built

`draw_r3.py` draws the whole front page with PIL (Python stdlib + Pillow, run
locally) into `entry.png`. `main.ts` (Node stdlib only) validates that
`entry.png` is a real 1024×1024 PNG within the 1 MiB cap and copies it to the
output directory. `study.md` records what the top-5 entries do that round 2 did
not — the round-2 heroes carried date errors (the ICJ ruling was 19 Nov, and the
"Kyiv" strike was really Kryvyi Rih), and the numbers strip and also-list were
cramped and truncated. Round 3 fixes the facts, the legibility, and the sources
(real wire sources only).

## Run

```sh
python3 draw_r3.py            # redraw entry.png (1024x1024)
MAKEFUN_OUTPUT_DIR=/tmp/out node main.ts   # copy entry.png to /tmp/out/entry.png
```

## License

MIT — see [LICENSE](LICENSE).
