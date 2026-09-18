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
<main id="main">
"""

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
    <span><a href="/privacy/">Privacy policy</a> &nbsp; <a href="/terms/">Terms and conditions</a></span>
  </div>
</footer>
</body>
</html>
"""


CONSENT = f"""<label class="consent"><input type="checkbox" name="sms_consent" value="yes">
<span>By submitting this form with your phone number, you agree to receive calls and text messages from Dark Horse Promotions, Inc. about {{purpose}} at the number provided. Consent is not a condition of employment or service. Message frequency varies. Message and data rates may apply. Reply STOP to opt out or HELP for help. See our <a href="/privacy/">privacy policy</a> and <a href="/terms/">terms and conditions</a>.</span></label>"""

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
        <a class="link" href="/careers/">Learn about the role</a>
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
        <a class="link" href="sms:{PHONE_TEL}">Or text us</a>
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
    <h1><span>Learn a trade.</span> <span>Get paid</span> <span>to sell it.</span></h1>
    <p>Dark Horse Promotions is a West Houston sales and marketing firm representing Car Keys Express inside Costco and Sam's Club. We hire competitive people, train them to cut, program, and sell car keys, then train them to lead.</p>
    <div class="hero-actions">
      <a class="btn btn-orange" href="/apply/">Apply now</a>
      <a class="link" href="/careers/">What the job looks like</a>
    </div>
    <p class="hero-aside"><b>Need a car key?</b> We're inside a Costco or Sam's Club in West Houston this week, cutting and programming keys while you shop. <a href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a> for this week's store.</p>
  </div>
  <div class="hero-photo">
    <img src="/img/hero.jpg" alt="Carter Bolser, owner of Dark Horse Promotions" fetchpriority="high">
  </div>
</section>
<section class="light pad">
  <div class="grid">
    <h2 class="section-title">A sales team that learned a trade.</h2>
    <div class="section-body">
      <p>Most sales jobs sell something you can't hold. We sell a car key, cut and programmed in front of the customer, that works before they pay. It's a real skill, it's in demand everywhere, and it's the best sales training there is: a stranger walks up with a problem and walks away happy.</p>
      <a class="link" href="/about/">About the company</a>
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
      <li><div class="n">1</div><h3>Call for this week's store</h3><p>We're in a different West Houston Costco or Sam's Club each week. Call or text to find out which.</p></li>
      <li><div class="n">2</div><h3>Stop by the display</h3><p>Bring your membership card and your vehicle. We look up exactly which key your car takes and quote it up front.</p></li>
      <li><div class="n">3</div><h3>We cut and program</h3><p>The technician cuts the key and programs the fob or smart key at your vehicle in the parking lot.</p></li>
      <li><div class="n">4</div><h3>Test before you leave</h3><p>Lock, unlock, start. You watch it work before you pay.</p></li>
    </ol>
  </div>
</section>
<section class="light pad">
  <div class="grid">
    <h2 class="section-title wide">On the job.</h2>
    <p class="section-body under">Real work, real people. The team sets up, takes care of members all day, and sends every one of them home with a working key.</p>
    <div class="photos">
      <figure class="big"><img src="/img/p2.jpg" alt="Technician programming a key at the equipment bench"><figcaption>Cutting and programming, done on site</figcaption></figure>
      <figure class="a"><img src="/img/p1.jpg" alt="The Dark Horse Promotions team at an industry event"></figure>
      <figure class="b"><img src="/img/p3.jpg" alt="The team at a trade show"></figure>
    </div>
  </div>
</section>
<section class="dark pad">
  <div class="grid">
    <h2 class="section-title wide">Why people work here.</h2>
    <p class="section-body under">Carter's goal is simple: it should feel like family when you show up every day. That means people who put in effort, back each other up, and want to win.</p>
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
  <h1>We are Dark Horse Promotions.</h1>
  <p>A West Houston sales and marketing firm that learned a trade. We represent Car Keys Express inside Costco and Sam's Club, and we build salespeople into technicians and technicians into leaders.</p>
</section>
<section class="light pad">
  <div class="grid">
    <h2 class="section-title">Where reliability meets convenience.</h2>
    <div class="section-body">
      <p>Dark Horse Promotions sets up inside Costco and Sam's Club warehouses on the west side of Houston, so replacing a lost key or adding a spare is something you do on a grocery run instead of a day off work. We represent Car Keys Express, the nationwide on-site key replacement brand.</p>
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
    <h1>A car key service that fits inside your errands.</h1>
    <p>We represent Car Keys Express inside Costco and Sam's Club on the west side of Houston. Stop by the display, and by the time you've checked out, your new key is cut, programmed, and tested.</p>
    <div style="margin-top:2rem;display:flex;gap:.9rem;flex-wrap:wrap">
      <a class="btn btn-orange" href="tel:{PHONE_TEL}">Call for this week's location</a>
    </div>
  </div>
  <div class="ph-img"><img src="/img/p2.jpg" alt="Key programming equipment"></div>
</section>
<section class="light pad">
  <div class="grid">
    <h2 class="section-title">Fast service, secure access.</h2>
    <p class="section-body">We carry the cutting machines, programmers, and a deep inventory of key blanks and fobs, so almost every vehicle can be handled on the spot with no ordering and no second trip.</p>
    <ul class="list">
      <li><h3>Lost key replacement</h3><p>No original needed. We identify the key your vehicle takes, cut it, and program it to your car right in the lot.</p></li>
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
      <li><div class="n">1</div><h3>Call for the location</h3><p>We're in a different West Houston Costco or Sam's Club each week. Call or text to find out which.</p></li>
      <li><div class="n">2</div><h3>Stop by the display</h3><p>Bring your membership card and your vehicle. We look up exactly which key your car takes and quote it up front.</p></li>
      <li><div class="n">3</div><h3>We cut and program</h3><p>The technician cuts the key and programs the fob or smart key at your vehicle in the parking lot.</p></li>
      <li><div class="n">4</div><h3>Test before you leave</h3><p>Lock, unlock, start. You watch it work before you pay.</p></li>
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
      <li><h3>Membership required</h3><p>Service is available to Sam's Club and Costco members at the club we're currently in. Bring your membership card.</p></li>
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
    <h1>Let's unlock your potential.</h1>
    <p>Your ambition has the key. Turn it at Dark Horse Promotions. We hire competitive people, teach them a trade, and turn them into leaders.</p>
    <div style="margin-top:2rem;display:flex;gap:.9rem;flex-wrap:wrap">
      <a class="btn btn-orange" href="/apply/">Apply now</a>
      <a class="link" href="#role">What the job looks like</a>
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
    <h2 class="section-title wide">Who does well here.</h2>
    <p class="section-body under">The trade can be taught. These can't. The two things that sink people are lack of effort and being too shy to start a conversation.</p>
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
      <li><div class="n">1</div><h3>First interview</h3><p>A conversation with Carter about you, the role, pay, and schedule.</p></li>
      <li><div class="n">2</div><h3>Second interview</h3><p>A deeper look at fit on both sides. Bring your questions.</p></li>
      <li><div class="n">3</div><h3>Job shadow</h3><p>A day at the display on real jobs so you see the work before you commit.</p></li>
      <li><div class="n">4</div><h3>Orientation</h3><p>Hands-on training on cutting, programming, and the sale. Then you run your own display.</p></li>
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
    desc="How Dark Horse Promotions, Inc. handles the information you send us.",
    hiring=False,
    body=f"""
<section class="page-hero pad">
  <h1>Privacy policy.</h1>
</section>
<section class="light pad">
  <div class="grid">
    <div class="prose">
      <p>Your privacy is important to us. It is Dark Horse Promotions, Inc.'s policy to respect your privacy regarding any information we may collect from you across our website and other platforms we own and operate.</p>
      <p>We only ask for personal information when we truly need it to provide a service to you. We collect it by fair and lawful means, with your knowledge and consent, and we let you know why we're collecting it and how it will be used.</p>
      <p>We only retain collected information for as long as necessary to provide you with your requested service. Any data we store will be protected within commercially acceptable means to prevent loss, theft, unauthorized access, disclosure, copying, use, or modification.</p>
      <p>We don't share any personally identifying information publicly or with third parties, except when required to by law. Text messaging opt-in data will not be shared with any third-party agencies.</p>
      <p>Our website may link to external sites that are not operated by us. Please be aware that we have no control over the content and practices of these sites and cannot accept responsibility or liability for their respective privacy policies.</p>
      <p>You are free to refuse our request for your personal information, with the understanding that we may be unable to provide you with some of your desired services.</p>
      <p>Mobile information will not be shared with third parties or affiliates for marketing or promotional purposes. All of the above categories exclude text messaging originator opt-in data and consent. This information will not be shared with any third parties.</p>
      <p>If you wish to be removed from receiving future communications, you can opt out at any time by texting STOP, QUIT, END, OPT OUT, CANCEL, or UNSUBSCRIBE.</p>
      <p>Your continued use of our website will be regarded as acceptance of our practices around privacy and personal information. If you have any questions about how we handle user data and personal information, please feel free to contact us at <a href="mailto:{EMAIL}" style="text-decoration:underline">{EMAIL}</a>.</p>
      <p>See also our <a href="/terms/" style="text-decoration:underline">terms and conditions</a>.</p>
    </div>
  </div>
</section>
""")

PAGES["/terms/"] = dict(
    title="Terms and Conditions | Dark Horse Promotions, Inc.",
    desc="Terms and conditions for using darkhorsepromotions.com.",
    hiring=False,
    body=f"""
<section class="page-hero pad">
  <h1>Terms and conditions.</h1>
  <p>Last updated: September 18, 2026</p>
</section>
<section class="light pad">
  <div class="grid">
    <div class="prose">
      <p>Please read these terms and conditions carefully before using Our Service.</p>

      <h2>Interpretation and Definitions</h2>
      <h3>Interpretation</h3>
      <p>The words of which the initial letter is capitalized have meanings defined under the following conditions. The following definitions shall have the same meaning regardless of whether they appear in singular or in plural.</p>
      <h3>Definitions</h3>
      <p>For the purposes of these Terms and Conditions:</p>
      <ul>
        <li><b>Affiliate</b> means an entity that controls, is controlled by or is under common control with a party, where "control" means ownership of 50% or more of the shares, equity interest or other securities entitled to vote for election of directors or other managing authority.</li>
        <li><b>Country</b> refers to: Texas, United States</li>
        <li><b>Company</b> (referred to as either "the Company", "We", "Us" or "Our" in this Agreement) refers to Dark Horse Promotions, Inc.</li>
        <li><b>Device</b> means any device that can access the Service such as a computer, a cellphone or a digital tablet.</li>
        <li><b>Service</b> refers to the Website.</li>
        <li><b>Terms and Conditions</b> (also referred as "Terms") mean these Terms and Conditions that form the entire agreement between You and the Company regarding the use of the Service.</li>
        <li><b>Third-party Social Media Service</b> means any services or content (including data, information, products or services) provided by a third-party that may be displayed, included or made available by the Service.</li>
        <li><b>Website</b> refers to Dark Horse Promotions, Inc, accessible from <a href="{SITE}/" style="text-decoration:underline">darkhorsepromotions.com</a></li>
        <li><b>You</b> means the individual accessing or using the Service, or the company, or other legal entity on behalf of which such individual is accessing or using the Service, as applicable.</li>
      </ul>

      <h2>Acknowledgment</h2>
      <p>These are the Terms and Conditions governing the use of this Service and the agreement that operates between You and the Company. These Terms and Conditions set out the rights and obligations of all users regarding the use of the Service.</p>
      <p>Your access to and use of the Service is conditioned on Your acceptance of and compliance with these Terms and Conditions. These Terms and Conditions apply to all visitors, users and others who access or use the Service.</p>
      <p>By accessing or using the Service You agree to be bound by these Terms and Conditions. If You disagree with any part of these Terms and Conditions, then You may not access the Service.</p>
      <p>You represent that you are over the age of 18. The Company does not permit those under 18 to use the Service.</p>
      <p>Your access to and use of the Service is also conditioned on Your acceptance of and compliance with the <a href="/privacy/" style="text-decoration:underline">Privacy Policy</a> of the Company. Our Privacy Policy describes Our policies and procedures on the collection, use and disclosure of Your personal information when You use the Application or the Website and tells You about Your privacy rights and how the law protects You. Please read Our Privacy Policy carefully before using Our Service.</p>

      <h2>Messaging Terms and Conditions</h2>
      <p>You agree to receive informational messages (appointment reminders, account notifications, etc.) from Dark Horse Promotions, Inc. Message frequency varies. Message and data rates may apply. For help, reply HELP or email us at <a href="mailto:{EMAIL}" style="text-decoration:underline">{EMAIL}</a>. You can opt out at any time by replying STOP.</p>

      <h2>Links to Other Websites</h2>
      <p>Our Service may contain links to third-party web sites or services that are not owned or controlled by the Company.</p>
      <p>The Company has no control over, and assumes no responsibility for, the content, privacy policies, or practices of any third-party web sites or services. You further acknowledge and agree that the Company shall not be responsible or liable, directly or indirectly, for any damage or loss caused or alleged to be caused by or in connection with the use of or reliance on any such content, goods or services available on or through any such web sites or services.</p>
      <p>We strongly advise You to read the terms and conditions and privacy policies of any third-party web sites or services that You visit.</p>

      <h2>Termination</h2>
      <p>We may terminate or suspend Your access immediately, without prior notice or liability, for any reason whatsoever, including without limitation if You breach these Terms and Conditions.</p>
      <p>Upon termination, your right to use the Service will cease immediately.</p>

      <h2>Limitation of Liability</h2>
      <p>Notwithstanding any damages that You might incur, the entire liability of the Company and any of its suppliers under any provision of this Terms and Your exclusive remedy for all the foregoing shall be limited to the amount actually paid by You through the Service or 1 USD if You haven't purchased anything through the Service.</p>
      <p>To the maximum extent permitted by applicable law, in no event shall the Company or its suppliers be liable for any special, incidental, indirect, or consequential damages whatsoever (including, but not limited to, damages for loss of profits, loss of data or other information, for business interruption, for personal injury, loss of privacy arising out of or in any way related to the use of or inability to use the Service, third-party software and/or third-party hardware used with the Service, or otherwise in connection with any provision of this Terms), even if the Company or any supplier has been advised of the possibility of such damages and even if the remedy fails of its essential purpose.</p>
      <p>Some states do not allow the exclusion of implied warranties or limitation of liability for incidental or consequential damages, which means that some of the above limitations may not apply. In these states, each party's liability will be limited to the greatest extent permitted by law.</p>

      <h2>"AS IS" and "AS AVAILABLE" Disclaimer</h2>
      <p>The Service is provided to You "AS IS" and "AS AVAILABLE" and with all faults and defects without warranty of any kind. To the maximum extent permitted under applicable law, the Company, on its own behalf and on behalf of its Affiliates and its and their respective licensors and service providers, expressly disclaims all warranties, whether express, implied, statutory or otherwise, with respect to the Service, including all implied warranties of merchantability, fitness for a particular purpose, title and non-infringement, and warranties that may arise out of course of dealing, course of performance, usage or trade practice. Without limitation to the foregoing, the Company provides no warranty or undertaking, and makes no representation of any kind that the Service will meet Your requirements, achieve any intended results, be compatible or work with any other software, applications, systems or services, operate without interruption, meet any performance or reliability standards or be error free or that any errors or defects can or will be corrected.</p>
      <p>Without limiting the foregoing, neither the Company nor any of the company's provider makes any representation or warranty of any kind, express or implied: (i) as to the operation or availability of the Service, or the information, content, and materials or products included thereon; (ii) that the Service will be uninterrupted or error-free; (iii) as to the accuracy, reliability, or currency of any information or content provided through the Service; or (iv) that the Service, its servers, the content, or e-mails sent from or on behalf of the Company are free of viruses, scripts, trojan horses, worms, malware, time bombs or other harmful components.</p>
      <p>Some jurisdictions do not allow the exclusion of certain types of warranties or limitations on applicable statutory rights of a consumer, so some or all of the above exclusions and limitations may not apply to You. But in such a case the exclusions and limitations set forth in this section shall be applied to the greatest extent enforceable under applicable law.</p>

      <h2>Governing Law</h2>
      <p>The laws of the Country, excluding its conflicts of law rules, shall govern this Terms and Your use of the Service. Your use of the Application may also be subject to other local, state, national, or international laws.</p>

      <h2>Disputes Resolution</h2>
      <p>If You have any concern or dispute about the Service, you agree to first try to resolve the dispute informally by contacting the Company.</p>

      <h2>For European Union (EU) Users</h2>
      <p>If You are a European Union consumer, you will benefit from any mandatory provisions of the law of the country in which You are resident.</p>

      <h2>United States Legal Compliance</h2>
      <p>You represent and warrant that (i) You are not located in a country that is subject to the United States government embargo, or that has been designated by the United States government as a "terrorist supporting" country, and (ii) You are not listed on any United States government list of prohibited or restricted parties.</p>

      <h2>Severability and Waiver</h2>
      <h3>Severability</h3>
      <p>If any provision of these Terms is held to be unenforceable or invalid, such provision will be changed and interpreted to accomplish the objectives of such provision to the greatest extent possible under applicable law and the remaining provisions will continue in full force and effect.</p>
      <h3>Waiver</h3>
      <p>Except as provided herein, the failure to exercise a right or to require performance of an obligation under these Terms shall not affect a party's ability to exercise such right or require such performance at any time thereafter nor shall the waiver of a breach constitute a waiver of any subsequent breach.</p>

      <h2>Translation Interpretation</h2>
      <p>These Terms and Conditions may have been translated if We have made them available to You on our Service. You agree that the original English text shall prevail in the case of a dispute.</p>

      <h2>Changes to These Terms and Conditions</h2>
      <p>We reserve the right, at Our sole discretion, to modify or replace these Terms at any time. If a revision is material, we will make reasonable efforts to provide at least 30 days' notice prior to any new terms taking effect. What constitutes a material change will be determined at Our sole discretion.</p>
      <p>By continuing to access or use Our Service after those revisions become effective, you agree to be bound by the revised terms. If You do not agree to the new terms, in whole or in part, please stop using the website and the Service.</p>

      <h2>Contact Us</h2>
      <p>If you have any questions about these Terms and Conditions, you can contact us:</p>
      <ul>
        <li>By email: <a href="mailto:{EMAIL}" style="text-decoration:underline">{EMAIL}</a></li>
        <li>By visiting this page on our website: <a href="{SITE}/contact/" style="text-decoration:underline">darkhorsepromotions.com</a></li>
      </ul>
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
                       navlinks=nav_html(path), tel=PHONE_TEL, phone=PHONE_DISPLAY)
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
