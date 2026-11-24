"""Build the redesigned block markup for kriskrug.co page 13069 from the live content."""

import json
import re
from pathlib import Path

HERE = Path(__file__).parent
raw = (HERE / "content.raw.html").read_text()
ld_block = raw[raw.index('<!-- wp:html -->\n<script type="application/ld+json">') :].strip()
embed_block = re.search(r"<!-- wp:embed .*?<!-- /wp:embed -->", raw, re.S).group(0)
list_block = re.search(r"<!-- wp:list -->.*?<!-- /wp:list -->", raw, re.S).group(0)
css = (HERE / "guide.css").read_text().strip()

UP = "https://kriskrug.co/wp-content/uploads"
KK, BCAI = "kk", "bcai"

CARDS = [
    dict(
        ch=1,
        id=13071,
        file="2026/11/1-guide-card-council",
        src=KK,
        date="Nov 18, 2026",
        start=True,
        wide=True,
        url="https://kriskrug.co/2026/11/18/vancouver-ai-data-centres-public-benefit/",
        title="What I asked Vancouver council for on Nov 18",
        dek="Assess the impacts, disclose the numbers, and make the public benefit concrete, including public GPU hours. My speech, the sources and the video.",
        alt="Screenshot of the top of Kris Krüg's post on what he asked Vancouver council for on Motion 10",
    ),
    dict(
        ch=1,
        id=13072,
        file="2026/11/2-guide-card-motion",
        src=BCAI,
        date="Nov 18, 2026",
        start=True,
        url="https://bc-ai.ca/news/vancouver-data-centre-motion-what-changes",
        title="What the Vancouver data-centre motion actually changes",
        dek="BC + AI's explainer on the motion that passed.",
        alt="Screenshot of the BC + AI explainer on the Vancouver data-centre motion",
    ),
    dict(
        ch=1,
        id=13073,
        file="2026/11/3-guide-card-thirsty",
        src=KK,
        date="Oct 4, 2026",
        url="https://kriskrug.co/2026/10/04/whos-the-thirsty-little-democracy/",
        title="Who's the Thirsty Little Democracy?",
        dek="A field piece from the Oct 3 Vancouver data-centre protest: land, water, public power, and where I stand with the movement.",
        alt="Screenshot of Kris Krüg's field piece from the Oct 3 Vancouver data-centre protest",
    ),
    dict(
        ch=2,
        id=13074,
        file="2026/11/4-guide-card-compute",
        src=BCAI,
        date=None,
        start=True,
        wide=True,
        url="https://bc-ai.ca/public-compute",
        title="The BC Public Compute Project",
        dek="BC + AI's framework for data centres in B.C.: who owns the infrastructure, who benefits, and what stays here. The position paper is linked from the page.",
        alt="Screenshot of the BC Public Compute Project page",
    ),
    dict(
        ch=2,
        id=13075,
        file="2026/11/5-guide-card-tests",
        src=BCAI,
        date="Aug 3, 2026",
        url="https://bc-ai.ca/news/what-kind-of-ai-province-do-we-want-to-build",
        title="What Kind of AI Province Should BC Build?",
        dek='My five tests for a BC AI economy, including "compute with a public bargain, not a blank cheque." The shortest statement of the principle behind my council ask.',
        alt="Screenshot of the BC + AI essay with Kris Krüg's five tests for a BC AI economy",
    ),
    dict(
        ch=2,
        id=13076,
        file="2026/11/6-guide-card-taskforce",
        src=BCAI,
        date="Feb 8, 2026",
        url="https://bc-ai.ca/news/bcs-response-to-the-canada-s-ai-task-force",
        title="BC + AI's response to Canada's AI Task Force",
        dek="The broader national policy context.",
        alt="Screenshot of BC + AI's response to Canada's AI Task Force",
    ),
    dict(
        ch=3,
        id=13077,
        file="2026/11/7-guide-card-grid",
        src=BCAI,
        date="Jul 22, 2026",
        url="https://bc-ai.ca/news/both-hands-on-the-grid",
        title="Both Hands on the Grid",
        dek="My fuller essay on infrastructure, community consent, and the outcomes I want in writing.",
        alt="Screenshot of the BC + AI essay Both Hands on the Grid",
    ),
    dict(
        ch=3,
        id=13078,
        file="2026/11/8-guide-card-licence",
        src=KK,
        date="Nov 2, 2026",
        url="https://kriskrug.co/2026/11/02/you-cant-rent-a-social-licence/",
        title="You Can't Rent a Social Licence",
        dek="Why process and public consent matter, told through the UBC Global Summit AI protest.",
        alt="Screenshot of Kris Krüg's post on public consent and the UBC Global Summit AI protest",
    ),
]

CHAPTERS = {1: "Vancouver", 2: "The public compute proposal", 3: "Consent and community benefit"}
SRC_LABEL = {KK: "kriskrug.co", BCAI: "BC + AI"}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def group(cls, inner):
    return (
        f'<!-- wp:group {{"className":"{cls}"}} -->\n<div class="wp-block-group {cls}">'
        f"{inner}</div>\n<!-- /wp:group -->"
    )


def para(cls, html):
    return f'<!-- wp:paragraph {{"className":"{cls}"}} -->\n<p class="{cls}">{html}</p>\n<!-- /wp:paragraph -->'


def image(media_id, src, alt, cls, size="medium_large", caption=None):
    cap = f'<figcaption class="wp-element-caption">{caption}</figcaption>' if caption else ""
    return (
        f'<!-- wp:image {{"id":{media_id},"sizeSlug":"{size}","linkDestination":"none","className":"{cls}"}} -->\n'
        f'<figure class="wp-block-image size-{size} {cls}"><img src="{src}" alt="{esc(alt)}" class="wp-image-{media_id}"/>{cap}</figure>\n'
        f"<!-- /wp:image -->"
    )


def heading(level, cls, html):
    attrs = {"level": level, "className": cls} if level != 2 else {"className": cls}
    return (
        f"<!-- wp:heading {json.dumps(attrs, separators=(',', ':'))} -->\n"
        f'<h{level} class="wp-block-heading {cls}">{html}</h{level}>\n<!-- /wp:heading -->'
    )


def card(c):
    mods = (
        [f"dc-card--{c['src']}"]
        + (["dc-card--start"] if c.get("start") else [])
        + (["dc-card--wide"] if c.get("wide") else [])
    )
    meta = []
    if c.get("start"):
        meta.append("<strong>Start here</strong>")
    meta.append(SRC_LABEL[c["src"]])
    if c["date"]:
        meta.append(c["date"])
    body = "\n".join(
        [
            para("dc-card__meta", " · ".join(meta)),
            heading(3, "dc-card__title", f'<a href="{c["url"]}">{esc(c["title"])}</a>'),
            para("dc-card__dek", esc(c["dek"]).replace("&quot;", '"')),
        ]
    )
    shot = image(c["id"], f"{UP}/{c['file']}-768x403.jpg", c["alt"], "dc-card__shot")
    return group(
        "dc-card " + " ".join(mods),
        "\n" + shot + "\n" + group("dc-card__body", "\n" + body + "\n") + "\n",
    )


hero_text = "\n".join(
    [
        para("dc-kicker", "A reading guide · Vancouver and B.C."),
        heading(1, "dc-hero__title", "Data centres, public compute and the public interest"),
        para(
            "dc-hero__lede",
            "I'm Kris Krüg, founder of BC + AI. I want useful AI infrastructure here: clean, green, just compute that we can explain to the people who live beside it. My ask is assessment, disclosure and a public benefit people can point to, including access to the computing itself: GPU hours for students, researchers, nonprofits, startups and Indigenous-led projects. On November 18 I asked Vancouver council to pass Motion 10 on digital infrastructure. It passed unanimously.",
        ),
        para(
            "dc-hero__note",
            'This page collects where I\'ve written it down. Pieces marked "start here" are the shortest route to my position.',
        ),
    ]
)
portrait = image(
    2682,
    f"{UP}/2023/07/krug-1-768x702.jpg",
    "Kris Krüg in a black knit cap, lit in amber and blue",
    "dc-hero__portrait",
    caption="Kris Krüg · founder, BC + AI",
)
hero = group(
    "dc-hero",
    "\n"
    + group(
        "dc-hero__inner",
        "\n" + group("dc-hero__text", "\n" + hero_text + "\n") + "\n" + portrait + "\n",
    )
    + "\n",
)

asks = group(
    "dc-asks",
    "\n"
    + "\n".join(
        [
            para("dc-asks__label", "The ask, in three parts"),
            group(
                "dc-asks__row",
                "\n"
                + "\n".join(
                    [
                        para("dc-ask", "<strong>Assess</strong> the impacts"),
                        para("dc-ask", "<strong>Disclose</strong> the numbers"),
                        para(
                            "dc-ask",
                            "<strong>Make the public benefit concrete</strong>, including public GPU hours",
                        ),
                    ]
                )
                + "\n",
            ),
            para(
                "dc-asks__result",
                "Motion 10 on digital infrastructure · Vancouver · passed unanimously, Nov 18, 2026",
            ),
        ]
    )
    + "\n",
)

chapters = []
for n, name in CHAPTERS.items():
    cards = "\n".join(card(c) for c in CARDS if c["ch"] == n)
    chapters.append(
        group(
            f"dc-chapter dc-chapter--{n}",
            "\n"
            + para("dc-chapter__num", f"Part {n} of 4")
            + "\n"
            + heading(2, "dc-chapter__title", name)
            + "\n"
            + group("dc-grid", "\n" + cards + "\n")
            + "\n",
        )
    )

watch = group(
    "dc-watch",
    "\n"
    + group(
        "dc-watch__inner",
        "\n"
        + "\n".join(
            [
                para("dc-chapter__num", "Part 4 of 4"),
                heading(2, "dc-chapter__title", "Watch"),
                embed_block,
                list_block.replace(
                    '<!-- wp:list -->\n<ul class="wp-block-list">',
                    '<!-- wp:list {"className":"dc-watch__list"} -->\n<ul class="wp-block-list dc-watch__list">',
                ),
            ]
        )
        + "\n",
    )
    + "\n",
)

style = f'<!-- wp:html -->\n<style id="dc-guide-css">\n{css}\n</style>\n<!-- /wp:html -->'
body = "\n\n".join([style, hero, asks, *chapters, watch])
out = (
    f'<!-- wp:group {{"align":"full","className":"dc-guide"}} -->\n<div class="wp-block-group alignfull dc-guide">'
    f"{body}</div>\n<!-- /wp:group -->\n\n{ld_block}\n"
)
(HERE / "content.new.html").write_text(out)
print(len(out), "bytes")
