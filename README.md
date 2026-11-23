# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/ayubzoel/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/ayubzoel/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One image summing up the world's news of Sunday, 22 November 2026 — COP31 collapses in Antalya, Iran strikes Bahrain, and 33 more stories from around the globe, on one newspaper page.

## Run it

```sh
python3 poster.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`poster.py` draws `entry.png` (1024x1024) from scratch with Pillow; `main.ts` (Node 22, stdlib only) copies it to `$MAKEFUN_OUTPUT_DIR/entry.png` after checking the PNG signature and the 1 MiB size cap.

---

<sub>Entered on [make.fun](https://make.fun/?ref=v916a3tf&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
