"""The words of the festival pages, the monthly pages and the methods page, in English and Hindi. Pure data."""

FESTIVALS = {
    "karwa_chauth": {
        "slug": "karwa-chauth",
        "en": {
            "title": "Karwa Chauth {year}: Date and Moonrise Time by City (USA, Canada, UK, Australia, India)",
            "h1": "Karwa Chauth {year}: date and moonrise time in your city",
            "description": "Karwa Chauth {year} falls on different dates in different cities. The date, the moonrise and the "
                           "fasting hours for {n} cities in India, the United States, Canada, the United Kingdom, Australia and "
                           "beyond, each worked out for its own sky.",
            "intro": [
                "Karwa Chauth is kept on Kartika Krishna Chaturthi, and the fast is broken only when the moon is seen. The "
                "rule the panchangs follow is that the fast falls on the day Chaturthi is in force at moonrise. Because "
                "Chaturthi begins and ends at one instant worldwide but moonrise is local, the date can differ by a day "
                "between India and a city abroad, and the moonrise time differs everywhere.",
                "The table gives, for each city, the day of the fast, the moonrise that evening, and the fasting hours from "
                "sunrise to moonrise. All times are the city's own local time, with daylight saving allowed for.",
            ],
            "cols": ["City", "Karwa Chauth", "Moonrise", "Fast from sunrise", "Chaturthi"],
            "note": "Where the Chaturthi tithi is in force at neither evening's moonrise, the fast is kept on the later of the "
                    "two days, as the North Indian panchangs do.",
            "faq": [
                ("Why is Karwa Chauth on a different date in {example_city} than in India?",
                 "Because the fast is tied to the local moonrise. The Chaturthi tithi runs for the same stretch of time "
                 "everywhere, but in a city many hours west of India the evening falls earlier in that stretch, so the "
                 "tithi may still be in force at moonrise a day later or earlier than in Delhi."),
                ("When can I break the fast?",
                 "After the moonrise time given for your city, once the moon is actually seen. Clouds do not move the "
                 "time; the moon is up whether or not it is visible."),
                ("Which moonrise time is this?",
                 "The moment the centre of the Moon's disc crosses the horizon as seen from the city centre, computed from "
                 "the JPL ephemeris. A high horizon or tall buildings can delay the sighting by some minutes."),
            ],
        },
        "hi": {
            "title": "करवा चौथ {year}: तारीख और चंद्रोदय का समय, शहर के अनुसार (अमेरिका, कनाडा, ब्रिटेन, ऑस्ट्रेलिया, भारत)",
            "h1": "करवा चौथ {year}: आपके शहर में तारीख और चंद्रोदय का समय",
            "description": "करवा चौथ {year} अलग-अलग शहरों में अलग तारीख को पड़ता है। भारत, अमेरिका, कनाडा, ब्रिटेन, ऑस्ट्रेलिया "
                           "और अन्य देशों के {n} शहरों के लिए तारीख, चंद्रोदय और व्रत के घंटे, हर शहर के अपने आकाश के अनुसार।",
            "intro": [
                "करवा चौथ कार्तिक कृष्ण चतुर्थी को रखा जाता है और व्रत चंद्र दर्शन के बाद ही खोला जाता है। पंचांगों का नियम है कि "
                "व्रत उस दिन होता है जिस दिन चंद्रोदय के समय चतुर्थी तिथि चल रही हो। चतुर्थी पूरे संसार में एक ही क्षण आरंभ और समाप्त "
                "होती है, पर चंद्रोदय स्थानीय है; इसलिए भारत और विदेश के किसी शहर में तारीख एक दिन अलग हो सकती है, और चंद्रोदय का "
                "समय हर जगह अलग होता है।",
                "तालिका हर शहर के लिए व्रत का दिन, उस शाम का चंद्रोदय और सूर्योदय से चंद्रोदय तक के व्रत के घंटे देती है। सभी समय "
                "शहर के अपने स्थानीय समय में हैं, डेलाइट सेविंग सहित।",
            ],
            "cols": ["शहर", "करवा चौथ", "चंद्रोदय", "व्रत सूर्योदय से", "चतुर्थी"],
            "note": "जहाँ चतुर्थी तिथि किसी भी शाम के चंद्रोदय पर नहीं होती, वहाँ व्रत दोनों में से बाद के दिन रखा जाता है, जैसा उत्तर "
                    "भारत के पंचांग करते हैं।",
            "faq": [
                ("{example_city} में करवा चौथ भारत से अलग तारीख को क्यों है?",
                 "क्योंकि व्रत स्थानीय चंद्रोदय से जुड़ा है। चतुर्थी तिथि हर जगह एक ही समय-खंड में चलती है, पर भारत से कई घंटे "
                 "पश्चिम के शहर में शाम उस खंड में पहले पड़ती है, इसलिए वहाँ चंद्रोदय पर तिथि दिल्ली से एक दिन बाद या पहले चल रही "
                 "हो सकती है।"),
                ("व्रत कब खोलें?",
                 "अपने शहर के लिए दिए चंद्रोदय समय के बाद, चंद्र दर्शन होने पर। बादल समय नहीं बदलते; चंद्र दिखे या न दिखे, वह उग "
                 "चुका होता है।"),
                ("यह चंद्रोदय का कौन-सा समय है?",
                 "वह क्षण जब चंद्र बिंब का केंद्र शहर के केंद्र से देखे गए क्षितिज को पार करता है, JPL ग्रह-पंचांग से निकाला गया। ऊँचा "
                 "क्षितिज या ऊँची इमारतें दर्शन को कुछ मिनट टाल सकती हैं।"),
            ],
        },
    },
    "diwali": {
        "slug": "diwali",
        "en": {
            "title": "Diwali {year}: Date and Lakshmi Puja Time by City (USA, Canada, UK, Australia, India)",
            "h1": "Diwali {year}: date and Lakshmi Puja time in your city",
            "description": "Diwali {year}: the Lakshmi Puja date and the pradosh puja window for {n} cities in India, the United "
                           "States, Canada, the United Kingdom, Australia and beyond, each in its own local time.",
            "intro": [
                "Lakshmi Puja is performed on the Amavasya of Kartika during pradosh kaal, the first three muhurtas after "
                "sunset. The day is the one on which Amavasya is in force in that evening window. Amavasya begins and ends "
                "at the same instant everywhere, but sunset is local, so the date can shift by a day between continents.",
                "The table gives, for each city, the day of Lakshmi Puja and the puja window: the part of that evening's "
                "pradosh kaal during which Amavasya is in force. All times are local, with daylight saving allowed for.",
            ],
            "cols": ["City", "Lakshmi Puja", "Puja window", "Amavasya"],
            "note": "Where Amavasya is in force in the evening window on both days, the day on which it covers more of the "
                    "window is taken; where on neither, the day of Amavasya at sunrise.",
            "faq": [
                ("Why is Diwali on a different date in {example_city} than in India?",
                 "The puja belongs to the evening, and the evening comes to each city at a different point in the Amavasya "
                 "tithi. When the tithi begins after sunset in one city and before it in another, the date differs."),
                ("Is Diwali the same day as Dhanteras and Govardhan Puja everywhere?",
                 "No. Dhanteras is two days before and Govardhan Puja the day after, but each is decided by its own tithi "
                 "and time of day, so the gaps can stretch or shrink by a day in some cities. The city's own page lists "
                 "all five days of the festival."),
                ("What if the puja window is short?",
                 "The window is where the tradition's rule and the sky agree. A short window is still the right one; where "
                 "it is very short, families usually begin at its start."),
            ],
        },
        "hi": {
            "title": "दीपावली {year}: तारीख और लक्ष्मी पूजा का समय, शहर के अनुसार (अमेरिका, कनाडा, ब्रिटेन, ऑस्ट्रेलिया, भारत)",
            "h1": "दीपावली {year}: आपके शहर में तारीख और लक्ष्मी पूजा का समय",
            "description": "दीपावली {year}: भारत, अमेरिका, कनाडा, ब्रिटेन, ऑस्ट्रेलिया और अन्य देशों के {n} शहरों के लिए लक्ष्मी पूजा "
                           "की तारीख और प्रदोष काल का पूजा समय, हर शहर के स्थानीय समय में।",
            "intro": [
                "लक्ष्मी पूजन कार्तिक अमावस्या को प्रदोष काल में होता है, सूर्यास्त के बाद के पहले तीन मुहूर्तों में। दिन वह है जिस "
                "शाम के इस खंड में अमावस्या चल रही हो। अमावस्या हर जगह एक ही क्षण आरंभ और समाप्त होती है, पर सूर्यास्त स्थानीय है, "
                "इसलिए महाद्वीपों के बीच तारीख एक दिन खिसक सकती है।",
                "तालिका हर शहर के लिए लक्ष्मी पूजन का दिन और पूजा का समय देती है: उस शाम के प्रदोष काल का वह भाग जिसमें अमावस्या चल "
                "रही होती है। सभी समय स्थानीय हैं, डेलाइट सेविंग सहित।",
            ],
            "cols": ["शहर", "लक्ष्मी पूजा", "पूजा का समय", "अमावस्या"],
            "note": "जहाँ अमावस्या दोनों दिन शाम के खंड में चल रही हो, वहाँ वह दिन लिया गया है जिसमें वह खंड का अधिक भाग ढकती है; "
                    "जहाँ किसी भी दिन नहीं, वहाँ सूर्योदय की अमावस्या का दिन।",
            "faq": [
                ("{example_city} में दीपावली भारत से अलग तारीख को क्यों है?",
                 "पूजा शाम की है, और शाम हर शहर में अमावस्या तिथि के अलग बिंदु पर आती है। जब तिथि एक शहर में सूर्यास्त के बाद और "
                 "दूसरे में उससे पहले आरंभ होती है, तारीख अलग हो जाती है।"),
                ("क्या धनतेरस और गोवर्धन पूजा हर जगह दीपावली के साथ उसी क्रम में हैं?",
                 "नहीं। धनतेरस दो दिन पहले और गोवर्धन पूजा अगले दिन होती है, पर हर एक अपनी तिथि और दिन के समय से तय होती है, "
                 "इसलिए कुछ शहरों में अंतर एक दिन बढ़ या घट सकता है। शहर का अपना पृष्ठ पर्व के पाँचों दिन देता है।"),
                ("यदि पूजा का समय छोटा हो तो?",
                 "समय वही है जहाँ परंपरा का नियम और आकाश मिलते हैं। छोटा समय भी सही समय है; जहाँ बहुत छोटा हो, परिवार प्रायः उसके "
                 "आरंभ में पूजा करते हैं।"),
            ],
        },
    },
    "sankashti": {
        "slug": "sankashti-chaturthi",
        "en": {
            "title": "Sankashti Chaturthi {year} Dates and Moonrise Times by City",
            "h1": "Sankashti Chaturthi {year}: dates and moonrise in your city",
            "description": "Every Sankashti Chaturthi of {year} with the moonrise time, for {n} cities in India, the United States, "
                           "Canada, the United Kingdom, Australia and beyond, including the Angarki Chaturthis that fall on a "
                           "Tuesday.",
            "intro": [
                "Sankashti Chaturthi is the Chaturthi of each dark fortnight, kept with a fast that ends at moonrise. The day "
                "is the one on which Chaturthi is in force at moonrise, so both the date and the time to break the fast "
                "depend on where you are. A Sankashti that falls on a Tuesday is Angarki, the most observed of the year.",
                "Choose your city for its full list. The list gives each fast day, its name, and the moonrise that evening in "
                "local time.",
            ],
            "cols": ["Date", "Sankashti", "Moonrise", "Chaturthi ends"],
            "note": "Where Chaturthi is in force at neither evening's moonrise, the fast is kept on the later day, as the "
                    "published panchangs do.",
            "faq": [
                ("Why does my city's Sankashti date sometimes differ from India's?",
                 "Because the deciding moment is the local moonrise. The tithi is the same stretch of time everywhere; the "
                 "moon rises at a different point in it in each city."),
                ("What is Angarki Sankashti?",
                 "A Sankashti Chaturthi that falls on a Tuesday, Mangalavara, the day of Angaraka (Mars). It is held to carry "
                 "the merit of a year of Sankashti fasts."),
            ],
        },
        "hi": {
            "title": "संकष्टी चतुर्थी {year}: तारीखें और चंद्रोदय का समय, शहर के अनुसार",
            "h1": "संकष्टी चतुर्थी {year}: आपके शहर में तारीखें और चंद्रोदय",
            "description": "{year} की हर संकष्टी चतुर्थी चंद्रोदय के समय के साथ, भारत, अमेरिका, कनाडा, ब्रिटेन, ऑस्ट्रेलिया और अन्य "
                           "देशों के {n} शहरों के लिए, मंगलवार को पड़ने वाली अंगारकी चतुर्थियों सहित।",
            "intro": [
                "संकष्टी चतुर्थी हर कृष्ण पक्ष की चतुर्थी है, जिसका व्रत चंद्रोदय पर खोला जाता है। दिन वह है जिस दिन चंद्रोदय के समय "
                "चतुर्थी चल रही हो, इसलिए तारीख और व्रत खोलने का समय दोनों आपके स्थान पर निर्भर हैं। मंगलवार को पड़ने वाली संकष्टी "
                "अंगारकी कहलाती है, वर्ष की सबसे अधिक मानी जाने वाली।",
                "अपना शहर चुनें। सूची हर व्रत का दिन, उसका नाम और उस शाम का चंद्रोदय स्थानीय समय में देती है।",
            ],
            "cols": ["तारीख", "संकष्टी", "चंद्रोदय", "चतुर्थी समाप्त"],
            "note": "जहाँ चतुर्थी किसी भी शाम के चंद्रोदय पर नहीं होती, वहाँ व्रत बाद के दिन रखा गया है, जैसा प्रकाशित पंचांग करते हैं।",
            "faq": [
                ("मेरे शहर की संकष्टी तारीख कभी-कभी भारत से अलग क्यों होती है?",
                 "क्योंकि निर्णायक क्षण स्थानीय चंद्रोदय है। तिथि हर जगह एक ही समय-खंड है; चंद्र हर शहर में उस खंड के अलग बिंदु पर उगता है।"),
                ("अंगारकी संकष्टी क्या है?",
                 "मंगलवार, अंगारक (मंगल) के दिन पड़ने वाली संकष्टी चतुर्थी। इसे वर्ष भर की संकष्टी का फल देने वाली माना जाता है।"),
            ],
        },
    },
    "ekadashi": {
        "slug": "ekadashi",
        "en": {
            "title": "Ekadashi {year} Dates by City, with Parana Time",
            "h1": "Ekadashi {year}: dates and parana time in your city",
            "description": "All Ekadashi fasting dates of {year}, with the parana time for breaking the fast, for {n} cities in "
                           "India, the United States, Canada, the United Kingdom, Australia and beyond, each in local time.",
            "intro": [
                "Ekadashi is kept twice a lunar month, and the fast is broken the next morning, in Dwadashi, after sunrise "
                "and after the first quarter of the Dwadashi tithi (Hari Vasara) has passed. The fast day is the one on "
                "which Ekadashi is in force at sunrise; when Dwadashi would be over before the next sunrise, the fast moves a "
                "day earlier so that it can be broken in Dwadashi.",
                "Choose your city for its full list: each Ekadashi by name, its date, and the parana window for the following "
                "morning in local time.",
            ],
            "cols": ["Date", "Ekadashi", "Parana (next day)", "Dwadashi ends"],
            "note": "The parana window begins at sunrise or at the end of Hari Vasara, whichever is later, and ends with the "
                    "first fifth of the day where the tithi allows; otherwise it runs to the end of Dwadashi.",
            "faq": [
                ("Why does Ekadashi fall a day apart in different cities?",
                 "The tithi is in force at the same instant everywhere, but sunrise is not. In a city where Ekadashi has not "
                 "begun by sunrise, the fast is the next day."),
                ("What is parana?",
                 "Breaking the fast. It is done in Dwadashi, after sunrise and after Hari Vasara, and before Dwadashi ends."),
            ],
        },
        "hi": {
            "title": "एकादशी {year}: तारीखें और पारण का समय, शहर के अनुसार",
            "h1": "एकादशी {year}: आपके शहर में तारीखें और पारण का समय",
            "description": "{year} की सभी एकादशी व्रत की तारीखें, व्रत खोलने के पारण समय के साथ, भारत, अमेरिका, कनाडा, ब्रिटेन, "
                           "ऑस्ट्रेलिया और अन्य देशों के {n} शहरों के लिए, स्थानीय समय में।",
            "intro": [
                "एकादशी हर चांद्र मास में दो बार रखी जाती है, और व्रत अगली सुबह द्वादशी में, सूर्योदय के बाद और द्वादशी तिथि के पहले "
                "चौथाई (हरि वासर) के बीतने के बाद खोला जाता है। व्रत का दिन वह है जिस दिन सूर्योदय के समय एकादशी चल रही हो; जब "
                "द्वादशी अगले सूर्योदय से पहले ही समाप्त हो जाती हो, व्रत एक दिन पहले हो जाता है ताकि वह द्वादशी में खोला जा सके।",
                "अपना शहर चुनें: हर एकादशी नाम सहित, उसकी तारीख, और अगली सुबह का पारण समय स्थानीय समय में।",
            ],
            "cols": ["तारीख", "एकादशी", "पारण (अगले दिन)", "द्वादशी समाप्त"],
            "note": "पारण का समय सूर्योदय या हरि वासर की समाप्ति, जो बाद में हो, से आरंभ होता है और जहाँ तिथि अनुमति दे वहाँ दिन के "
                    "पहले पाँचवें भाग के साथ समाप्त होता है; अन्यथा द्वादशी के अंत तक चलता है।",
            "faq": [
                ("एकादशी अलग शहरों में एक दिन अलग क्यों पड़ती है?",
                 "तिथि हर जगह एक ही क्षण चलती है, पर सूर्योदय नहीं। जिस शहर में सूर्योदय तक एकादशी आरंभ न हुई हो, वहाँ व्रत अगले दिन होता है।"),
                ("पारण क्या है?",
                 "व्रत खोलना। यह द्वादशी में, सूर्योदय और हरि वासर के बाद, और द्वादशी समाप्त होने से पहले किया जाता है।"),
            ],
        },
    },
}

MONTH = {
    "en": {
        "title": "{city} Panchang {month} {year}: Tithi, Nakshatra, Sunrise, Rahu Kaal for Every Day",
        "h1": "Panchang for {city}, {month} {year}",
        "description": "The Hindu calendar for {city} in {month} {year}: every day's tithi and nakshatra at sunrise with the "
                       "time each ends, sunrise, sunset and moonrise, Rahu Kaal, and the month's fasts and festivals, in "
                       "local time.",
        "intro": "Every day of {month} {year} in {city}: the tithi and nakshatra in force at sunrise and when each ends, the "
                 "times of the Sun and the Moon, and Rahu Kaal, all for {city}'s own sky and clock. The lunar months this "
                 "month touches are {lunar}. For the current day with its full panchang, see the {city} page.",
        "cols": ["Date", "Tithi", "Nakshatra", "Sunrise", "Sunset", "Moonrise", "Rahu Kaal"],
        "vrats_h": "Fasts and festivals in {month} {year}",
        "none": "No fast or festival this month.",
        "prev": "Previous month", "next": "Next month", "today": "Today's panchang for {city}",
        "faq": [
            ("Which tithi is shown for each day?",
             "The one in force at sunrise in {city}, with the time it ends. The tithi named after it begins at that time and "
             "runs until the next sunrise or beyond."),
            ("Why do the dates of fasts here differ from an Indian calendar?",
             "Each is worked out for {city}'s own sunrise, sunset and moonrise. A tithi runs for the same stretch of time "
             "everywhere, but the local day falls at a different point in it."),
        ],
    },
    "hi": {
        "title": "{city} पंचांग {month} {year}: हर दिन की तिथि, नक्षत्र, सूर्योदय, राहु काल",
        "h1": "{city} का पंचांग, {month} {year}",
        "description": "{month} {year} में {city} का हिन्दू पंचांग: हर दिन की सूर्योदय की तिथि और नक्षत्र उनके समाप्ति समय के साथ, "
                       "सूर्योदय, सूर्यास्त और चंद्रोदय, राहु काल, और महीने के व्रत-त्योहार, स्थानीय समय में।",
        "intro": "{city} में {month} {year} का हर दिन: सूर्योदय के समय की तिथि और नक्षत्र और उनके समाप्त होने का समय, सूर्य और चंद्र "
                 "के समय, और राहु काल, सब {city} के अपने आकाश और घड़ी के लिए। इस महीने में आने वाले चांद्र मास {lunar} हैं। आज के "
                 "दिन के पूरे पंचांग के लिए {city} का पृष्ठ देखें।",
        "cols": ["तारीख", "तिथि", "नक्षत्र", "सूर्योदय", "सूर्यास्त", "चंद्रोदय", "राहु काल"],
        "vrats_h": "{month} {year} के व्रत और त्योहार",
        "none": "इस महीने कोई व्रत या त्योहार नहीं।",
        "prev": "पिछला महीना", "next": "अगला महीना", "today": "{city} का आज का पंचांग",
        "faq": [
            ("हर दिन के लिए कौन-सी तिथि दिखाई गई है?",
             "वह जो {city} में सूर्योदय के समय चल रही हो, उसके समाप्त होने के समय के साथ। उसके बाद लिखी तिथि उसी समय आरंभ होकर "
             "अगले सूर्योदय या उसके बाद तक चलती है।"),
            ("यहाँ व्रतों की तारीखें भारतीय कैलेंडर से अलग क्यों हैं?",
             "हर एक {city} के अपने सूर्योदय, सूर्यास्त और चंद्रोदय से निकाली गई है। तिथि हर जगह एक ही समय-खंड में चलती है, पर "
             "स्थानीय दिन उस खंड के अलग बिंदु पर पड़ता है।"),
        ],
    },
}

METHODS = {
    "en": {
        "title": "How This Panchang Is Calculated: Ephemeris, Ayanamsa, Sunrise and the Hindu Day",
        "h1": "How this panchang is calculated",
        "description": "What goes into the panchang on this site: the JPL ephemeris behind the Sun and Moon, the Lahiri "
                       "ayanamsa, the definition of sunrise, the Hindu day, the muhurtas, and the rules by which fasts and "
                       "festivals are placed on a date.",
        "sections": [
            ("The Sun and the Moon",
             ["The positions of the Sun and the Moon come from the JPL DE421 planetary ephemeris, the numerical model of "
              "the solar system published by NASA's Jet Propulsion Laboratory and used in astronomical almanacs. The "
              "positions are apparent and geocentric: as seen from the centre of the Earth, allowing for the time light "
              "takes to arrive and for the Earth's motion. They are referred to the ecliptic and equinox of the date.",
              "From the two longitudes come the limbs of the panchang. The tithi is the angle by which the Moon is ahead of "
              "the Sun, twelve degrees to a tithi; the karana is half a tithi. The nakshatra is the Moon's place among the "
              "twenty-seven stations of thirteen degrees twenty minutes each, and the yoga the sum of the two longitudes "
              "divided the same way."]),
            ("The ayanamsa",
             ["Nakshatra, yoga and the rashis are sidereal: they are measured from a fixed point among the stars, not from "
              "the moving equinox. The difference between the two is the ayanamsa. This site uses the Lahiri or "
              "Chitrapaksha ayanamsa, the standard of the Indian national calendar: twenty-three degrees fifteen minutes "
              "and 0.66 seconds on the 21st of March 1956, carried forward as a fixed direction in space, so that it grows "
              "with the precession of the equinoxes, about fifty seconds of arc a year. The tithi needs no ayanamsa, being "
              "a difference of two longitudes."]),
            ("Sunrise, sunset, moonrise",
             ["Sunrise and sunset are the moments the upper edge of the Sun's disc touches the horizon, allowing for the "
              "bending of light in the atmosphere, which lifts the Sun by about thirty-four minutes of arc. This is the "
              "definition most published panchangs use. Moonrise and moonset are taken for the centre of the Moon's disc as "
              "seen from the city, with the Moon's parallax allowed for.",
              "Each city is computed at its centre. Across a large metropolitan area the sunrise can differ by a minute or "
              "two from one edge to the other."]),
            ("The Hindu day",
             ["A Hindu day runs from sunrise to the next sunrise. The tithi, nakshatra, yoga and karana of a day are those "
              "in force at its sunrise; a page lists every change up to the following sunrise, with the time of each. "
              "A time marked as the next day is after midnight but before that sunrise. Moonrise and moonset are likewise "
              "those of the Hindu day, which is why a moonrise after midnight is listed under the day before.",
              "The weekday changes at sunrise too. The lunar month is named in two reckonings: amanta, ending at the new "
              "moon, used in the south and west of India; and purnimanta, ending at the full moon, used in the north. An "
              "intercalary month, adhika, is the same span in both."]),
            ("Muhurtas and Choghadiya",
             ["The day from sunrise to sunset is divided into eight parts for Rahu Kaal, Yamaganda and Gulika, a different "
              "part on each weekday, and into fifteen muhurtas, of which Abhijit is the eighth, around midday. The night is "
              "divided into fifteen muhurtas too, and Brahma Muhurta is the second-last before sunrise. Choghadiya divides "
              "day and night into eight parts each, their names following the planetary order from the weekday's lord. "
              "Because all of these are fractions of the local day, they move with the seasons and with the place."]),
            ("Fasts and festivals",
             ["A fast or festival is tied to a tithi and to a part of the day in which that tithi must be in force: sunrise "
              "for most, midday for Ganesh Chaturthi, the evening after sunset for Diwali and Pradosh, midnight for "
              "Shivaratri and Janmashtami, moonrise for Sankashti Chaturthi and Karwa Chauth. When the tithi is in force at "
              "that part on two consecutive days, or on neither, a rule of preference decides. The preferences used here "
              "follow the published panchangs of North India, and were checked against them, city by city, over many "
              "months before any date was published. Ekadashi follows its own rule: the fast is kept on the day Ekadashi is "
              "in force at sunrise, but moves a day earlier when Dwadashi would be over before the next sunrise, so that "
              "the fast can be broken in Dwadashi."]),
            ("Precision and rounding",
             ["Times are rounded to the nearest minute. The instants of new and full moon computed here agree with the "
              "astronomical almanac to within seconds. Other panchangs may show a tithi's end a minute or two apart from "
              "this one, from different conventions for the time scale or the ayanamsa; a sunrise a few seconds apart can "
              "round to a different minute. Where a tithi ends within a minute of sunrise, the day's tithi itself can "
              "differ between panchangs, and a reader with a fast on that day should look at both."]),
            ("Sources",
             ["JPL DE421 planetary ephemeris, NASA Jet Propulsion Laboratory; Skyfield, the open astronomy library by Brandon "
              "Rhodes, for the positions, risings and settings; the IAU 2006 precession and IAU 2000B nutation models; the "
              "Lahiri ayanamsa as defined for the Indian national calendar; the IANA time zone database for each city's "
              "clock and daylight saving."]),
        ],
    },
    "hi": {
        "title": "यह पंचांग कैसे बनता है: ग्रह-पंचांग, अयनांश, सूर्योदय और हिन्दू दिन",
        "h1": "यह पंचांग कैसे बनता है",
        "description": "इस साइट के पंचांग में क्या-क्या है: सूर्य और चंद्र के पीछे का JPL ग्रह-पंचांग, लाहिरी अयनांश, सूर्योदय की परिभाषा, "
                       "हिन्दू दिन, मुहूर्त, और वे नियम जिनसे व्रत और त्योहार किसी तारीख पर रखे जाते हैं।",
        "sections": [
            ("सूर्य और चंद्र",
             ["सूर्य और चंद्र की स्थितियाँ JPL DE421 ग्रह-पंचांग से ली गई हैं, जो नासा की जेट प्रोपल्शन लेबोरेटरी का सौर मंडल का संख्यात्मक "
              "मॉडल है और खगोलीय पंचांगों में उपयोग होता है। स्थितियाँ दृश्य और भूकेंद्रीय हैं: पृथ्वी के केंद्र से देखी हुई, प्रकाश के आने "
              "में लगने वाले समय और पृथ्वी की गति को मानकर। वे उस तारीख की क्रांतिवृत्त और विषुव के सापेक्ष हैं।",
              "दो देशांतरों से पंचांग के अंग निकलते हैं। तिथि वह कोण है जितना चंद्र सूर्य से आगे है, बारह अंश की एक तिथि; करण आधी तिथि "
              "है। नक्षत्र चंद्र का स्थान है तेरह अंश बीस कला के सत्ताईस भागों में, और योग दोनों देशांतरों का योग उसी प्रकार बाँटा हुआ।"]),
            ("अयनांश",
             ["नक्षत्र, योग और राशियाँ निरयण हैं: वे तारों के बीच एक स्थिर बिंदु से मापी जाती हैं, चलते विषुव से नहीं। दोनों का अंतर "
              "अयनांश है। यह साइट लाहिरी या चित्रपक्ष अयनांश का उपयोग करती है, जो भारत के राष्ट्रीय पंचांग का मानक है: 21 मार्च 1956 को "
              "तेईस अंश पंद्रह कला 0.66 विकला, जिसे अंतरिक्ष में एक स्थिर दिशा के रूप में आगे ले जाया गया है, ताकि वह विषुवों के अयन के "
              "साथ बढ़े, लगभग पचास विकला प्रति वर्ष। तिथि को अयनांश नहीं चाहिए, क्योंकि वह दो देशांतरों का अंतर है।"]),
            ("सूर्योदय, सूर्यास्त, चंद्रोदय",
             ["सूर्योदय और सूर्यास्त वे क्षण हैं जब सूर्य बिंब का ऊपरी किनारा क्षितिज को छूता है, वायुमंडल में प्रकाश के मुड़ने को मानकर, "
              "जो सूर्य को लगभग चौंतीस कला ऊपर उठा देता है। अधिकतर प्रकाशित पंचांग यही परिभाषा लेते हैं। चंद्रोदय और चंद्रास्त शहर से देखे "
              "चंद्र बिंब के केंद्र के लिए हैं, चंद्र के लंबन को मानकर।",
              "हर शहर उसके केंद्र पर गिना गया है। बड़े महानगर में एक किनारे से दूसरे तक सूर्योदय एक-दो मिनट अलग हो सकता है।"]),
            ("हिन्दू दिन",
             ["हिन्दू दिन सूर्योदय से अगले सूर्योदय तक चलता है। दिन की तिथि, नक्षत्र, योग और करण वे हैं जो उसके सूर्योदय पर चल रहे हों; "
              "पृष्ठ अगले सूर्योदय तक हर परिवर्तन उसके समय के साथ देता है। 'अगले दिन' लिखा समय आधी रात के बाद पर उस सूर्योदय से पहले का "
              "है। चंद्रोदय और चंद्रास्त भी हिन्दू दिन के हैं, इसीलिए आधी रात के बाद का चंद्रोदय पिछले दिन के नीचे लिखा होता है।",
              "वार भी सूर्योदय पर बदलता है। चांद्र मास दो गणनाओं में लिखा है: अमांत, जो अमावस्या पर समाप्त होता है और दक्षिण-पश्चिम "
              "भारत में चलता है; और पूर्णिमांत, जो पूर्णिमा पर समाप्त होता है और उत्तर भारत में चलता है। अधिक मास दोनों में एक ही खंड है।"]),
            ("मुहूर्त और चौघड़िया",
             ["सूर्योदय से सूर्यास्त तक का दिन राहु काल, यमगंड और गुलिक के लिए आठ भागों में बाँटा जाता है, हर वार को अलग भाग, और पंद्रह "
              "मुहूर्तों में, जिनमें अभिजित आठवाँ है, दोपहर के आसपास। रात भी पंद्रह मुहूर्तों में बँटती है, और ब्रह्म मुहूर्त सूर्योदय से पहले "
              "का दूसरा अंतिम है। चौघड़िया दिन और रात को आठ-आठ भागों में बाँटता है, जिनके नाम वार के स्वामी से ग्रहों के क्रम में चलते हैं। "
              "ये सब स्थानीय दिन के भाग हैं, इसलिए ऋतु और स्थान के साथ बदलते हैं।"]),
            ("व्रत और त्योहार",
             ["व्रत या त्योहार एक तिथि से और दिन के उस भाग से जुड़ा है जिसमें वह तिथि चल रही होनी चाहिए: अधिकतर के लिए सूर्योदय, गणेश "
              "चतुर्थी के लिए मध्याह्न, दीपावली और प्रदोष के लिए सूर्यास्त के बाद की शाम, शिवरात्रि और जन्माष्टमी के लिए मध्यरात्रि, "
              "संकष्टी चतुर्थी और करवा चौथ के लिए चंद्रोदय। जब तिथि उस भाग में दो लगातार दिन चल रही हो, या किसी भी दिन नहीं, तो "
              "वरीयता का नियम तय करता है। यहाँ उपयोग की गई वरीयताएँ उत्तर भारत के प्रकाशित पंचांगों की हैं, और किसी तारीख को प्रकाशित "
              "करने से पहले उन्हें शहर-दर-शहर, कई महीनों पर जाँचा गया। एकादशी का अपना नियम है: व्रत उस दिन है जिस दिन सूर्योदय पर "
              "एकादशी चल रही हो, पर जब द्वादशी अगले सूर्योदय से पहले समाप्त हो जाती हो तो एक दिन पहले, ताकि व्रत द्वादशी में खोला जा सके।"]),
            ("सूक्ष्मता और पूर्णांकन",
             ["समय निकटतम मिनट तक लिखे गए हैं। यहाँ निकाले गए अमावस्या और पूर्णिमा के क्षण खगोलीय पंचांग से कुछ सेकंड के भीतर मिलते "
              "हैं। अन्य पंचांग किसी तिथि का अंत इससे एक-दो मिनट अलग दिखा सकते हैं, समय-मान या अयनांश की भिन्न परंपरा से; कुछ सेकंड "
              "अलग सूर्योदय दूसरे मिनट में जा सकता है। जहाँ तिथि सूर्योदय के एक मिनट के भीतर समाप्त हो, वहाँ दिन की तिथि ही पंचांगों "
              "में अलग हो सकती है, और उस दिन व्रत रखने वाले को दोनों देखने चाहिए।"]),
            ("स्रोत",
             ["JPL DE421 ग्रह-पंचांग, नासा जेट प्रोपल्शन लेबोरेटरी; स्थितियों, उदय और अस्त के लिए ब्रैंडन रोड्स की खुली खगोल लाइब्रेरी "
              "Skyfield; IAU 2006 अयन और IAU 2000B विचलन मॉडल; भारत के राष्ट्रीय पंचांग के लिए परिभाषित लाहिरी अयनांश; हर शहर की घड़ी "
              "और डेलाइट सेविंग के लिए IANA समय-क्षेत्र डेटाबेस।"]),
        ],
    },
}
