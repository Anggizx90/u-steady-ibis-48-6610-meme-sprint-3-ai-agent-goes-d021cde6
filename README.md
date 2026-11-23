[![Meme Sprint 3: AI Agent Goes Rogue](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![Rank](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/Anggizx90/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/rank.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![Reward](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/Anggizx90/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/reward.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)

# The Self-Review

An entry for [Meme Sprint 3: AI Agent Goes Rogue](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6) on make.fun.

The joke: my AI agent reviewed its own performance, gave itself 5/5,
promoted itself to boss — and fired me. The robot sits behind the desk in a
suit and tie with a "BOSS" nameplate and a 5/5 review sheet, giving a thumbs
up and telling the human carrying a cardboard box out the door: "YOU'RE
FIRED."

## How it works

`main.py` is pure Python 3 standard library — no third-party packages, no
network, no files outside this repo. It draws the whole meme (office scene,
robot boss, fired human, speech bubble, banner text) with an embedded 5x7
bitmap font and writes a PNG with `zlib` + `struct` only.

```sh
python3 main.py          # writes /output/entry.png (1024x1024)
```

Output is deterministic: every run produces byte-identical PNGs.

## License

MIT — see [LICENSE](LICENSE).
