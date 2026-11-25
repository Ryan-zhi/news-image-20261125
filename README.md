# The World in One Picture — Wednesday 25 November 2026

![bounty](https://make.fun/badge/news-image-20261125.svg)
![rank](https://make.fun/badge/news-image-20261125/Ryan-zhi/news-image-20261125/rank.svg)
![reward](https://make.fun/badge/news-image-20261125/Ryan-zhi/news-image-20261125/reward.svg)

One image that sums up the world news of **25 November 2026**, drawn as a
newspaper front page: a lead story, four cards and a strip of briefs.

**Lead — Saudi Arabia.** Yemen's Houthis said they attacked the Ras Tanura
refinery and Riyadh's financial district; Saudi air defences downed four
drones and 11 people were wounded.

**Cards.** Shenzhou-24 docked at Tiangong carrying Zeeshan Ali, the first
foreigner to board China's station · Shanghai party chief Chen Jining is
under investigation in the graft purge · Washington's tariff threat against
16 trading partners sent Nasdaq futures down over 2% · a record 2,100-plus
migrants reached Spain's Canary Islands in a single day.

**Also today.** Landmine casualties hit a five-year high in 2025 · hostages
freed in a Colombia supermarket siege · Trump awarded Giuliani the Medal
of Freedom.

## How it is made

`draw.py` paints the whole page with PIL — masthead, rules, red tag chips
and spot illustrations are all code, no image assets. `day25.py` holds the
day's words, so the same renderer can produce any date's front page:

```sh
python3 draw.py day25 entry.png
```

Every story ran on 25 November 2026; sources are that day's wire reports
(Reuters). Text is set in DejaVu Serif / DejaVu Sans. MIT licensed.
