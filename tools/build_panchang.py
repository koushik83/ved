"""Build the panchang pages: an index and one page per city in English and Hindi, each holding every day from
the first date to the last as data the page reads for the day it is opened on, in the city's own time zone.

Run from the repo root with the site's own environment (.venv: skyfield, tzdata) and the ephemeris in
tools/panchang/ephem/:

    .venv\\Scripts\\python tools/build_panchang.py [--first 2026-11-01] [--last 2027-12-31]

It writes panchang/*.html, hi/panchang/*.html, the markdown copies, one data file per city in
panchang/data/ (shared by both languages, read by the page), and adds the pages to sitemap.xml.
The page's behaviour (today's row, the date picker, the muhurtas, the sky drawing) is in /panchang.js.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_prashnavali import FOOTER, GROW, INSTALL, JOURNEY, SITE, STYLE, jsonld, nav_css, nav_html, others_html  # noqa: E402
from panchang import engine, names  # noqa: E402
from panchang.cities import CITIES, COUNTRY_ORDER  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]


# ------------------------------------------------------------------ the words

T = {
    "en": {
        "index_title": "Panchang Today for Your City | Tithi, Nakshatra, Rahu Kaal, Choghadiya",
        "index_h1": "Today's Panchang",
        "index_description": "Today's Hindu panchang for cities in India, the United States, Canada, the United Kingdom, "
                             "Australia, the UAE and Singapore: tithi, nakshatra, sunrise, Rahu Kaal and Choghadiya in "
                             "each city's own local time.",
        "index_intro": [
            "A panchang is the Hindu almanac: the day's tithi, nakshatra, yoga and karana, the weekday, and the times "
            "of the day that tradition keeps or avoids. All of it hangs on the local sunrise, so a devotee in New Jersey "
            "or Sydney needs a panchang for New Jersey or Sydney, not for Delhi.",
            "Choose your city. Each page shows today and lets you look up any date up to {last}, in that city's own "
            "clock, with daylight saving taken care of.",
        ],
        "choose": "Choose your city",
        "remembered": "Open the panchang for {city}",
        "title": "Panchang for {city} Today | Tithi, Nakshatra, Rahu Kaal, Choghadiya",
        "description": "Today's panchang for {city}, {country}: sunrise and moonrise, tithi, nakshatra, yoga and karana "
                       "with the time each ends, Rahu Kaal, Abhijit Muhurat and Choghadiya, worked out for the city's "
                       "own sky and shown in local time.",
        "h1": "Panchang for {city}",
        "sub": "{country} · local time",
        "breadcrumb": "Panchang",
        "intro": "This page gives the Hindu almanac for {city} for today, and for any date up to {last}. Every time is "
                 "for {city}'s own sunrise and clock, not India's, so a fast or a muhurat can be kept where you live.",
        "read_h": "How to read the panchang",
        "read": [
            "The Hindu day runs from one sunrise to the next. The tithi, nakshatra, yoga and karana named first are the "
            "ones in force at sunrise; \"till\" gives the moment each ends, after which the next one named begins. A time "
            "marked \"next day\" falls after midnight, before the following sunrise.",
            "Rahu Kaal, Yamaganda and Gulika are the portions of the day tradition avoids for starting something new. "
            "Abhijit Muhurat around midday and Brahma Muhurta before dawn are the portions it favours. Choghadiya "
            "divides the day and the night into eight parts each, named good, neutral or bad.",
        ],
        "how_h": "How these times are worked out",
        "how": [
            "The positions of the Sun and the Moon come from the JPL DE421 planetary ephemeris, the data astronomers use.",
            "Sunrise and sunset are the moments the upper edge of the Sun crosses the horizon, allowing for the bending "
            "of light in the air, as most panchangs print them. Moonrise and moonset are for the centre of the Moon.",
            "Nakshatra, yoga and the rashis use the Lahiri (Chitrapaksha) ayanamsa, the standard of India's national "
            "calendar. The tithi needs no ayanamsa: it is the angle between the Moon and the Sun.",
            "Rahu Kaal, Yamaganda and Gulika are eighths of the day from sunrise to sunset. Abhijit is the eighth of the "
            "day's fifteen muhurtas, and Brahma Muhurta the second-last muhurta of the night.",
            "Times are rounded to the nearest minute. Another panchang may differ by a minute or two where its "
            "conventions differ.",
        ],
        "sky_h": "The sky at sunrise",
        "sky": "The Sun and the Moon on the zodiac at the moment of sunrise, with the Moon's phase as it is. The outer "
               "ring is the twelve rashis, the inner ring the twenty-seven nakshatras. The gap between the Moon and "
               "the Sun is the tithi.",
        "faq_h": "Frequently Asked Questions",
        "faq": [
            ("Why does the panchang for {city} differ from the one in India?",
             "Tithi and nakshatra change at the same instant everywhere, but the clock time differs, and the day's "
             "tithi is the one in force at the local sunrise. {city}'s sunrise is hours away from India's, so a tithi "
             "can fall on a different date, and every muhurat moves with the local sun."),
            ("Which tithi do I follow for a fast?",
             "For most observances, the tithi in force at sunrise where you are. Some fasts turn on a particular "
             "moment instead, such as moonrise or midnight, and their rules differ. This page gives the times; the "
             "rule belongs to the tradition you follow."),
            ("What is Rahu Kaal?",
             "One eighth of the daytime, a different eighth on each weekday, which tradition avoids for beginning new "
             "work. It is counted from the local sunrise, so it shifts with the season and the place."),
            ("What does \"till\" mean?",
             "The time at which that tithi or nakshatra ends. From then until the next sunrise, the next one named is "
             "in force."),
            ("Is this a horoscope?",
             "No. A panchang is a calendar: the positions of the Sun and the Moon and the divisions of the day. It "
             "predicts nothing."),
        ],
        "cities_h": "Panchang for other cities",
        "more_h": "More on this site",
        "more": [
            ("/today", "Today's Guidance", "one reading a day from Shri Ram or Hanuman Ji"),
            ("/jaap", "Naam Jaap Counter", "a digital mala of 108"),
        ],
        "md_note": "The day's figures are computed in the page for the date it is opened on.",
        "labels": {
            "sunrise": "Sunrise", "sunset": "Sunset", "moonrise": "Moonrise", "moonset": "Moonset",
            "noMoonrise": "no moonrise this day", "noMoonset": "no moonset this day", "dayLength": "Day length",
            "tithi": "Tithi", "nakshatra": "Nakshatra", "yoga": "Yoga", "karana": "Karana", "till": "till",
            "nextDay": "next day", "paksha": "Paksha", "amanta": "Amanta month", "purnimanta": "Purnimanta month",
            "vikram": "Vikram Samvat", "shaka": "Shaka Samvat", "gujarati": "Gujarati Samvat",
            "sunRashi": "Sun in", "moonRashi": "Moon in", "ritu": "Ritu", "ayana": "Ayana",
            "brahma": "Brahma Muhurta", "abhijit": "Abhijit Muhurat", "rahu": "Rahu Kaal", "yamaganda": "Yamaganda",
            "gulika": "Gulika Kaal", "good": "Good times", "avoid": "Times to avoid",
            "day": "Day choghadiya", "night": "Night choghadiya", "today": "Today", "pick": "Another date",
            "share": "Share on WhatsApp", "shareHead": "Panchang for {city}",
            "range": "This page holds dates from {first} to {last}.", "to": "to",
            "loadFail": "The day's figures could not be loaded. Please reload the page.",
            "sky": "Sky at sunrise", "elong": "Moon ahead of the Sun by", "sun": "Sun", "moon": "Moon",
            "hours": "h", "minutes": "m",
        },
    },
    "hi": {
        "index_title": "आज का पंचांग, अपने शहर का | तिथि, नक्षत्र, राहु काल, चौघड़िया",
        "index_h1": "आज का पंचांग",
        "index_description": "भारत, अमेरिका, कनाडा, ब्रिटेन, ऑस्ट्रेलिया, संयुक्त अरब अमीरात और सिंगापुर के शहरों का आज का "
                             "हिन्दू पंचांग: तिथि, नक्षत्र, सूर्योदय, राहु काल और चौघड़िया, हर शहर के अपने स्थानीय समय में।",
        "index_intro": [
            "पंचांग हिन्दू कालगणना है: दिन की तिथि, नक्षत्र, योग और करण, वार, और दिन के वे समय जिन्हें परंपरा रखती या "
            "छोड़ती है। यह सब स्थानीय सूर्योदय पर टिका है, इसलिए न्यू जर्सी या सिडनी के भक्त को न्यू जर्सी या सिडनी का "
            "पंचांग चाहिए, दिल्ली का नहीं।",
            "अपना शहर चुनें। हर पृष्ठ आज का पंचांग दिखाता है और {last} तक किसी भी तारीख का, उस शहर की अपनी घड़ी में, "
            "डेलाइट सेविंग सहित।",
        ],
        "choose": "अपना शहर चुनें",
        "remembered": "{city} का पंचांग खोलें",
        "title": "{city} का आज का पंचांग | तिथि, नक्षत्र, राहु काल, चौघड़िया",
        "description": "{city}, {country} का आज का पंचांग: सूर्योदय और चंद्रोदय, तिथि, नक्षत्र, योग और करण उनके समाप्ति समय "
                       "के साथ, राहु काल, अभिजित मुहूर्त और चौघड़िया, शहर के अपने आकाश के लिए, स्थानीय समय में।",
        "h1": "{city} का पंचांग",
        "sub": "{country} · स्थानीय समय",
        "breadcrumb": "पंचांग",
        "intro": "यह पृष्ठ {city} के लिए आज का, और {last} तक किसी भी दिन का, हिन्दू पंचांग देता है। हर समय {city} के अपने "
                 "सूर्योदय और घड़ी के अनुसार है, भारत के नहीं, ताकि व्रत और मुहूर्त वहाँ रखे जा सकें जहाँ आप रहते हैं।",
        "read_h": "पंचांग कैसे पढ़ें",
        "read": [
            "हिन्दू दिन एक सूर्योदय से अगले सूर्योदय तक चलता है। पहले लिखी तिथि, नक्षत्र, योग और करण सूर्योदय के समय चल रहे "
            "होते हैं; \"तक\" वह क्षण है जब वह समाप्त होता है और उसके बाद अगला नाम लगता है। \"अगले दिन\" लिखा समय आधी रात "
            "के बाद, अगले सूर्योदय से पहले आता है।",
            "राहु काल, यमगंड और गुलिक दिन के वे भाग हैं जिनमें परंपरा नया काम आरंभ करने से बचती है। दोपहर का अभिजित "
            "मुहूर्त और भोर से पहले का ब्रह्म मुहूर्त वे भाग हैं जिन्हें वह शुभ मानती है। चौघड़िया दिन और रात को "
            "आठ-आठ भागों में बाँटता है, जो शुभ, सम या अशुभ कहे जाते हैं।",
        ],
        "how_h": "ये समय कैसे निकाले गए हैं",
        "how": [
            "सूर्य और चंद्र की स्थितियाँ JPL DE421 ग्रह-पंचांग से ली गई हैं, वही आँकड़े जो खगोलशास्त्री उपयोग करते हैं।",
            "सूर्योदय और सूर्यास्त वह क्षण हैं जब सूर्य का ऊपरी किनारा क्षितिज पर आता है, वायु में प्रकाश के मुड़ने सहित, "
            "जैसा अधिकतर पंचांग छापते हैं। चंद्रोदय और चंद्रास्त चंद्र के केंद्र के लिए हैं।",
            "नक्षत्र, योग और राशियाँ लाहिरी (चित्रपक्ष) अयनांश से निकाली गई हैं, जो भारत के राष्ट्रीय पंचांग का मानक है। "
            "तिथि को अयनांश की आवश्यकता नहीं: वह चंद्र और सूर्य के बीच का कोण है।",
            "राहु काल, यमगंड और गुलिक सूर्योदय से सूर्यास्त तक के दिन के आठवें भाग हैं। अभिजित दिन के पंद्रह मुहूर्तों में "
            "आठवाँ है, और ब्रह्म मुहूर्त रात का दूसरा अंतिम मुहूर्त।",
            "समय निकटतम मिनट तक लिखे गए हैं। किसी अन्य पंचांग से एक-दो मिनट का अंतर हो सकता है, जहाँ उसकी परंपरा भिन्न हो।",
        ],
        "sky_h": "सूर्योदय के समय का आकाश",
        "sky": "सूर्योदय के क्षण राशिचक्र पर सूर्य और चंद्र, चंद्र की उस समय की कला के साथ। बाहरी वलय बारह राशियाँ, "
               "भीतरी वलय सत्ताईस नक्षत्र। चंद्र और सूर्य के बीच की दूरी ही तिथि है।",
        "faq_h": "अक्सर पूछे जाने वाले प्रश्न",
        "faq": [
            ("{city} का पंचांग भारत के पंचांग से अलग क्यों है?",
             "तिथि और नक्षत्र हर जगह एक ही क्षण बदलते हैं, पर घड़ी का समय अलग होता है, और दिन की तिथि वह मानी जाती है जो "
             "स्थानीय सूर्योदय पर चल रही हो। {city} का सूर्योदय भारत से घंटों अलग है, इसलिए तिथि दूसरी तारीख पर पड़ सकती "
             "है, और हर मुहूर्त स्थानीय सूर्य के साथ चलता है।"),
            ("व्रत के लिए कौन-सी तिथि मानें?",
             "अधिकतर व्रतों में वह तिथि जो आपके स्थान के सूर्योदय पर चल रही हो। कुछ व्रत किसी विशेष क्षण से तय होते हैं, "
             "जैसे चंद्रोदय या मध्यरात्रि, और उनके नियम अलग हैं। यह पृष्ठ समय देता है; नियम आपकी परंपरा का है।"),
            ("राहु काल क्या है?",
             "दिन का आठवाँ भाग, हर वार को अलग भाग, जिसमें परंपरा नया काम आरंभ करने से बचती है। यह स्थानीय सूर्योदय से "
             "गिना जाता है, इसलिए ऋतु और स्थान के साथ बदलता है।"),
            ("\"तक\" का क्या अर्थ है?",
             "वह समय जब वह तिथि या नक्षत्र समाप्त होता है। उसके बाद अगले सूर्योदय तक अगला नाम चलता है।"),
            ("क्या यह राशिफल है?",
             "नहीं। पंचांग एक कालगणना है: सूर्य और चंद्र की स्थितियाँ और दिन के विभाग। यह कोई भविष्यवाणी नहीं करता।"),
        ],
        "cities_h": "अन्य शहरों का पंचांग",
        "more_h": "इस साइट पर और",
        "more": [
            ("/today", "आज का मार्गदर्शन", "श्री राम या हनुमान जी से दिन का एक संदेश"),
            ("/jaap", "नाम जप काउंटर", "108 की डिजिटल माला"),
        ],
        "md_note": "दिन के आँकड़े पृष्ठ में उसी तारीख के लिए निकाले जाते हैं जिस दिन वह खोला जाए।",
        "labels": {
            "sunrise": "सूर्योदय", "sunset": "सूर्यास्त", "moonrise": "चंद्रोदय", "moonset": "चंद्रास्त",
            "noMoonrise": "इस दिन चंद्रोदय नहीं", "noMoonset": "इस दिन चंद्रास्त नहीं", "dayLength": "दिनमान",
            "tithi": "तिथि", "nakshatra": "नक्षत्र", "yoga": "योग", "karana": "करण", "till": "तक",
            "nextDay": "अगले दिन", "paksha": "पक्ष", "amanta": "अमांत मास", "purnimanta": "पूर्णिमांत मास",
            "vikram": "विक्रम संवत", "shaka": "शक संवत", "gujarati": "गुजराती संवत",
            "sunRashi": "सूर्य राशि", "moonRashi": "चंद्र राशि", "ritu": "ऋतु", "ayana": "अयन",
            "brahma": "ब्रह्म मुहूर्त", "abhijit": "अभिजित मुहूर्त", "rahu": "राहु काल", "yamaganda": "यमगंड",
            "gulika": "गुलिक काल", "good": "शुभ समय", "avoid": "वर्जित समय",
            "day": "दिन का चौघड़िया", "night": "रात का चौघड़िया", "today": "आज", "pick": "दूसरी तारीख",
            "share": "WhatsApp पर भेजें", "shareHead": "{city} का पंचांग",
            "range": "यह पृष्ठ {first} से {last} तक की तारीखें रखता है।", "to": "से",
            "loadFail": "दिन के आँकड़े लोड नहीं हो सके। कृपया पृष्ठ फिर से खोलें।",
            "sky": "सूर्योदय का आकाश", "elong": "चंद्र सूर्य से आगे", "sun": "सूर्य", "moon": "चंद्र",
            "hours": "घं", "minutes": "मि",
        },
    },
}
LONG_DATE = {"en": "{d:%-d} {month} {d.year}", "hi": "{d:%-d} {month} {d.year}"}
MONTHS_CIVIL = {
    "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
           "November", "December"],
    "hi": ["जनवरी", "फ़रवरी", "मार्च", "अप्रैल", "मई", "जून", "जुलाई", "अगस्त", "सितंबर", "अक्टूबर", "नवंबर", "दिसंबर"],
}

CSS = """        .pan-head { text-align: center; color: #666; margin: 0 0 6px; font-size: 16px; }
        .pan-date { text-align: center; font-size: 19px; color: #5D2E00; font-weight: bold; margin: 0 0 4px; }
        .pan-hindu { text-align: center; font-size: 17px; color: #A04000; margin: 0 0 14px; }
        .pan-controls { display: flex; flex-wrap: wrap; justify-content: center; gap: 8px 10px; margin: 0 0 14px; }
        .pan-controls select, .pan-controls input, .pan-controls button { font: inherit; font-size: 15px; padding: 8px 12px; border-radius: 20px; border: 1px solid #ff9933; background: white; color: #333; }
        .pan-controls button { cursor: pointer; } .pan-controls button.on { background: #ff9933; color: white; }
        .pan-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px 14px; margin: 0; }
        .pan-grid dt { color: #666; font-size: 14px; margin: 6px 0 0; } .pan-grid dd { margin: 0; font-size: 17px; color: #333; }
        .pan-grid dd .sub { font-size: 14px; color: #8a5a2b; display: block; }
        .pan-two { display: flex; flex-wrap: wrap; gap: 16px; align-items: flex-start; }
        .pan-two > * { flex: 1 1 260px; min-width: 0; }
        .pan-sky svg { width: 100%; height: auto; max-width: 340px; display: block; margin: 0 auto; }
        .pan-sky figcaption { font-size: 14px; color: #666; text-align: center; margin-top: 6px; }
        .limb { display: flex; justify-content: space-between; gap: 10px; padding: 7px 0; border-bottom: 1px solid #F3E7D3; font-size: 17px; }
        .limb:last-child { border-bottom: 0; } .limb .k { color: #666; font-size: 14px; min-width: 84px; }
        .limb .v b { color: #5D2E00; } .limb .v .till { color: #666; font-size: 15px; }
        table.chogh { width: 100%; border-collapse: collapse; font-size: 15px; }
        table.chogh td { padding: 6px 8px; border-bottom: 1px solid #F3E7D3; }
        table.chogh td:first-child { font-weight: bold; }
        .tone-good { color: #2E7D32; } .tone-bad { color: #C62828; } .tone-neutral { color: #8a5a2b; }
        .spans .limb .v { text-align: right; }
        .pan-cities { columns: 2; column-gap: 24px; } .pan-cities li { break-inside: avoid; }
        .pan-cities h3 { column-span: all; }
        @media (max-width: 480px) { .pan-grid { grid-template-columns: 1fr; } .pan-cities { columns: 1; } }
"""


# ------------------------------------------------------------------ the data

def epoch(d):
    return int(d.timestamp()) if d is not None else None


def encode(day: dict) -> dict:
    """One day as the page reads it: UTC epoch seconds, name indices, and the Hindu calendar's numbers."""
    limbs = {k: [[i, epoch(t)] for i, t in day[k]] for k in ("tithi", "nakshatra", "yoga", "karana")}
    return {
        "d": day["date"], "w": day["weekday"],
        "sr": epoch(day["sunrise"]), "ss": epoch(day["sunset"]), "nsr": epoch(day["next_sunrise"]),
        "mr": epoch(day["moonrise"]), "ms": epoch(day["moonset"]),
        "t": limbs["tithi"], "n": limbs["nakshatra"], "y": limbs["yoga"], "k": limbs["karana"],
        "p": "s" if day["paksha"] == "shukla" else "k",
        "am": day["amanta_month"], "aa": int(day["adhika"]),
        "pm": day["purnimanta_month"], "pa": int(day["purnimanta_adhika"]),
        "vs": day["vikram"], "sk": day["shaka"], "gs": day["gujarati"],
        "sun": day["sun_rashi"], "moon": day["moon_rashi"],
        "bm": [epoch(day["brahma"][0]), epoch(day["brahma"][1])],
        "ay": round(day["ayanamsa"], 4), "sl": round(day["sun_lon"], 2), "ml": round(day["moon_lon"], 2),
    }


EPOCH_FIELDS = ("sr", "ss", "nsr", "mr", "ms")


def relativize(rows):
    """Epoch seconds as offsets from the first sunrise: shorter numbers, same instants. The page adds the base back."""
    base = rows[0]["sr"]
    out = []
    for r in rows:
        r = dict(r)
        for k in EPOCH_FIELDS:
            if r[k] is not None:
                r[k] -= base
        r["bm"] = [r["bm"][0] - base, r["bm"][1] - base]
        for k in ("t", "n", "y", "k"):
            r[k] = [[i, (e - base) if e is not None else None] for i, e in r[k]]
        out.append(r)
    return base, out


def names_for(lang):
    return {
        "tithi": names.TITHI[lang], "paksha": names.PAKSHA[lang], "nakshatra": names.NAKSHATRA[lang],
        "yoga": names.YOGA[lang], "karana": [names.karana(i, lang) for i in range(60)],
        "month": names.MONTH[lang], "adhika": names.ADHIKA[lang], "rashi": names.RASHI[lang],
        "weekday": names.WEEKDAY[lang], "ritu": names.RITU[lang], "ayana": names.AYANA[lang],
        "choghadiya": names.CHOGHADIYA[lang], "tone": names.CHOGHADIYA_TONE,
    }


# ------------------------------------------------------------------ the pages

def long_date(d: dt.date, lang: str) -> str:
    return f"{d.day} {MONTHS_CIVIL[lang][d.month - 1]} {d.year}"


def head(lang, title, description, url, alt_en, alt_hi, crumbs, faq_ld, extra_css=""):
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    <link rel="canonical" href="{url}" />
    <link rel="alternate" hreflang="en" href="{alt_en}" />
    <link rel="alternate" hreflang="hi" href="{alt_hi}" />
    <link rel="alternate" hreflang="x-default" href="{alt_en}" />
    <link rel="apple-touch-icon" sizes="180x180" href="/favicon/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon/favicon-16x16.png">
    <link rel="manifest" href="/favicon/site.webmanifest">
    <meta name="description" content="{html.escape(description, quote=True)}">
    <meta property="og:title" content="{html.escape(title, quote=True)}">
    <meta property="og:description" content="{html.escape(description, quote=True)}">
    <meta property="og:url" content="{url}">
    <meta property="og:type" content="website">
    <meta property="og:image" content="{SITE}/images/og-default.jpg">
    <meta name="twitter:card" content="summary_large_image">

    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-32DZ0S3QTT"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'G-32DZ0S3QTT');
    </script>
    <script src="/app-events.js" defer></script>
    <script type="application/ld+json">
    {jsonld(crumbs)}
    </script>
    <style>
{STYLE % {"image": ""}}{nav_css()}{extra_css}    </style>
    <script type="application/ld+json">
{jsonld(faq_ld)}
    </script>
    <!-- Grow by Mediavine -->
    {GROW}
    <!-- Journey by Mediavine -->
    {JOURNEY}
</head>
"""


def paragraphs(items, **kw):
    return "".join("<p>%s</p>\n            " % html.escape(p.format(**kw)) for p in items)


def faq_html(items, **kw):
    return "".join("<h3>%s</h3>\n            <p>%s</p>\n            " % (html.escape(q.format(**kw)), html.escape(a.format(**kw)))
                   for q, a in items)


def faq_ld(items, **kw):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q.format(**kw),
                            "acceptedAnswer": {"@type": "Answer", "text": a.format(**kw)}} for q, a in items]}


def city_name(place, lang):
    return place.en if lang == "en" else place.hi


def country_name(place, lang):
    return place.country_en if lang == "en" else place.country_hi


def cities_list(lang, exclude=None):
    out = []
    for country in COUNTRY_ORDER:
        places = [p for p in CITIES if p.country_en == country and p.slug != exclude]
        if not places:
            continue
        out.append("<h3>%s</h3>" % html.escape(country_name(places[0], lang)))
        out.append("<ul>" + "".join('<li><a href="%s/panchang/%s">%s</a></li>' % ("" if lang == "en" else "/hi", p.slug,
                                                                               html.escape(city_name(p, lang)))
                                    for p in places) + "</ul>")
    return "\n            ".join(out)


def city_select(lang, current):
    groups = []
    for country in COUNTRY_ORDER:
        places = [p for p in CITIES if p.country_en == country]
        opts = "".join('<option value="%s"%s>%s</option>' % (p.slug, " selected" if p.slug == current else "",
                                                             html.escape(city_name(p, lang))) for p in places)
        groups.append('<optgroup label="%s">%s</optgroup>' % (html.escape(country_name(places[0], lang)), opts))
    return '<select id="city" aria-label="%s">%s</select>' % (html.escape(T[lang]["choose"]), "".join(groups))


def more_html(lang):
    t = T[lang]
    items = "".join('<li><a href="%s">%s</a>: %s</li>' % (h, html.escape(n), html.escape(d)) for h, n, d in t["more"])
    return '<section class="card"><h2>%s</h2><ul>%s</ul></section>' % (html.escape(t["more_h"]), items)


def city_page(place, lang, first, last):
    t = T[lang]
    city, country = city_name(place, lang), country_name(place, lang)
    kw = dict(city=city, country=country, last=long_date(last, lang), first=long_date(first, lang))
    url = SITE + ("" if lang == "en" else "/hi") + "/panchang/" + place.slug
    alt_en, alt_hi = SITE + "/panchang/" + place.slug, SITE + "/hi/panchang/" + place.slug
    switch = ("/hi/panchang/" + place.slug, "हिंदी") if lang == "en" else ("/panchang/" + place.slug, "English")
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home" if lang == "en" else "होम", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": t["breadcrumb"], "item": SITE + ("" if lang == "en" else "/hi") + "/panchang"},
        {"@type": "ListItem", "position": 3, "name": city, "item": url}]}
    data = {"slug": place.slug, "city": city, "tz": place.tz, "lang": lang, "url": url,
            "first": first.isoformat(), "last": last.isoformat(), "data": f"/panchang/data/{place.slug}.json",
            "labels": {k: v.format(**kw) for k, v in t["labels"].items()}, "names": names_for(lang)}
    labels = t["labels"]
    return head(lang, t["title"].format(**kw), t["description"].format(**kw), url, alt_en, alt_hi, crumbs,
                faq_ld(t["faq"], **kw), CSS) + f"""<body>
{nav_html(lang, None, switch)}
    <main class="wrap">
        <h1>{html.escape(t["h1"].format(**kw))}</h1>
        <p class="pan-head">{html.escape(t["sub"].format(**kw))}</p>
        <p class="pan-date" id="panDate">…</p>
        <p class="pan-hindu" id="panHindu"></p>
        <div class="pan-controls">
            {city_select(lang, place.slug)}
            <button type="button" id="todayBtn" class="on">{html.escape(labels["today"])}</button>
            <label>{html.escape(labels["pick"])} <input type="date" id="pickDate" min="{first.isoformat()}" max="{last.isoformat()}"></label>
        </div>
        <p id="panNote" class="pan-head" hidden></p>

        <section class="card">
            <div class="pan-two">
                <div>
                    <h2>{html.escape(labels["sunrise"])} · {html.escape(labels["moonrise"])}</h2>
                    <dl class="pan-grid" id="panSky"></dl>
                </div>
                <figure class="pan-sky" id="panWheel"></figure>
            </div>
        </section>

        <section class="card">
            <h2>{html.escape(labels["tithi"])} · {html.escape(labels["nakshatra"])} · {html.escape(labels["yoga"])} · {html.escape(labels["karana"])}</h2>
            <div id="panLimbs"></div>
            <dl class="pan-grid" id="panCal" style="margin-top: 14px;"></dl>
        </section>

        <section class="card spans">
            <div class="pan-two">
                <div><h2>{html.escape(labels["good"])}</h2><div id="panGood"></div></div>
                <div><h2>{html.escape(labels["avoid"])}</h2><div id="panAvoid"></div></div>
            </div>
        </section>

        <section class="card">
            <div class="pan-two">
                <div><h2>{html.escape(labels["day"])}</h2><table class="chogh" id="panChoghDay"></table></div>
                <div><h2>{html.escape(labels["night"])}</h2><table class="chogh" id="panChoghNight"></table></div>
            </div>
            <div class="actions" style="margin-top: 14px;"><button type="button" class="btn btn-whatsapp" id="panShare">{html.escape(labels["share"])}</button></div>
        </section>

        <section class="card">
            <h2>{html.escape(t["read_h"])}</h2>
            {paragraphs([t["intro"]] + t["read"], **kw)}
        </section>

        <section class="card">
            <h2>{html.escape(t["sky_h"])}</h2>
            <p>{html.escape(t["sky"].format(**kw))}</p>
            <h2 style="margin-top: 18px;">{html.escape(t["how_h"])}</h2>
            <ul>{"".join("<li>%s</li>" % html.escape(p) for p in t["how"])}</ul>
        </section>

        <section class="card">
            <h2>{html.escape(t["faq_h"])}</h2>
            {faq_html(t["faq"], **kw)}
        </section>

        <section class="card pan-cities">
            <h2>{html.escape(t["cities_h"])}</h2>
            {cities_list(lang, exclude=place.slug)}
        </section>
        {more_html(lang)}
        {others_html(lang, None)}
    </main>
{FOOTER}
    <script>window.PANCHANG = {json.dumps(data, ensure_ascii=False, separators=(",", ":"))};</script>
    <script src="/panchang.js" defer></script>
{INSTALL}</body>
</html>
"""


def index_page(lang, last):
    t = T[lang]
    kw = dict(last=long_date(last, lang))
    url = SITE + ("" if lang == "en" else "/hi") + "/panchang"
    alt_en, alt_hi = SITE + "/panchang", SITE + "/hi/panchang"
    switch = ("/hi/panchang", "हिंदी") if lang == "en" else ("/panchang", "English")
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home" if lang == "en" else "होम", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": t["breadcrumb"], "item": url}]}
    generic = [(q, a) for q, a in t["faq"] if "{city}" not in q + a]
    city_names = {p.slug: city_name(p, lang) for p in CITIES}
    return head(lang, t["index_title"], t["index_description"], url, alt_en, alt_hi, crumbs, faq_ld(generic), CSS) + f"""<body>
{nav_html(lang, None, switch)}
    <main class="wrap">
        <h1>{html.escape(t["index_h1"])}</h1>
        <p class="pan-head" id="remembered" hidden><a href="#" id="rememberedLink"></a></p>
        <section class="card">
            {paragraphs(t["index_intro"], **kw)}
        </section>
        <section class="card pan-cities">
            <h2>{html.escape(t["choose"])}</h2>
            {cities_list(lang)}
        </section>
        <section class="card">
            <h2>{html.escape(t["how_h"])}</h2>
            <ul>{"".join("<li>%s</li>" % html.escape(p) for p in t["how"])}</ul>
        </section>
        <section class="card">
            <h2>{html.escape(t["faq_h"])}</h2>
            {faq_html(generic)}
        </section>
        {more_html(lang)}
        {others_html(lang, None)}
    </main>
{FOOTER}
    <script>
    (function () {{
        var names = {json.dumps(city_names, ensure_ascii=False)};
        var slug = null;
        try {{ slug = localStorage.getItem('ved_panchang_city'); }} catch (e) {{ /* storage blocked */ }}
        if (slug && names[slug]) {{
            var a = document.getElementById('rememberedLink');
            a.href = '{"" if lang == "en" else "/hi"}/panchang/' + slug;
            a.textContent = {json.dumps(t["remembered"], ensure_ascii=False)}.replace('{{city}}', names[slug]);
            document.getElementById('remembered').hidden = false;
        }}
    }})();
    </script>
{INSTALL}</body>
</html>
"""


def markdown(place, lang, first, last):
    t = T[lang]
    kw = dict(city=city_name(place, lang), country=country_name(place, lang), last=long_date(last, lang),
              first=long_date(first, lang))
    url = SITE + ("" if lang == "en" else "/hi") + "/panchang/" + place.slug
    lines = ["# " + t["title"].format(**kw), "", "Source: " + url, "", t["intro"].format(**kw), "", t["md_note"], "",
             "## " + t["read_h"], ""]
    for p in t["read"]:
        lines += [p, ""]
    lines += ["## " + t["how_h"], ""] + ["- " + p for p in t["how"]] + ["", "## " + t["faq_h"], ""]
    for q, a in t["faq"]:
        lines += ["### " + q.format(**kw), "", a.format(**kw), ""]
    return "\n".join(lines)


def index_markdown(lang, last):
    t = T[lang]
    kw = dict(last=long_date(last, lang))
    url = SITE + ("" if lang == "en" else "/hi") + "/panchang"
    lines = ["# " + t["index_title"], "", "Source: " + url, ""]
    for p in t["index_intro"]:
        lines += [p.format(**kw), ""]
    lines += ["## " + t["choose"], ""]
    for p in CITIES:
        lines.append("- [%s](%s/panchang/%s)" % (city_name(p, lang), SITE + ("" if lang == "en" else "/hi"), p.slug))
    lines += ["", "## " + t["how_h"], ""] + ["- " + p for p in t["how"]] + [""]
    return "\n".join(lines)


# ------------------------------------------------------------------ the sitemap

def add_to_sitemap(urls, today: dt.date):
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    nl = "\r\n" if "\r\n" in text else "\n"
    added = 0
    for url in urls:
        if f"<loc>{url}</loc>" in text:
            continue
        entry = (f"  <url>{nl}    <loc>{url}</loc>{nl}    <lastmod>{today.isoformat()}</lastmod>{nl}"
                 f"    <changefreq>daily</changefreq>{nl}    <priority>0.8</priority>{nl}  </url>{nl}")
        text = text.replace("</urlset>", entry + "</urlset>")
        added += 1
    path.write_text(text, encoding="utf-8")
    return added


# ------------------------------------------------------------------ main

def build(first: dt.date, last: dt.date, only=None, cities=True):
    places = [p for p in CITIES if not only or p.slug in only] if cities else []
    sky = engine.Sky(first, last) if places else None
    written, urls = [], []
    data_dir = ROOT / "panchang" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    for place in places:
        city = engine.City(place.slug, place.lat, place.lon, place.tz)
        days = engine.compute(city, first, last, sky)
        base, rows = relativize([encode(d) for d in days])
        payload = {"slug": place.slug, "tz": place.tz, "first": first.isoformat(), "last": last.isoformat(),
                   "base": base, "rows": rows}
        (data_dir / f"{place.slug}.json").write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
                                                     encoding="utf-8")
        for lang in ("en", "hi"):
            folder = ROOT / ("panchang" if lang == "en" else "hi/panchang")
            folder.mkdir(parents=True, exist_ok=True)
            (folder / f"{place.slug}.html").write_text(city_page(place, lang, first, last), encoding="utf-8")
            (folder / f"{place.slug}.md").write_text(markdown(place, lang, first, last), encoding="utf-8")
            written.append(str((folder / f"{place.slug}.html").relative_to(ROOT)))
            urls.append(SITE + ("" if lang == "en" else "/hi") + "/panchang/" + place.slug)
    # the index pages sit beside the folder as panchang.html, the site's convention: Cloudflare Pages serves
    # foo.html at /foo, whereas a folder's index.html is served at /foo/ with a redirect
    for lang in ("en", "hi"):
        folder = ROOT if lang == "en" else ROOT / "hi"
        (folder / "panchang.html").write_text(index_page(lang, last), encoding="utf-8")
        (folder / "panchang.md").write_text(index_markdown(lang, last), encoding="utf-8")
        written.append(str((folder / "panchang.html").relative_to(ROOT)))
        urls.insert(0, SITE + ("" if lang == "en" else "/hi") + "/panchang")
    added = add_to_sitemap(urls, dt.date.today())
    return written, added


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    today = dt.date.today()
    ap.add_argument("--first", default=today.isoformat())
    ap.add_argument("--last", default=dt.date(today.year + 1, 12, 31).isoformat())
    ap.add_argument("--only", nargs="*", help="city slugs, for a quick run")
    ap.add_argument("--no-cities", action="store_true", help="rewrite the index pages only")
    a = ap.parse_args()
    pages, added = build(dt.date.fromisoformat(a.first), dt.date.fromisoformat(a.last), a.only, not a.no_cities)
    for w in pages:
        print("wrote", w)
    print(f"{len(pages)} pages, {added} sitemap entries added")
