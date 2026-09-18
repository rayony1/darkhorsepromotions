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
  <span><b>We're hiring.</b> Car key technicians for our Sam's Club and Costco locations. No locksmith experience needed, we train you.</span>
  <a href="/careers/">See what the job looks like</a>
</div>"""

FOOT = """</main>
<footer class="pad">
  <div class="foot">
    <div>
      <a class="brand" href="/"><img src="/img/logo-dark.jpg" alt=""><span class="brand-name">Dark Horse<small>Promotions, Inc.</small></span></a>
      <p>Car key replacement and programming inside Sam's Club and Costco. Call for this week's location. And we're hiring the team that runs them.</p>
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
      <p style="margin-top:.5rem;font-size:.85rem">We set up inside a Sam's Club or Costco for a few weeks at a time. Call or text to find out which one.</p>
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

MARQUEE_ITEMS = ["Inside Sam's Club and Costco","Lost key replacement","Key fob programming","Smart key duplication","Broken key extraction","Fob batteries","Done in minutes while you shop","All makes and models"]
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
      <p>We're building a team that thrives on challenges and craves growth. If you can talk to anyone, learn fast, and want a trade that pays, we want you on our side.</p>
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
    <h2 class="section-title">Where to find us.</h2>
    <div class="section-body">
      <p>We set up inside a Sam's Club or Costco warehouse for a few weeks at a time, then move to the next one. Call or text for this week's location and hours. A club membership is required for service.</p>
      <div style="display:flex;gap:.9rem;flex-wrap:wrap;margin-top:1.75rem">
        <a class="btn btn-orange" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a>
        <a class="btn btn-line" href="sms:{PHONE_TEL}">Text us</a>
      </div>
    </div>
  </div>
</section>"""

PAGES["/"] = dict(
    title="Dark Horse Promotions, Inc. | Car Key Replacement at Sam's Club and Costco",
    desc="Dark Horse Promotions replaces and programs car keys inside Sam's Club and Costco while you shop. Call for this week's location. We're also hiring technicians.",
    hiring=True,
    body=f"""
<section class="hero pad">
  <div class="hero-copy">
    <h1>
      <span>Lost your</span>
      <span>car key?</span>
      <span><i class="rule" aria-hidden="true"></i>Find us</span>
      <span>at the club.</span>
    </h1>
    <p>Dark Horse Promotions cuts and programs replacement car keys inside Sam's Club and Costco. Stop by while you shop, and leave with a working key in minutes. Every make, every model.</p>
    <div class="hero-actions">
      <a class="btn btn-orange" href="tel:{PHONE_TEL}">Call for this week's location</a>
      <a class="btn btn-line" href="/services/">How it works</a>
    </div>
  </div>
  <div class="hero-photo">
    <img src="/img/hero.jpg" alt="Carter Bolser standing in the door of the Dark Horse Promotions key service van" fetchpriority="high">
  </div>
  <aside class="hero-note">
    <b>Now hiring technicians</b>
    Run a key display inside the biggest warehouse clubs in the country. No locksmith background required.
    <a href="/careers/">See the role</a>
  </aside>
</section>
{marquee()}
<section class="light pad">
  <div class="grid">
    <h2 class="section-title">Unlocking convenience, one key at a time.</h2>
    <div class="section-body">
      <p>Dark Horse Promotions, Inc. provides fast, reliable car key replacement and programming at the warehouse clubs you already shop at. Whether you need a spare or lost your only key, we've got you covered, and you're done before your cart is full.</p>
      <a class="btn btn-line" href="/about/">About the company</a>
    </div>
    <ul class="statements">
      <li><h3>Keys while you shop</h3><p>Stop by the display, hand us your vehicle info, and finish your shopping. The key is cut, programmed, and tested at your car in the lot.</p></li>
      <li><h3>Save against the dealership</h3><p>No appointment, no tow, no dealership markup. Members typically pay far less than the dealer quotes for the same key.</p></li>
      <li><h3>Fob programming and repairs</h3><p>From reprogramming to battery replacement, your key fob leaves working flawlessly.</p></li>
    </ul>
  </div>
</section>
<section class="dark pad">
  <div class="grid">
    <h2 class="section-title">How it works.</h2>
    <p class="section-body">Four steps, and most members are done in the time it takes to shop.</p>
    <ol class="steps">
      <li><div class="n">Step 1</div><h3>Call for the location</h3><p>We rotate between Sam's Club and Costco warehouses. Call or text to find out where we are this week.</p></li>
      <li><div class="n">Step 2</div><h3>Stop by the display</h3><p>Bring your membership card and your vehicle. We look up exactly which key your car takes.</p></li>
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
    <h2 class="section-title">Why members trust us, and why people work here.</h2>
    <p class="section-body">A lost key is a bad day. We fix it fast, at a fair price, with a technician who knows the vehicle. The same standard applies to how we treat the people on our team.</p>
    <ul class="claims">
      <li><h3>Done in minutes</h3><p>Most keys are cut, programmed, and tested before you finish shopping.</p></li>
      <li><h3>Expert key solutions</h3><p>From replacements to fob programming, we handle all makes and models with precision.</p></li>
      <li><h3>Member first</h3><p>Straight pricing, no pressure, and a working key before you pay.</p></li>
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
  <p>When you need a key, we're the ones to call. We bring dealership-quality key replacement into the warehouse clubs you already shop at, at prices that make sense.</p>
</section>
<section class="light pad">
  <div class="grid">
    <h2 class="section-title">Where reliability meets convenience.</h2>
    <div class="section-body">
      <p>Life moves fast, and so do we. Dark Horse Promotions sets up inside Sam's Club and Costco warehouses, so replacing a lost key or adding a spare is something you do on a grocery run instead of a day off work.</p>
      <p>The company is led by Carter Bolser. Every job is done on site by a trained technician with the equipment and the key inventory to finish it while you shop.</p>
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
        <p>Carter runs Dark Horse Promotions and is the technician you're most likely to meet at the display. He built the company around a simple promise: be there, do the job right the first time, and treat every member like a neighbor.</p>
        <p>He's now hiring and training the next technicians on the team, and he answers the phone himself.</p>
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
      <p>We're growing, and the team page is short on purpose. We'd rather add people who want to build something than fill seats. If you're driven, dependable, and want to learn a trade that pays, read about the role.</p>
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
    <p>You're already at the club. Stop by the display, and by the time you've checked out, your new key is cut, programmed, and tested.</p>
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
      <li><div class="n">Step 1</div><h3>Call for the location</h3><p>We rotate between Sam's Club and Costco warehouses. Call or text to find out where we are this week.</p></li>
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
    title="Careers | Car Key Technician at Sam's Club and Costco | Dark Horse Promotions, Inc.",
    desc="Join Dark Horse Promotions as a car key technician running displays inside Sam's Club and Costco. No locksmith experience needed. We train you.",
    hiring=False,
    body=f"""
<section class="page-hero with-photo pad">
  <div class="ph-copy">
    <span class="kicker">Careers</span>
    <h1>Let's unlock your potential.</h1>
    <p>Your ambition has the key. Turn it at Dark Horse Promotions. We don't just open doors to opportunity, we help you break them down.</p>
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
      <p>Our success comes from dedication, determination, and an unstoppable work ethic. We're looking for driven, dependable people to join us. If you love tackling challenges head-on and want to grow personally and professionally, you'll fit right in.</p>
      <p>You don't need a locksmith background. You need to show up, talk to people, learn fast, and care about the member standing in front of you.</p>
    </div>
  </div>
</section>
<section id="role" class="dark pad">
  <div class="grid">
    <h2 class="section-title">What the job looks like.</h2>
    <p class="section-body">You're a car key technician running our display inside a Sam's Club or Costco. Thousands of members walk past you every day, and a lot of them need a key.</p>
    <ul class="list">
      <li><h3>Run the display</h3><p>Set up in the morning, keep the display sharp, and be the face of the operation for every member who stops.</p></li>
      <li><h3>Talk to members</h3><p>Most people don't know a replacement key can be done here. You explain it, look up their vehicle, and quote it on the spot.</p></li>
      <li><h3>Cut and program keys</h3><p>Using the equipment on site, you cut the key, program the fob or smart key at the member's vehicle, and test it before they leave.</p></li>
      <li><h3>Move with the show</h3><p>Displays run at a club for a few weeks, then move to the next one. You'll work different clubs, and sometimes travel.</p></li>
    </ul>
  </div>
</section>
<section class="light pad">
  <div class="grid">
    <h2 class="section-title">Who does well here.</h2>
    <p class="section-body">The trade can be taught. These can't.</p>
    <ul class="statements four">
      <li><h3>People people</h3><p>You're comfortable starting a conversation with a stranger and making them feel taken care of. This is a sales job as much as a technical one.</p></li>
      <li><h3>Self-starters</h3><p>You'll run the display on your own most days. Nobody is standing over your shoulder, and nobody should need to.</p></li>
      <li><h3>Problem solvers</h3><p>Every vehicle is a little different. You like figuring things out and finishing what you start.</p></li>
      <li><h3>Reliable and mobile</h3><p>You show up on time every day the display is open, and you're open to working different clubs and traveling when the show moves.</p></li>
    </ul>
  </div>
</section>
<section class="dark pad">
  <div class="grid">
    <h2 class="section-title">How hiring works.</h2>
    <p class="section-body">Four steps, and we move quickly. Most people hear back within a couple of days.</p>
    <ol class="steps">
      <li><div class="n">Step 1</div><h3>Apply</h3><p>Send the short form. A resume helps but isn't required.</p></li>
      <li><div class="n">Step 2</div><h3>Talk with Carter</h3><p>A phone call to hear your story, answer your questions, and talk about pay and schedule.</p></li>
      <li><div class="n">Step 3</div><h3>Shadow at the club</h3><p>Spend a day at the display on real jobs so you can see the work before you commit.</p></li>
      <li><div class="n">Step 4</div><h3>Start training</h3><p>Learn key cutting, programming, and how to talk to members, hands-on, then run your own display.</p></li>
    </ol>
  </div>
</section>
<section class="light pad">
  <div class="grid">
    <h2 class="section-title">Questions people ask.</h2>
    <p class="section-body">Straight answers. Anything else, ask Carter on the call.</p>
    <ul class="list">
      <li><h3>Do I need locksmith or automotive experience?</h3><p>No. We train you on the equipment and the vehicles. Sales or customer-facing experience helps more than a toolbox.</p></li>
      <li><h3>Where will I work?</h3><p>Inside Sam's Club and Costco warehouses. Displays run at one club for a few weeks, then move. Ask Carter about the current rotation and how far it reaches.</p></li>
      <li><h3>What are the hours?</h3><p>Displays are open during club hours, so the schedule follows the roadshow calendar. Carter will walk you through the current schedule.</p></li>
      <li><h3>Is there travel?</h3><p>Sometimes. When the show moves to a club out of town, so does the team. If you like seeing new places, it's a perk.</p></li>
      <li><h3>How am I paid?</h3><p>Pay is discussed on the first call. Bring your questions.</p></li>
    </ul>
  </div>
</section>
<section class="careers-band pad">
  <div class="grid">
    <h2>Ready to take the wheel?</h2>
    <div class="aside">
      <p>Your next opportunity is a few steps away. Send your details and Carter will reach out. Or skip the form and call or text <a href="tel:{PHONE_TEL}" style="font-weight:700;text-decoration:underline;text-underline-offset:3px">{PHONE_DISPLAY}</a>.</p>
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
  <p>Ready to take the wheel on a rewarding career? Become part of Dark Horse Promotions and help members walk out of the club with a working key.</p>
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
