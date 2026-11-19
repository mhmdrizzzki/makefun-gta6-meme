# makefun-gta6-meme

This repository hands in the address of our public X post: a GTA 6 launch-week
meme with make.fun's ghost worked into the picture, made for the make.fun bounty
[Post a GTA 6 meme on X](https://make.fun/bounty/gta6-meme-x-01).

[![make.fun](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/mhmdrizzzki/makefun-gta6-meme/rank.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/mhmdrizzzki/makefun-gta6-meme/reward.svg)](https://make.fun/bounty/gta6-meme-x-01)

The post itself is the entry. `main.ts` copies `POST.json` to the output directory;
`POST.json` holds the post's address.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`tools/make_meme.py` builds `meme.png` from `assets/makefun-ghost.png` (make.fun's
mascot, from its press kit) with a Vice City sunset drawn in PIL.
