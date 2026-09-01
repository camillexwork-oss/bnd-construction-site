#!/usr/bin/env python3
"""
BND Construction — static site generator.

Header, footer and <head> live here once, so the seven top-level
pages and every project page stay in sync.

    python3 build.py

Project data is the single source of truth in js/projects.js.
To add a project: add a block there, drop images/projects/<slug>.jpg
(900px wide) and images/projects/<slug>-lg.jpg (1800px wide), then
re-run this script.

NOTE: this OVERWRITES the generated .html files. Edit this script,
not the output.
"""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://bnd-co.com"          # TODO: confirm host before launch

NAV = [
    ("index.html",          "Home"),
    ("about.html",          "About"),
    ("company.html",        "Services"),
    ("portfolio.html",      "Portfolio"),
    ("careers.html",        "Careers"),
    ("subcontractors.html", "Subcontractors"),
    ("contact.html",        "Contact"),
]

# Live pages that are deliberately not in the primary nav. They stay reachable
# from the footer — the subcontractor prequalification form is a deliverable.
FOOTER_EXTRA = [
    ("request-an-estimate.html", "Request an estimate"),
]

OFFICES = [
    ("Dallas",  "9101 Lyndon B Johnson Fwy",  "Dallas, TX 75243"),
    ("Houston", "2602 Genoa Red Bluff Rd",    "Houston, TX 77034"),
]

FOOTER_CONTACTS = [
    ("Estimating &amp; business development", "Burhaan Nadeem",
     "+19093587635", "909 &middot; 358 &middot; 7635", "burhaan@bnd-co.com"),
    ("Project management", "Daniel Prieto",
     "+14694353250", "469 &middot; 435 &middot; 3250", "daniel@bnd-co.com"),
]

CONTACTS = [
    ("Estimating &amp; business development", "Nawa Mwiya", "", "", "vcgcbids@gmail.com", ""),
]

MARKETS = [
    ("Restaurant &amp; Food Service",
     "High-end restaurants, quick service and full-service dining, delivered as ground-up builds and as finish-outs inside live centers.",
     "Finish-out &amp; ground-up"),
    ("Retail",
     "National brand stores and multi-tenant retail centers, including finish-outs completed inside trading centers without shutting the neighbours down.",
     "National brands &amp; centers"),
    ("Medical &amp; Dental",
     "Clinics, dental practices and medical centers, built to the finishes and compliance those fit-outs demand.",
     "Clinics &amp; medical centers"),
    ("Education",
     "Educational facilities and multi-building campuses, sequenced around academic calendars.",
     "Campuses &amp; facilities"),
    ("Multifamily",
     "Ground-up multifamily developments, from individual buildings through to full residential communities.",
     "Ground-up developments"),
    ("Industrial &amp; Warehouse",
     "Industrial and warehouse developments, flex space and distribution facilities.",
     "Flex &amp; distribution"),
    ("Convenience &amp; Fuel",
     "Convenience stores, travel centers and fuel sites, a sector we build in repeatedly across Texas and Oklahoma.",
     "C-stores &amp; travel centers"),
]

SERVICES = [
    ("New Construction", "ground-up-construction", "oak-point",
     ["Ground-up construction projects require more than just a general building contractor. "
      "With numerous years of ground-up experience, we apply that expertise to large-scale work "
      "with acute attention to detail and cost.",
      "We manage our clients&rsquo; projects to safely stay on schedule and under budget, and we keep "
      "our jobsites as neat and clean as possible to eliminate hassle. We know that being responsive "
      "to your needs and managing the materials we use is critical to a successful project."],
     ["Site development", "Shell &amp; core", "Full build-out", "Multi-building campuses"]),
    ("Tenant Finish-Out / Build Out", "tenant-finish-out", "walk-ons-sports-bistreaux",
     ["Whether your project is a 5,000 sq ft restaurant remodel, a busy flex space, or a 50,000 sq ft "
      "call center on the 10th floor, our finish-out division completes it on time, under budget and "
      "with minimal impact to other tenants.",
      "We value engineer your project to maximise the value of your investment, and we are equally "
      "qualified to interface with your design team and set preliminary budgets during planning."],
     ["Restaurant finish-out", "Retail finish-out", "Medical suites", "Office &amp; flex"]),
    ("Renovation &amp; Remodeling", "renovation-remodeling", "massage-luxe",
     ["We work with tenants of all sizes, from minor construction through to full renovation &mdash; "
      "privately owned companies and publicly traded corporations alike.",
      "Existing spaces are brought up to standard with the same schedule and budget discipline we "
      "bring to new construction, and with the same attention to keeping a site clean while occupied."],
     ["Targeted upgrades", "Full renovation", "Occupied premises", "Remodels"]),
    ("Design-Build", "design-build", "evolve-dermatology",
     ["Most of our projects arrive through relationships built with developers, building owners, "
      "management companies, real estate brokers and architects.",
      "That puts us in the room early. We interface with your design team, set preliminary budgets "
      "during planning, and carry a single line of accountability from the first sketch through to "
      "handover."],
     ["Early budgeting", "Value engineering", "Single point of contact", "Design coordination"]),
]


def projects():
    """Read js/projects.js through node so the data has one home."""
    out = subprocess.check_output([
        "node", "-e",
        "global.window={};require('%s/js/projects.js');"
        "process.stdout.write(JSON.stringify(window.BND_PROJECTS))" % ROOT
    ])
    return json.loads(out)


# ------------------------------------------------------------------ chrome
def head(title, desc, path, og_image="images/projects/oak-point-lg.jpg", depth=0):
    up = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow"><!-- MOCKUP ONLY: remove this line at launch -->

<!-- TODO before launch: confirm the live host, then match canonical exactly -->
<link rel="canonical" href="{SITE}/{path}">

<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}/{path}">
<meta property="og:image" content="{SITE}/{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#15171A">

<link rel="icon" href="{up}images/favicon.svg" type="image/svg+xml">
<link rel="preload" href="{up}fonts/PlusJakartaSans-ExtraBold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{up}fonts/PlusJakartaSans-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{up}css/site.css">
</head>
<body>

<a class="skip" href="#main">Skip to content</a>
"""


def market_menu(up=""):
    """Sector links for the Portfolio dropdown. Sourced from the project data so
    the menu and the filter chips can never drift apart."""
    from urllib.parse import quote
    ms = sorted({p["market"] for p in projects()})
    return "".join(
        f'\n        <a href="{up}portfolio.html?market={quote(m)}">{m}</a>' for m in ms)


def header(active, depth=0, solid=False):
    up = "../" * depth
    links, drawer = [], []
    for i, (href, label) in enumerate(NAV, 1):
        cur = ' aria-current="page"' if href == active else ""
        links.append(f'      <a href="{up}{href}"{cur}>{label}</a>')
        drawer.append(f'    <a href="{up}{href}"{cur}><span>{i:02d}</span> {label}</a>')
    return f"""
<header class="head head--solid">
  <div class="head__inner">
    <a href="{up}index.html" aria-label="BND Construction — home">
      <img class="head__logo" src="{up}images/bnd-logo-white.png" alt="BND Construction" width="1312" height="502">
    </a>

    <nav class="nav" aria-label="Primary">
{chr(10).join(links)}
    </nav>

    <a class="btn btn--bronze head__cta" href="{up}request-an-estimate.html">
      Request an estimate <span class="btn__arrow" aria-hidden="true">&rarr;</span>
    </a>

    <button class="burger" type="button" aria-expanded="false" aria-controls="drawer" aria-label="Menu">
      <span></span>
    </button>
  </div>
</header>

<div class="drawer" id="drawer">
  <nav aria-label="Mobile">
{chr(10).join(drawer)}
  </nav>
  <div class="drawer__foot">
    <a href="mailto:vcgcbids@gmail.com">vcgcbids@gmail.com</a>
  </div>
</div>
"""


def footer(depth=0, forms=False):
    up = "../" * depth
    nav = "\n".join(
        f'          <li><a href="{up}{h}">{l}</a></li>'
        for h, l in list(NAV)[1:] + FOOTER_EXTRA
    )
    cc = ""
    for role, name, tel, telp, mail in FOOTER_CONTACTS:
        phone = f'\n          <a href="tel:{tel}">{telp}</a>' if tel else ""
        cc += f"""        <div class="fcontact">
{f'          <p class="fcontact__name">{name}</p>' if name else ''}{phone}
          <a href="mailto:{mail}">{mail}</a>
        </div>
"""
    offices = ""
    for city, street, region in OFFICES:
        offices += f"""        <div class="fcontact">
          <p class="fcontact__role">{city}</p>
          <p class="foffice">{street}<br>{region}</p>
        </div>
"""

    fjs = f'\n<script src="{up}js/forms.js"></script>' if forms else ""
    return f"""
<footer class="foot">
  <div class="wrap">
    <div class="foot__top">
      <div>
        <img class="foot__logo" src="{up}images/bnd-logo-white.png" alt="BND Construction" width="1312" height="502" loading="lazy">
        <p class="foot__blurb">
          Licensed and insured commercial general contractor. Ground-up construction,
          tenant finish-out, renovation and remodeling throughout Texas and surrounding states.
        </p>
      </div>

      <div>
        <p class="foot__h">Site</p>
        <ul class="foot__nav">
{nav}
        </ul>
      </div>

      <div>
        <p class="foot__h">Offices</p>
{offices}      </div>

      <div>
        <p class="foot__h">Management</p>
{cc}      </div>
    </div>

    <div class="foot__bar">
      <span>&copy; <span id="year">2026</span> BND Construction</span>
      <span>Powered &amp; designed by <a href="https://cnstudiogroup.com" target="_blank" rel="noopener">cnstudiogroup.com</a></span>
    </div>
  </div>
</footer>

<script src="{up}js/site.js"></script>{fjs}
</body>
</html>
"""


def phead(title, lede, crumb, image, depth=0):
    up = "../" * depth
    media = "" if not image else (
        f'<div class="phead__media" data-reveal data-delay="2">'
        f'<img src="{up}images/projects/{image}-lg.jpg" alt="" '
        f'width="1800" height="1241" fetchpriority="high"></div>'
    )
    return f"""
<main id="main">
  <section class="section pintro">
    <div class="wrap">
      <nav class="crumb" aria-label="Breadcrumb">
        <a href="{up}index.html">Home</a> <span aria-hidden="true">/</span> <span>{crumb}</span>
      </nav>
      <h1 class="h1 phead__title" data-reveal>{title}</h1>
      {f'<p class="lede phead__lede" data-reveal data-delay="1">{lede}</p>' if lede else ''}

      {media}
    </div>
  </section>
"""


GABLE = ""


# ---------------------------------------------------------------------------
# The standard inner-page chrome. Every page below the homepage opens the same
# way (breadcrumb, title, short lede) and closes the same way (one supporting
# image beside a headline, a line of copy and a single CTA). The homepage is
# the only page that carries a full visual hero.
# ---------------------------------------------------------------------------

def pintro(crumb, title, lede, eyebrow="", extra="", depth=0, title_style=""):
    """Breadcrumb, page title, 2-3 line lede. No image - that lives in the close."""
    up = "../" * depth
    ts = f' style="{title_style}"' if title_style else ""
    return f"""
<main id="main">

  <section class="section pintro">
    <div class="wrap">
      <nav class="crumb" aria-label="Breadcrumb">
        <a href="{up}index.html">Home</a> <span aria-hidden="true">/</span> <span>{crumb}</span>
      </nav>
      {f'<p class="eyebrow" data-reveal>{eyebrow}</p>' if eyebrow else ''}
      <h1 class="h1 pintro__title" data-reveal data-delay="1"{ts}>{title}</h1>
      {f'<p class="lede pintro__lede" data-reveal data-delay="2">{lede}</p>' if lede else ''}
{extra}
    </div>
  </section>
"""


CLOSING = {
    # page          slug for the photo             headline
    "about":        ("oak-point",
                     "Duncanville Shopping Center photographed at dusk, with a stucco parapet and colonnade",
                     "Built on relationships.",
                     "Most of our work arrives through developers, owners and brands who have "
                     "built with us before. We would rather earn the next project than win the "
                     "lowest bid on this one.",
                     "Learn more", "company.html"),
    "services":     ("gas-station-fuel",
                     "H Express convenience store exterior in stone and stucco with red awnings",
                     "Let&rsquo;s build your next project.",
                     "Send drawings and a scope, or just a location and the date you need to "
                     "open. Estimating will come back to you.",
                     "Request an estimate", "request-an-estimate.html"),
    "portfolio":    ("celine-highland-park-village",
                     "Celine boutique interior with handbags on backlit shelving and a stone plinth display",
                     "Ready to start your project?",
                     "Ground-up, finish-out, renovation or design-build &mdash; send it through "
                     "and it goes straight to estimating.",
                     "Request an estimate", "request-an-estimate.html"),
    "careers":      ("prosper-retail-shell",
                     "Prosper Retail Shell under construction &mdash; timber framing and structural "
                     "steel being set by crane over a poured slab",
                     "Build with us.",
                     "We&rsquo;re always looking for dependable people who take pride in their "
                     "work. If that sounds like you, we&rsquo;d love to hear from you.",
                     "Apply today", "#apply"),
    "subcontractors": ("villa-at-vanston",
                     "Villa at Vanston multifamily building in brick with projecting balconies",
                     "Become a trusted trade partner.",
                     "We build projects that work for everyone on them. Submit a "
                     "prequalification and estimating will have your details when the next "
                     "package goes out.",
                     "Prequalify", "#prequal"),
    "contact":      ("panera-bread",
                     "Panera Bread dining room with pendant lighting, timber banquettes and a tiled service counter",
                     "Let&rsquo;s discuss your project.",
                     "Tell us what you are planning and who to speak to. We will come back to "
                     "you with the right person on it.",
                     "Send message", "#enquiry"),
}


def closing_split(page, depth=0):
    """Two-column close: supporting image left, headline + copy + one CTA right."""
    up = "../" * depth
    slug, alt, title, para, label, href = CLOSING[page]
    if not href.startswith("#"):
        href = up + href
    return f"""
  <section class="section pclose">
    <div class="wrap">
      <div class="closing">
        <div class="closing__media" data-reveal>
          <img src="{up}images/projects/{slug}-lg.jpg" alt="{alt}"
               width="1800" height="1350" loading="lazy" decoding="async">
        </div>
        <div class="closing__body" data-reveal data-delay="1">
          <h2 class="closing__title">{title}</h2>
          <p>{para}</p>
          <a class="btn btn--bronze" href="{href}">{label} <span class="btn__arrow" aria-hidden="true">&rarr;</span></a>
        </div>
      </div>
    </div>
  </section>
"""


def cta_split(depth=0):
    up = "../" * depth
    return f"""
  <section class="section section--tight">
    <div class="wrap">
      <div class="ctaband" data-reveal>
        <div>
          <h2 class="h2">Have a project coming up?</h2>
        </div>
        <div class="ctaband__actions">
          <a class="btn btn--bronze" href="{up}request-an-estimate.html">Request an estimate <span class="btn__arrow" aria-hidden="true">&rarr;</span></a>
          <a class="btn btn--ghost" href="{up}subcontractors.html">Prequalify</a>
        </div>
      </div>
    </div>
  </section>
"""


INDUSTRY_COPY = {
    "Restaurant & food service": "High-volume hospitality builds, delivered as ground-up work and as finish-outs inside trading centres without shutting the neighbours down.",
    "Retail": "National brand stores and multi-tenant centres, finished to the standard those brands hold their fit-outs to.",
    "Medical & dental": "Clinics and practices built to the finishes and compliance those fit-outs demand.",
    "Education": "Educational facilities and multi-building campuses, sequenced around academic calendars.",
    "Multifamily": "Ground-up residential developments, from single buildings through to full communities.",
    "Convenience & fuel": "Convenience stores, travel centres and fuel sites — a sector we build in repeatedly across Texas and Oklahoma.",
}

PROCESS = [
    ("Consultation", "Send drawings and a scope, or a location and the date you need to open. Estimating comes back to you."),
    ("Preconstruction", "We interface with your design team and set preliminary budgets during planning, where value engineering still changes the number."),
    ("Construction", "Managed to stay on schedule and under budget, with OSHA-trained superintendents and a jobsite kept clean throughout."),
    ("Handover", "Closeout and handover, with the relationship intact — most of our work comes from clients who have built with us before."),
]

ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" '
         'aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>')


def page_company(pr):
    """Our Company - built to answer 'why trust this contractor', not to list services."""
    from urllib.parse import quote

    # --- services as full features ---
    svc = ""
    for n, (name, slug, image, paras, tags) in enumerate(SERVICES, 1):
        pills = "".join(f'<li>{t}</li>' for t in tags)
        svc += f"""
      <article class="feat" id="{slug}" data-reveal>
        <div class="feat__media"><img src="images/projects/{image}.jpg" alt="" width="900" height="675" loading="lazy" decoding="async"></div>
        <div class="feat__body">
          <p class="feat__n">{n:02d}</p>
          <h3 class="h2" style="font-size:clamp(1.45rem,1.2rem + 1.2vw,2.1rem)">{name}</h3>
          <p>{paras[0]}</p>
          <ul class="feat__pills">{pills}</ul>
          <a class="tlink" href="#">Learn more <span aria-hidden="true">&rarr;</span></a>
        </div>
      </article>
"""

    # --- industries, each with its real projects ---
    ind = ""
    for i, (name, blurb, note) in enumerate(MARKETS, 1):
        plain = name.replace("&amp;", "&")
        rel = [p for p in pr if p["market"].lower() == plain.lower()]
        if not rel:
            continue
        names = "".join(f'<li>{p["name"]}</li>' for p in rel[:5])
        copy = INDUSTRY_COPY.get(plain, blurb)
        ind += f"""
        <details class="ind" data-reveal>
          <summary><span class="ind__n">{i:02d}</span><span class="ind__name">{name}</span><span class="ind__count">{len(rel)} projects</span></summary>
          <div class="ind__body">
            <p>{copy}</p>
            <p class="ind__label">Featured projects</p>
            <ul class="ind__list">{names}</ul>
            <a class="tlink" href="portfolio.html?market={quote(rel[0]['market'])}">View {plain.lower()} projects <span aria-hidden="true">&rarr;</span></a>
          </div>
        </details>
"""

    # --- featured projects ---
    shot = [p for p in pr if p["photo"]]
    picks = [p for p in shot if p["slug"] in ("oak-point", "villa-at-vanston", "ralph-lauren-northpark")] or shot[:3]
    cards = ""
    for q in picks:
        place = f'<span class="pcard__line">{q["location"]}</span>' if q["location"] else ""
        cards += f"""
        <a class="pcard" href="projects/{q['slug']}.html" data-reveal>
          <span class="pcard__media"><img src="images/projects/{q['slug']}.jpg" alt="{q['alt']}" width="900" height="675" loading="lazy" decoding="async"></span>
          <span class="pcard__body">
            <span class="pcard__type">{q['market']}</span>
            <span class="pcard__name">{q['name']}</span>
            <span class="pcard__line">{q['scope'].split(' — ')[0]}</span>
            {place}
            <span class="pcard__go">View project <i aria-hidden="true">&rarr;</i></span>
          </span>
        </a>
"""

    steps = ""
    for n, (title, body) in enumerate(PROCESS, 1):
        steps += f"""
        <li class="step" data-reveal>
          <span class="step__n">{n:02d}</span>
          <h3 class="h3">{title}</h3>
          <p>{body}</p>
        </li>
"""

    why = [
        ("Transparent communication", "You deal with the people running the job. If something changes on site, you hear it from us first &mdash; not at handover."),
        ("On schedule. Under control.", "We manage projects to safely stay on schedule and under budget, and value engineer early enough for it to matter."),
        ("Safety without compromise.", "Zero tolerance for safety violations. Every superintendent carries OSHA safety training and SWPPP certification."),
        ("Relationships that last.", "Most of our work arrives through developers, owners, brokers and architects who have built with us before."),
    ]
    why_html = "".join(
        f'<div class="vcard" data-reveal>{ARROW}<h3 class="h3">{t}</h3><p>{d}</p></div>' for t, d in why)

    return (
        head("Services | BND Construction",
             "BND Construction is a licensed and insured commercial general contractor delivering "
             "ground-up construction, tenant finish-out, renovation and design-build across Texas.",
             "company.html", "images/projects/walk-ons-sports-bistreaux-lg.jpg")
        + header("company.html")
        + f"""
<main id="main">

  <section class="section pintro">
    <div class="wrap">
      <nav class="crumb" aria-label="Breadcrumb">
        <a href="index.html">Home</a> <span aria-hidden="true">/</span> <span>Services</span>
      </nav>
      <p class="eyebrow" data-reveal>Our company</p>
      <h1 class="h1" data-reveal data-delay="1" style="max-width:17ch;margin-top:1rem">Building relationships before buildings.</h1>
      <p class="lede" data-reveal data-delay="2" style="max-width:56ch;margin-top:1.4rem">
        A licensed and insured commercial general contractor with over 25 years of combined
        management experience across restaurants, retail, medical, education, multifamily,
        industrial and convenience. Most of our work arrives through people who have built
        with us before.
      </p>
      <div data-reveal data-delay="3" style="display:flex;gap:.8rem;flex-wrap:wrap;margin-top:2rem">
        <a class="btn btn--bronze" href="request-an-estimate.html">Request an estimate <span class="btn__arrow" aria-hidden="true">&rarr;</span></a>
        <a class="btn btn--outline" href="portfolio.html">View portfolio</a>
      </div>
    </div>
  </section>

  <section class="section section--tight">
    <div class="wrap">
      <div class="metrics metrics--3" data-reveal>
        <div class="metric"><p class="metric__k">25+</p><p class="metric__v">Years combined management experience</p></div>
        <div class="metric"><p class="metric__k">7</p><p class="metric__v">Industries served</p></div>
        <div class="metric"><p class="metric__k">100%</p><p class="metric__v">Licensed &amp; insured</p></div>
      </div>
    </div>
  </section>

  <section class="section section--mist">
    <div class="wrap">
      <div class="phil">
        <div class="phil__body">
          <p class="eyebrow" data-reveal>Our philosophy</p>
          <p class="phil__statement" data-reveal data-delay="1">We believe successful projects begin long before construction <em>starts</em>.</p>
          <p data-reveal data-delay="2">
            We maintain honesty and integrity while achieving the finished product our clients expect.
            That means setting preliminary budgets during planning, interfacing with your design team
            early, and being straight about what a schedule can carry.
          </p>
          <p data-reveal data-delay="2">
            On site it means responsiveness, careful management of the materials we use, and jobsites
            kept as clean as possible &mdash; because on a finish-out inside a trading centre, that is
            the difference between a neighbour complaint and a repeat client.
          </p>
        </div>
        <div class="phil__media" data-reveal data-delay="1">
          <img src="images/projects/villa-at-vanston-lg.jpg" alt="Villa at Vanston, a 176-unit multifamily development built by BND Construction" width="1800" height="1100" loading="lazy" decoding="async">
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <p class="eyebrow" data-reveal>What we build</p>
      <h2 class="h2" data-reveal data-delay="1" style="margin:1rem 0 clamp(2.5rem,5vw,4rem);max-width:16ch">Four ways we take a project <em>on</em>.</h2>
{svc}    </div>
  </section>

  <section class="section section--mist">
    <div class="wrap">
      <p class="eyebrow" data-reveal>Why clients return</p>
      <h2 class="h2" data-reveal data-delay="1" style="margin:1rem 0 clamp(2rem,4vw,3rem);max-width:18ch">The reasons they come <em>back</em>.</h2>
      <div class="vcards">{why_html}</div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <p class="eyebrow" data-reveal>Industries</p>
      <h2 class="h2" data-reveal data-delay="1" style="margin:1rem 0 clamp(2rem,4vw,3rem);max-width:16ch">Sectors we <em>build in</em>.</h2>
      <div class="inds">{ind}      </div>
    </div>
  </section>

  <section class="section section--mist">
    <div class="wrap">
      <p class="eyebrow" data-reveal>Selected work</p>
      <h2 class="h2" data-reveal data-delay="1" style="margin:1rem 0 clamp(2rem,4vw,3rem);max-width:16ch">Recently <em>delivered</em>.</h2>
      <div class="pgrid pgrid--3">{cards}      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <p class="eyebrow" data-reveal>How a project runs</p>
      <h2 class="h2" data-reveal data-delay="1" style="margin:1rem 0 clamp(2rem,4vw,3rem);max-width:16ch">From first call to <em>handover</em>.</h2>
      <ol class="steps">{steps}      </ol>
    </div>
  </section>

"""
        + closing_split("services")
        + "</main>"
        + footer())


def page_careers():
    """Careers - restrained and text-led. The form is the page, not a
    destination buried under marketing sections."""
    return (
        head("Careers | BND Construction",
             "BND Construction hires superintendents and field staff who hold OSHA safety "
             "training and SWPPP certification, and who work to a zero-tolerance safety standard.",
             "careers.html", "images/projects/prosper-retail-shell-lg.jpg")
        + header("careers.html")
        + f"""
<main id="main">

  <section class="section pintro">
    <div class="wrap">
      <nav class="crumb" aria-label="Breadcrumb">
        <a href="index.html">Home</a> <span aria-hidden="true">/</span> <span>Careers</span>
      </nav>
      <h1 class="h1" data-reveal style="margin-top:.9rem">Careers</h1>
      <p class="lede" data-reveal data-delay="1" style="margin-top:1.3rem;max-width:56ch">
        Join a team that values quality craftsmanship, safety, and long-term professional growth.
        We&rsquo;re always looking for people who take pride in building commercial projects the
        right way.
      </p>
    </div>
  </section>

  <section class="section" style="padding-top:0">
    <div class="wrap wrap--narrow">
      <div class="applycard" id="apply" data-reveal>
        <form data-validate
              action="https://formsubmit.co/vcgcbids@gmail.com"
              method="POST" enctype="multipart/form-data" novalidate>
          <input type="hidden" name="_subject" value="BND careers application">
          <input type="hidden" name="_template" value="table">
          <input type="hidden" name="_captcha" value="false">
          <input type="hidden" name="_cc" value="daniel@bnd-co.com">
          <input type="hidden" name="_next" value="https://bnd-construction-site.vercel.app/thank-you.html">
          <div class="fgrid fgrid--2">
            <div class="fld">
              <label for="k-first">First name</label>
              <input id="k-first" name="first_name" data-label="First name" type="text" autocomplete="given-name" required>
            </div>
            <div class="fld">
              <label for="k-last">Last name</label>
              <input id="k-last" name="last_name" data-label="Last name" type="text" autocomplete="family-name" required>
            </div>
            <div class="fld">
              <label for="k-email">Email</label>
              <input id="k-email" name="email" data-label="Email" type="email" autocomplete="email" required>
            </div>
            <div class="fld">
              <label for="k-phone">Phone</label>
              <input id="k-phone" name="phone" data-label="Phone" type="tel" autocomplete="tel" required>
            </div>

            <fieldset class="fld fspan roles">
              <legend>What position(s) are you applying for?</legend>
              <div class="roles__grid">
                <label><input type="checkbox" name="positions" value="Project Manager"> Project Manager</label>
                <label><input type="checkbox" name="positions" value="Assistant Project Manager"> Assistant Project Manager</label>
                <label><input type="checkbox" name="positions" value="Project Engineer"> Project Engineer</label>
                <label><input type="checkbox" name="positions" value="Superintendent"> Superintendent</label>
                <label><input type="checkbox" name="positions" value="Assistant Superintendent"> Assistant Superintendent</label>
                <label><input type="checkbox" name="positions" value="Estimator"> Estimator</label>
                <label><input type="checkbox" name="positions" value="Preconstruction"> Preconstruction</label>
                <label><input type="checkbox" name="positions" value="Field / trades"> Field / trades</label>
                <label><input type="checkbox" name="positions" value="Accounting"> Accounting</label>
                <label><input type="checkbox" name="positions" value="Admin"> Admin</label>
                <label><input type="checkbox" name="positions" value="Other"> Other</label>
              </div>
            </fieldset>

            <div class="fld">
              <label for="k-start">Available start date</label>
              <input id="k-start" name="start_date" data-label="Start date" type="date">
            </div>
            <div class="fld">
              <label for="k-years">Years in commercial construction</label>
              <input id="k-years" name="years" data-label="Years experience" type="text">
            </div>
            <div class="fld fspan">
              <label for="k-certs">Certifications held</label>
              <input id="k-certs" name="certs" data-label="Certifications" type="text" placeholder="OSHA 30, SWPPP&hellip;">
            </div>

            <div class="fld fspan">
              <label for="k-resume">Upload your resume <span style="text-transform:none;letter-spacing:0;color:#A8341F">(required)</span> <span style="text-transform:none;letter-spacing:0;color:var(--slate)">&mdash; PDF or Word, up to 5&nbsp;MB</span></label>
              <input id="k-resume" name="attachment" data-label="Resume" type="file" required
                     accept=".pdf,.doc,.docx,application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document">
            </div>

            <div class="fld fspan">
              <label for="k-msg">References</label>
              <textarea id="k-msg" name="message" data-label="References" rows="4" required></textarea>
            </div>
          </div>
          <button class="btn btn--bronze" type="submit" style="margin-top:1.5rem">
            Send application <span class="btn__arrow" aria-hidden="true">&rarr;</span>
          </button>
        </form>
        <p class="fmsg" data-form-msg role="status" aria-live="polite"></p>
      </div>
    </div>
  </section>

  <section class="section section--tight">
    <div class="wrap">
      <div class="cvals"><div class="cval"><p class="cval__n">01</p><h3 class="cval__t">Safety first</h3><p class="cval__d">OSHA training and SWPPP certification on every superintendent.</p></div><div class="cval"><p class="cval__n">02</p><h3 class="cval__t">Built on integrity</h3><p class="cval__d">Honesty and integrity, from the first budget to handover.</p></div><div class="cval"><p class="cval__n">03</p><h3 class="cval__t">Long-term careers</h3><p class="cval__d">Most of our work is repeat business. The same is true of our people.</p></div><div class="cval"><p class="cval__n">04</p><h3 class="cval__t">Quality without compromise</h3><p class="cval__d">The finished product our clients expect, every time.</p></div></div>
    </div>
  </section>

"""
        + closing_split("careers")
        + "</main>"
        + footer(forms=True))


def page_thankyou():
    """Landing page for the careers form. A multipart POST navigates away, so
    FormSubmit needs somewhere on our own site to send people back to."""
    return (
        head("Application received | BND Construction",
             "Thanks — your application has reached BND Construction.",
             "thank-you.html", "images/projects/villa-at-vanston-lg.jpg")
        + header("careers.html")
        + """
<main id="main">
  <section class="section" style="padding-top:clamp(3rem,7vw,5.5rem)">
    <div class="wrap wrap--narrow" style="text-align:center">
      <p class="kicker">Application received</p>
      <h1 class="h1" style="margin:1rem 0 1.1rem">That&rsquo;s with us.</h1>
      <p class="lede" style="margin:0 auto 2rem;max-width:46ch">
        Thanks for sending it through. If your experience fits something we have
        coming up, we&rsquo;ll be in touch.
      </p>
      <div style="display:flex;gap:.8rem;justify-content:center;flex-wrap:wrap">
        <a class="btn btn--bronze" href="index.html">Back to home <span class="btn__arrow" aria-hidden="true">&rarr;</span></a>
        <a class="btn btn--outline" href="portfolio.html">See our projects</a>
      </div>
    </div>
  </section>
</main>
""" + footer())



def page_thankyou_estimate():
    """Landing page for the estimate form. A multipart POST navigates away, so
    FormSubmit needs somewhere on our own site to return people to."""
    return (
        head("Request received | BND Construction",
             "Thanks - your project has reached BND Construction estimating.",
             "thank-you-estimate.html", "images/projects/oak-point-lg.jpg")
        + header("contact.html")
        + """
<main id="main">
  <section class="section" style="padding-top:clamp(3rem,7vw,5.5rem)">
    <div class="wrap wrap--narrow" style="text-align:center">
      <p class="kicker">Request received</p>
      <h1 class="h1" style="margin:1rem 0 1.1rem">That&rsquo;s with estimating.</h1>
      <p class="lede" style="margin:0 auto 2rem;max-width:48ch">
        Thanks for sending it through. If you have further drawings or a bid
        package to add, reply to the confirmation email and it will reach the
        same place.
      </p>
      <div style="display:flex;gap:.8rem;justify-content:center;flex-wrap:wrap">
        <a class="btn btn--bronze" href="index.html">Back to home <span class="btn__arrow" aria-hidden="true">&rarr;</span></a>
        <a class="btn btn--outline" href="portfolio.html">See our projects</a>
      </div>
    </div>
  </section>
</main>
""" + footer())


def page_thankyou_prequal():
    """Landing page for the prequalification form. A multipart POST navigates
    away, so FormSubmit needs somewhere on our own site to return people to."""
    return (
        head("Prequalification received | BND Construction",
             "Thanks - your prequalification has reached BND Construction.",
             "thank-you-prequal.html", "images/projects/villa-at-vanston-lg.jpg")
        + header("subcontractors.html")
        + """
<main id="main">
  <section class="section" style="padding-top:clamp(3rem,7vw,5.5rem)">
    <div class="wrap wrap--narrow" style="text-align:center">
      <p class="kicker">Prequalification received</p>
      <h1 class="h1" style="margin:1rem 0 1.1rem">That&rsquo;s with us.</h1>
      <p class="lede" style="margin:0 auto 2rem;max-width:48ch">
        Thanks for sending it through. We will be in touch when your trade fits
        a project we are bidding.
      </p>
      <div style="display:flex;gap:.8rem;justify-content:center;flex-wrap:wrap">
        <a class="btn btn--bronze" href="index.html">Back to home <span class="btn__arrow" aria-hidden="true">&rarr;</span></a>
        <a class="btn btn--outline" href="portfolio.html">See our projects</a>
      </div>
    </div>
  </section>
</main>
""" + footer())


def page_estimate():
    """The bid form on its own page. Contact keeps the offices and direct lines;
    this page is purely the request path, so it can be linked straight from a
    proposal or an email."""
    return (
        head("Request an Estimate | BND Construction",
             "Send your project to BND Construction estimating - drawings and a scope, or "
             "just a location and the date you need to open.",
             "request-an-estimate.html", "images/projects/oak-point-lg.jpg")
        + header("request-an-estimate.html")
        + phead("Request an estimate",
                "Drawings and a scope are ideal. A location and the date you need to open "
                "is enough to start.",
                "Request an Estimate", None)
        + f"""  <section class="section section--mist" id="request-estimate" aria-labelledby="bid-h">
    <div class="wrap wrap--narrow">
      <p class="eyebrow">Request an estimate</p>
      <h2 class="h3" id="bid-h" style="font-size:clamp(1.15rem,1.05rem + .5vw,1.45rem);margin-bottom:.9rem">Tell us about the project</h2>

      <div class="formwrap" data-reveal style="background:var(--paper)">
        <form data-validate
              action="https://formsubmit.co/vcgcbids@gmail.com"
              method="POST" enctype="multipart/form-data" novalidate>
          <input type="hidden" name="_subject" value="BND estimate request">
          <input type="hidden" name="_template" value="table">
          <input type="hidden" name="_captcha" value="false">
          <input type="hidden" name="_cc" value="daniel@bnd-co.com">
          <input type="hidden" name="_next" value="https://bnd-construction-site.vercel.app/thank-you-estimate.html">
          <div class="fgrid fgrid--2">
            <div class="fld">
              <label for="c-name">Name</label>
              <input id="c-name" name="name" data-label="Name" type="text" autocomplete="name" required>
            </div>
            <div class="fld">
              <label for="c-company">Company</label>
              <input id="c-company" name="company" data-label="Company" type="text" autocomplete="organization">
            </div>
            <div class="fld">
              <label for="c-email">Email</label>
              <input id="c-email" name="email" data-label="Email" type="email" autocomplete="email" required>
            </div>
            <div class="fld">
              <label for="c-phone">Phone</label>
              <input id="c-phone" name="phone" data-label="Phone" type="tel" autocomplete="tel" required>
            </div>
            <div class="fld">
              <label for="c-market">Market</label>
              <select id="c-market" name="market" data-label="Market">
                <option>Restaurant &amp; food service</option>
                <option>Retail</option>
                <option>Medical &amp; dental</option>
                <option>Education</option>
                <option>Multifamily</option>
                <option>Industrial &amp; warehouse</option>
                <option>Convenience &amp; fuel</option>
                <option>Other</option>
              </select>
            </div>
            <div class="fld">
              <label for="c-scope">Type of work</label>
              <select id="c-scope" name="scope" data-label="Type of work">
                <option>Ground-up construction</option>
                <option>Tenant finish-out</option>
                <option>Renovation &amp; remodeling</option>
                <option>Design-build</option>
                <option>Not sure yet</option>
              </select>
            </div>
            <div class="fld fspan">
              <label for="c-location">Project location</label>
              <input id="c-location" name="location" data-label="Location" type="text" placeholder="City and state">
            </div>
            <div class="fld fspan">
              <label for="c-message">Project Scope</label>
              <textarea id="c-message" name="message" data-label="Project Scope" rows="5" required></textarea>
            </div>

            <div class="fld fspan">
              <label for="c-plans">Submit plans <span style="text-transform:none;letter-spacing:0;color:var(--slate)">— optional, if you have drawings. PDF or image, up to 5&nbsp;MB</span></label>
              <input id="c-plans" name="attachment" data-label="Plans" type="file"
                     accept=".pdf,.jpg,.jpeg,.png,application/pdf,image/jpeg,image/png">
            </div>
          </div>
          <button class="btn btn--ink" type="submit" style="margin-top:1.5rem">
            Send to estimating <span class="btn__arrow" aria-hidden="true">&rarr;</span>
          </button>
        </form>
        <p class="fmsg" data-form-msg role="status" aria-live="polite"></p>
      </div>
    </div>
  </section>

"""
        + "\n</main>\n" + footer(forms=True))


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(content)
    print("  wrote %-42s %6d bytes" % (path, len(content)))


# ------------------------------------------------------------------ pages
ICON = {
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><path d="M12 3l8 3v6c0 5-3.4 8.2-8 9-4.6-.8-8-4-8-9V6z"/></svg>',
    "check":  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>',
    "scale":  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><path d="M12 3v18M5 7h14M7 7l-3 7h6zM17 7l-3 7h6z"/></svg>',
    "link":   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><path d="M10 13a5 5 0 007.5.5l2-2A5 5 0 1012.5 4.5L11 6"/><path d="M14 11a5 5 0 00-7.5-.5l-2 2A5 5 0 1011.5 19.5L13 18"/></svg>',
    "people": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><circle cx="9" cy="8" r="3.2"/><path d="M3 20a6 6 0 0112 0"/><path d="M16 5.5a3.2 3.2 0 010 5.6M17 20a6 6 0 00-2-4.4"/></svg>',
}


def page_about():
    """About - proof and storytelling rather than consecutive text blocks."""
    values = [
        ("scale",  "Honesty &amp; integrity", "We maintain honesty and integrity while achieving the finished product our clients expect."),
        ("check",  "Accountability", "Being responsive to your needs and managing the materials we use is critical to a successful project."),
        ("shield", "Safety without compromise", "Zero tolerance for safety violations, from senior management to laborers in the field."),
        ("link",   "Long-term relationships", "We cultivate strong business relationships for continued mutual success."),
    ]
    val_html = "".join(
        f'<div class="vcard" data-reveal>{ICON[k]}<h3 class="h3">{t}</h3><p>{d}</p></div>'
        for k, t, d in values)

    trust = [
        ("Transparent communication.", "You deal with the people running the job. If something changes on site, you hear it from us first."),
        ("On schedule.", "Projects are planned around real deadlines and managed to hold them."),
        ("Under budget.", "We value engineer early, while it still changes the number rather than the paperwork."),
        ("Relationships built to last.", "Most of our work arrives through people who have built with us before."),
    ]
    trust_html = "".join(
        f'<div class="vcard" data-reveal><h3 class="h3">{t}</h3><p>{d}</p></div>' for t, d in trust)

    safety = ["OSHA safety training", "SWPPP certification", "Daily site supervision", "Strict quality control"]
    safety_html = "".join(f'<li data-reveal>{ICON["check"]}<span>{x}</span></li>' for x in safety)

    return (
        head("About | BND Construction",
             "Over 25 years of combined commercial construction experience. Licensed and insured, "
             "with OSHA-trained superintendents and zero tolerance for safety violations.",
             "about.html", "images/projects/villa-at-vanston-lg.jpg")
        + header("about.html")
        + f"""
<main id="main">

  <section class="section pintro">
    <div class="wrap">
      <nav class="crumb" aria-label="Breadcrumb">
        <a href="index.html">Home</a> <span aria-hidden="true">/</span> <span>About</span>
      </nav>
      <p class="eyebrow" data-reveal>About BND</p>
      <h1 class="h1" data-reveal data-delay="1" style="max-width:14ch;margin-top:1rem">Built on trust.<br>Focused on quality.</h1>
      <p class="lede" data-reveal data-delay="2" style="max-width:58ch;margin-top:1.4rem">
        BND Construction is a licensed and insured commercial general contractor delivering
        ground-up construction, tenant finish-out, renovation and design-build throughout Texas
        and surrounding states &mdash; for developers, building owners, brokers, architects and
        national brands.
      </p>

      <div class="metrics metrics--3" data-reveal data-delay="3" style="margin-top:clamp(2.5rem,5vw,3.5rem)">
        <div class="metric"><p class="metric__k">25+</p><p class="metric__v">Years combined experience</p></div>
        <div class="metric"><p class="metric__k">7</p><p class="metric__v">Market sectors</p></div>
        <div class="metric"><p class="metric__k">OSHA</p><p class="metric__v">Certified superintendents</p></div>
      </div>

    </div>
  </section>

  <section class="section section--mist">
    <div class="wrap">
      <div class="phil">
        <div class="phil__body">
          <p class="eyebrow" data-reveal>Our philosophy</p>
          <p class="phil__statement" data-reveal data-delay="1">We believe successful projects begin long before construction <em>starts</em>.</p>
          <p data-reveal data-delay="2">
            Budgets get set during planning, not after drawings land. We interface with your design
            team early, say plainly what a schedule can carry, and stay responsive once the job is
            running.
          </p>
          <p data-reveal data-delay="2">
            On site that means careful management of the materials we use and jobsites kept as clean
            as possible &mdash; because on a finish-out inside a trading centre, that is the difference
            between a neighbour complaint and a repeat client.
          </p>
        </div>
        <div class="phil__media" data-reveal data-delay="1">
          <img src="images/projects/villa-at-vanston-lg.jpg" alt="Villa at Vanston, a 176-unit multifamily development built by BND Construction" width="1800" height="1100" loading="lazy" decoding="async">
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="mv">
        <div data-reveal>
          <p class="eyebrow">Mission</p>
          <p class="mv__k">Deliver the finished product our clients expect.</p>
          <p>To build commercial projects safely, on schedule and under budget &mdash; maintaining
             honesty and integrity from the first budget through to handover.</p>
        </div>
        <div data-reveal data-delay="1">
          <p class="eyebrow">Vision</p>
          <p class="mv__k">To be the contractor that gets called back.</p>
          <p>To grow through repeat work and referral rather than through the lowest number on a
             bid tab, and to keep the relationships that produce it.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--mist">
    <div class="wrap">
      <p class="eyebrow" data-reveal>Experience</p>
      <h2 class="h2" data-reveal data-delay="1" style="margin:1rem 0 1.4rem;max-width:20ch">Over 25 years of commercial construction experience.</h2>
      <p class="lede" data-reveal data-delay="2" style="max-width:62ch">
        Our management team has provided construction and design-build services for high-end
        restaurants, educational facilities, retail and hotel developments, industrial and warehouse
        space, tenant build-outs, supermarkets, convenience stores and medical centers.
      </p>
      <div class="metrics metrics--2" data-reveal style="margin-top:clamp(2.5rem,5vw,3.5rem)">
        <div class="metric"><p class="metric__k">12</p><p class="metric__v">Ground-up builds</p></div>
        <div class="metric"><p class="metric__k">7</p><p class="metric__v">Tenant finish-outs</p></div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <p class="eyebrow" data-reveal>Project experience</p>
      <div class="showcase">
        <div class="showcase__media" data-reveal>
          <img src="images/projects/walk-ons-sports-bistreaux-lg.jpg" alt="Walk-On's Sports interior bar and dining room, built by BND Construction" width="1800" height="1436" loading="lazy" decoding="async">
        </div>
        <div class="showcase__body" data-reveal data-delay="1">
          <h2 class="h2" style="font-size:clamp(1.5rem,1.2rem + 1.4vw,2.2rem)">Walk-On&rsquo;s Sports</h2>
          <dl class="showcase__facts">
            <div><dt>Location</dt><dd>Conroe, TX</dd></div>
            <div><dt>Market</dt><dd>Restaurant &amp; food service</dd></div>
            <div><dt>Scope</dt><dd>New construction</dd></div>
            <div><dt>Status</dt><dd>Complete</dd></div>
          </dl>
          <a class="btn btn--outline" href="projects/walk-ons-sports-bistreaux.html" style="margin-top:1.8rem">View project <span class="btn__arrow" aria-hidden="true">&rarr;</span></a>
        </div>
      </div>
    </div>
  </section>

"""
        + closing_split("about")
        + "</main>"
        + footer())


def page_services():
    rows = ""
    for i, (name, slug, image, paras, tags) in enumerate(SERVICES, 1):
        body = "\n          ".join("<p>%s</p>" % p for p in paras)
        chips = "\n            ".join("<li>%s</li>" % t for t in tags)
        rows += f"""
      <div class="srow" id="{slug}" data-reveal>
        <div class="srow__media">
          <img src="images/projects/{image}.jpg" alt="" width="900" height="675" loading="lazy" decoding="async">
        </div>
        <div class="srow__body">
          <p class="srow__n">{i:02d} &nbsp;/&nbsp; Service</p>
          <h2 class="h2" style="font-size:clamp(1.5rem,1.2rem + 1.4vw,2.2rem)">{name}</h2>
          <div style="margin-top:1rem">
          {body}
          </div>
          <ul class="srow__list">
            {chips}
          </ul>
        </div>
      </div>
"""
    return (
        head("Services | BND Construction",
             "Ground-up construction, tenant finish-out, renovation and remodeling, and design-build "
             "delivered on schedule and under budget throughout Texas and surrounding states.",
             "services.html", "images/projects/walk-ons-sports-bistreaux-lg.jpg")
        + header("services.html")
        + phead("Services",
                "Four ways we take a project on &mdash; each managed to stay on schedule, under budget, "
                "and clean on site.",
                "Services", None)
        + GABLE
        + '\n  <section class="section">\n    <div class="wrap">\n' + rows
        + "    </div>\n  </section>\n"
        + cta_split() + "\n</main>\n" + footer())


def page_markets(pr):
    rows = ""
    for i, (name, blurb, note) in enumerate(MARKETS, 1):
        plain = name.replace("&amp;", "&")
        rel = [p for p in pr if p["market"].replace("&", "&").lower() == plain.lower()]
        chips = ""
        if rel:
            chips = ('<ul class="msec__projects">'
                     + "".join("<li>%s</li>" % p["name"] for p in rel[:6])
                     + "</ul>")
        rows += f"""
      <div class="msec" data-reveal>
        <p class="msec__n">{i:02d}</p>
        <div>
          <h2 class="h3" style="font-size:clamp(1.25rem,1.1rem + .8vw,1.65rem)">{name}</h2>
          <p class="spec" style="margin-top:.6rem">{note}</p>
        </div>
        <div class="msec__body">
          <p>{blurb}</p>
          {chips}
        </div>
      </div>
"""
    return (
        head("Markets We Serve | BND Construction",
             "Restaurant and food service, retail, medical and dental, education, multifamily, "
             "industrial and warehouse, and convenience and fuel — seven sectors, one standard.",
             "markets.html", "images/projects/evolve-dermatology-lg.jpg")
        + header("markets.html")
        + phead("Markets we serve",
                "Seven sectors. Our management team has delivered in all of them, and the lessons "
                "carry from one to the next.",
                "Markets", None)
        + GABLE
        + '\n  <section class="section">\n    <div class="wrap">\n' + rows
        + "    </div>\n  </section>\n"
        + cta_split() + "\n</main>\n" + footer())


def page_portfolio(pr):
    shot = [p for p in pr if p["photo"]]

    markets = sorted({p["market"] for p in pr})
    chips = '<button type="button" data-filter="all" aria-pressed="true">All work</button>'
    for m in markets:
        chips += f'\n        <button type="button" data-filter="{m}" aria-pressed="false">{m}</button>'

    cards = ""
    for p in shot:
        loc = f'<i class="spec__sep" aria-hidden="true"></i><span>{p["location"]}</span>' if p["location"] else ""
        place = f'<span class="pcard__line">{p["location"]}</span>' if p["location"] else ""
        cards += f"""
        <a class="pcard" href="projects/{p['slug']}.html" data-market="{p['market']}" data-reveal>
          <span class="pcard__media">
            <img src="images/projects/{p['slug']}.jpg" alt="{p['alt']}" width="900" height="675" loading="lazy" decoding="async">
          </span>
          <span class="pcard__body">
            <span class="pcard__type">{p['market']}</span>
            <span class="pcard__name">{p['name']}</span>
            <span class="pcard__line">{p['scope']}</span>
            {place}
            <span class="pcard__go">View project <i aria-hidden="true">&rarr;</i></span>
          </span>
        </a>
"""

    listed = [p for p in pr if not p["photo"]]
    rows = ""
    for p in listed:
        rows += f"""        <div class="plist__row" data-market="{p['market']}">
          <p class="plist__name">{p['name']}</p>
          <p class="plist__loc">{p['location'] or '&mdash;'}</p>
          <p class="plist__tag">{p['scope']}</p>
        </div>
"""

    return (
        head("Portfolio | BND Construction",
             "Completed commercial construction across restaurants, retail, medical, education, "
             "multifamily and convenience and fuel throughout Texas and surrounding states.",
             "portfolio.html", "images/projects/oak-point-lg.jpg")
        + header("portfolio.html")
        + phead("Portfolio",
                "Completed commercial work across restaurants, retail, medical and dental, education, multifamily, and convenience and fuel &mdash; built throughout Texas and surrounding states.",
                "Portfolio", None)
        + GABLE
        + f"""
  <section class="section">
    <div class="wrap">

      <div class="filter" role="group" aria-label="Filter projects by market">
        {chips}
      </div>

      <div class="pgrid pgrid--3" id="pgrid">
{cards}      </div>

      <div class="plist" id="plist" hidden>
        <p class="plist__head">Also delivered in this market</p>
{rows}      </div>

    </div>
  </section>
"""
        + closing_split("portfolio") + """
</main>
<script>
/* portfolio filter — plain DOM, no dependency.
   The text-only entries stay out of the default "All work" view and appear
   only when their own market is selected. */
(function () {
  var buttons = document.querySelectorAll('.filter button');
  var cards   = document.querySelectorAll('#pgrid .pcard');
  var rows    = document.querySelectorAll('#plist .plist__row');
  var plist   = document.getElementById('plist');
  if (!buttons.length) return;

  function apply(market) {
    var all = market === 'all';
    var shown = 0;

    Array.prototype.forEach.call(cards, function (el) {
      var hit = all || el.getAttribute('data-market') === market;
      el.classList.toggle('is-hidden', !hit);
      if (hit) shown++;
    });

    var listedShown = 0;
    Array.prototype.forEach.call(rows, function (el) {
      var hit = !all && el.getAttribute('data-market') === market;
      el.classList.toggle('is-hidden', !hit);
      if (hit) listedShown++;
    });

    if (plist) plist.hidden = listedShown === 0;
    /* an empty grid still reserves its gap, so collapse it when a market has
       no photographed work */
    var grid = document.getElementById('pgrid');
    if (grid) grid.hidden = shown === 0;

  }

  /* deep link: /portfolio.html?market=Retail opens already filtered, so the
     nav dropdown lands on the right view instead of the full grid */
  var wanted = new URLSearchParams(window.location.search).get('market');
  if (wanted) {
    var match = Array.prototype.filter.call(buttons, function (b) {
      return b.getAttribute('data-filter') === wanted;
    })[0];
    if (match) {
      Array.prototype.forEach.call(buttons, function (o) { o.setAttribute('aria-pressed', 'false'); });
      match.setAttribute('aria-pressed', 'true');
      apply(wanted);
    }
  }

  Array.prototype.forEach.call(buttons, function (b) {
    b.addEventListener('click', function () {
      Array.prototype.forEach.call(buttons, function (o) { o.setAttribute('aria-pressed', 'false'); });
      b.setAttribute('aria-pressed', 'true');
      apply(b.getAttribute('data-filter'));
    });
  });
})();
</script>
""" + footer())


def page_subcontractors():
    return (
        head("Subcontractors &amp; Bidding | BND Construction",
             "BND Construction seeks competitive, qualified local and national subcontractors and "
             "suppliers. Submit your prequalification to get on the bid list.",
             "subcontractors.html", "images/projects/villa-at-vanston-lg.jpg")
        + header("subcontractors.html")
        + phead("Subcontractors &amp; bidding",
                "We build projects that are successful for all parties involved. That starts with who "
                "we put on the job.",
                "Subcontractors", None)
        + GABLE
        + """
  <section class="section">
    <div class="wrap">
      <div class="block" data-reveal>
        <p class="block__label">What we look for</p>
        <div class="block__body">
          <p class="lede" style="color:var(--ink)">
            We seek the most competitive and qualified local and national subcontractors and suppliers.
            They must have the operational and financial capacity to successfully perform on each project.
          </p>
          <p style="margin-top:1.1rem">
            We work closely with our trades throughout a build rather than handing down a scope and
            walking away. Every superintendent on our sites carries OSHA safety training and SWPPP
            certification, and we hold our subcontractors to the same zero-tolerance standard on safety.
          </p>
        </div>
      </div>

      <div class="block" data-reveal>
        <p class="block__label">Before you submit</p>
        <div class="block__body">
          <h2 class="h3">Have these ready</h2>
          <p>
            Current licensing for the trades you perform, certificates of insurance, bonding capacity if
            you carry it, and the counties or metro areas you can genuinely cover. Tell us the truth about
            capacity &mdash; a trade that is honest about its limits gets called back.
          </p>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--mist" id="prequal" aria-labelledby="pq-k">
    <div class="wrap wrap--narrow">
      <p class="eyebrow" id="pq-k">Prequalification</p>

      <div class="formwrap" data-reveal>
        <form data-validate
              action="https://formsubmit.co/vcgcbids@gmail.com"
              method="POST" enctype="multipart/form-data" novalidate>
          <input type="hidden" name="_subject" value="BND subcontractor prequalification">
          <input type="hidden" name="_template" value="table">
          <input type="hidden" name="_captcha" value="false">
          <input type="hidden" name="_cc" value="daniel@bnd-co.com">
          <input type="hidden" name="_next" value="https://bnd-construction-site.vercel.app/thank-you-prequal.html">
          <div class="fgrid fgrid--2">
            <div class="fld">
              <label for="sc-company">Company</label>
              <input id="sc-company" name="company" data-label="Company" type="text" autocomplete="organization" required>
            </div>
            <div class="fld">
              <label for="sc-trade">Trade</label>
              <input id="sc-trade" name="trade" data-label="Trade" type="text" placeholder="Electrical, MEP, drywall…" required>
            </div>
            <div class="fld">
              <label for="sc-name">Contact name</label>
              <input id="sc-name" name="name" data-label="Name" type="text" autocomplete="name" required>
            </div>
            <div class="fld">
              <label for="sc-email">Email</label>
              <input id="sc-email" name="email" data-label="Email" type="email" autocomplete="email" required>
            </div>
            <div class="fld">
              <label for="sc-phone">Phone</label>
              <input id="sc-phone" name="phone" data-label="Phone" type="tel" autocomplete="tel" required>
            </div>
            <div class="fld">
              <label for="sc-area">Coverage area</label>
              <input id="sc-area" name="area" data-label="Coverage area" type="text" placeholder="DFW metro, statewide…" required>
            </div>
            <div class="fld">
              <label for="sc-licensed">Licensed</label>
              <select id="sc-licensed" name="licensed" data-label="Licensed">
                <option value="Yes">Yes</option>
                <option value="No">No</option>
                <option value="Not applicable">Not applicable to my trade</option>
              </select>
            </div>
            <div class="fld">
              <label for="sc-bonded">Bonding capacity</label>
              <select id="sc-bonded" name="bonded" data-label="Bonding capacity">
                <option value="Yes">Yes</option>
                <option value="No">No</option>
              </select>
            </div>
            <div class="fld fspan">
              <label for="sc-insured">Insurance carried</label>
              <input id="sc-insured" name="insured" data-label="Insurance" type="text" placeholder="General liability, workers' comp, limits">
            </div>
            <div class="fld fspan">
              <label for="sc-notes">Anything else</label>
              <textarea id="sc-notes" name="notes" data-label="Notes" rows="4" placeholder="Recent comparable projects, crew size, current capacity"></textarea>
            </div>

            <div class="fld fspan">
              <label for="sc-file">Attach a document <span style="text-transform:none;letter-spacing:0;color:var(--slate)">&mdash; optional. Capability statement, COI or licence. PDF, Word or image, up to 5&nbsp;MB</span></label>
              <input id="sc-file" name="attachment" data-label="Document" type="file"
                     accept=".pdf,.doc,.docx,.jpg,.jpeg,.png,application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document,image/jpeg,image/png">
            </div>
          </div>
          <button class="btn btn--bronze" type="submit" style="margin-top:1.5rem">
            Submit prequalification <span class="btn__arrow" aria-hidden="true">&rarr;</span>
          </button>
        </form>
        <p class="fmsg" data-form-msg role="status" aria-live="polite"></p>
      </div>
    </div>
  </section>
"""
        + closing_split("subcontractors")
        + "</main>"
        + footer(forms=True))


def page_contact():
    offices = ""
    for city, street, region in OFFICES:
        offices += f"""        <div class="ccard" data-reveal>
          <p class="ccard__role">{city}</p>
          <p class="ccard__name" style="font-size:1.05rem">{street}</p>
          <p class="ccard__for" style="margin-bottom:0">{region}</p>
        </div>
"""

    return (
        head("Contact | BND Construction",
             "Request an estimate from BND Construction — your project goes straight to estimating.",
             "contact.html", "images/projects/oak-point-lg.jpg")
        + header("contact.html")
        + phead("Contact",
                "Project enquiries and bid invitations go straight to estimating. General questions reach the same desk &mdash; use the form below, or the office details further down.",
                "Contact", None)
        + GABLE
        + f"""
  <section class="section section--mist" id="enquiry" aria-labelledby="enq-h">
    <div class="wrap wrap--narrow">
      <p class="eyebrow">General enquiries</p>
      <h2 class="h3" id="enq-h" style="font-size:clamp(1.15rem,1.05rem + .5vw,1.45rem);margin-bottom:.8rem">Send us a message</h2>
      <p class="lede" style="margin-bottom:1.75rem;max-width:52ch">
        For anything that isn&rsquo;t a bid request or a trade prequalification &mdash; those each have
        their own form.
      </p>

      <div class="formwrap" data-reveal style="background:var(--paper)">
        <form data-form data-subject="BND general enquiry"
              data-success="Thanks — your message is with us. We'll come back to you shortly."
              novalidate>
          <div class="fgrid fgrid--2">
            <div class="fld">
              <label for="e-first">First name</label>
              <input id="e-first" name="first_name" data-label="First name" type="text" autocomplete="given-name" required>
            </div>
            <div class="fld">
              <label for="e-last">Last name</label>
              <input id="e-last" name="last_name" data-label="Last name" type="text" autocomplete="family-name" required>
            </div>
            <div class="fld">
              <label for="e-email">Email</label>
              <input id="e-email" name="email" data-label="Email" type="email" autocomplete="email" required>
            </div>
            <div class="fld">
              <label for="e-phone">Phone</label>
              <input id="e-phone" name="phone" data-label="Phone" type="tel" autocomplete="tel">
            </div>
            <div class="fld fspan">
              <label for="e-msg">Message</label>
              <textarea id="e-msg" name="message" data-label="Message" rows="5" required></textarea>
            </div>
          </div>
          <button class="btn btn--ink" type="submit" style="margin-top:1.5rem">
            Send message <span class="btn__arrow" aria-hidden="true">&rarr;</span>
          </button>
        </form>
        <p class="fmsg" data-form-msg role="status" aria-live="polite"></p>
      </div>
    </div>
  </section>

  <section class="section section--tight">
    <div class="wrap">
      <p class="kicker" data-reveal>Offices</p>
      <div class="pgrid pgrid--2" style="margin:1.1rem 0 clamp(1.5rem,3vw,2.25rem)">
{offices}      </div>
    </div>
  </section>

  <section class="section section--tight">
    <div class="wrap">
      <div class="pgrid pgrid--2">
        <div class="ccard" data-reveal>
          <p class="ccard__role">Subcontractors</p>
          <p class="h3" style="margin-bottom:.5rem">Not a project enquiry?</p>
          <p class="ccard__for">Trades and suppliers should submit a prequalification instead &mdash; it captures the licensing and coverage detail we need.</p>
          <a class="tlink" href="subcontractors.html">Prequalify <span aria-hidden="true">&rarr;</span></a>
        </div>
        <div class="ccard" data-reveal data-delay="1">
          <p class="ccard__role">Service area</p>
          <p class="h3" style="margin-bottom:.5rem">Texas and surrounding states</p>
          <p class="ccard__for">We build throughout Texas and into neighbouring states, with completed work in Oklahoma. If you are outside that footprint, ask &mdash; we will tell you straight.</p>
        </div>
      </div>
    </div>
  </section>
"""
        + closing_split("contact")
        + "</main>"
        + footer(forms=True))


def project_overview(p):
    """Composed from the recorded fields only. BND has no written overviews, so
    this states what is known rather than inventing case-study narrative."""
    where = f" in {p['location']}" if p["location"] else ""
    first = f"{p['name']} was delivered by BND Construction as a {p['scope'].split(' — ')[0].lower()} project{where}."
    sc = p["scope"].lower()
    if "finish" in sc or "build-out" in sc or "remodel" in sc or "renovation" in sc:
        second = ("The work was sequenced to keep disruption to neighbouring tenants to a minimum, "
                  "and managed to stay on schedule and under budget.")
    else:
        second = ("The build was managed from site through to handover, staying on schedule and "
                  "under budget, with the jobsite kept clean throughout.")
    return first + " " + second


def project_highlights(p):
    """Work packages implied by the recorded scope, using BND's own service
    language rather than claiming systems we cannot verify."""
    sc = p["scope"].lower()
    if "new construction" in sc or "ground-up" in sc:
        return ["Site development", "Shell & core", "Full build-out", "Handover on schedule"]
    if "finish" in sc or "build-out" in sc:
        return ["Interior fit-out", "Occupied premises", "Value engineering", "Handover on schedule"]
    return ["Targeted upgrades", "Full renovation", "Occupied premises", "Handover on schedule"]


TICK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" '
        'aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>')


def page_project(p, prev_p, next_p, pr):
    """One project page — a case study rather than a gallery entry.
    Every project publishes through this same template."""
    facts = [("Market", p["market"]), ("Project type", p["scope"].split(" — ")[0])]
    if p["location"]:
        facts.append(("Location", p["location"]))
    facts.append(("Status", p["status"]))
    if " — " in p["scope"]:                       # square footage, where recorded
        facts.append(("Project size", p["scope"].split(" — ")[1]))
    fact_html = "".join(
        f'<div class="cfact" data-reveal><p class="cfact__k">{k}</p><p class="cfact__v">{v}</p></div>'
        for k, v in facts)

    hi_html = "".join(
        f'<li data-reveal>{TICK}<span>{h}</span></li>' for h in project_highlights(p))

    related = [q for q in pr if q["photo"] and q["market"] == p["market"] and q["slug"] != p["slug"]][:3]
    rel_html = ""
    if related:
        cards = ""
        for q in related:
            place = f'<span class="pcard__line">{q["location"]}</span>' if q["location"] else ""
            cards += f"""
          <a class="pcard" href="{q['slug']}.html" data-reveal>
            <span class="pcard__media">
              <img src="../images/projects/{q['slug']}.jpg" alt="{q['alt']}" width="900" height="675" loading="lazy" decoding="async">
            </span>
            <span class="pcard__body">
              <span class="pcard__type">{q['market']}</span>
              <span class="pcard__name">{q['name']}</span>
              <span class="pcard__line">{q['scope'].split(' — ')[0]}</span>
              {place}
              <span class="pcard__go">View project <i aria-hidden="true">&rarr;</i></span>
            </span>
          </a>
"""
        rel_html = f"""
  <section class="section section--mist">
    <div class="wrap">
      <p class="eyebrow">More {p['market'].lower()} projects</p>
      <div class="pgrid pgrid--3" style="margin-top:clamp(1.75rem,3.5vw,2.75rem)">{cards}      </div>
    </div>
  </section>
"""

    prev_link = (f'<a class="tlink" href="{prev_p["slug"]}.html"><span aria-hidden="true">&larr;</span> {prev_p["name"]}</a>'
                 if prev_p else '<span></span>')
    next_link = (f'<a class="tlink" href="{next_p["slug"]}.html">{next_p["name"]} <span aria-hidden="true">&rarr;</span></a>'
                 if next_p else '<span></span>')
    place_label = f'<span>{p["location"]}</span>' if p["location"] else ""

    return (
        head(f"{p['name']} | BND Construction",
             f"{p['name']} - {p['scope'].split(' - ')[0].lower()} in {p['market'].lower()}, delivered by BND Construction.",
             f"projects/{p['slug']}.html",
             f"images/projects/{p['slug']}-lg.jpg", depth=1)
        + header("portfolio.html", depth=1, solid=True)
        + f"""
<main id="main">

  <!-- hero -->
  <section class="chero">
    <div class="chero__media">
      <img src="../images/projects/{p['slug']}-lg.jpg" alt="{p['alt']}" width="1800" height="1350" fetchpriority="high">
    </div>
    <div class="wrap chero__inner">
      <nav class="crumb" aria-label="Breadcrumb">
        <a href="../index.html">Home</a> <span aria-hidden="true">/</span>
        <a href="../portfolio.html">Portfolio</a> <span aria-hidden="true">/</span>
        <span>{p['name']}</span>
      </nav>
      <div class="chero__tags">
        <span>{p['market']}</span>
        <span>{p['scope'].split(' — ')[0]}</span>
        {place_label}
        <span>{p['status']}</span>
      </div>
    </div>
  </section>

  <!-- title + overview -->
  <section class="section">
    <div class="wrap cintro">
      <h1 class="h1" data-reveal>{p['name']}</h1>
      <p class="lede" data-reveal data-delay="1">{project_overview(p)}</p>
    </div>
  </section>

  <!-- facts -->
  <section class="section" style="padding-top:0">
    <div class="wrap">
      <div class="cfacts">{fact_html}</div>
    </div>
  </section>

  <!-- highlights -->
  <section class="section section--mist">
    <div class="wrap">
      <p class="eyebrow" data-reveal>Scope of works</p>
      <ul class="chighlights">{hi_html}</ul>
    </div>
  </section>

  <!-- quote -->
  <section class="section cquote">
    <div class="wrap wrap--narrow" style="text-align:center">
      <blockquote data-reveal>Every project is built to earn <em>the next one</em>.</blockquote>
      <p class="cquote__attr" data-reveal data-delay="1">BND Construction</p>
    </div>
  </section>

  <div class="wrap">
    <div class="pnav">
      {prev_link}
      {next_link}
    </div>
  </div>
{rel_html}
  <!-- cta -->
  <section class="section">
    <div class="wrap wrap--narrow" style="text-align:center">
      <h2 class="h2" data-reveal style="max-width:20ch;margin-inline:auto">Ready to build your next commercial project?</h2>
      <p class="lede" data-reveal data-delay="1" style="margin:1.2rem auto 2rem;max-width:52ch">
        Whether you are planning a ground-up development, a tenant finish-out or a renovation,
        send it through and estimating will come back to you.
      </p>
      <div data-reveal data-delay="2" style="display:flex;gap:.8rem;justify-content:center;flex-wrap:wrap">
        <a class="btn btn--bronze" href="../request-an-estimate.html">Request an estimate <span class="btn__arrow" aria-hidden="true">&rarr;</span></a>
        <a class="btn btn--outline" href="../portfolio.html">View portfolio</a>
      </div>
    </div>
  </section>
</main>
"""
        + footer(depth=1))


def main():
    pr = projects()
    shot = [p for p in pr if p["photo"]]

    print("Building BND Construction — %d projects (%d with photography)" % (len(pr), len(shot)))

    write("about.html",          page_about())
    write("company.html",        page_company(pr))
    write("careers.html",        page_careers())
    write("thank-you.html",      page_thankyou())
    write("thank-you-estimate.html", page_thankyou_estimate())
    write("thank-you-prequal.html",  page_thankyou_prequal())
    write("services.html",       page_services())
    write("markets.html",        page_markets(pr))
    write("portfolio.html",      page_portfolio(pr))
    write("subcontractors.html", page_subcontractors())
    write("contact.html",        page_contact())
    write("request-an-estimate.html", page_estimate())

    for i, p in enumerate(shot):
        write("projects/%s.html" % p["slug"],
              page_project(p, shot[i - 1] if i else None,
                           shot[i + 1] if i + 1 < len(shot) else None, pr))

    print("Done. %d pages." % (11 + len(shot)))


if __name__ == "__main__":
    main()
