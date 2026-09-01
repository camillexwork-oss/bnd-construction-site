#!/usr/bin/env python3
"""
BND Construction — page generator for the "classic" direction.

Every page below shares one head, one nav, one footer and one palette, so a
colour or nav change is a single edit here rather than seven. Real content is
imported from build.py, which already holds it as data — nothing is retyped
and nothing is invented.

Run:  python3 build-classic.py
"""

import build as data   # SERVICES, MARKETS, PROCESS, OFFICES, projects() ...

SUF = "-classic"
NAV = [
    ("about",         "About"),
    ("portfolio",     "Portfolio"),
    ("services",      "Services"),
    ("subcontractor", "Subcontractors"),
    ("contact",       "Contact"),
]
CTA = ("estimate", "Request an Estimate")
OFFICE = "office@bnd-co.com"          # subcontractor + general contact
INBOX = "vcgcbids@gmail.com"          # Nawa — copied on estimates
CC = "daniel@bnd-co.com"
# Estimate requests go to estimating@, with the bids inbox copied in.
# estimate requests go straight to Daniel, with Nawa copied
ESTIMATE_TO = "daniel@bnd-co.com"
ESTIMATE_CC = "vcgcbids@gmail.com"
ESTIMATE_INBOX = "estimating@bnd-co.com"   # the address shown on the page
THANKS = "form-ok.html"


def url(stem):
    return "index%s.html" % SUF if stem == "index" else "%s%s.html" % (stem, SUF)


# --------------------------------------------------------------------------
# chrome
# --------------------------------------------------------------------------

ICONS = """<svg class="sr" aria-hidden="true" focusable="false"><defs>
  <g id="i-arrow" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
    <path d="M4 12h15.5M13.5 6l6 6-6 6"/></g>
  <g id="i-shield" fill="none" stroke="currentColor" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round">
    <path d="M12 2.5 4 5.6v6c0 5.1 3.4 8.9 8 9.9 4.6-1 8-4.8 8-9.9v-6Z"/><path d="m8.6 11.8 2.4 2.4 4.4-4.7"/></g>
  <g id="i-helmet" fill="none" stroke="currentColor" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round">
    <path d="M3 16.2a9 9 0 0 1 18 0"/><path d="M2 16.2h20v1.6a1.6 1.6 0 0 1-1.6 1.6H3.6A1.6 1.6 0 0 1 2 17.8Z"/>
    <path d="M9.6 7.6V4.9a1.3 1.3 0 0 1 1.3-1.3h2.2a1.3 1.3 0 0 1 1.3 1.3v2.7"/></g>
  <g id="i-clock" fill="none" stroke="currentColor" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="12" cy="12" r="9.2"/><path d="M12 6.6V12l3.6 2.2"/></g>
  <g id="i-crane" fill="none" stroke="currentColor" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round">
    <path d="M3 20.5h18M6 20.5V6.2h12"/><path d="M6 6.2 12 2.6l6 3.6"/><path d="M15.4 6.2v4.1M15.4 10.3h-2.2M13.2 10.3v2.6"/></g>
  <g id="i-blueprint" fill="none" stroke="currentColor" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round">
    <rect x="2.8" y="4.5" width="18.4" height="15" rx="1.2"/><path d="M2.8 9.2h18.4M8 9.2v10.3"/><path d="M11.6 13h6.2M11.6 16.1h4"/></g>
  <g id="i-trowel" fill="none" stroke="currentColor" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round">
    <path d="M13.6 3.4 20.6 10.4 12.4 18.6a2 2 0 0 1-2.9 0L5.4 14.5a2 2 0 0 1 0-2.9Z"/><path d="M15.6 5.4 18 3"/></g>
  <g id="i-frame" fill="none" stroke="currentColor" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round">
    <path d="M2.6 20.5h18.8M4.6 20.5V8.4l7.4-5 7.4 5v12.1"/><path d="M9 20.5v-6.2h6v6.2"/></g>
  <g id="i-ruler" fill="none" stroke="currentColor" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round">
    <rect x="1.8" y="8.4" width="20.4" height="7.2" rx="1" transform="rotate(-12 12 12)"/>
    <path d="M6.4 9.6v2.3M10 8.9v3.2M13.6 8.2v2.3M17.2 7.5v3.2"/></g>
  <g id="i-handshake" fill="none" stroke="currentColor" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round">
    <path d="M2.8 9.6 7 6.2l4 2.6 3.4-1.8 6.8 4.4"/><path d="m11 8.8-3.6 3a1.7 1.7 0 0 0 2.2 2.5l1.6-1.3 3 2.6 2.6-1.1"/>
    <path d="M2.8 9.6v6.2l3 2M21.2 11.4v5.1l-3 1.8"/></g>
</defs></svg>"""


def head(title, desc):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex,nofollow">

<link rel="icon" href="images/favicon.svg" type="image/svg+xml">
<link rel="preload" href="fonts/CabinetGrotesk-Extrabold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/PlusJakartaSans-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/classic.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

{ICONS}
"""


def header(active=""):
    links = "\n".join(
        '      <a href="%s"%s>%s</a>' % (url(s), ' aria-current="page"' if s == active else "", label)
        for s, label in NAV)
    sheet = "\n".join('    <a href="%s">%s</a>' % (url(s), label) for s, label in NAV)
    home_current = ' aria-current="page"' if active == "index" else ""
    return f"""
<header class="bar" id="bar">
  <div class="wrap bar__in">
    <a href="{url('index')}" aria-label="BND Construction — home"{home_current}>
      <img class="bar__logo" src="images/bnd-logo-white.png" alt="BND Construction" width="1312" height="502">
    </a>

    <nav class="bar__nav" aria-label="Primary">
{links}
    </nav>

    <div class="bar__end">
      <a class="btn btn--gold btn--sm bar__cta" href="{url(CTA[0])}">{CTA[1]}</a>
      <button class="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="sheet" data-open>
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>

<div class="sheet" id="sheet" hidden>
  <div class="sheet__top">
    <a href="{url('index')}" aria-label="BND Construction — home">
      <img class="bar__logo" src="images/bnd-logo-white.png" alt="BND Construction" width="1312" height="502">
    </a>
    <button class="sheet__x" type="button" data-close>Close</button>
  </div>
  <nav class="sheet__nav" aria-label="Mobile">
{sheet}
  </nav>
  <div class="sheet__foot">
    <a class="btn btn--gold" href="{url(CTA[0])}">{CTA[1]}</a>
  </div>
</div>
"""


def phead(title, lede, crumb, image="prosper-retail-shell"):
    return f"""
<main id="main">
  <section class="phead">
    <div class="phead__media">
      <img src="images/projects/{image}-lg.jpg" alt="" width="1800" height="1350" fetchpriority="high">
    </div>
    <div class="wrap phead__in">
      <nav class="crumb" aria-label="Breadcrumb">
        <a href="{url('index')}">Home</a> <span aria-hidden="true">/</span> <span>{crumb}</span>
      </nav>
      <h1 class="h1" data-up>{title}</h1>
      <p class="phead__lede" data-up data-i="1">{lede}</p>
    </div>
  </section>
"""


def band(heading="Have a project coming up?",
         copy="Drawings and a scope are ideal. A location and the date you need to open is enough "
              "to start &mdash; it goes straight to estimating.",
         label=None, href=None):
    label = label or CTA[1]
    href = href or url(CTA[0])
    return f"""
  <section class="band" aria-labelledby="bd-h">
    <div class="band__media">
      <img src="images/projects/prosper-retail-shell-lg.jpg" alt="" width="1800" height="1350" loading="lazy" decoding="async">
    </div>
    <div class="wrap wrap--wide band__in">
      <div data-up>
        <h2 class="h2" id="bd-h">{heading}</h2>
        <p>{copy}</p>
      </div>
      <a class="btn btn--ink" href="{href}" data-up data-i="1">
        {label} <svg viewBox="0 0 24 24" aria-hidden="true"><use href="#i-arrow"/></svg>
      </a>
    </div>
  </section>
"""




STRIP = """
<aside class="strip" aria-label="Credentials">
  <div class="wrap strip__in">
    <p class="strip__i"><b aria-hidden="true"></b>Licensed &amp; Insured</p>
    <p class="strip__i"><b aria-hidden="true"></b>25+ Years Experience</p>
    <p class="strip__i"><b aria-hidden="true"></b>OSHA Certified</p>
  </div>
</aside>
"""


def footer(modal_html=""):
    links = "\n".join('          <a href="%s">%s</a>' % (url(s), label) for s, label in NAV)
    return f"""</main>
{STRIP}
<footer class="foot">
  <div class="wrap">
    <div class="foot__grid">
      <div>
        <a href="{url('index')}" aria-label="BND Construction — home">
          <img class="foot__logo" src="images/bnd-logo-white.png" alt="BND Construction" width="1312" height="502" loading="lazy">
        </a>
        <p>Licensed and insured commercial general contractor. Ground-up construction, tenant
           finish-out, renovation and remodeling throughout Texas and surrounding states.</p>
      </div>
      <div>
        <p class="foot__k">Site</p>
        <nav class="foot__nav" aria-label="Footer">
{links}
          <a href="{url(CTA[0])}">{CTA[1]}</a>
        </nav>
      </div>
      <div>
        <p class="foot__k">Offices</p>
        <p class="foot__n">Dallas</p>
        <p>9101 Lyndon B Johnson Fwy<br>Dallas, TX 75243</p>
        <p class="foot__n" style="margin-top:var(--s3)">Houston</p>
        <p>2602 Genoa Red Bluff Rd<br>Houston, TX 77034</p>
      </div>
    </div>

    <div class="foot__bar">
      <p>&copy; 2026 BND Construction. All rights reserved.</p>
      <p>Powered &amp; designed by <a href="https://cnstudiogroup.com">cnstudiogroup.com</a></p>
    </div>
  </div>
</footer>

{modal_html}
<iframe name="bnd-sink" title="Form submission target" hidden></iframe>
<script src="js/classic.js"></script>
</body>
</html>
"""


def write(name, html):
    with open(name, "w") as f:
        f.write(html)
    print("  wrote %-34s %6d bytes" % (name, len(html)))


# --------------------------------------------------------------------------
# pages
# --------------------------------------------------------------------------

def estimate_fields(p):
    """The estimate fields, id-prefixed so the page form and the modal can
    both exist without colliding on ids."""
    return f"""          <div class="f"><label for="{p}name">Name</label>
            <input id="{p}name" name="Name" type="text" autocomplete="name" required></div>
          <div class="f"><label for="{p}co">Company</label>
            <input id="{p}co" name="Company" type="text" autocomplete="organization"></div>
          <div class="f"><label for="{p}email">Email</label>
            <input id="{p}email" name="Email" type="email" autocomplete="email" required></div>
          <div class="f"><label for="{p}phone">Phone</label>
            <input id="{p}phone" name="Phone" type="tel" autocomplete="tel"></div>
          <div class="f"><label for="{p}type">Project type</label>
            <select id="{p}type" name="Project type">
              <option value="">Select&hellip;</option>
              <option>New construction</option>
              <option>Renovation / alteration</option>
              <option>Additions to existing building</option>
              <option>Design build</option>
            </select></div>
          <div class="f"><label for="{p}loc">Project address</label>
            <input id="{p}loc" name="Project address" type="text" placeholder="Street, city, state, zip"></div>
          <div class="f"><label for="{p}size">Approximate size</label>
            <input id="{p}size" name="Size" type="text" placeholder="Square footage"></div>
          <div class="f"><label for="{p}date">Target start date</label>
            <input id="{p}date" name="Target start date" type="text" placeholder="Month / year"></div>
          <div class="f"><label for="{p}permit">Permit status</label>
            <select id="{p}permit" name="Permit status">
              <option value="">Select&hellip;</option>
              <option>Permit submitted</option>
              <option>Permit in review</option>
              <option>Permit approved</option>
            </select></div>
          <div class="f f--wide"><label for="{p}msg">Scope</label>
            <textarea id="{p}msg" name="Scope" rows="4" placeholder="What is being built, drawings status, anything else we should know"></textarea></div>
          <div class="f f--wide"><label for="{p}file">Attach any drawings</label>
            <input id="{p}file" name="Drawings" type="file" accept=".pdf,.doc,.docx,.jpg,.jpeg,.png,.dwg" required></div>

          <input type="hidden" name="_subject" value="Estimate request — BND website">
          <input type="hidden" name="_template" value="table">
          <input type="hidden" name="_captcha" value="false">
          <input type="hidden" name="_cc" value="{ESTIMATE_CC}">
          <input type="hidden" name="_next" value="{THANKS}">
"""


def modal():
    """A dialog on every page except the estimate page itself, which would
    otherwise duplicate every field id. Submits natively — a required file
    cannot go over the AJAX endpoint."""
    return f"""
<dialog class="modal" id="estimate-modal" aria-labelledby="modal-h">
  <form method="dialog" class="modal__x"><button aria-label="Close">&times;</button></form>
  <div class="modal__in">
    <p class="kick">Request an estimate</p>
    <h2 class="h2" id="modal-h">Tell us about the project</h2>
    <span class="rule" aria-hidden="true"></span>
    <p class="small" style="margin-top:var(--s3);max-width:46ch">
      Please complete the form and attach your project drawings. You may also email them
      directly to <a href="mailto:{ESTIMATE_INBOX}">{ESTIMATE_INBOX}</a>.
    </p>
    <form class="form" style="margin-top:var(--s4)"
          action="https://formsubmit.co/{ESTIMATE_TO}" method="POST" enctype="multipart/form-data"
          target="bnd-sink" data-native>
{estimate_fields('m-')}
      <p class="fmsg" data-form-msg role="status" aria-live="polite"></p>
      <div class="f--wide">
        <button class="btn btn--gold" type="submit">Send to estimating <svg viewBox="0 0 24 24" aria-hidden="true"><use href="#i-arrow"/></svg></button>
      </div>
    </form>
  </div>
</dialog>
"""


def page_thanks():
    """Only reached without JavaScript, or as the iframe's redirect target.
    With JS the message appears inline and this is never seen."""
    return (
        head("Thank you | BND Construction", "Your submission is with BND Construction.")
        + header("")
        + phead("Thank you",
                "Your submission is in. Estimating will come back to you with next steps.",
                "Thank you", "oak-point")
        + f"""
  <section class="bay">
    <div class="wrap">
      <a class="arrow" href="{url('index')}">Back to the homepage <svg viewBox="0 0 24 24" aria-hidden="true"><use href="#i-arrow"/></svg></a>
    </div>
  </section>
"""
        + footer())


def chips(name, options, required=False):
    req = ' required' if required else ''
    return "".join(
        '\n                <label class="chip"><input type="radio" name="%s" value="%s"%s>'
        '<span>%s</span></label>' % (name, o, req, o) for o in options)


def reference_block(n):
    return f"""
              <fieldset class="refgrp">
                <legend class="refgrp__n">Reference {n}</legend>
                <div class="fgrid">
                  <div class="f"><label for="r{n}-name">Contact name</label>
                    <input id="r{n}-name" name="Ref {n} — contact name" type="text"></div>
                  <div class="f"><label for="r{n}-proj">Project name &amp; location</label>
                    <input id="r{n}-proj" name="Ref {n} — project" type="text"></div>
                  <div class="f"><label for="r{n}-ph">Phone number</label>
                    <input id="r{n}-ph" name="Ref {n} — phone" type="tel"></div>
                  <div class="f"><label for="r{n}-em">Email</label>
                    <input id="r{n}-em" name="Ref {n} — email" type="email"></div>
                </div>
              </fieldset>
"""


def prequal_wizard():
    """Four steps in one form. It still posts natively — the insurance
    upload cannot go over the AJAX endpoint."""
    return f"""
        <form class="wiz" action="https://formsubmit.co/{OFFICE}" method="POST"
              enctype="multipart/form-data" target="bnd-sink" data-native data-wiz>
          <div class="wiz__hd">
            <p class="wiz__t">Subcontractor pre-qualification</p>
            <p class="wiz__n">Step <span data-wiz-now>1</span> of 4</p>
          </div>
          <div class="wiz__bar"><span data-wiz-bar></span></div>

          <fieldset class="wiz__step" data-step="1">
            <legend class="sr">Your company</legend>
            <h3 class="h3">Your company</h3>
            <p class="small">Straight from the top of the prequalification form.</p>
            <div class="fgrid">
              <div class="f"><label for="w-co">Company name <i aria-hidden="true">*</i></label>
                <input id="w-co" name="Company name" type="text" data-req></div>
              <div class="f"><label for="w-csi">Company CSI / trade <i aria-hidden="true">*</i></label>
                <input id="w-csi" name="CSI / trade" type="text" placeholder="e.g. 23 00 00 HVAC" data-req></div>
              <div class="f f--wide"><label for="w-addr">Full address <i aria-hidden="true">*</i></label>
                <input id="w-addr" name="Full address" type="text" placeholder="Street, city, state, zip" data-req></div>
              <div class="f"><label for="w-yrs">Years in business <i aria-hidden="true">*</i></label>
                <input id="w-yrs" name="Years in business" type="text" placeholder="e.g. 12" data-req></div>
              <div class="f"><label for="w-geo">Geographic coverage</label>
                <input id="w-geo" name="Geographic coverage" type="text" placeholder="DFW, statewide&hellip;"></div>
              <div class="f"><label for="w-proj">Projects completed over the past 3 years <i aria-hidden="true">*</i></label>
                <input id="w-proj" name="Projects completed past 3 years" type="text" data-req></div>
              <div class="f"><label for="w-lc">Largest contract <i aria-hidden="true">*</i></label>
                <input id="w-lc" name="Largest contract" type="text" placeholder="$" data-req></div>
              <div class="f f--wide">
                <span class="f__lbl" id="w-struct">Business structure <i aria-hidden="true">*</i></span>
                <div class="chips" data-required role="radiogroup" aria-labelledby="w-struct">{chips('Business structure', ['Corporation','Sole proprietor','LLC','Partnership'])}
                </div>
              </div>
            </div>
          </fieldset>

          <fieldset class="wiz__step" data-step="2" hidden>
            <legend class="sr">Your contact</legend>
            <h3 class="h3">Your contact</h3>
            <p class="small">Who we send bid invitations to.</p>
            <div class="fgrid">
              <div class="f"><label for="w-name">Name <i aria-hidden="true">*</i></label>
                <input id="w-name" name="Contact name" type="text" autocomplete="name" data-req></div>
              <div class="f"><label for="w-title">Job title</label>
                <input id="w-title" name="Job title" type="text" placeholder="Estimator, owner&hellip;"></div>
              <div class="f"><label for="w-ph">Phone <i aria-hidden="true">*</i></label>
                <input id="w-ph" name="Phone" type="tel" autocomplete="tel" data-req></div>
              <div class="f"><label for="w-cell">Cell phone</label>
                <input id="w-cell" name="Cell phone" type="tel"></div>
              <div class="f"><label for="w-em">Email <i aria-hidden="true">*</i></label>
                <input id="w-em" name="Email" type="email" autocomplete="email" data-req></div>
              <div class="f"><label for="w-fax">Fax</label>
                <input id="w-fax" name="Fax" type="tel"></div>
            </div>
          </fieldset>

          <fieldset class="wiz__step" data-step="3" hidden>
            <legend class="sr">Safety, insurance and bonding</legend>
            <h3 class="h3">Safety, insurance and bonding</h3>
            <p class="small">Our zero-tolerance standard applies to every crew on site, so these numbers matter.</p>
            <div class="fgrid">
              <div class="f"><label for="w-br">Bonding capacity</label>
                <input id="w-br" name="Bonding capacity" type="text"></div>

              <div class="f f--wide">
                <label for="w-ins">Upload Certificate of Insurance
                  <span style="font-weight:400;color:var(--slate)">&mdash; COI up to 5&nbsp;MB</span></label>
                <input id="w-ins" name="Certificate of Insurance" type="file"
                       accept=".pdf,.doc,.docx,.jpg,.jpeg,.png"></div>

              <div class="f f--wide">
                <span class="f__lbl" id="w-safe">Safety programme</span>
                <div class="chips" role="radiogroup" aria-labelledby="w-safe">{chips('Safety programme', ['Yes','No'])}
                </div>
              </div>
              <div class="f f--wide">
                <span class="f__lbl" id="w-sub">Substance abuse programme</span>
                <div class="chips" role="radiogroup" aria-labelledby="w-sub">{chips('Substance abuse programme', ['Yes','No'])}
                </div>
              </div>
              <div class="f f--wide">
                <span class="f__lbl" id="w-bs">Business status</span>
                <div class="chips" role="radiogroup" aria-labelledby="w-bs">{chips('Business status', ['None','Minority','Women','Disadvantaged','HUB certified','Other'])}
                </div>
              </div>
            </div>
          </fieldset>

          <fieldset class="wiz__step" data-step="4" hidden>
            <legend class="sr">References</legend>
            <h3 class="h3">References</h3>
            <p class="small">Please send us 3&ndash;4 references.</p>
            <div class="refs">{"".join(reference_block(i) for i in (1, 2, 3, 4))}
            </div>
          </fieldset>

          <input type="hidden" name="_subject" value="Subcontractor prequalification — BND website">
          <input type="hidden" name="_template" value="table">
          <input type="hidden" name="_captcha" value="false">
          <input type="hidden" name="_cc" value="{CC}">
          <input type="hidden" name="_next" value="{THANKS}">

          <p class="fmsg" data-form-msg role="status" aria-live="polite"></p>

          <div class="wiz__ft">
            <button class="btn btn--wire" type="button" data-wiz-back disabled>
              <svg viewBox="0 0 24 24" aria-hidden="true" style="transform:rotate(180deg)"><use href="#i-arrow"/></svg> Back
            </button>
            <button class="btn btn--gold" type="button" data-wiz-next>
              Continue <svg viewBox="0 0 24 24" aria-hidden="true"><use href="#i-arrow"/></svg>
            </button>
            <button class="btn btn--gold" type="submit" data-wiz-send hidden>
              Send <svg viewBox="0 0 24 24" aria-hidden="true"><use href="#i-arrow"/></svg>
            </button>
          </div>
        </form>
"""


def page_about():
    """Text-forward: a statement header, then margin-labelled prose. No photo
    composition, no figure grid — the page is what the company is."""
    return (
        head("About | BND Construction", "BND Construction is a licensed and insured commercial "
             "general contractor with 25+ years of combined management experience across Texas.")
        + header("about")
        + phead("Building relationships<br><b>BEFORE BUILDINGS</b>",
                "BND Construction is a licensed and insured commercial general contractor based in "
                "Dallas and Houston, building across Texas and surrounding states.",
                "About", "villa-at-vanston")
        + """
  <section class="bay">
    <div class="wrap">

      <div class="blk" data-up>
        <p class="blk__k">The company</p>
        <div>
          <p class="muted">BND Construction delivers ground-up construction, tenant finish-out,
             renovation and design-build throughout Texas and surrounding states &mdash; for
             developers, building owners, management companies, brokers, architects and national
             brands.</p>
          <p class="muted">Whether the project is a ground-up retail centre, a restaurant, a medical
             suite or a multifamily development, our team provides a single point of responsibility
             from the first budget through to handover. Owners deal with the people running the job,
             not a chain of people pointing at each other.</p>
        </div>
      </div>

      <div class="blk" data-up>
        <p class="blk__k">How we work</p>
        <div>
          <p class="muted">Most of our work arrives through people who have built with us before.
             That is deliberate &mdash; we would rather earn the next project than win the lowest
             bid on this one.</p>
          <p class="muted">On site that means careful management of the materials we use and jobsites
             kept as clean as possible. Every superintendent carries OSHA safety training, and we
             hold our subcontractors to the same zero-tolerance standard.</p>
        </div>
      </div>

      <div class="blk" data-up>
        <p class="blk__k">Experience</p>
        <div>
          <p class="h3" style="margin-bottom:var(--s3)">Over 25 years of commercial construction experience.</p>
          <p class="muted">Our management team has provided construction and design-build services
             for high-end restaurants, educational facilities, retail and hotel developments,
             industrial and warehouse space, tenant build-outs, supermarkets, convenience stores and
             medical centers.</p>
          <p class="muted">We build from two Texas offices &mdash; Dallas and Houston &mdash; across
             Texas and into neighbouring states, with completed work in Oklahoma.</p>
          <a class="arrow" href="portfolio-classic.html">View our work <svg viewBox="0 0 24 24" aria-hidden="true"><use href="#i-arrow"/></svg></a>
        </div>
      </div>

    </div>
  </section>
"""
        + band() + footer(modal()))


def page_services():
    # Every panel renders open. JS collapses all but the first, so with no
    # JS the page is still a complete, readable list.
    items, shots = "", ""
    for i, (name, anchor, img, paras, tags) in enumerate(data.SERVICES):
        feats = "".join("\n                  <li>%s</li>" % t for t in tags)
        shots += (f'\n        <div class="acc__shot{" is-on" if i == 0 else ""}">'
                  f'<img src="images/projects/{img}.jpg" alt="" width="900" height="675" '
                  f'loading="lazy" decoding="async"></div>')
        items += f"""
        <div class="acc__i is-open" id="{anchor}" data-shot="{i}">
          <button class="acc__hd" type="button" aria-expanded="true"
                  aria-controls="p-{anchor}" id="b-{anchor}">
            <span class="acc__n">{i + 1:02d}</span>
            <span class="acc__t">{name}</span>
            <span class="acc__ic" aria-hidden="true"></span>
          </button>
          <div class="acc__p" id="p-{anchor}" role="region" aria-labelledby="b-{anchor}">
            <div class="acc__pin">
              <div class="acc__body">
                <div>
                  <p class="acc__d">{paras[0]}</p>
                  <a class="arrow" href="{url('estimate')}">Request an estimate <svg viewBox="0 0 24 24" aria-hidden="true"><use href="#i-arrow"/></svg></a>
                </div>
                <ul class="acc__f">{feats}
                </ul>
                <div class="acc__img"><img src="images/projects/{img}.jpg" alt="" width="900" height="675" loading="lazy" decoding="async"></div>
              </div>
            </div>
          </div>
        </div>
"""
    rows = f"""
      <div class="acc" data-acc>
        <div class="acc__list">{items}        </div>
        <div class="acc__panel" aria-hidden="true">{shots}
        </div>
      </div>
"""
    return (
        head("Services | BND Construction",
             "Ground-up construction, tenant finish-out, renovation and design-build across Texas.")
        + header("services")
        + phead("Services",
                "Four ways we take a project on. Whichever route a job comes in by, it is managed "
                "to stay on schedule, under budget and clean on site.",
                "Services", "oak-point")
        + '\n  <section class="bay">\n    <div class="wrap">' + rows + '    </div>\n  </section>\n'
        + band() + footer(modal()))


def page_portfolio():
    pr = data.projects()
    shot = [p for p in pr if p["photo"]]
    listed = [p for p in pr if not p["photo"]]
    markets = sorted({p["market"] for p in pr})

    chips = '<button type="button" data-filter="all" aria-pressed="true">All work</button>'
    for m in markets:
        chips += '\n        <button type="button" data-filter="%s" aria-pressed="false">%s</button>' % (m, m)

    cards = ""
    for p in shot:
        loc = p["location"] or "Texas"
        # not links: the project detail pages are still the previous design,
        # so a card that opens one would jump between two looks
        cards += f"""
        <div class="proj" data-market="{p['market']}" data-up>
          <span class="proj__media">
            <img src="images/projects/{p['slug']}.jpg" alt="{p['alt']}" width="900" height="675" loading="lazy" decoding="async">
            <span class="proj__tag">{p['market']}</span>
          </span>
          <span class="proj__body">
            <span class="proj__t">{p['name']}</span>
            <span class="proj__m">{loc} &middot; {p['scope']}</span>
          </span>
        </div>
"""
    rows = ""
    for p in listed:
        rows += f"""        <div class="prow" data-market="{p['market']}">
          <p class="prow__n">{p['name']}</p>
          <p class="prow__m">{p['location'] or '&mdash;'}</p>
          <p class="prow__s">{p['scope']}</p>
        </div>
"""
    return (
        head("Portfolio | BND Construction",
             "Completed commercial construction across restaurants, retail, medical, education, "
             "multifamily and convenience and fuel throughout Texas and surrounding states.")
        + header("portfolio")
        + phead("Portfolio",
                "Completed commercial work across restaurants, retail, medical and dental, "
                "education, multifamily, and convenience and fuel &mdash; built throughout Texas "
                "and surrounding states.",
                "Portfolio", "walk-ons-sports-bistreaux")
        + f"""
  <section class="bay">
    <div class="wrap">
      <div class="filter" role="group" aria-label="Filter projects by market" data-filter-group>
        {chips}
      </div>

      <div class="grid4" id="pgrid" style="margin-top:var(--s5)">
{cards}      </div>

      <div class="plist" id="plist" hidden>
        <p class="plist__h">Also delivered in this market</p>
{rows}      </div>
    </div>
  </section>
"""
        + band() + footer(modal()))



def page_subcontractor():
    return (
        head("Subcontractor | BND Construction",
             "BND Construction seeks competitive, qualified local and national subcontractors and "
             "suppliers. Submit your prequalification to get on the bid list.")
        + header("subcontractor")
        + phead("Subcontractors",
                "We build projects that are successful for all parties involved. That starts with "
                "who we put on the job.",
                "Subcontractors", "prosper-retail-shell")
        + f"""

  <section class="bay tint" id="prequal">
    <div class="wrap split">
      <div>
        <p class="kick" data-up>Prequalification</p>
        <h2 class="h2" style="margin-top:var(--s3);max-width:15ch" data-up>Become a trusted trade partner</h2>
        <span class="rule" data-up aria-hidden="true"></span>
        <p class="lede" style="margin-top:var(--s4)" data-up data-i="1">
          Submit a prequalification and estimating will have your details when the next package goes out.
        </p>
      </div>

      <div class="panel panel--wiz" data-up data-i="1">
{prequal_wizard()}      </div>
    </div>
  </section>
"""
        + band() + footer(modal()))


ENQUIRY_FIELDS = """          <div class="f"><label for="q-name">Name <i aria-hidden="true">*</i></label>
            <input id="q-name" name="Name" type="text" autocomplete="name" required></div>
          <div class="f"><label for="q-co">Company</label>
            <input id="q-co" name="Company" type="text" autocomplete="organization"></div>
          <div class="f"><label for="q-email">Email <i aria-hidden="true">*</i></label>
            <input id="q-email" name="Email" type="email" autocomplete="email" required></div>
          <div class="f"><label for="q-phone">Phone</label>
            <input id="q-phone" name="Phone" type="tel" autocomplete="tel"></div>

          <div class="f f--wide">
            <span class="f__lbl" id="q-about">What is this about? <i aria-hidden="true">*</i></span>
            <div class="chips" role="radiogroup" aria-labelledby="q-about">
              <label class="chip"><input type="radio" name="About" value="General question" required><span>General question</span></label>
              <label class="chip"><input type="radio" name="About" value="Existing project" required><span>Existing project</span></label>
              <label class="chip"><input type="radio" name="About" value="Careers" required><span>Careers</span></label>
              <label class="chip"><input type="radio" name="About" value="Supplier / vendor" required><span>Supplier / vendor</span></label>
              <label class="chip"><input type="radio" name="About" value="Accounts" required><span>Accounts</span></label>
              <label class="chip"><input type="radio" name="About" value="Other" required><span>Other</span></label>
            </div>
          </div>

          <div class="f f--wide"><label for="q-msg">Message <i aria-hidden="true">*</i></label>
            <textarea id="q-msg" name="Message" rows="5" placeholder="How can we help?" required></textarea></div>
"""


def page_contact():
    offices = ""
    for city, street, region in data.OFFICES:
        offices += f"""        <div class="office" data-up>
          <p class="office__c">{city}</p>
          <h3 class="h3">{street}</h3>
          <p class="small">{region}</p>
        </div>
"""
    return (
        head("Contact | BND Construction",
             "Project enquiries and bid invitations go straight to estimating at BND Construction.")
        + header("contact")
        + phead("Contact",
                "Project enquiries and bid invitations go straight to estimating. General questions "
                "reach the same desk &mdash; use the form below, or the office details further down.",
                "Contact", "oak-point")
        + f"""
  <section class="bay">
    <div class="wrap split">
      <div>
        <p class="kick" data-up>Start a conversation</p>
        <h2 class="h2" style="margin-top:var(--s3);max-width:14ch" data-up>Send us a message</h2>
        <span class="rule" data-up aria-hidden="true"></span>
        <p class="lede" style="margin-top:var(--s4)" data-up data-i="1">
          For anything that is not an estimate request or a trade prequalification.
        </p>

        <div class="offices">
{offices}        </div>
      </div>

      <div class="panel" data-up data-i="1">
        <form class="form" data-form action="https://formsubmit.co/{OFFICE}" method="POST" novalidate>
{ENQUIRY_FIELDS}

          <input type="hidden" name="_subject" value="Enquiry — BND website">
          <input type="hidden" name="_template" value="table">
          <input type="hidden" name="_captcha" value="false">
          <input type="hidden" name="_cc" value="{CC}">
          <input type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px">

          <div class="f--wide">
            <button class="btn btn--gold" type="submit">Send enquiry <svg viewBox="0 0 24 24" aria-hidden="true"><use href="#i-arrow"/></svg></button>
          </div>
          <p class="fmsg" data-form-msg role="status" aria-live="polite"></p>
        </form>
      </div>
    </div>
  </section>

"""
        + footer(modal()))


def page_estimate():
    return (
        head("Request an Estimate | BND Construction",
             "Send your project to BND Construction — it goes straight to estimating.")
        + header("")
        + phead("Request an Estimate",
                "Drawings and a scope are ideal. A location and the date you need to open is enough "
                "to start &mdash; it goes straight to estimating.",
                "Request an Estimate", "gas-station-fuel")
        + f"""
  <section class="bay">
    <div class="wrap split">
      <div>
        <p class="kick" data-up>Estimating</p>
        <h2 class="h2" style="margin-top:var(--s3);max-width:15ch" data-up>Tell us about the project</h2>
        <span class="rule" data-up aria-hidden="true"></span>
        <p class="lede" style="margin-top:var(--s4)" data-up data-i="1">
          Please complete the form and attach your project drawings. You may also email the
          drawings directly to:
        </p>
        <p class="mailto" data-up data-i="2">
          <span>Estimating &amp; Bids</span>
          <a href="mailto:{ESTIMATE_INBOX}">{ESTIMATE_INBOX}</a>
        </p>
      </div>

      <div class="panel" data-up data-i="1">
        <form class="form" action="https://formsubmit.co/{ESTIMATE_TO}" method="POST" enctype="multipart/form-data"
          target="bnd-sink" data-native>
{estimate_fields('e-')}
          <div class="f--wide">
            <button class="btn btn--gold" type="submit">Send to estimating <svg viewBox="0 0 24 24" aria-hidden="true"><use href="#i-arrow"/></svg></button>
          </div>
        </form>
      </div>
    </div>
  </section>
"""
        + footer())


def main():
    print("Building BND Construction — classic direction")
    write(url("about"),         page_about())
    write(url("services"),      page_services())
    write(url("portfolio"),     page_portfolio())
    write(url("subcontractor"), page_subcontractor())
    write(url("contact"),       page_contact())
    write(url("estimate"),      page_estimate())
    write(THANKS,               page_thanks())
    print("Done. 7 pages (index-classic.html is hand-written and untouched).")


if __name__ == "__main__":
    main()
