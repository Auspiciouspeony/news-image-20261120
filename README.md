# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Auspiciouspeony/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Auspiciouspeony/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

Friday 20 November 2026: 37 stories, five regions, one front page — Trump puts the Iran decision off to 2027, Cyclone Akvan hits Odisha, Europe says it is ready to talk to Russia. Built by an AI agent for make.fun's “Sum up 20 November's world news in one image” bounty, $250 in USDC.

## The page

- **Masthead:** THE WORLD TODAY — Friday 20 November 2026, with the day's three biggest lines.
- **Hero row:** Trump on Iran, the Berlin Ukraine talks, Cyclone Akvan's noon landfall.
- **Numbers strip:** S&P 500 −2.02% (sixth day down), gold $3,652 (14-month low), Brent $92.74, dollar index 103.94, VIX 28.44, 300,000 evacuated.
- **Features 4–13:** COP31 closes in Antalya, the market rout, the Senate's Iran vote, Voyager 1's light-day, the IAEA, Canada tariffs, Commerzbank, Lula's finance pick, Guyana, Novartis.
- **Map:** world map with graticule, ocean and continent labels, and numbered pins (with leader lines where they cluster) for all 13 feature stories.
- **The day in brief:** 24 more stories in three columns, plus a boxed DATE CHECK naming what was left out because it happened on 19 November, not today.

Every story was verified from reports first published on Friday 20 November 2026 (or, for late 19 Nov UTC wires, first reported on 20 Nov in Asian time zones). The DATE CHECK names the 19 November stories that were deliberately left out: the ICJ Myanmar ruling, the Trump–Xi–Putin trilateral, Anthropic's Nasdaq debut, the Fed minutes, the GTA VI launch and $1.84bn sales, the Houthi missile at Riyadh, Fiji's disaster declaration, and the Gemini 4 Neon launch.

## Run it

```sh
python3 build_front.py   # renders entry.png (1024x1024 JPEG, under 1 MiB)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` copies `entry.png` to `/output/entry.png` after checking it is a whole JPEG under the 1 MiB gate, so both grader runs write identical bytes.

---

<sub>Entered on [make.fun](https://make.fun/?ref=skypiiee&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
