"""Build the panchang section: an index, one page per city in English and Hindi, a page per city per month, the
festival pages, the methods page, and one data file per city that the city page reads for the day it is opened on.

Run from the repo root with the site's own environment (.venv: skyfield, tzdata) and the ephemeris in
tools/panchang/ephem/:

    .venv\\Scripts\\python tools/build_panchang.py [--first 2026-11-01] [--last 2027-12-31] [--only delhi toronto]

The astronomy of each city is computed once and cached under tools/panchang/cache/ (not committed), so a rebuild
after a change to the pages takes a minute. The page's behaviour in the browser (today's row, the date picker, the
muhurtas, the sky drawing, the fasts) is in /panchang.js.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import pathlib
import sys
from zoneinfo import ZoneInfo

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import update_sitemap  # noqa: E402
from build_prashnavali import (AD_ZONE, AD_ZONE_END, FOOTER, GROW, INSTALL, JOURNEY, SITE, STYLE, jsonld,  # noqa: E402
                               nav_css, nav_html, others_html)
from panchang import engine, names, vrats  # noqa: E402
from panchang.cities import CITIES, COUNTRY_ORDER, INDEXED  # noqa: E402
from panchang.texts import FESTIVALS, METHODS  # noqa: E402
from panchang.texts import MONTH as MONTH_TEXT  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
CACHE_DIR = ROOT / "tools" / "panchang" / "cache"
# the cities whose festival lists are written into the festival pages in full; the rest are read from their data
MAIN_CITIES = ["new-jersey", "new-york", "san-francisco", "chicago", "dallas", "toronto", "london", "sydney",
               "melbourne", "delhi", "mumbai", "dubai"]
EXAMPLE_CITY = {"en": "New Jersey", "hi": "न्यू जर्सी"}


# ------------------------------------------------------------------ the words

T = {
    "en": {
        "index_title": "Panchang Today for Your City | Tithi, Nakshatra, Rahu Kaal, Choghadiya",
        "index_h1": "Today's Panchang",
        # descriptions kept near 155 characters, the length Google shows, with the words people type
        "index_description": "Today's panchang for your city in the USA, Canada, UK, Australia and India: tithi, Rahu "
                             "Kalam, Choghadiya and the next fast, in local time.",
        "index_intro": [
            "A panchang is the Hindu almanac: the day's tithi, nakshatra, yoga and karana, the weekday, and the times "
            "of the day that tradition keeps or avoids. All of it hangs on the local sunrise, so a devotee in New Jersey "
            "or Sydney needs a panchang for New Jersey or Sydney, not for Delhi.",
            "Choose your city. Each page shows today and lets you look up any date up to {last}, in that city's own "
            "clock, with daylight saving taken care of, and lists the city's fasts and festivals for the year.",
        ],
        "choose": "Choose your city",
        "remembered": "Open the panchang for {city}",
        "festival_pages_h": "Festival dates by city",
        # permanent addresses since 15 Nov 2026: each page shows the next occurrence, the year in its title
        "festival_pages": [
            ("makar-sankranti", "Makar Sankranti, Pongal and Lohri: date and time in every city"),
            ("maha-shivratri", "Maha Shivratri: date and nishita puja time in every city"),
            ("holi", "Holi and Holika Dahan: date and time in every city"),
            ("karwa-chauth", "Karwa Chauth: date and moonrise in every city"),
            ("diwali", "Diwali: Lakshmi Puja date and time in every city"),
            ("ekadashi", "Ekadashi dates and parana time by city"),
            ("sankashti-chaturthi", "Sankashti Chaturthi dates and moonrise by city"),
        ],
        "methods_link": "How this panchang is calculated",
        "title": "Panchang for {city} Today | Tithi, Nakshatra, Rahu Kaal, Choghadiya",
        "description": "Today's panchang (panchangam) for {city}: tithi, nakshatra, Rahu Kalam, Choghadiya and the "
                       "next Ekadashi, in local time.",
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
             "moment instead, such as moonrise or midnight, and their rules differ. The fasts and festivals listed on "
             "this page already apply each rule for {city}."),
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
        "vrat_h": "Fasts and festivals",
        "year_h": "Festivals in {city}: {span}",
        "year_intro": "The dates below are for {city}: each festival falls on the day its tithi is in force at the "
                      "moment the tradition names, worked out for {city}'s own sunrise, sunset and moonrise. A festival "
                      "can fall a day apart from India for that reason.",
        "ekadashi_h": "Ekadashi dates in {city}",
        "ekadashi_intro": "The fast day, and the parana window for breaking it the next morning, in {city}'s time.",
        "sankashti_h": "Sankashti Chaturthi in {city}",
        "sankashti_intro": "The fast day and the moonrise that ends it, in {city}'s time. A Tuesday Sankashti is Angarki.",
        "cols_year": ["Date", "Festival", "The moment that decides it"],
        "cols_ekadashi": ["Date", "Ekadashi", "Parana (next day)"],
        "cols_sankashti": ["Date", "Sankashti", "Moonrise"],
        "months_h": "Panchang by month",
        "months_intro": "Each month's page lists every day's tithi and nakshatra at sunrise, the sunrise, sunset and "
                        "moonrise, and Rahu Kaal, with the month's fasts and festivals.",
        "facts_h": "The sky over {city}",
        "dst_yes": "{city} moves its clocks forward on {start} and back on {end} in {year}; every time here already "
                   "allows for it, including the fasts that straddle the change.",
        "dst_no": "{city} keeps the same clock all year, so no tithi's end time ever jumps by an hour.",
        "facts": "In {city} the Sun rises between {sr_early} ({sr_early_d}) and {sr_late} ({sr_late_d}) and sets "
                 "between {ss_early} ({ss_early_d}) and {ss_late} ({ss_late_d}). The longest day, {long_d}, lasts "
                 "{long_len}; the shortest, {short_d}, {short_len}. Rahu Kaal, an eighth of the day, is therefore "
                 "{rahu_short} long in midwinter and {rahu_long} in midsummer.",
        "zone": "Times are in {zone}, the clock {city} keeps.",
        "faq_city": [
            ("Does {city} change its clocks, and does the panchang allow for it?", "{dst}"),
            ("When is Diwali {year} in {city}?", "{diwali}"),
            ("When is Karwa Chauth {year} in {city}, and when does the moon rise?", "{karwa}"),
        ],
        "diwali_a": "Diwali, the Lakshmi Puja night, falls on {date} in {city}: Amavasya is in force after sunset "
                    "that evening, and the puja window is {window}.",
        "karwa_a": "Karwa Chauth {year} is on {date} in {city}. The moon rises at {moonrise}, and the fast runs from "
                   "sunrise at {sunrise} until then.",
        "unknown_a": "The {year} date for {city} is on the festival page linked below.",
        "window_word": "puja window", "moonrise_word": "moonrise", "parana_word": "parana", "ends_word": "ends",
        "sankranti_word": "the Sun enters the sign at", "next_day_word": "next day",
        "labels": {
            "sunrise": "Sunrise", "sunset": "Sunset", "moonrise": "Moonrise", "moonset": "Moonset",
            "noMoonrise": "no moonrise this day", "noMoonset": "no moonset this day", "dayLength": "Day length",
            "vratToday": "Today", "vratNext": "Coming up", "vratNone": "No fast or festival today",
            "moonriseAt": "moonrise", "fastTill": "fast from sunrise", "parana": "parana (breaking the fast)",
            "pujaTime": "puja time", "tithiEnds": "tithi ends", "angarki": "Angarki",
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
        "index_description": "भारत, अमेरिका, कनाडा, ब्रिटेन, ऑस्ट्रेलिया, न्यूज़ीलैंड, यूरोप, संयुक्त अरब अमीरात और सिंगापुर के शहरों "
                             "का आज का हिन्दू पंचांग: तिथि, नक्षत्र, सूर्योदय, राहु काल और चौघड़िया, हर शहर के अपने स्थानीय समय में, "
                             "वर्ष के व्रत-त्योहारों के साथ।",
        "index_intro": [
            "पंचांग हिन्दू कालगणना है: दिन की तिथि, नक्षत्र, योग और करण, वार, और दिन के वे समय जिन्हें परंपरा रखती या "
            "छोड़ती है। यह सब स्थानीय सूर्योदय पर टिका है, इसलिए न्यू जर्सी या सिडनी के भक्त को न्यू जर्सी या सिडनी का "
            "पंचांग चाहिए, दिल्ली का नहीं।",
            "अपना शहर चुनें। हर पृष्ठ आज का पंचांग दिखाता है और {last} तक किसी भी तारीख का, उस शहर की अपनी घड़ी में, "
            "डेलाइट सेविंग सहित, और शहर के वर्ष भर के व्रत-त्योहार देता है।",
        ],
        "choose": "अपना शहर चुनें",
        "remembered": "{city} का पंचांग खोलें",
        "festival_pages_h": "त्योहारों की तारीखें, शहर के अनुसार",
        "festival_pages": [
            ("makar-sankranti", "मकर संक्रांति, पोंगल और लोहड़ी: हर शहर में तारीख और समय"),
            ("maha-shivratri", "महाशिवरात्रि: हर शहर में तारीख और निशीथ पूजा का समय"),
            ("holi", "होली और होलिका दहन: हर शहर में तारीख और समय"),
            ("karwa-chauth", "करवा चौथ: हर शहर में तारीख और चंद्रोदय"),
            ("diwali", "दीपावली: हर शहर में लक्ष्मी पूजा की तारीख और समय"),
            ("ekadashi", "एकादशी: शहर के अनुसार तारीखें और पारण"),
            ("sankashti-chaturthi", "संकष्टी चतुर्थी: शहर के अनुसार तारीखें और चंद्रोदय"),
        ],
        "methods_link": "यह पंचांग कैसे बनता है",
        "title": "{city} का आज का पंचांग | तिथि, नक्षत्र, राहु काल, चौघड़िया",
        "description": "{city}, {country} का आज का पंचांग: सूर्योदय और चंद्रोदय, तिथि, नक्षत्र, योग और करण उनके समाप्ति समय "
                       "के साथ, राहु काल, अभिजित मुहूर्त और चौघड़िया, शहर के अपने आकाश के लिए, स्थानीय समय में, {city} के {year} "
                       "के व्रत-त्योहारों सहित।",
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
             "जैसे चंद्रोदय या मध्यरात्रि, और उनके नियम अलग हैं। इस पृष्ठ पर दिए व्रत-त्योहार {city} के लिए हर नियम लगाकर "
             "निकाले गए हैं।"),
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
        "vrat_h": "व्रत और त्योहार",
        "year_h": "{city} में त्योहार: {span}",
        "year_intro": "नीचे की तारीखें {city} के लिए हैं: हर त्योहार उस दिन पड़ता है जब उसकी तिथि परंपरा द्वारा बताए क्षण पर चल "
                      "रही हो, और यह {city} के अपने सूर्योदय, सूर्यास्त और चंद्रोदय से निकाला गया है। इसी कारण कोई त्योहार "
                      "भारत से एक दिन अलग पड़ सकता है।",
        "ekadashi_h": "{city} में एकादशी की तारीखें",
        "ekadashi_intro": "व्रत का दिन, और अगली सुबह व्रत खोलने का पारण समय, {city} के समय में।",
        "sankashti_h": "{city} में संकष्टी चतुर्थी",
        "sankashti_intro": "व्रत का दिन और उसे पूरा करने वाला चंद्रोदय, {city} के समय में। मंगलवार की संकष्टी अंगारकी है।",
        "cols_year": ["तारीख", "त्योहार", "निर्णायक क्षण"],
        "cols_ekadashi": ["तारीख", "एकादशी", "पारण (अगले दिन)"],
        "cols_sankashti": ["तारीख", "संकष्टी", "चंद्रोदय"],
        "months_h": "महीने का पंचांग",
        "months_intro": "हर महीने का पृष्ठ हर दिन की सूर्योदय की तिथि और नक्षत्र, सूर्योदय, सूर्यास्त और चंद्रोदय, और राहु काल "
                        "देता है, उस महीने के व्रत और त्योहारों के साथ।",
        "facts_h": "{city} का आकाश",
        "dst_yes": "{city} में {year} में {start} को घड़ी एक घंटा आगे और {end} को पीछे होती है; यहाँ का हर समय इसे पहले से "
                   "मानकर चलता है, उन व्रतों सहित जो इस बदलाव के आर-पार पड़ते हैं।",
        "dst_no": "{city} की घड़ी पूरे वर्ष एक-सी रहती है, इसलिए किसी तिथि का समाप्ति समय कभी एक घंटा नहीं खिसकता।",
        "facts": "{city} में सूर्य {sr_early} ({sr_early_d}) से {sr_late} ({sr_late_d}) के बीच उगता है और {ss_early} "
                 "({ss_early_d}) से {ss_late} ({ss_late_d}) के बीच डूबता है। सबसे लंबा दिन {long_d} को {long_len} का और "
                 "सबसे छोटा {short_d} को {short_len} का है। इसलिए दिन का आठवाँ भाग, राहु काल, शीत में {rahu_short} और "
                 "ग्रीष्म में {rahu_long} का होता है।",
        "zone": "समय {zone} में हैं, जो घड़ी {city} रखता है।",
        "faq_city": [
            ("क्या {city} की घड़ी बदलती है, और क्या पंचांग उसे मानता है?", "{dst}"),
            ("{city} में {year} की दीपावली कब है?", "{diwali}"),
            ("{city} में {year} का करवा चौथ कब है, और चंद्रोदय कब होगा?", "{karwa}"),
        ],
        "diwali_a": "दीपावली, लक्ष्मी पूजन की रात, {city} में {date} को है: उस शाम सूर्यास्त के बाद अमावस्या चल रही होती है, और "
                    "पूजा का समय {window} है।",
        "karwa_a": "{city} में करवा चौथ {year} {date} को है। चंद्रोदय {moonrise} पर होगा, और व्रत सूर्योदय {sunrise} से "
                   "तब तक चलता है।",
        "unknown_a": "{city} के लिए {year} की तारीख नीचे जुड़े त्योहार पृष्ठ पर है।",
        "window_word": "पूजा का समय", "moonrise_word": "चंद्रोदय", "parana_word": "पारण", "ends_word": "समाप्त",
        "sankranti_word": "सूर्य राशि में प्रवेश", "next_day_word": "अगले दिन",
        "labels": {
            "sunrise": "सूर्योदय", "sunset": "सूर्यास्त", "moonrise": "चंद्रोदय", "moonset": "चंद्रास्त",
            "noMoonrise": "इस दिन चंद्रोदय नहीं", "noMoonset": "इस दिन चंद्रास्त नहीं", "dayLength": "दिनमान",
            "vratToday": "आज", "vratNext": "आगे", "vratNone": "आज कोई व्रत या त्योहार नहीं",
            "moonriseAt": "चंद्रोदय", "fastTill": "व्रत सूर्योदय से", "parana": "पारण (व्रत खोलना)",
            "pujaTime": "पूजा का समय", "tithiEnds": "तिथि समाप्त", "angarki": "अंगारकी",
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
MONTHS_CIVIL = {
    "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
           "November", "December"],
    "hi": ["जनवरी", "फ़रवरी", "मार्च", "अप्रैल", "मई", "जून", "जुलाई", "अगस्त", "सितंबर", "अक्टूबर", "नवंबर", "दिसंबर"],
}
WEEKDAY_SHORT = {"en": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                 "hi": ["सोम", "मंगल", "बुध", "गुरु", "शुक्र", "शनि", "रवि"]}

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
        table.chogh, table.pan { width: 100%; border-collapse: collapse; font-size: 15px; }
        table.chogh td, table.pan td, table.pan th { padding: 6px 8px; border-bottom: 1px solid #F3E7D3; text-align: left; vertical-align: top; }
        table.pan th { color: #666; font-weight: normal; font-size: 13px; }
        table.chogh td:first-child { font-weight: bold; }
        table.pan td.d { white-space: nowrap; color: #5D2E00; }
        .tone-good { color: #2E7D32; } .tone-bad { color: #C62828; } .tone-neutral { color: #8a5a2b; }
        .spans .limb .v { text-align: right; }
        .pan-cities { columns: 2; column-gap: 24px; } .pan-cities li { break-inside: avoid; }
        .pan-cities h3 { column-span: all; }
        .vrat { padding: 7px 0; border-bottom: 1px solid #F3E7D3; } .vrat:last-child { border-bottom: 0; }
        .vrat .d { color: #5D2E00; font-weight: bold; } .vrat .x { color: #666; font-size: 14px; display: block; }
        .months a { display: inline-block; margin: 3px 8px 3px 0; white-space: nowrap; }
        details.pan summary { cursor: pointer; color: #A04000; font-weight: bold; padding: 6px 0; }
        .scroll { overflow-x: auto; }
        @media (max-width: 480px) { .pan-grid { grid-template-columns: 1fr; } .pan-cities { columns: 1; } table.pan { font-size: 13px; } }
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


def encode_vrats(obs: list, base: int) -> list[dict]:
    """The observances as the page reads them: offsets from the base, one compact record each."""
    out = []
    for o in obs:
        rel = lambda v: (int(v) - base) if v is not None else None  # noqa: E731
        rec = {"k": o.key, "d": o.date.isoformat(), "kind": o.kind, "en": o.en, "hi": o.hi}
        dd = o.details
        if dd.get("moonrise") is not None:
            rec["mr"] = rel(dd["moonrise"])
        if dd.get("fast"):
            rec["fast"] = [rel(dd["fast"][0]), rel(dd["fast"][1])]
        if dd.get("window"):
            rec["win"] = [rel(dd["window"][0]), rel(dd["window"][1])]
        if dd.get("parana"):
            rec["pr"] = [rel(dd["parana"][0]), rel(dd["parana"][1])]
        if dd.get("tithi_ends") is not None:
            rec["te"] = rel(dd["tithi_ends"])
        if dd.get("angarki"):
            rec["ang"] = 1
        out.append(rec)
    return out


def names_for(lang):
    return {
        "tithi": names.TITHI[lang], "paksha": names.PAKSHA[lang], "nakshatra": names.NAKSHATRA[lang],
        "yoga": names.YOGA[lang], "karana": [names.karana(i, lang) for i in range(60)],
        "month": names.MONTH[lang], "adhika": names.ADHIKA[lang], "rashi": names.RASHI[lang],
        "weekday": names.WEEKDAY[lang], "ritu": names.RITU[lang], "ayana": names.AYANA[lang],
        "choghadiya": names.CHOGHADIYA[lang], "tone": names.CHOGHADIYA_TONE,
    }


def city_rows(place, first, last, sky_holder):
    """The city's encoded days and its sunrise, sunset, moonrise and moonset instants, from the cache if present.
    The Sky is built only when a city is missing from the cache, since it takes twenty seconds."""
    path = CACHE_DIR / f"{place.slug}-{first}-{last}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    if sky_holder.get("sky") is None:
        sky_holder["sky"] = engine.Sky(first, last)
    city = engine.City(place.slug, place.lat, place.lon, place.tz)
    pl = engine.Place(sky_holder["sky"], city, first, last)
    rows, d = [], first
    while d <= last:
        rows.append(encode(pl.day(d)))
        d += dt.timedelta(days=1)
    stamp = lambda t: int(t.utc_datetime().timestamp())  # noqa: E731
    events = {"sunrise": sorted(stamp(t) for ts in pl.sunrise.values() for t in ts),
              "sunset": sorted(stamp(t) for ts in pl.sunset.values() for t in ts),
              "moonrise": [stamp(t) for t in pl.moonrises], "moonset": [stamp(t) for t in pl.moonsets]}
    payload = {"rows": rows, "events": events}
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")
    return payload


# ------------------------------------------------------------------ small helpers

def long_date(d: dt.date, lang: str) -> str:
    return f"{d.day} {MONTHS_CIVIL[lang][d.month - 1]} {d.year}"


def short_date(d: dt.date, lang: str) -> str:
    return f"{d.day} {MONTHS_CIVIL[lang][d.month - 1]}"


def weekday_date(d: dt.date, lang: str) -> str:
    wd = names.WEEKDAY["civil"][d.weekday()] if lang == "en" else names.WEEKDAY["hi"][d.weekday()]
    return f"{wd}, {long_date(d, lang)}"


def clock(epoch, zone) -> str:
    """A local clock time rounded to the minute, 12-hour, as the page shows it."""
    if epoch is None:
        return "-"
    return dt.datetime.fromtimestamp(epoch + 30, zone).strftime("%I:%M %p")


def clock_dated(epoch, zone, date: dt.date, lang: str) -> str:
    """A clock time, with the day named when it falls on another civil date."""
    if epoch is None:
        return "-"
    t = dt.datetime.fromtimestamp(epoch + 30, zone)
    s = t.strftime("%I:%M %p")
    if t.date() != date:
        s += ", " + short_date(t.date(), lang)
    return s


def span_text(a, b, zone, date, lang) -> str:
    return f"{clock_dated(a, zone, date, lang)} {T[lang]['labels']['to']} {clock_dated(b, zone, date, lang)}"


def length(seconds, lang) -> str:
    h, m = int(seconds // 3600), int(round((seconds % 3600) / 60))
    return f"{h} h {m} min" if lang == "en" else f"{h} घंटे {m} मिनट"


def esc(s) -> str:
    return html.escape(str(s))


def month_range(first: dt.date, last: dt.date):
    y, m = first.year, first.month
    while (y, m) <= (last.year, last.month):
        yield y, m
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def city_name(place, lang):
    return place.en if lang == "en" else place.hi


def country_name(place, lang):
    return place.country_en if lang == "en" else place.country_hi


def prefix(lang):
    return "" if lang == "en" else "/hi"


def obs_name(o, lang):
    return o.en if lang == "en" else o.hi


def city_facts(place, rows, lang, year):
    """True sentences about this city's sky and clock, from its own rows: no two cities read alike."""
    zone = ZoneInfo(place.tz)
    t = T[lang]
    city = city_name(place, lang)
    in_year = [r for r in rows if r["d"].startswith(str(year))] or rows
    tod = lambda r, k: (dt.datetime.fromtimestamp(r[k] + 30, zone).hour * 60  # noqa: E731
                        + dt.datetime.fromtimestamp(r[k] + 30, zone).minute)
    sr_early = min(in_year, key=lambda r: tod(r, "sr"))
    sr_late = max(in_year, key=lambda r: tod(r, "sr"))
    ss_early = min(in_year, key=lambda r: tod(r, "ss"))
    ss_late = max(in_year, key=lambda r: tod(r, "ss"))
    longest = max(in_year, key=lambda r: r["ss"] - r["sr"])
    shortest = min(in_year, key=lambda r: r["ss"] - r["sr"])
    d = lambda r: short_date(dt.date.fromisoformat(r["d"]), lang)  # noqa: E731
    facts = t["facts"].format(
        city=city, sr_early=clock(sr_early["sr"], zone), sr_early_d=d(sr_early), sr_late=clock(sr_late["sr"], zone),
        sr_late_d=d(sr_late), ss_early=clock(ss_early["ss"], zone), ss_early_d=d(ss_early),
        ss_late=clock(ss_late["ss"], zone), ss_late_d=d(ss_late), long_d=d(longest),
        long_len=length(longest["ss"] - longest["sr"], lang), short_d=d(shortest),
        short_len=length(shortest["ss"] - shortest["sr"], lang),
        rahu_short=length((shortest["ss"] - shortest["sr"]) / 8, lang),
        rahu_long=length((longest["ss"] - longest["sr"]) / 8, lang))
    changes = []
    prev = None
    for r in in_year:
        off = dt.datetime.fromtimestamp((r["sr"] + r["ss"]) / 2, zone).utcoffset()
        if prev is not None and off != prev:
            changes.append((dt.date.fromisoformat(r["d"]), off > prev))
        prev = off
    forward = [c for c, fwd in changes if fwd]
    back = [c for c, fwd in changes if not fwd]
    if forward and back:
        start, end = (forward[0], back[0]) if forward[0] < back[0] else (forward[0], back[-1])
        dst = t["dst_yes"].format(city=city, start=long_date(start, lang), end=long_date(end, lang), year=year)
    else:
        dst = t["dst_no"].format(city=city)
    zone_name = dt.datetime.fromtimestamp(in_year[0]["sr"], zone).tzname() or place.tz
    return {"facts": facts, "dst": dst, "zone": t["zone"].format(zone=f"{zone_name} ({place.tz})", city=city)}


# ------------------------------------------------------------------ page pieces

def head(lang, title, description, url, alt_en, alt_hi, crumbs, faq_ld, extra_css="", og_type="website", robots=""):
    robots_tag = f'\n    <meta name="robots" content="{robots}">' if robots else ""
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">{robots_tag}
    <title>{esc(title)}</title>
    <link rel="canonical" href="{url}" />{"" if alt_hi is None else f'''
    <link rel="alternate" hreflang="en" href="{alt_en}" />
    <link rel="alternate" hreflang="hi" href="{alt_hi}" />
    <link rel="alternate" hreflang="x-default" href="{alt_en}" />'''}
    <link rel="apple-touch-icon" sizes="180x180" href="/favicon/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon/favicon-16x16.png">
    <link rel="manifest" href="/favicon/site.webmanifest">
    <meta name="description" content="{html.escape(description, quote=True)}">
    <meta property="og:title" content="{html.escape(title, quote=True)}">
    <meta property="og:description" content="{html.escape(description, quote=True)}">
    <meta property="og:url" content="{url}">
    <meta property="og:type" content="{og_type}">
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
    return "".join("<p>%s</p>\n            " % esc(p.format(**kw)) for p in items)


def faq_html(items, **kw):
    return "".join("<h3>%s</h3>\n            <p>%s</p>\n            " % (esc(q.format(**kw)), esc(a.format(**kw)))
                   for q, a in items)


def faq_ld(items, **kw):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q.format(**kw),
                            "acceptedAnswer": {"@type": "Answer", "text": a.format(**kw)}} for q, a in items]}


def crumbs(lang, *items):
    """BreadcrumbList from (name, url) pairs after Home."""
    trail = [{"@type": "ListItem", "position": 1, "name": "Home" if lang == "en" else "होम", "item": SITE + "/"}]
    for i, (name, url) in enumerate(items, start=2):
        trail.append({"@type": "ListItem", "position": i, "name": name, "item": url})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": trail}


def cities_list(lang, exclude=None):
    out = []
    for country in COUNTRY_ORDER:
        places = [p for p in CITIES if p.country_en == country and p.slug != exclude]
        if not places:
            continue
        out.append("<h3>%s</h3>" % esc(country_name(places[0], lang)))
        out.append("<ul>" + "".join('<li><a href="%s/panchang/%s">%s</a></li>' % (prefix(lang), p.slug, esc(city_name(p, lang)))
                                    for p in places) + "</ul>")
    return "\n            ".join(out)


def city_select(lang, current, element_id="city"):
    groups = []
    for country in COUNTRY_ORDER:
        places = [p for p in CITIES if p.country_en == country]
        opts = "".join('<option value="%s"%s>%s</option>' % (p.slug, " selected" if p.slug == current else "",
                                                             esc(city_name(p, lang))) for p in places)
        groups.append('<optgroup label="%s">%s</optgroup>' % (esc(country_name(places[0], lang)), opts))
    return '<select id="%s" aria-label="%s">%s</select>' % (element_id, esc(T[lang]["choose"]), "".join(groups))


def more_html(lang):
    t = T[lang]
    items = "".join('<li><a href="%s">%s</a>: %s</li>' % (h, esc(n), esc(d)) for h, n, d in t["more"])
    items += '<li><a href="%s/panchang/how-it-works">%s</a></li>' % (prefix(lang), esc(t["methods_link"]))
    return '<section class="card"><h2>%s</h2><ul>%s</ul></section>' % (esc(t["more_h"]), items)


def festival_links_html(lang):
    t = T[lang]
    items = "".join('<li><a href="%s/panchang/%s">%s</a></li>' % (prefix(lang), slug, esc(text))
                    for slug, text in t["festival_pages"])
    countries = " · ".join('<a href="/panchang/%s">%s</a>' % (slug, esc(short)) for slug, _, short, _, _ in COUNTRY_PAGES)
    return '<section class="card"><h2>%s</h2><ul>%s</ul><p>%s %s</p></section>' % (
        esc(t["festival_pages_h"]), items, esc(COUNTRY_LINE[lang]), countries)


# ------------------------------------------------------------------ the country pages (English only)

# one column per main city, the first the reference; a time-zone label where the country has several
COUNTRY_PAGES = [
    ("usa", "United States", "USA", "the USA", [("new-york", "Eastern"), ("chicago", "Central"),
                                                ("denver", "Mountain"), ("los-angeles", "Pacific")]),
    ("canada", "Canada", "Canada", "Canada", [("toronto", "Eastern"), ("winnipeg", "Central"),
                                              ("calgary", "Mountain"), ("vancouver", "Pacific")]),
    ("uk", "United Kingdom", "UK", "the UK", [("london", ""), ("birmingham", ""), ("manchester", ""),
                                              ("glasgow", "")]),
    ("australia", "Australia", "Australia", "Australia", [("sydney", ""), ("melbourne", ""), ("brisbane", ""),
                                                          ("adelaide", ""), ("perth", "")]),
]
COUNTRY_LINE = {"en": "Hindu calendar by country:", "hi": "देश के अनुसार हिन्दू कैलेंडर (अंग्रेज़ी में):"}
COUNTRY_KEYS = ("ekadashi", "ekadashi_vaishnava", "purnima", "amavasya", "sankashti", "pradosh_s", "pradosh_k",
                "shivaratri")
KEY_PAGES = {"makar_sankranti": "makar-sankranti", "maha_shivaratri": "maha-shivratri", "holika_dahan": "holi",
             "holi": "holi", "karwa_chauth": "karwa-chauth", "diwali": "diwali", "ekadashi": "ekadashi",
             "ekadashi_vaishnava": "ekadashi", "sankashti": "sankashti-chaturthi"}


def short_day(d: dt.date) -> str:
    return f"{WEEKDAY_SHORT['en'][d.weekday()]} {d.day} {MONTHS_CIVIL['en'][d.month - 1][:3]}"


def country_page(slug, country, short, in_name, columns, per_city_obs, today, years):
    """The year's festivals and main fasts for a country, dated in each column city; dates that differ from the first
    column in bold. Rows follow the first city; the same observance elsewhere is the one of the same kind and name
    within two days. A Vaishnava Ekadashi row appears when any column city keeps it on another day than the Smarta
    one; a city that keeps both on one day shows its Smarta date there."""
    cities = [per_city_obs[c][0] for c, _ in columns]
    head_cells = ["Festival or fast"] + ["%s%s" % (p.en, " (%s)" % z if z else "") for p, (_, z) in zip(cities, columns)]
    all_obs = [[o for o in per_city_obs[c][2] if o.date >= today - dt.timedelta(days=3)] for c, _ in columns]
    ref_obs = [o for o in all_obs[0] if o.date >= today and o.key != "ekadashi_vaishnava"
               and (o.kind == "festival" or o.key in COUNTRY_KEYS)]

    def find(obs, key, name, near):
        match = [x for x in obs if x.key == key and x.en == name and abs((x.date - near).days) <= 2]
        return min(match, key=lambda x: abs((x.date - near).days)).date if match else None

    def row(name_html, dates):
        first = dates[0]
        cells = []
        for d in dates:
            text = esc(short_day(d)) if d else "-"
            cells.append('<td class="d">%s</td>' % (("<b>%s</b>" % text) if d and d != first else text))
        return "<tr><td>%s</td>%s</tr>" % (name_html, "".join(cells))

    body, month = "", None
    for o in ref_obs:
        if (o.date.year, o.date.month) != month:
            if month:
                body += "</tbody></table></div>"
            month = (o.date.year, o.date.month)
            body += '<h3>%s %d</h3><div class="scroll"><table class="pan"><thead><tr>%s</tr></thead><tbody>' % (
                MONTHS_CIVIL["en"][o.date.month - 1], o.date.year, "".join("<th>%s</th>" % esc(c) for c in head_cells))
        name = esc(obs_name(o, "en"))
        if o.key in KEY_PAGES:
            name = '<a href="/panchang/%s">%s</a>' % (KEY_PAGES[o.key], name)
        smarta = [o.date] + [find(obs, o.key, o.en, o.date) for obs in all_obs[1:]]
        body += row(name, smarta)
        if o.key == "ekadashi":
            vname = "Vaishnava " + o.en
            vaish = [find(obs, "ekadashi_vaishnava", vname, o.date) for obs in all_obs]
            if any(vaish):
                vrow = [v or s for v, s in zip(vaish, smarta)]
                body += row('<a href="/panchang/ekadashi">%s</a>' % esc(vname), vrow)
    if month:
        body += "</tbody></table></div>"
    names = ", ".join(p.en for p in cities[:-1]) + " and " + cities[-1].en
    zones = [z for _, z in columns if z]
    split = (" and sometimes between its time zones" if zones else " and sometimes between its cities")
    title = "Hindu Calendar %s %s: Festivals, Ekadashi, Purnima and Amavasya by %s" % (
        years, short, "Time Zone" if zones else "City")
    description = ("Hindu festivals and fasts in %s, %s: Ekadashi, Purnima, Amavasya and every festival, dated "
                   "for %s." % (in_name, years, names))
    url = SITE + "/panchang/" + slug
    intro = [
        "Hindu festivals and fasts are set by the tithi in force at the time of day each tradition names: sunrise for "
        "most fasts, moonrise for Sankashti, the evening for Diwali and Karwa Chauth, midnight for Maha Shivratri. "
        "The tithi changes at one instant worldwide, but each city meets it at its own hour, so a date in %s can "
        "differ from India's%s." % (in_name, split),
        "The table gives each date for %s, worked out for each city's own sunrise, sunset and moonrise. A date in "
        "bold differs from the first column. Ekadashi is the Smarta date; where the Vaishnava date differs it has its "
        "own row. Every city below has its own page with the times." % names,
    ]
    faq = [
        ("Why is a festival on a different date in %s than in India?" % in_name,
         "The deciding moment, a sunrise, a moonrise or an evening, comes to each city at a different point in the "
         "tithi. When the tithi begins or ends close to that moment, the date moves by a day."),
        ("Which date should I follow if I live between two of these cities?",
         "The nearest city's, or your own city's page if it has one. The date differs between cities only when the "
         "deciding moment falls close to the local sunrise, sunset or moonrise."),
    ]
    city_links = " · ".join('<a href="/panchang/%s">%s</a>' % (p.slug, esc(p.en))
                            for p in CITIES if p.country_en == country)
    return head("en", title, description, url, url, None,
                crumbs("en", (T["en"]["breadcrumb"], SITE + "/panchang"), ("Hindu calendar, " + short, url)),
                faq_ld(faq), CSS, og_type="article") + f"""<body>
{nav_html("en", None, None)}
    <main class="wrap">
        <h1>{esc("Hindu calendar %s for %s" % (years, in_name))}</h1>
        <section class="card">
            {"".join("<p>%s</p>" % esc(p) for p in intro)}
            <p>{city_links}</p>
        </section>
        <section class="card">
            {body}
        </section>
        {AD_ZONE}
        <section class="card">
            <h2>{esc(T["en"]["faq_h"])}</h2>
            {faq_html(faq)}
        </section>
        {AD_ZONE_END}
        {festival_links_html("en")}
        {more_html("en")}
    </main>
{FOOTER}
{INSTALL}</body>
</html>
"""


def table(cols, rows_html, cls="pan"):
    head_html = "".join("<th>%s</th>" % esc(c) for c in cols)
    return '<div class="scroll"><table class="%s"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (cls, head_html, rows_html)


# ------------------------------------------------------------------ observance tables

def moment_text(o, zone, lang) -> str:
    """The deciding moment of an observance, as a short phrase."""
    t = T[lang]
    dd = o.details
    if dd.get("moonrise") is not None:
        return f"{t['moonrise_word']} {clock_dated(dd['moonrise'], zone, o.date, lang)}"
    if o.key == "holika_dahan" and dd.get("light"):
        return holika_text(dd["light"], zone, o.date, lang)
    if dd.get("window"):
        return f"{t['window_word']} {span_text(dd['window'][0], dd['window'][1], zone, o.date, lang)}"
    if dd.get("parana"):
        return f"{t['parana_word']} {span_text(dd['parana'][0], dd['parana'][1], zone, o.date + dt.timedelta(days=1), lang)}"
    if dd.get("sankranti") is not None:
        return f"{t['sankranti_word']} {clock_dated(dd['sankranti'], zone, o.date, lang)}"
    if dd.get("tithi_ends") is not None:
        return f"{t['labels']['tithiEnds']} {clock_dated(dd['tithi_ends'], zone, o.date, lang)}"
    return ""


def year_table(place, lang, obs):
    zone = ZoneInfo(place.tz)
    rows = ""
    for o in obs:
        if o.kind != "festival":
            continue
        rows += '<tr><td class="d">%s</td><td>%s</td><td>%s</td></tr>' % (
            esc(weekday_date(o.date, lang)), esc(obs_name(o, lang)), esc(moment_text(o, zone, lang)))
    return table(T[lang]["cols_year"], rows)


def ekadashi_table(place, lang, obs, year=None):
    zone = ZoneInfo(place.tz)
    rows = ""
    for o in obs:
        if o.key not in ("ekadashi", "ekadashi_vaishnava") or (year and o.date.year != year):
            continue
        p = o.details.get("parana")
        parana = span_text(p[0], p[1], zone, o.date + dt.timedelta(days=1), lang) if p else "-"
        rows += '<tr><td class="d">%s</td><td>%s</td><td>%s</td></tr>' % (
            esc(weekday_date(o.date, lang)), esc(obs_name(o, lang)), esc(parana))
    return table(T[lang]["cols_ekadashi"], rows)


def sankashti_table(place, lang, obs, year=None):
    zone = ZoneInfo(place.tz)
    rows = ""
    for o in obs:
        if o.key != "sankashti" or (year and o.date.year != year):
            continue
        name = obs_name(o, lang) + (" (" + T[lang]["labels"]["angarki"] + ")" if o.details.get("angarki") else "")
        rows += '<tr><td class="d">%s</td><td>%s</td><td>%s</td></tr>' % (
            esc(weekday_date(o.date, lang)), esc(name), esc(clock_dated(o.details.get("moonrise"), zone, o.date, lang)))
    return table(T[lang]["cols_sankashti"], rows)


def month_links(place, lang, first, last, current=None):
    out = []
    for y, m in month_range(first, last):
        label = f"{MONTHS_CIVIL[lang][m - 1]} {y}"
        if (y, m) == current:
            out.append("<b>%s</b>" % esc(label))
        else:
            out.append('<a href="%s/panchang/%s/%04d-%02d">%s</a>' % (prefix(lang), place.slug, y, m, esc(label)))
    return '<p class="months">' + " ".join(out) + "</p>"


# ------------------------------------------------------------------ the city page

def city_page(place, lang, first, last, rows, obs, facts, year):
    t = T[lang]
    zone = ZoneInfo(place.tz)
    city, country = city_name(place, lang), country_name(place, lang)
    kw = dict(city=city, country=country, last=long_date(last, lang), first=long_date(first, lang), year=year)
    url = SITE + prefix(lang) + "/panchang/" + place.slug
    alt_en, alt_hi = SITE + "/panchang/" + place.slug, SITE + "/hi/panchang/" + place.slug
    switch = ("/hi/panchang/" + place.slug, "हिंदी") if lang == "en" else ("/panchang/" + place.slug, "English")
    # the city's own answers for the FAQ
    diwali = next((o for o in obs if o.key == "diwali" and o.date.year == year), None)
    karwa = next((o for o in obs if o.key == "karwa_chauth" and o.date.year == year), None)
    if diwali and diwali.details.get("window"):
        w = diwali.details["window"]
        diwali_a = t["diwali_a"].format(city=city, date=weekday_date(diwali.date, lang),
                                        window=span_text(w[0], w[1], zone, diwali.date, lang))
    else:
        diwali_a = t["unknown_a"].format(city=city, year=year)
    if karwa and karwa.details.get("moonrise") is not None and karwa.details.get("fast"):
        karwa_a = t["karwa_a"].format(city=city, year=year, date=weekday_date(karwa.date, lang),
                                      moonrise=clock(karwa.details["moonrise"], zone),
                                      sunrise=clock(karwa.details["fast"][0], zone))
    else:
        karwa_a = t["unknown_a"].format(city=city, year=year)
    faq_items = [(q.format(**kw), a.format(**kw)) for q, a in t["faq"]]
    faq_items += [(q.format(**kw), a.format(dst=facts["dst"], diwali=diwali_a, karwa=karwa_a)) for q, a in t["faq_city"]]
    data = {"slug": place.slug, "city": city, "tz": place.tz, "lang": lang, "url": url,
            "first": first.isoformat(), "last": last.isoformat(), "data": f"/panchang/data/{place.slug}.json",
            "labels": {k: v.format(**kw) for k, v in t["labels"].items()}, "names": names_for(lang)}
    labels = t["labels"]
    span = f"{short_date(first, lang)} {first.year} – {long_date(last, lang)}" if lang == "en" else \
        f"{short_date(first, lang)} {first.year} – {long_date(last, lang)}"
    # only the English pages of the 30 cities in INDEXED are in search; the rest serve visitors who pick them
    robots = "" if lang == "en" and place.slug in INDEXED else "noindex, follow"
    return head(lang, t["title"].format(**kw), t["description"].format(**kw), url, alt_en, alt_hi,
                crumbs(lang, (t["breadcrumb"], SITE + prefix(lang) + "/panchang"), (city, url)),
                faq_ld(faq_items), CSS, robots=robots) + f"""<body>
{nav_html(lang, None, switch)}
    <main class="wrap">
        <h1>{esc(t["h1"].format(**kw))}</h1>
        <p class="pan-head">{esc(t["sub"].format(**kw))}</p>
        <p class="pan-date" id="panDate">…</p>
        <p class="pan-hindu" id="panHindu"></p>
        <div class="pan-controls">
            {city_select(lang, place.slug)}
            <button type="button" id="todayBtn" class="on">{esc(labels["today"])}</button>
            <label>{esc(labels["pick"])} <input type="date" id="pickDate" min="{first.isoformat()}" max="{last.isoformat()}"></label>
        </div>
        <p id="panNote" class="pan-head" hidden></p>

        <section class="card">
            <div class="pan-two">
                <div>
                    <h2>{esc(labels["sunrise"])} · {esc(labels["moonrise"])}</h2>
                    <dl class="pan-grid" id="panSky"></dl>
                </div>
                <figure class="pan-sky" id="panWheel"></figure>
            </div>
        </section>

        <section class="card">
            <h2>{esc(labels["tithi"])} · {esc(labels["nakshatra"])} · {esc(labels["yoga"])} · {esc(labels["karana"])}</h2>
            <div id="panLimbs"></div>
            <dl class="pan-grid" id="panCal" style="margin-top: 14px;"></dl>
        </section>

        <section class="card">
            <h2>{esc(t["vrat_h"])}</h2>
            <div id="panVrats"></div>
        </section>

        <section class="card spans">
            <div class="pan-two">
                <div><h2>{esc(labels["good"])}</h2><div id="panGood"></div></div>
                <div><h2>{esc(labels["avoid"])}</h2><div id="panAvoid"></div></div>
            </div>
        </section>

        <section class="card">
            <div class="pan-two">
                <div><h2>{esc(labels["day"])}</h2><table class="chogh" id="panChoghDay"></table></div>
                <div><h2>{esc(labels["night"])}</h2><table class="chogh" id="panChoghNight"></table></div>
            </div>
            <div class="actions" style="margin-top: 14px;"><button type="button" class="btn btn-whatsapp" id="panShare">{esc(labels["share"])}</button></div>
        </section>

        <section class="card">
            <h2>{esc(t["year_h"].format(city=city, span=span))}</h2>
            <p>{esc(t["year_intro"].format(**kw))}</p>
            {year_table(place, lang, obs)}
        </section>

        <section class="card">
            <h2>{esc(t["ekadashi_h"].format(**kw))}</h2>
            <p>{esc(t["ekadashi_intro"].format(**kw))}</p>
            {ekadashi_table(place, lang, obs)}
            <h2 style="margin-top: 18px;">{esc(t["sankashti_h"].format(**kw))}</h2>
            <p>{esc(t["sankashti_intro"].format(**kw))}</p>
            {sankashti_table(place, lang, obs)}
        </section>

        <section class="card">
            <h2>{esc(t["months_h"])}</h2>
            <p>{esc(t["months_intro"])}</p>
            {month_links(place, lang, first, last)}
        </section>

        <section class="card">
            <h2>{esc(t["facts_h"].format(**kw))}</h2>
            <p>{esc(facts["facts"])}</p>
            <p>{esc(facts["dst"])} {esc(facts["zone"])}</p>
        </section>

        <section class="card">
            <h2>{esc(t["read_h"])}</h2>
            {paragraphs([t["intro"]] + t["read"], **kw)}
        </section>

        <section class="card">
            <h2>{esc(t["sky_h"])}</h2>
            <p>{esc(t["sky"].format(**kw))}</p>
            <h2 style="margin-top: 18px;">{esc(t["how_h"])}</h2>
            <ul>{"".join("<li>%s</li>" % esc(p) for p in t["how"])}</ul>
            <p><a href="{prefix(lang)}/panchang/how-it-works">{esc(t["methods_link"])}</a></p>
        </section>

        {AD_ZONE}
        <section class="card">
            <h2>{esc(t["faq_h"])}</h2>
            {faq_html(faq_items)}
        </section>
        {AD_ZONE_END}
        {festival_links_html(lang)}
        <section class="card pan-cities">
            <h2>{esc(t["cities_h"])}</h2>
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


# ------------------------------------------------------------------ the monthly page

def month_page(place, lang, year, month, rows, obs, first, last):
    t = MONTH_TEXT[lang]
    zone = ZoneInfo(place.tz)
    city = city_name(place, lang)
    mname = MONTHS_CIVIL[lang][month - 1]
    kw = dict(city=city, month=mname, year=year)
    url = SITE + prefix(lang) + f"/panchang/{place.slug}/{year:04d}-{month:02d}"
    alt_en = SITE + f"/panchang/{place.slug}/{year:04d}-{month:02d}"
    alt_hi = SITE + f"/hi/panchang/{place.slug}/{year:04d}-{month:02d}"
    other = (f"/hi/panchang/{place.slug}/{year:04d}-{month:02d}", "हिंदी") if lang == "en" else \
        (f"/panchang/{place.slug}/{year:04d}-{month:02d}", "English")
    month_rows = [r for r in rows if r["d"][:7] == f"{year:04d}-{month:02d}"]
    lunar = []
    for r in month_rows:
        name = (names.ADHIKA[lang] if r["pa"] else "") + names.MONTH[lang][r["pm"]]
        if name not in lunar:
            lunar.append(name)
    rahu = {6: 8, 0: 2, 1: 7, 2: 5, 3: 6, 4: 4, 5: 3}
    body = ""
    for r in month_rows:
        date = dt.date.fromisoformat(r["d"])
        ti, te = r["t"][0]
        ni, ne = r["n"][0]
        tithi = names.TITHI[lang][ti] + (f" ({T[lang]['labels']['till']} {clock_dated(te, zone, date, lang)})" if te else "")
        nak = names.NAKSHATRA[lang][ni] + (f" ({T[lang]['labels']['till']} {clock_dated(ne, zone, date, lang)})" if ne else "")
        seg = rahu[r["w"]]
        d8 = (r["ss"] - r["sr"]) / 8
        rk = span_text(r["sr"] + d8 * (seg - 1), r["sr"] + d8 * seg, zone, date, lang)
        body += '<tr><td class="d">%s %s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
            date.day, WEEKDAY_SHORT[lang][r["w"]], esc(tithi), esc(nak), clock(r["sr"], zone), clock(r["ss"], zone),
            esc(clock_dated(r["mr"], zone, date, lang)) if r["mr"] else "-", esc(rk))
    month_obs = [o for o in obs if o.date.year == year and o.date.month == month]
    vrat_rows = "".join('<tr><td class="d">%s</td><td>%s</td><td>%s</td></tr>' % (
        esc(weekday_date(o.date, lang)), esc(obs_name(o, lang)), esc(moment_text(o, zone, lang))) for o in month_obs)
    vrats_html = table(T[lang]["cols_year"], vrat_rows) if month_obs else "<p>%s</p>" % esc(t["none"])
    months = list(month_range(first, last))
    i = months.index((year, month))
    nav = []
    if i > 0:
        py, pm = months[i - 1]
        nav.append('<a href="%s/panchang/%s/%04d-%02d">← %s</a>' % (prefix(lang), place.slug, py, pm, esc(t["prev"])))
    nav.append('<a href="%s/panchang/%s">%s</a>' % (prefix(lang), place.slug, esc(t["today"].format(**kw))))
    if i + 1 < len(months):
        ny, nm = months[i + 1]
        nav.append('<a href="%s/panchang/%s/%04d-%02d">%s →</a>' % (prefix(lang), place.slug, ny, nm, esc(t["next"])))
    faq = [(q.format(**kw), a.format(**kw)) for q, a in t["faq"]]
    joiner = " and " if lang == "en" else " और "
    return head(lang, t["title"].format(**kw), t["description"].format(**kw), url, alt_en, alt_hi,
                crumbs(lang, (T[lang]["breadcrumb"], SITE + prefix(lang) + "/panchang"),
                       (city, SITE + prefix(lang) + "/panchang/" + place.slug), (f"{mname} {year}", url)),
                # kept out of search (owner, 15 Nov 2026): 2,044 month pages share their text across cities, and
                # many near-identical pages risk the whole site's standing; visitors still reach them from the city
                # page, and "follow" keeps their links counted. update_sitemap leaves noindex pages out.
                faq_ld(faq), CSS, robots="noindex, follow") + f"""<body>
{nav_html(lang, None, other)}
    <main class="wrap">
        <h1>{esc(t["h1"].format(**kw))}</h1>
        <p class="pan-head">{esc(country_name(place, lang))} · {esc(T[lang]["sub"].format(city=city, country=country_name(place, lang)).split("·")[-1].strip())}</p>
        <p class="pan-head months">{" · ".join(nav)}</p>
        <section class="card">
            <p>{esc(t["intro"].format(lunar=joiner.join(lunar), **kw))}</p>
            {table(t["cols"], body)}
        </section>
        <section class="card">
            <h2>{esc(t["vrats_h"].format(**kw))}</h2>
            {vrats_html}
        </section>
        <section class="card">
            <h2>{esc(T[lang]["months_h"])}</h2>
            {month_links(place, lang, first, last, current=(year, month))}
        </section>
        <section class="card">
            <h2>{esc(T[lang]["faq_h"])}</h2>
            {faq_html(faq)}
        </section>
        {festival_links_html(lang)}
        {more_html(lang)}
    </main>
{FOOTER}
{INSTALL}</body>
</html>
"""


# ------------------------------------------------------------------ the festival pages

# the festival pages that list every city by country, one occurrence each, with the words of their at-a-glance box
COUNTRY_TABLES = ("makar_sankranti", "maha_shivaratri", "holi", "karwa_chauth", "diwali")
GLANCE = {
    "en": {"h": "The date at a glance", "all": "in every city listed", "of": "in {k} of {n} cities",
           "more": "and {m} more", "after_bhadra": "after Bhadra, from {t}",
           "past_midnight": "Bhadra lasts past midnight: your temple's time", "holika": "Holika Dahan", "holi": "Holi"},
    "hi": {"h": "एक नज़र में तारीख", "all": "सूची के सभी शहरों में", "of": "{n} में से {k} शहरों में",
           "more": "और {m} अन्य", "after_bhadra": "भद्रा के बाद, {t} से",
           "past_midnight": "भद्रा आधी रात के बाद तक: अपने मंदिर का समय", "holika": "होलिका दहन", "holi": "होली"},
}


def holika_light(dd):
    """When to light the Holika fire: ("window", a, b) in pradosh kaal once Bhadra is over, ("after", b) when Bhadra
    ends after pradosh but before midnight, ("temple", None) when it lasts past midnight, where practice varies."""
    w, b, mid = dd.get("window"), dd.get("bhadra_ends"), dd.get("night_mid")
    if not w:
        return None
    if b is None or b <= w[0]:
        return ("window", w[0], w[1])
    if b < w[1]:
        return ("window", b, w[1])
    if mid is None or b < mid:
        return ("after", b)
    return ("temple", None)


def holika_text(light, zone, date, lang):
    if light[0] == "window":
        return f"{T[lang]['window_word']} {span_text(light[1], light[2], zone, date, lang)}"
    if light[0] == "after":
        return GLANCE[lang]["after_bhadra"].format(t=clock_dated(light[1], zone, date, lang))
    return GLANCE[lang]["past_midnight"]


def glance_html(per_city, lang, key=""):
    """One line per country: the date in most of its cities, and any city where it differs, answer first. For Holi
    the date is Holika Dahan's, and both days are named."""
    g = GLANCE[lang]

    def day(d):
        if key == "holi":
            return "%s %s, %s %s" % (g["holika"], weekday_date(d, lang), g["holi"],
                                     weekday_date(d + dt.timedelta(days=1), lang))
        return weekday_date(d, lang)
    out = []
    for country in COUNTRY_ORDER:
        dates: dict = {}
        for place in CITIES:
            if place.country_en == country and place.slug in per_city:
                dates.setdefault(per_city[place.slug][2][0].date, []).append(city_name(place, lang))
        if not dates:
            continue
        n = sum(len(v) for v in dates.values())
        ordered = sorted(dates.items(), key=lambda kv: (-len(kv[1]), kv[0]))
        main_date, main_cities = ordered[0]
        if len(ordered) == 1:
            text = "%s %s" % (day(main_date), g["all"] if n > 1 else "")
        else:
            parts = ["%s %s" % (day(main_date), g["of"].format(k=len(main_cities), n=n))]
            for d, cities in ordered[1:]:
                shown = cities[:5] + ([g["more"].format(m=len(cities) - 5)] if len(cities) > 5 else [])
                parts.append("%s: %s" % (day(d), ", ".join(shown)))
            text = "; ".join(parts)
        place0 = next(p for p in CITIES if p.country_en == country)
        out.append("<li><b>%s:</b> %s</li>" % (esc(country_name(place0, lang)), esc(text.strip())))
    return '<section class="card"><h2>%s</h2><ul>%s</ul></section>' % (esc(g["h"]), "".join(out))


def festival_row(key, o, zone, lang, link):
    """One city's row of a country table."""
    dd = o.details
    L = T[lang]["labels"]
    cell = '<td>%s</td>'
    if key == "karwa_chauth":
        fast = span_text(dd["fast"][0], dd["fast"][1], zone, o.date, lang) if dd.get("fast") else "-"
        cells = [esc(clock_dated(dd.get("moonrise"), zone, o.date, lang)), esc(fast),
                 esc(L["tithiEnds"] + " " + clock_dated(dd.get("tithi_ends"), zone, o.date, lang))]
    elif key == "diwali":
        w = dd.get("window")
        cells = [esc(span_text(w[0], w[1], zone, o.date, lang) if w else "-"),
                 esc(L["tithiEnds"] + " " + clock_dated(dd.get("tithi_ends"), zone, o.date, lang))]
    elif key == "makar_sankranti":
        cells = [esc(clock_dated(dd.get("sankranti"), zone, o.date, lang)),
                 esc(weekday_date(o.date - dt.timedelta(days=1), lang))]
    elif key == "maha_shivaratri":
        w = dd.get("window")
        cells = [esc(span_text(w[0], w[1], zone, o.date, lang) if w else "-"),
                 esc(clock_dated(dd.get("tithi_ends"), zone, o.date, lang))]
    else:  # holi: the row is Holika Dahan's, and Holi is the day after
        light = dd.get("light")
        text = span_text(light[1], light[2], zone, o.date, lang) if light and light[0] == "window" else \
            (holika_text(light, zone, o.date, lang) if light else "-")
        cells = [esc(text), esc(clock_dated(dd.get("bhadra_ends"), zone, o.date, lang)),
                 esc(weekday_date(o.date + dt.timedelta(days=1), lang))]
    return '<tr><td>%s</td><td class="d">%s</td>%s</tr>' % (link, esc(weekday_date(o.date, lang)),
                                                           "".join(cell % c for c in cells))


def festival_page(key, lang, year, per_city):
    """per_city: slug -> (place, zone, [observances of that key]): for the country tables the next occurrence in
    each city, for the Ekadashi and Sankashti lists every one still to come. The address is permanent; the year is
    in the title."""
    f = FESTIVALS[key]
    t = f[lang]
    slug = f["slug"]
    n = len(per_city)
    kw = dict(year=year, n=n, example_city=EXAMPLE_CITY[lang])
    url = SITE + prefix(lang) + "/panchang/" + slug
    alt_en, alt_hi = SITE + "/panchang/" + slug, SITE + "/hi/panchang/" + slug
    other = ("/hi/panchang/" + slug, "हिंदी") if lang == "en" else ("/panchang/" + slug, "English")
    L = T[lang]["labels"]
    sections = ""
    glance = ""
    if key in COUNTRY_TABLES:
        glance = glance_html(per_city, lang, key)
        for country in COUNTRY_ORDER:
            rows = ""
            for place in CITIES:
                if place.country_en != country or place.slug not in per_city:
                    continue
                _, zone, items = per_city[place.slug]
                link = '<a href="%s/panchang/%s">%s</a>' % (prefix(lang), place.slug, esc(city_name(place, lang)))
                rows += "".join(festival_row(key, o, zone, lang, link) for o in items)
            if rows:
                head_country = country_name(next(p for p in CITIES if p.country_en == country), lang)
                sections += "<h3>%s</h3>%s" % (esc(head_country), table(t["cols"], rows))
        chooser = ""
    else:
        others_links = []
        for slug_city in MAIN_CITIES + [p.slug for p in CITIES if p.slug not in MAIN_CITIES]:
            if slug_city not in per_city:
                continue
            place, zone, items = per_city[slug_city]
            if key == "sankashti":
                rows = "".join('<tr><td class="d">%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
                    esc(weekday_date(o.date, lang)),
                    esc(obs_name(o, lang) + (" (" + L["angarki"] + ")" if o.details.get("angarki") else "")),
                    esc(clock_dated(o.details.get("moonrise"), zone, o.date, lang)),
                    esc(clock_dated(o.details.get("tithi_ends"), zone, o.date, lang))) for o in items)
            else:
                rows = ""
                for o in items:
                    p = o.details.get("parana")
                    rows += '<tr><td class="d">%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
                        esc(weekday_date(o.date, lang)), esc(obs_name(o, lang)),
                        esc(span_text(p[0], p[1], zone, o.date + dt.timedelta(days=1), lang) if p else "-"),
                        esc(clock_dated(o.details.get("dwadashi_ends"), zone, o.date + dt.timedelta(days=1), lang)))
            # the main cities carry their full list here; every other city links to its own page, which has the list
            is_main = slug_city in MAIN_CITIES
            link = '<p><a href="%s/panchang/%s">%s</a></p>' % (prefix(lang), slug_city,
                                                               esc(T[lang]["h1"].format(city=city_name(place, lang))))
            if is_main:
                sections += '<details class="pan"%s><summary>%s, %s</summary>%s%s</details>' % (
                    " open" if slug_city == MAIN_CITIES[0] else "", esc(city_name(place, lang)),
                    esc(country_name(place, lang)), table(t["cols"], rows), link)
            else:
                others_links.append('<a href="%s/panchang/%s">%s</a>' % (prefix(lang), slug_city, esc(city_name(place, lang))))
        if others_links:
            sections += '<h3>%s</h3><p class="months">%s</p>' % (esc(T[lang]["cities_h"]), " · ".join(others_links))
        chooser = ""
    faq = [(q.format(**kw), a.format(**kw)) for q, a in t["faq"]]
    return head(lang, t["title"].format(**kw), t["description"].format(**kw), url, alt_en, alt_hi,
                crumbs(lang, (T[lang]["breadcrumb"], SITE + prefix(lang) + "/panchang"), (t["h1"].format(**kw), url)),
                faq_ld(faq), CSS, og_type="article") + f"""<body>
{nav_html(lang, None, other)}
    <main class="wrap">
        <h1>{esc(t["h1"].format(**kw))}</h1>
        {glance}
        <section class="card">
            {paragraphs(t["intro"], **kw)}
        </section>
        <section class="card">
            {chooser}
            {sections}
            <p style="margin-top: 12px; color: #666; font-size: 14px;">{esc(t["note"])}</p>
        </section>
        {AD_ZONE}
        <section class="card">
            <h2>{esc(T[lang]["faq_h"])}</h2>
            {faq_html(faq)}
        </section>
        {AD_ZONE_END}
        {festival_links_html(lang)}
        {more_html(lang)}
    </main>
{FOOTER}
{INSTALL}</body>
</html>
"""


# ------------------------------------------------------------------ the methods page

def methods_page(lang):
    t = METHODS[lang]
    url = SITE + prefix(lang) + "/panchang/how-it-works"
    other = ("/hi/panchang/how-it-works", "हिंदी") if lang == "en" else ("/panchang/how-it-works", "English")
    body = ""
    for heading, paras in t["sections"]:
        body += '<section class="card"><h2>%s</h2>%s</section>' % (esc(heading), "".join("<p>%s</p>" % esc(p) for p in paras))
    return head(lang, t["title"], t["description"], url, SITE + "/panchang/how-it-works", SITE + "/hi/panchang/how-it-works",
                crumbs(lang, (T[lang]["breadcrumb"], SITE + prefix(lang) + "/panchang"), (t["h1"], url)),
                {"@context": "https://schema.org", "@type": "Article", "headline": t["title"], "inLanguage": lang,
                 "author": {"@type": "Organization", "name": "Ved Prashnavali"}}, CSS, og_type="article") + f"""<body>
{nav_html(lang, None, other)}
    <main class="wrap">
        <h1>{esc(t["h1"])}</h1>
        {AD_ZONE}{body}{AD_ZONE_END}
        {festival_links_html(lang)}
        {more_html(lang)}
    </main>
{FOOTER}
{INSTALL}</body>
</html>
"""


# ------------------------------------------------------------------ the index page

def index_page(lang, last):
    t = T[lang]
    kw = dict(last=long_date(last, lang))
    url = SITE + prefix(lang) + "/panchang"
    alt_en, alt_hi = SITE + "/panchang", SITE + "/hi/panchang"
    switch = ("/hi/panchang", "हिंदी") if lang == "en" else ("/panchang", "English")
    generic = [(q, a) for q, a in t["faq"] if "{city}" not in q + a]
    city_names = {p.slug: city_name(p, lang) for p in CITIES}
    return head(lang, t["index_title"], t["index_description"], url, alt_en, alt_hi,
                crumbs(lang, (t["breadcrumb"], url)), faq_ld(generic), CSS) + f"""<body>
{nav_html(lang, None, switch)}
    <main class="wrap">
        <h1>{esc(t["index_h1"])}</h1>
        <p class="pan-head" id="remembered" hidden><a href="#" id="rememberedLink"></a></p>
        <section class="card">
            {paragraphs(t["index_intro"], **kw)}
        </section>
        <section class="card pan-cities">
            <h2>{esc(t["choose"])}</h2>
            {cities_list(lang)}
        </section>
        {festival_links_html(lang)}
        {AD_ZONE}
        <section class="card">
            <h2>{esc(t["how_h"])}</h2>
            <ul>{"".join("<li>%s</li>" % esc(p) for p in t["how"])}</ul>
            <p><a href="{prefix(lang)}/panchang/how-it-works">{esc(t["methods_link"])}</a></p>
        </section>
        <section class="card">
            <h2>{esc(t["faq_h"])}</h2>
            {faq_html(generic)}
        </section>
        {AD_ZONE_END}
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
            a.href = '{prefix(lang)}/panchang/' + slug;
            a.textContent = {json.dumps(t["remembered"], ensure_ascii=False)}.replace('{{city}}', names[slug]);
            document.getElementById('remembered').hidden = false;
        }}
    }})();
    </script>
{INSTALL}</body>
</html>
"""


# ------------------------------------------------------------------ markdown copies

def markdown(place, lang, first, last, obs, facts):
    t = T[lang]
    zone = ZoneInfo(place.tz)
    kw = dict(city=city_name(place, lang), country=country_name(place, lang), last=long_date(last, lang),
              first=long_date(first, lang), year=last.year)
    url = SITE + prefix(lang) + "/panchang/" + place.slug
    lines = ["# " + t["title"].format(**kw), "", "Source: " + url, "", t["intro"].format(**kw), "", t["md_note"], "",
             facts["facts"], "", facts["dst"] + " " + facts["zone"], "",
             "## " + t["year_h"].format(city=kw["city"], span=f"{long_date(first, lang)} – {long_date(last, lang)}"), ""]
    for o in obs:
        if o.kind == "festival":
            lines.append(f"- {weekday_date(o.date, lang)}: {obs_name(o, lang)}" + (f" ({moment_text(o, zone, lang)})" if moment_text(o, zone, lang) else ""))
    lines += ["", "## " + t["read_h"], ""]
    for p in t["read"]:
        lines += [p, ""]
    lines += ["## " + t["how_h"], ""] + ["- " + p for p in t["how"]] + ["", "## " + t["faq_h"], ""]
    for q, a in t["faq"]:
        lines += ["### " + q.format(**kw), "", a.format(**kw), ""]
    return "\n".join(lines)


def index_markdown(lang, last):
    t = T[lang]
    kw = dict(last=long_date(last, lang))
    url = SITE + prefix(lang) + "/panchang"
    lines = ["# " + t["index_title"], "", "Source: " + url, ""]
    for p in t["index_intro"]:
        lines += [p.format(**kw), ""]
    lines += ["## " + t["choose"], ""]
    for p in CITIES:
        lines.append("- [%s](%s/panchang/%s)" % (city_name(p, lang), SITE + prefix(lang), p.slug))
    lines += ["", "## " + t["festival_pages_h"], ""]
    for slug, text in t["festival_pages"]:
        lines.append("- [%s](%s/panchang/%s)" % (text, SITE + prefix(lang), slug))
    lines += ["", "## " + t["how_h"], ""] + ["- " + p for p in t["how"]] + [""]
    return "\n".join(lines)


# ------------------------------------------------------------------ main

def zone_offsets(tz: str, first: dt.date, last: dt.date):
    """[[utc_epoch, offset_seconds], ...]: the city's UTC offset from each instant on, over the data's span and a
    margin. The edge function (functions/panchang/[slug].js) uses it to show local times without Intl, which costs
    more than the free plan's CPU allowance on a cold start; tools/check_edge.mjs proves it agrees with Intl."""
    zone = ZoneInfo(tz)
    utc = dt.timezone.utc
    t = int(dt.datetime.combine(first - dt.timedelta(days=2), dt.time(), utc).timestamp())
    end = int(dt.datetime.combine(last + dt.timedelta(days=3), dt.time(), utc).timestamp())

    def off(s):
        return int((dt.datetime.fromtimestamp(s, zone).utcoffset() or dt.timedelta(0)).total_seconds())

    out = [[t, off(t)]]
    while t < end:
        nxt = t + 3600
        if off(nxt) != out[-1][1]:
            lo, hi = t, nxt                         # the change lies in (lo, hi]: narrow it to the second
            while hi - lo > 1:
                mid = (lo + hi) // 2
                if off(mid) == out[-1][1]:
                    lo = mid
                else:
                    hi = mid
            out.append([hi, off(hi)])
        t = nxt
    return out


def bhadra_end(rows, begin, end):
    """When Bhadra ends on a Purnima: the end of Vishti karana, the first half of the tithi (half-tithi index 28)."""
    for r in rows:
        for index, finish in r["k"]:
            if index == 28 and finish is not None and begin < finish <= end:
                return finish
    return None


def build(first: dt.date, last: dt.date, only=None, today: dt.date | None = None):
    today = today or dt.date.today()
    places = [p for p in CITIES if not only or p.slug in only]
    sky_holder: dict = {}
    sky_json = None
    written, entries = [], []
    year = last.year
    data_dir = ROOT / "panchang" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    per_city_obs = {}
    for place in places:
        payload = city_rows(place, first, last, sky_holder)
        if sky_json is None:
            sky_json = vrats.sky_cache(first, last)
        alm = vrats.Almanac(sky_json, payload["events"], place.tz)
        obs = vrats.observances(alm, first, last)
        per_city_obs[place.slug] = (place, ZoneInfo(place.tz), obs)
        rows = payload["rows"]
        for o in obs:
            if o.key == "holika_dahan":
                o.details["bhadra_ends"] = bhadra_end(rows, o.details["tithi_begins"], o.details["tithi_ends"])
                day = next((r for r in rows if r["d"] == o.date.isoformat()), None)
                if day and day["nsr"]:
                    o.details["night_mid"] = day["ss"] + (day["nsr"] - day["ss"]) / 2
                # one decision for every page: the Holi page, the city's festival table and its card (the window
                # the card reads is the one after Bhadra, or none when the time is not a pradosh window)
                o.details["light"] = holika_light(o.details)
                if o.details["light"] and o.details["light"][0] == "window":
                    o.details["window"] = (int(o.details["light"][1]), int(o.details["light"][2]))
                else:
                    o.details.pop("window", None)
        base, rel_rows = relativize(rows)
        data = {"slug": place.slug, "tz": place.tz, "first": first.isoformat(), "last": last.isoformat(),
                "base": base, "rows": rel_rows, "vrats": encode_vrats(obs, base),
                "zoff": zone_offsets(place.tz, first, last)}
        (data_dir / f"{place.slug}.json").write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")),
                                                     encoding="utf-8")
        for lang in ("en", "hi"):
            facts = city_facts(place, rows, lang, year)
            folder = ROOT / ("panchang" if lang == "en" else "hi/panchang")
            (folder / place.slug).mkdir(parents=True, exist_ok=True)
            (folder / f"{place.slug}.html").write_text(city_page(place, lang, first, last, rows, obs, facts, year), encoding="utf-8")
            (folder / f"{place.slug}.md").write_text(markdown(place, lang, first, last, obs, facts), encoding="utf-8")
            written.append(str((folder / f"{place.slug}.html").relative_to(ROOT)))
            entries.append((SITE + prefix(lang) + "/panchang/" + place.slug, "daily", "0.8"))
            for y, m in month_range(first, last):
                (folder / place.slug / f"{y:04d}-{m:02d}.html").write_text(
                    month_page(place, lang, y, m, rows, obs, first, last), encoding="utf-8")
                written.append(str((folder / place.slug / f"{y:04d}-{m:02d}.html").relative_to(ROOT)))
                entries.append((SITE + prefix(lang) + f"/panchang/{place.slug}/{y:04d}-{m:02d}", "monthly", "0.6"))
    # the festival pages, on permanent addresses since 15 Nov 2026: the next occurrence on or after `today` in each
    # city (Ekadashi and Sankashti: every one still to come), the year of it in the title
    keys = {"makar_sankranti": ("makar_sankranti",), "maha_shivaratri": ("maha_shivaratri",), "holi": ("holika_dahan",),
            "karwa_chauth": ("karwa_chauth",), "diwali": ("diwali",), "sankashti": ("sankashti",),
            "ekadashi": ("ekadashi", "ekadashi_vaishnava")}
    for key, wanted in keys.items():
        per_city = {}
        for slug, (place, zone, obs) in per_city_obs.items():
            items = [o for o in obs if o.key in wanted and o.date >= today]
            if items and key in COUNTRY_TABLES:
                items = items[:1]
            if items:
                per_city[slug] = (place, zone, items)
        if not per_city:
            continue
        years = sorted(o.date.year for _, _, items in per_city.values() for o in items)
        if key in COUNTRY_TABLES:
            y = max(set(years), key=years.count)
        else:  # the lists run from today, so they can span two years: "2026–2027"
            y = f"{years[0]}–{years[-1]}" if years[0] != years[-1] else years[0]
        for lang in ("en", "hi"):
            folder = ROOT / ("panchang" if lang == "en" else "hi/panchang")
            fslug = FESTIVALS[key]["slug"]
            (folder / f"{fslug}.html").write_text(festival_page(key, lang, y, per_city), encoding="utf-8")
            written.append(str((folder / f"{fslug}.html").relative_to(ROOT)))
            entries.append((SITE + prefix(lang) + "/panchang/" + fslug, "yearly", "0.8"))
    # the small files the block after a prashnavali answer reads: each city's coming fasts and festivals, worded as
    # on the city page, and a map from a browser's time zone to a city (the first city listed in that zone)
    next_dir = ROOT / "panchang" / "data" / "next"
    next_dir.mkdir(parents=True, exist_ok=True)
    zones = {}
    for slug, (place, zone, obs) in per_city_obs.items():
        zones.setdefault(place.tz, slug)
        items = []
        for o in obs:
            if o.date < today or not (o.kind == "festival" or o.key in COUNTRY_KEYS) or o.key == "ekadashi_vaishnava":
                continue
            items.append({"d": o.date.isoformat(), "en": o.en, "hi": o.hi, "ten": moment_text(o, zone, "en"),
                          "thi": moment_text(o, zone, "hi"), "p": KEY_PAGES.get(o.key, "")})
        (next_dir / f"{slug}.json").write_text(json.dumps({"slug": slug, "en": place.en, "hi": place.hi, "tz": place.tz,
                                                           "items": items}, ensure_ascii=False, separators=(",", ":")),
                                               encoding="utf-8")
    if not only:
        # names some browsers still report for these zones (Chrome long gave India as Asia/Calcutta)
        for old, new in (("Asia/Calcutta", "Asia/Kolkata"), ("America/Montreal", "America/Toronto")):
            if new in zones:
                zones[old] = zones[new]
        (next_dir / "zones.json").write_text(json.dumps(zones, separators=(",", ":")), encoding="utf-8")
    # the country pages, English only, from today to the end of the data
    if not only:
        span_years = f"{today.year}–{last.year}" if today.year != last.year else str(last.year)
        for slug, country, short, in_name, columns in COUNTRY_PAGES:
            path = ROOT / "panchang" / f"{slug}.html"
            path.write_text(country_page(slug, country, short, in_name, columns, per_city_obs, today, span_years),
                            encoding="utf-8")
            written.append(str(path.relative_to(ROOT)))
            entries.append((SITE + "/panchang/" + slug, "monthly", "0.8"))
    for lang in ("en", "hi"):
        folder = ROOT / ("panchang" if lang == "en" else "hi/panchang")
        (folder / "how-it-works.html").write_text(methods_page(lang), encoding="utf-8")
        written.append(str((folder / "how-it-works.html").relative_to(ROOT)))
        entries.append((SITE + prefix(lang) + "/panchang/how-it-works", "yearly", "0.6"))
        root_folder = ROOT if lang == "en" else ROOT / "hi"
        (root_folder / "panchang.html").write_text(index_page(lang, last), encoding="utf-8")
        (root_folder / "panchang.md").write_text(index_markdown(lang, last), encoding="utf-8")
        written.append(str((root_folder / "panchang.html").relative_to(ROOT)))
        entries.insert(0, (SITE + prefix(lang) + "/panchang", "daily", "0.9"))
    # the sitemap: new pages added with these frequencies and priorities, every date moved to the page's last change
    report = update_sitemap.update(hints={url: (freq, prio) for url, freq, prio in entries})
    return written, report


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    today = dt.date.today()
    ap.add_argument("--first", default=today.isoformat())
    ap.add_argument("--last", default=dt.date(today.year + 1, 12, 31).isoformat())
    ap.add_argument("--only", nargs="*", help="city slugs, for a quick run")
    ap.add_argument("--today", default=today.isoformat(), help="the day the festival pages count from")
    a = ap.parse_args()
    pages, report = build(dt.date.fromisoformat(a.first), dt.date.fromisoformat(a.last), a.only,
                          dt.date.fromisoformat(a.today))
    print(f"{len(pages)} pages; sitemap: {update_sitemap.describe(report)}")
