# Front-page content for Wednesday 25 November 2026.
#
# Every item below was reported on 25 November 2026 itself; the poster is a
# one-picture digest of that single day, not a week-in-review. Sources are
# the day's wire reporting (Reuters unless noted in the README).
#
# Final edition: the evening wires widened the lead story -- after the
# morning Ras Tanura claim the Houthis also said they hit the ports of
# Jazan and Jeddah, a projectile landed at Jazan port, and Brent crude
# jumped over 2%. The tariff card now carries the evening USTR detail
# (14 partners, up to 25%), and the strip swaps the Giuliani brief for
# the US warning to citizens to leave Iran.

KICKER = "THE WORLD IN ONE PICTURE"
DATELINE = "WEDNESDAY 25 NOVEMBER 2026"

# The lead story takes the wide box under the masthead.
LEAD = {
    "tag": "SAUDI ARABIA",
    "icon": "flame",
    "title": "Houthis widen strikes on Saudi ports and refinery",
    "body": (
        "Yemen's Houthis said they hit the Ras Tanura refinery and "
        "Riyadh's finance hub, then claimed strikes on the ports of "
        "Jazan and Jeddah. Saudi defences downed four drones; Brent "
        "crude jumped over 2%."
    ),
}

# Four cards fill the grid under the lead, two by two.
CARDS = [
    {
        "tag": "SPACE",
        "icon": "station",
        "title": "Pakistan's first astronaut reaches China's station",
        "body": (
            "Shenzhou-24 docked at Tiangong with Zeeshan Ali, the first "
            "foreigner to board China's station."
        ),
    },
    {
        "tag": "CHINA",
        "icon": "capitol",
        "title": "Graft purge reaches into the Politburo again",
        "body": (
            "Shanghai's Chen Jining is under investigation, the fourth "
            "Politburo member probed since 2025."
        ),
    },
    {
        "tag": "TRADE",
        "icon": "globe",
        "title": "US proposes tariffs of up to 25% on 14 partners",
        "body": (
            "Washington proposed duties up to 25% on 14 partners; Seoul "
            "stocks fell 6%."
        ),
    },
    {
        "tag": "MIGRATION",
        "icon": "ship",
        "title": "Record 2,100 migrants reach Canaries in a day",
        "body": (
            "Overcrowded boats brought 2,100-plus people to Spain's Canary "
            "Islands in 24 hours, a record."
        ),
    },
]

# One-line briefs for the strip along the bottom edge.
STRIP = [
    "Landmines killed or injured nearly 7,000 in 2025, a five-year high",
    "Police free hostages in Colombia supermarket siege",
    "US tells citizens to leave Iran as Gulf attacks spread",
]
