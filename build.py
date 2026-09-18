#!/usr/bin/env python3
"""Builds the static pages. Run `python3 build.py` after editing, then commit the output.

Each page is a folder with an index.html so URLs are clean (/careers, /apply).
"""
import os, pathlib

ROOT = pathlib.Path(__file__).parent
SITE = "https://darkhorsepromotions.com"
EMAIL = "carterscarkeys@gmail.com"
PHONE_DISPLAY = "(502) 325-1109"
PHONE_TEL = "+15023251109"
FORM_ACTION = f"https://formsubmit.co/{EMAIL}"

NAV = [
    ("/", "Home"),
    ("/about/", "About"),
    ("/team/", "Team"),
    ("/services/", "Services"),
    ("/careers/", "Careers"),
    ("/contact/", "Contact"),
]

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{site}{path}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{site}/img/hero.jpg">
<meta property="og:type" content="website">
<link rel="icon" href="/img/logo-horse.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header id="header">
  <nav class="pad">
    <a class="brand" href="/" aria-label="Dark Horse Promotions home">
      <img src="/img/logo-horse.jpg" alt="">
      <span class="brand-name">Dark Horse<small>Promotions, Inc.</small></span>
    </a>
    <ul class="nav-links" id="nav-links">
{navlinks}
    </ul>
    <div class="nav-right">
      <a class="nav-phone" href="tel:{tel}">{phone}</a>
      <a class="btn btn-orange" href="/apply/">Apply now</a>
      <button class="menu-btn" aria-label="Menu" aria-expanded="false" aria-controls="nav-links" onclick="var h=document.getElementById('header');var o=h.classList.toggle('open');this.setAttribute('aria-expanded',o)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
      </button>
    </div>
  </nav>
</header>
{hiring}
<main id="main">
"""

HIRING = """<div class="hiring">
  <span><b>Now hiring in West Houston.</b> Sales and key technicians, $600 to $800 a week to start. No experience needed, we train you.</span>
  <a href="/careers/">See the role</a>
</div>"""

FOOT = """</main>
<footer class="pad">
  <div class="foot">
    <div>
      <a class="brand" href="/"><img src="/img/logo-dark.jpg" alt=""><span class="brand-name">Dark Horse<small>Promotions, Inc.</small></span></a>
      <p>A West Houston sales and marketing firm representing Car Keys Express inside Costco and Sam's Club. Call for this week's store. And we're hiring.</p>
    </div>
    <div>
      <h4>Company</h4>
      <a href="/about/">About</a>
      <a href="/team/">Team</a>
      <a href="/services/">Services</a>
    </div>
    <div>
      <h4>Work with us</h4>
      <a href="/careers/">Careers</a>
      <a href="/apply/">Apply</a>
      <a href="/contact/">Contact</a>
    </div>
    <div>
      <h4>Where we are this week</h4>
      <a class="big-link" href="tel:{tel}">{phone}</a>
      <a href="mailto:{email}">{email}</a>
      <p style="margin-top:.5rem;font-size:.85rem">We're inside a Costco or Sam's Club on the west side of Houston. The store changes weekly. Call or text for this week's.</p>
    </div>
  </div>
  <div class="copy">
    <span>© 2026 Dark Horse Promotions, Inc. All rights reserved.</span>
    <a href="/privacy/">Privacy policy</a>
  </div>
</footer>
</body>
</html>
"""

MARQUEE_ITEMS = ["West Houston","Inside Costco and Sam's Club","Lost key replacement","Key fob programming","Smart key duplication","Broken key extraction","Fob batteries","Done in minutes while you shop","All makes and models","Now hiring"]
def marquee():
    a = "".join(f"<span>{i}</span>" for i in MARQUEE_ITEMS)
    b = "".join(f'<span class="dup">{i}</span>' for i in MARQUEE_ITEMS)
    return f'<div class="marquee" aria-hidden="true"><div class="marquee-track">{a}{b}</div></div>'

CONSENT = f"""<label class="consent"><input type="checkbox" name="sms_consent" value="yes">
<span>By submitting this form with your phone number, you agree to receive calls and text messages from Dark Horse Promotions, Inc. about {{purpose}} at the number provided. Consent is not a condition of employment or service. Message and data rates may apply. Reply STOP to opt out. See our <a href="/privacy/">privacy policy</a>.</span></label>"""

def apply_form(light=False):
    return f"""<form class="form" action="{FORM_ACTION}" method="POST" enctype="multipart/form-data">
  <div class="two">
    <div class="field"><label for="f-first">First name</label><input id="f-first" name="first_name" autocomplete="given-name" required></div>
    <div class="field"><label for="f-last">Last name</label><input id="f-last" name="last_name" autocomplete="family-name" required></div>
  </div>
  <div class="two">
    <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
    <div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
  </div>
  <div class="field"><label for="f-city">City and state</label><input id="f-city" name="location" autocomplete="address-level2" placeholder="Where you're based"></div>
  <div class="field">
    <label for="f-resume">Resume</label>
    <input id="f-resume" name="attachment" type="file" accept=".pdf,.doc,.docx">
    <span class="hint">PDF or Word, up to 10 MB. Optional, but it helps us call you back faster.</span>
  </div>
  <div class="field"><label for="f-msg">Tell us about yourself</label><textarea id="f-msg" name="message" placeholder="Why this role, what you've done, when you can start"></textarea></div>
  {CONSENT.format(purpose="potential employment")}
  <input type="hidden" name="_subject" value="New application from darkhorsepromotions.com">
  <input type="hidden" name="_template" value="table">
  <input type="hidden" name="_next" value="{SITE}/thanks/">
  <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
  <button class="btn btn-orange" type="submit">Send application</button>
</form>"""

def contact_form():
    return f"""<form class="form" action="{FORM_ACTION}" method="POST">
  <div class="two">
    <div class="field"><label for="c-first">First name</label><input id="c-first" name="first_name" autocomplete="given-name" required></div>
    <div class="field"><label for="c-last">Last name</label><input id="c-last" name="last_name" autocomplete="family-name"></div>
  </div>
  <div class="two">
    <div class="field"><label for="c-email">Email</label><input id="c-email" name="email" type="email" autocomplete="email"></div>
    <div class="field"><label for="c-phone">Phone</label><input id="c-phone" name="phone" type="tel" autocomplete="tel" required></div>
  </div>
  <div class="field"><label for="c-vehicle">Vehicle</label><input id="c-vehicle" name="vehicle" placeholder="Year, make, model"></div>
  <div class="field"><label for="c-msg">What do you need?</label><textarea id="c-msg" name="message" placeholder="What happened to the key, and which club is closest to you"></textarea></div>
  {CONSENT.format(purpose="your request")}
  <input type="hidden" name="_subject" value="New service request from darkhorsepromotions.com">
  <input type="hidden" name="_template" value="table">
  <input type="hidden" name="_next" value="{SITE}/thanks/">
  <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
  <button class="btn btn-orange" type="submit">Send request</button>
</form>"""

def careers_cta(cls="careers-band"):
    return f"""<section class="{cls} pad">
  <div class="grid">
    <h2>A future that opens doors.</h2>
    <div class="aside">
      <p>We're a sales and marketing team that learned a trade, and we're hiring people who want to do the same. If you compete, show up, and can talk to anyone, we want you on our side.</p>
      <div class="actions">
        <a class="btn btn-orange" href="/apply/">Apply now</a>
        <a class="btn btn-line" href="/careers/">Learn about the role</a>
      </div>
    </div>
  </div>
</section>"""

# ------------------------------------------------------------------ pages
PAGES = {}

FIND_US = f"""<section class="light-2 pad" id="find-us">
  <div class="grid">
    <h2 class="section-title">Where to find us this week.</h2>
    <div class="section-body">
      <p>We're set up inside a Costco or Sam's Club on the west side of Houston, and the store changes every week. Call or text and we'll tell you exactly which one and what hours. A club membership is required for service.</p>
      <div style="display:flex;gap:.9rem;flex-wrap:wrap;margin-top:1.75rem">
        <a class="btn btn-orange" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a>
        <a class="btn btn-line" href="sms:{PHONE_TEL}">Text us</a>
      </div>
    </div>
  </div>
</section>"""

PAGES["/"] = dict(
    title="Dark Horse Promotions, Inc. | West Houston Sales Team and Car Key Service",
    desc="Dark Horse Promotions is a West Houston sales and marketing firm representing Car Keys Express inside Costco and Sam's Club. Now hiring. Need a key? Call for this week's store.",
    hiring=True,
    body=f"""
<section class="hero pad">
  <div class="hero-copy">
    <h1>
      <span>Learn a trade.</span>
      <span><i class="rule" aria-hidden="true"></i>Get paid</span>
      <span>to sell it.</span>
    </h1>
    <p>Dark Horse Promotions is a West Houston sales and marketing firm representing Car Keys Express inside Costco and Sam's Club. We hire competitors, train them to cut, program, and sell car keys, then train them to lead.</p>
    <div class="hero-actions">
      <a class="btn btn-orange" href="/apply/">Apply now</a>
      <a class="btn btn-line" href="/careers/">What the job looks like</a>
    </div>
  </div>
  <div class="hero-photo">
    <img src="/img/hero.jpg" alt="Carter Bolser, owner of Dark Horse Promotions" fetchpriority="high">
  </div>
  <aside class="hero-note">
    <b>Need a car key?</b>
    We're inside a Costco or Sam's Club in West Houston this week. Keys cut and programmed while you shop.
    <a href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY} for this week's store</a>
  </aside>
</section>
{marquee()}
<section class="light pad">
  <div class="grid">
    <h2 class="section-title">A sales team that learned a trade.</h2>
    <div class="section-body">
      <p>Most sales jobs sell something you can't hold. We sell a car key, cut and programmed in front of the customer, that works before they pay. It's a real skill, it's in demand everywhere, and it's the best sales training there is: a stranger walks up with a problem and walks away happy.</p>
      <a class="btn btn-line" href="/about/">About the company</a>
    </div>
    <ul class="statements">
      <li><h3>Real trade</h3><p>You learn to cut and program keys for every make and model. That skill is yours for life.</p></li>
      <li><h3>Real sales</h3><p>Thousands of members walk past the display every day. You start the conversation, find the need, and close it on the spot.</p></li>
      <li><h3>Real growth</h3><p>Top performers train and develop the next hires. Leadership here is earned by doing, not by waiting.</p></li>
    </ul>
  </div>
</section>
<section class="dark pad">
  <div class="grid">
    <h2 class="section-title">For members: how it works.</h2>
    <p class="section-body">Lost a key or need a spare? Four steps, and most members are done in the time it takes to shop.</p>
    <ol class="steps">
      <li><div class="n">Step 1</div><h3>Call for this week's store</h3><p>We're in a different West Houston Costco or Sam's Club each week. Call or text to find out which.</p></li>
      <li><div class="n">Step 2</div><h3>Stop by the display</h3><p>Bring your membership card and your vehicle. We look up exactly which key your car takes and quote it up front.</p></li>
      <li><div class="n">Step 3</div><h3>We cut and program</h3><p>The technician cuts the key and programs the fob or smart key at your vehicle in the parking lot.</p></li>
      <li><div class="n">Step 4</div><h3>Test before you leave</h3><p>Lock, unlock, start. You watch it work before you pay.</p></li>
    </ol>
  </div>
</section>
<section class="light pad">
  <div class="grid">
    <h2 class="section-title">On the job.</h2>
    <p class="section-body">Real work, real people. The team sets up, takes care of members all day, and sends every one of them home with a working key.</p>
    <div class="photos">
      <figure class="big"><img src="/img/p2.jpg" alt="Technician programming a key at the equipment bench"><figcaption>Cutting and programming, done on site</figcaption></figure>
      <figure class="a"><img src="/img/p1.jpg" alt="The Dark Horse Promotions team at an industry event"></figure>
      <figure class="b"><img src="/img/p3.jpg" alt="The team at a trade show"></figure>
    </div>
  </div>
</section>
<section class="dark pad">
  <div class="grid">
    <h2 class="section-title">Why people work here.</h2>
    <p class="section-body">Carter's goal is simple: it should feel like family when you show up every day. That means people who put in effort, back each other up, and want to win.</p>
    <ul class="claims">
      <li><h3>Paid to learn</h3><p>$600 to $800 a week to start while you train. No experience required.</p></li>
      <li><h3>Home every night</h3><p>Every store is on the west side of Houston, a 20 to 30 minute commute. No travel.</p></li>
      <li><h3>A path up</h3><p>Learn the trade, master the sale, then train and develop the next people through the door.</p></li>
    </ul>
  </div>
</section>
{FIND_US}
{careers_cta()}
""")

PAGES["/about/"] = dict(
    title="About | Dark Horse Promotions, Inc.",
    desc="Dark Horse Promotions runs car key replacement displays inside Sam's Club and Costco, built on reliability, transparency, and a team that shows up.",
    hiring=True,
    body=f"""
<section class="page-hero pad">
  <span class="kicker">About us</span>
  <h1>We are Dark Horse Promotions.</h1>
  <p>A West Houston sales and marketing firm that learned a trade. We represent Car Keys Express inside Costco and Sam's Club, and we build salespeople into technicians and technicians into leaders.</p>
</section>
<section class="light pad">
  <div class="grid">
    <h2 class="section-title">Where reliability meets convenience.</h2>
    <div class="section-body">
      <p>Dark Horse Promotions sets up inside Costco and Sam's Club warehouses on the west side of Houston, so replacing a lost key or adding a spare is something you do on a grocery run instead of a day off work. We represent Car Keys Express, the national leader in on-site key replacement.</p>
      <p>The company is owned by Carter Bolser, who started as a technician himself. Every job is done on site by a trained team member with the equipment and the key inventory to finish it while you shop.</p>
    </div>
  </div>
</section>
<section class="dark pad">
  <div class="grid">
    <h2 class="section-title">What guides us.</h2>
    <p class="section-body">Our commitment is built on expertise, reliability, and member-first service.</p>
    <ul class="statements">
      <li><h3>Our mission</h3><p>We exist to keep you moving. Fast, professional, hassle-free key replacement, in the places you already go.</p></li>
      <li><h3>Our vision</h3><p>A world where lost keys never mean lost time. Expert workmanship plus real convenience is changing how drivers get reliable key service.</p></li>
      <li><h3>Our culture</h3><p>Precision, urgency, and trust. The team solves problems so every member gets back on the road with confidence.</p></li>
    </ul>
  </div>
</section>
<section class="light pad">
  <div class="grid">
    <h2 class="section-title">The keys to our success.</h2>
    <p class="section-body">Great service is built on strong principles, and we stand by them every day.</p>
    <ul class="statements four">
      <li><h3>Reliability first</h3><p>We show up equipped and ready, every day the display is open.</p></li>
      <li><h3>Member-centric service</h3><p>Your convenience is the priority. From replacements to reprogramming, the process is seamless and stress-free.</p></li>
      <li><h3>Trust and transparency</h3><p>No hidden fees, no gimmicks. Honest pricing and expert work you can count on.</p></li>
      <li><h3>Continuous improvement</h3><p>Vehicle technology evolves, and so do we. We stay current on programming and security so we can serve you better.</p></li>
    </ul>
  </div>
</section>
<section class="dark cta-band pad">
  <div class="grid">
    <h2>Are you a dark horse?</h2>
    <div class="aside">
      <p>Success isn't just about getting there. It's about having the right support. If you're ready to be part of a team that keeps people on the road, we want to hear from you.</p>
      <a class="btn btn-orange" href="/careers/">Join the team</a>
    </div>
  </div>
</section>
""")

PAGES["/team/"] = dict(
    title="Team | Dark Horse Promotions, Inc.",
    desc="Meet the people behind Dark Horse Promotions, a car key team led by Carter Bolser.",
    hiring=True,
    body=f"""
<section class="page-hero pad">
  <span class="kicker">Team</span>
  <h1>A team that delivers.</h1>
  <p>Behind every successful service is a team dedicated to doing the job right. We don't just replace keys. We restore access, provide peace of mind, and keep you moving forward.</p>
</section>
<section class="light pad">
  <div class="grid">
    <h2 class="section-title">Driven by dedication, powered by reliability.</h2>
    <p class="section-body">We do more than replace keys. We restore access and peace of mind. The team is committed to fast, precise, professional key service, and there isn't a vehicle that rolls into the lot we haven't seen.</p>
    <div class="person">
      <img src="/img/hero.jpg" alt="Carter Bolser">
      <div>
        <h3>Carter Bolser</h3>
        <span class="role">Owner, Dark Horse Promotions, Inc.</span>
        <p>Carter found this business the same way most of his team will: an Indeed ad. He started as a technician in Dallas, fell in love with the work, and a year and a half later took the opportunity to move closer to family in Houston and run his own operation.</p>
        <p>His goal for Dark Horse is that it feels like family when you come to work every day. He still works the display, he still trains every new hire himself, and he still answers the phone.</p>
        <div class="contact-lines">
          <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>
          <a href="mailto:{EMAIL}">{EMAIL}</a>
        </div>
      </div>
    </div>
  </div>
</section>
<section class="dark pad">
  <div class="grid">
    <h2 class="section-title">The next name on this page could be yours.</h2>
    <div class="section-body">
      <p>We're growing, and the team page is short on purpose. We'd rather add people who want to build something than fill seats. If you compete, put in effort, and want to learn a trade that pays, read about the role.</p>
      <a class="btn btn-orange" href="/careers/">See the role</a>
    </div>
  </div>
</section>
<section class="light cta-band pad">
  <div class="grid">
    <h2>Unlock more access.</h2>
    <div class="aside">
      <p>Lost or broken keys shouldn't slow you down. Find us inside Sam's Club or Costco and leave with a working key.</p>
      <a class="btn btn-line" href="/services/">Discover our services</a>
    </div>
  </div>
</section>
""")

PAGES["/services/"] = dict(
    title="Services | Car Key Replacement at Sam's Club and Costco | Dark Horse Promotions",
    desc="Lost key replacement, fob and smart key programming, spares, extraction, and fob repair, done inside Sam's Club and Costco while you shop.",
    hiring=True,
    body=f"""
<section class="page-hero with-photo pad">
  <div class="ph-copy">
    <span class="kicker">Services</span>
    <h1>A car key service that fits inside your errands.</h1>
    <p>We represent Car Keys Express inside Costco and Sam's Club on the west side of Houston. Stop by the display, and by the time you've checked out, your new key is cut, programmed, and tested.</p>
    <div style="margin-top:2rem;display:flex;gap:.9rem;flex-wrap:wrap">
      <a class="btn btn-orange" href="tel:{PHONE_TEL}">Call for this week's location</a>
    </div>
  </div>
  <div class="ph-img"><img src="/img/p2.jpg" alt="Key programming equipment"></div>
</section>
{marquee()}
<section class="light pad">
  <div class="grid">
    <h2 class="section-title">Fast service, secure access.</h2>
    <p class="section-body">We carry the cutting machines, programmers, and a deep inventory of key blanks and fobs, so almost every vehicle can be handled on the spot with no ordering and no second trip.</p>
    <ul class="list">
      <li><h3>Lost key replacement</h3><p>No original needed. We identify the key your vehicle takes, cut it, and program it to the car at your vehicle in the lot.</p></li>
      <li><h3>Key fob and smart key programming</h3><p>Push-to-start, proximity, and remote fobs for domestic and import vehicles, programmed and tested before you drive off.</p></li>
      <li><h3>Spare key duplication</h3><p>A second key now costs far less than a replacement later. We recommend every driver keeps one.</p></li>
      <li><h3>Broken key extraction</h3><p>Snapped keys removed and replaced so you're not stuck with half a key.</p></li>
      <li><h3>Fob repair and batteries</h3><p>Dead buttons, cracked shells, and low batteries fixed while you wait.</p></li>
    </ul>
  </div>
</section>
<section class="dark pad">
  <div class="grid">
    <h2 class="section-title">How it works.</h2>
    <p class="section-body">Four steps, and most members are done in the time it takes to shop.</p>
    <ol class="steps">
      <li><div class="n">Step 1</div><h3>Call for the location</h3><p>We're in a different West Houston Costco or Sam's Club each week. Call or text to find out which.</p></li>
      <li><div class="n">Step 2</div><h3>Stop by the display</h3><p>Bring your membership card and your vehicle. We look up exactly which key your car takes and quote it up front.</p></li>
      <li><div class="n">Step 3</div><h3>We cut and program</h3><p>The technician cuts the key and programs the fob or smart key at your vehicle in the parking lot.</p></li>
      <li><div class="n">Step 4</div><h3>Test before you leave</h3><p>Lock, unlock, start. You watch it work before you pay.</p></li>
    </ol>
  </div>
</section>
<section class="light pad">
  <div class="grid">
    <h2 class="section-title">Reliable solutions to keep you moving.</h2>
    <p class="section-body">We prioritize reliability, transparency, and expert craftsmanship. You'll know the price before we start, and you'll have a working key before we're done.</p>
    <ul class="claims">
      <li><h3>Dealership quality</h3><p>Same programming standards as the dealer, without the appointment, the tow, or the dealership price.</p></li>
      <li><h3>Straight pricing</h3><p>Quoted up front at the display. No hidden fees, no gimmicks.</p></li>
      <li><h3>Membership required</h3><p>Service is available to Sam's Club and Costco members at the club we're currently in. Not a member? Ask about signing up at the front desk.</p></li>
    </ul>
  </div>
</section>
{FIND_US}
{careers_cta()}
""")

PAGES["/careers/"] = dict(
    title="Careers | Sales and Key Technician, West Houston | Dark Horse Promotions, Inc.",
    desc="Join Dark Horse Promotions in West Houston. $600 to $800 a week to start, no experience needed. Learn to cut, program, and sell car keys inside Costco and Sam's Club, then lead.",
    hiring=False,
    body=f"""
<section class="page-hero with-photo pad">
  <div class="ph-copy">
    <span class="kicker">Careers, West Houston</span>
    <h1>Let's unlock your potential.</h1>
    <p>Your ambition has the key. Turn it at Dark Horse Promotions. We hire competitors, teach them a trade, and turn them into leaders.</p>
    <div style="margin-top:2rem;display:flex;gap:.9rem;flex-wrap:wrap">
      <a class="btn btn-orange" href="/apply/">Apply now</a>
      <a class="btn btn-line" href="#role">What the job looks like</a>
    </div>
  </div>
  <div class="ph-img"><img src="/img/p3.jpg" alt="Dark Horse Promotions team members at an industry event"></div>
</section>
<section class="light pad">
  <div class="grid">
    <h2 class="section-title">Your hustle. Your growth. Your future.</h2>
    <div class="section-body">
      <p>Dark Horse Promotions is a sales and marketing firm that learned a trade. We represent Car Keys Express inside Costco and Sam's Club on the west side of Houston, and we're looking for driven, competitive people to join us.</p>
      <p>You don't need a locksmith background or a sales resume. You need effort, a personality that isn't afraid of strangers, and the drive to get better every day.</p>
    </div>
    <ul class="statements">
      <li><h3>$600 to $800 a week</h3><p>To start, while you learn. Pay grows as you do.</p></li>
      <li><h3>No experience needed</h3><p>We train you on the equipment, the vehicles, and the sale. Coachability matters more than credentials.</p></li>
      <li><h3>Home every night</h3><p>Every store is in West Houston, a 20 to 30 minute commute. No travel, no hotels.</p></li>
    </ul>
  </div>
</section>
<section id="role" class="dark pad">
  <div class="grid">
    <h2 class="section-title">What the job looks like.</h2>
    <p class="section-body">You run our display inside a Costco or Sam's Club. Thousands of members walk past you every day, and a lot of them need a key. The day is three things.</p>
    <ul class="list">
      <li><h3>Cutting and programming</h3><p>You learn to identify, cut, and program keys and fobs for every make and model, at the member's vehicle in the lot, tested before they leave. This is the trade.</p></li>
      <li><h3>Sales</h3><p>Most people don't know a replacement key can be done at the club. You start the conversation, look up their vehicle, quote it, and close it on the spot. This is the skill.</p></li>
      <li><h3>Training and developing</h3><p>As you get good, you train the people hired after you. This is the path to leadership, and it starts sooner than you'd think.</p></li>
    </ul>
  </div>
</section>
<section class="light pad">
  <div class="grid">
    <h2 class="section-title">Who does well here.</h2>
    <p class="section-body">The trade can be taught. These can't. The two things that sink people are lack of effort and being too shy to start a conversation.</p>
    <ul class="statements four">
      <li><h3>Competitors</h3><p>Athletes, team captains, anyone who's used to keeping score and hates losing. You'll fit right in.</p></li>
      <li><h3>Outgoing</h3><p>You can walk up to a stranger, start talking, and make them feel taken care of. If that sounds terrifying, this isn't the job.</p></li>
      <li><h3>Effort</h3><p>You show up every day the display is open and you work the whole day. Nobody here coasts.</p></li>
      <li><h3>Leaders</h3><p>You want to be the person others learn from. We promote from within and we do it fast.</p></li>
    </ul>
  </div>
</section>
<section class="dark pad">
  <div class="grid">
    <h2 class="section-title">How hiring works.</h2>
    <p class="section-body">Four steps, and we move quickly. Most people hear back within a couple of days.</p>
    <ol class="steps">
      <li><div class="n">Step 1</div><h3>First interview</h3><p>A conversation with Carter about you, the role, pay, and schedule.</p></li>
      <li><div class="n">Step 2</div><h3>Second interview</h3><p>A deeper look at fit on both sides. Bring your questions.</p></li>
      <li><div class="n">Step 3</div><h3>Job shadow</h3><p>A day at the display on real jobs so you see the work before you commit.</p></li>
      <li><div class="n">Step 4</div><h3>Orientation</h3><p>Hands-on training on cutting, programming, and the sale. Then you run your own display.</p></li>
    </ol>
  </div>
</section>
<section class="light pad">
  <div class="grid">
    <h2 class="section-title">Questions people ask.</h2>
    <p class="section-body">Straight answers. Anything else, ask Carter in the first interview.</p>
    <ul class="list">
      <li><h3>Do I need locksmith or automotive experience?</h3><p>No. We train you on the equipment and the vehicles. Sports, customer-facing work, or anything competitive helps more than a toolbox.</p></li>
      <li><h3>Where will I work?</h3><p>Inside Costco and Sam's Club stores on the west side of Houston. The store changes weekly, but it's always a 20 to 30 minute commute.</p></li>
      <li><h3>Is there travel?</h3><p>No. You're home every night.</p></li>
      <li><h3>How am I paid?</h3><p>$600 to $800 a week to start. Details, including how pay grows with performance, are covered in the first interview.</p></li>
      <li><h3>What's the culture like?</h3><p>Carter's word for it is family. Small team, everyone knows everyone, and people back each other up. Effort is expected. Ego isn't.</p></li>
    </ul>
  </div>
</section>
<section class="careers-band pad">
  <div class="grid">
    <h2>Ready to take the wheel?</h2>
    <div class="aside">
      <p>Send your details and Carter will reach out to set up a first interview. Or skip the form and call or text <a href="tel:{PHONE_TEL}" style="font-weight:700;text-decoration:underline;text-underline-offset:3px">{PHONE_DISPLAY}</a>.</p>
      <div class="actions">
        <a class="btn btn-orange" href="/apply/">Apply now</a>
      </div>
    </div>
  </div>
</section>
""")

PAGES["/apply/"] = dict(
    title="Apply | Dark Horse Promotions, Inc.",
    desc="Apply to join Dark Horse Promotions as a car key technician at Sam's Club and Costco. Upload your resume and Carter will reach out.",
    hiring=False,
    body=f"""
<section class="page-hero pad">
  <span class="kicker">Apply</span>
  <h1>Join the drive for success.</h1>
  <p>West Houston. $600 to $800 a week to start. No experience needed. Send your details and Carter will reach out to set up a first interview.</p>
</section>
<section class="light pad">
  <div class="grid">
    <div class="form-title">
      <h2>Let's move forward together.</h2>
      <p>Complete the application and take the first step. Carter reads every one.</p>
      <div class="direct">
        <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}<small>Prefer to talk? Call or text.</small></a>
        <a href="mailto:{EMAIL}?subject=Application">{EMAIL}<small>Or email your resume directly.</small></a>
      </div>
    </div>
    {apply_form(light=True)}
  </div>
</section>
<section class="dark pad">
  <div class="grid">
    <h2 class="section-title">Not sure yet?</h2>
    <div class="section-body">
      <p>Read what the job actually looks like day to day, who does well in it, and how the hiring process works.</p>
      <a class="btn btn-line" href="/careers/">About the role</a>
    </div>
  </div>
</section>
""")

PAGES["/contact/"] = dict(
    title="Contact | Dark Horse Promotions, Inc.",
    desc="Find Dark Horse Promotions inside Sam's Club or Costco this week. Call or text for the current location, or send a request.",
    hiring=True,
    body=f"""
<section class="page-hero pad">
  <span class="kicker">Contact</span>
  <h1>Your key to more possibilities.</h1>
  <p>Need a key, have a question, or ready to take the next step? Call or text and we'll tell you which club we're in this week.</p>
</section>
<section class="dark pad">
  <div class="grid">
    <div class="form-title">
      <h2>Let's turn the key.</h2>
      <p>Fastest way: call or text. Or send the form and we'll get back to you with our current location and a quote.</p>
      <div class="direct">
        <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}<small>Call or text for this week's location and hours.</small></a>
        <a href="mailto:{EMAIL}">{EMAIL}<small>For quotes and everything else.</small></a>
        <a href="/apply/">Looking to work with us?<small>Applications go through the apply page.</small></a>
      </div>
    </div>
    {contact_form()}
  </div>
</section>
{FIND_US}
""")

PAGES["/thanks/"] = dict(
    title="Thanks | Dark Horse Promotions, Inc.",
    desc="We received your message.",
    hiring=False,
    body=f"""
<section class="page-hero pad">
  <span class="kicker">Received</span>
  <h1>Got it. We'll be in touch.</h1>
  <p>Your message is on its way to Carter. If it's urgent, call or text <a href="tel:{PHONE_TEL}" style="text-decoration:underline;text-underline-offset:3px;color:var(--bone)">{PHONE_DISPLAY}</a>.</p>
  <div style="margin-top:2rem;display:flex;gap:.9rem;flex-wrap:wrap">
    <a class="btn btn-orange" href="/">Back to home</a>
    <a class="btn btn-line" href="/services/">See services</a>
  </div>
</section>
""")

PAGES["/privacy/"] = dict(
    title="Privacy Policy | Dark Horse Promotions, Inc.",
    desc="How Dark Horse Promotions handles the information you send us.",
    hiring=False,
    body=f"""
<section class="page-hero pad">
  <span class="kicker">Privacy</span>
  <h1>Privacy policy.</h1>
  <p>Short version: we use what you send us to get back to you, and we don't sell it.</p>
</section>
<section class="light pad">
  <div class="grid">
    <div class="prose">
      <p>Effective 2026-09-17. This policy covers darkhorsepromotions.com, operated by Dark Horse Promotions, Inc.</p>
      <h2>What we collect</h2>
      <p>Only what you type into our forms or send us directly: your name, phone number, email, location, vehicle details, your message, and any resume you attach.</p>
      <h2>How we use it</h2>
      <ul>
        <li>To respond to service questions and tell you where we are.</li>
        <li>To review job applications and contact applicants about employment.</li>
        <li>To send text messages or calls about your request or application, if you gave us your number.</li>
      </ul>
      <h2>Text messages</h2>
      <p>If you provide a phone number and check the consent box, we may call or text you about your request or application. Consent is not a condition of service or employment. Message and data rates may apply. Reply STOP at any time to opt out, or HELP for help.</p>
      <h2>Sharing</h2>
      <p>We don't sell or rent your information. Form submissions are delivered to us through a form-processing service, which handles them only to pass them along to us. We share information otherwise only if the law requires it.</p>
      <h2>Retention and your choices</h2>
      <p>We keep applications and messages as long as we need them for the purpose above. Email <a href="mailto:{EMAIL}" style="text-decoration:underline">{EMAIL}</a> to ask what we hold about you or to have it deleted.</p>
      <h2>Contact</h2>
      <p>Dark Horse Promotions, Inc.<br>{EMAIL}<br>{PHONE_DISPLAY}</p>
    </div>
  </div>
</section>
""")

# ------------------------------------------------------------------ build
def nav_html(current):
    out = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        out.append(f'      <li><a href="{href}"{cur}>{label}</a></li>')
    return "\n".join(out)

def render(path, page):
    head = HEAD.format(title=page["title"], desc=page["desc"], site=SITE, path=path,
                       navlinks=nav_html(path), tel=PHONE_TEL, phone=PHONE_DISPLAY,
                       hiring=HIRING if page.get("hiring") else "")
    foot = FOOT.format(tel=PHONE_TEL, phone=PHONE_DISPLAY, email=EMAIL)
    return head + page["body"] + foot

def main():
    for path, page in PAGES.items():
        out = ROOT / path.strip("/") / "index.html" if path != "/" else ROOT / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(path, page))
        print("wrote", out.relative_to(ROOT))
    # sitemap
    urls = "".join(f"<url><loc>{SITE}{p}</loc></url>" for p in PAGES if p not in ("/thanks/",))
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")

if __name__ == "__main__":
    main()
