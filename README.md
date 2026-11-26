[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/Nopnop15/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/Nopnop15/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

# The World in One Page — Thursday 26 November 2026

A front-page image summing up the world news of Thursday 26 November
2026. Six stories, each drawn as its own panel with a short headline
and subline:

1. **Trump's new tariffs** — Washington proposes 20% more on Chinese
   goods — up to 45% in all — plus levies on the EU, Japan and 11
   others. A Section 301 action covering 14 trading partners, with
   hearings on 25 January and nothing effective before January 2027.
2. **Cairo tanker fire kills 31** — A fuel tanker overturns on Cairo's
   Ring Road near Al-Warraq, Giza; the fire engulfs 27 vehicles,
   killing 31 people and injuring 21.
3. **Nasdaq plunges on AI fears** — The Nasdaq dives about 4%
   intraday before closing 0.6% down; Nvidia falls 4% as AI doubts
   deepen. The Nasdaq 100 briefly flirted with a bear market, 20%
   below its peak.
4. **Netanyahu wins court boost** — Jerusalem judges urge prosecutors
   to drop the bribery charge in Case 4000 and reconsider Case 2000.
   A recommendation, not a ruling; Case 1000 is to be settled by deal.
5. **Pyongyang expels Swiss envoy** — North Korea gives envoy Sylvain
   Astier 48 hours to leave over Swiss sanctions on a children's
   camp. The Swiss office had reopened only in late October, weeks
   earlier.
6. **Brent rebounds on Hormuz attacks** — Brent climbs 2.3% to
   $91.40 as fresh tanker attacks are reported; Gulf transits are
   down about 40%. Prices as of the 24 November close.

## How it is built

`generate_image.py` draws the 1024×1024 front page with Pillow (masthead,
a wide hero panel for the tariffs story, three panels, two wide panels
and a footer) and writes `entry.png`. `main.ts` (Node, standard library
only) copies `entry.png` into the output folder. Run it with:

```sh
python3 generate_image.py
MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see `LICENSE`.
