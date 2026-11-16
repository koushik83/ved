"""The words of the festival pages, the monthly pages and the methods page, in English and Hindi. Pure data."""

FESTIVALS = {
    "karwa_chauth": {
        "slug": "karwa-chauth",
        "en": {
            "title": "Karwa Chauth {year}: Date and Moonrise Time by City (USA, Canada, UK, Australia, India)",
            "h1": "Karwa Chauth {year}: date and moonrise time in your city",
            "description": "Karwa Chauth {year}: the date, moonrise time and fasting hours for {n} cities in the USA, "
                           "Canada, UK, Australia and India, in local time.",
            "intro": [
                "Karwa Chauth is kept on Kartika Krishna Chaturthi, and the fast is broken only when the moon is seen. The "
                "fast falls on the day Chaturthi is in force in the evening, in pradosh kaal, the 144 minutes after sunset "
                "when the puja is done and the moon is awaited; if Chaturthi touches both evenings, on the one it covers "
                "more of. Because Chaturthi begins and ends at one instant worldwide but sunset is local, the date can "
                "differ by a day between India and a city abroad. In some cities Chaturthi has ended by the time the moon "
                "rises; the fast is still kept that day and broken at moonrise.",
                "The table gives, for each city, the day of the fast, the moonrise that evening, and the fasting hours from "
                "sunrise to moonrise. All times are the city's own local time, with daylight saving allowed for.",
            ],
            "cols": ["City", "Karwa Chauth", "Moonrise", "Fast from sunrise", "Chaturthi"],
            "note": "Where the Chaturthi tithi is in force in neither evening's pradosh kaal, the fast is kept on the later "
                    "of the two days, as the North Indian panchangs do.",
            "faq": [
                ("Why is Karwa Chauth on a different date in {example_city} than in India?",
                 "Because the fast is tied to the local evening. The Chaturthi tithi runs for the same stretch of time "
                 "everywhere, but in a city many hours west of India the evening falls earlier in that stretch, so the "
                 "tithi may be in force after sunset a day later or earlier than in Delhi."),
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
                "करवा चौथ कार्तिक कृष्ण चतुर्थी को रखा जाता है और व्रत चंद्र दर्शन के बाद ही खोला जाता है। व्रत उस दिन होता है जिस "
                "दिन शाम को, सूर्यास्त के बाद के 144 मिनट के प्रदोष काल में, चतुर्थी तिथि चल रही हो, जब पूजा होती है और चंद्रमा की "
                "प्रतीक्षा होती है; यदि चतुर्थी दोनों शामों को छूती हो, तो उस शाम जिसका अधिक भाग वह ढकती है। चतुर्थी पूरे संसार में एक "
                "ही क्षण आरंभ और समाप्त होती है, पर सूर्यास्त स्थानीय है; इसलिए भारत और विदेश के किसी शहर में तारीख एक दिन अलग हो "
                "सकती है। कुछ शहरों में चंद्रोदय तक चतुर्थी समाप्त हो चुकी होती है; व्रत फिर भी उसी दिन रखा जाता है और चंद्रोदय पर "
                "खोला जाता है।",
                "तालिका हर शहर के लिए व्रत का दिन, उस शाम का चंद्रोदय और सूर्योदय से चंद्रोदय तक के व्रत के घंटे देती है। सभी समय "
                "शहर के अपने स्थानीय समय में हैं, डेलाइट सेविंग सहित।",
            ],
            "cols": ["शहर", "करवा चौथ", "चंद्रोदय", "व्रत सूर्योदय से", "चतुर्थी"],
            "note": "जहाँ चतुर्थी तिथि किसी भी शाम के प्रदोष काल में नहीं होती, वहाँ व्रत दोनों में से बाद के दिन रखा जाता है, जैसा "
                    "उत्तर भारत के पंचांग करते हैं।",
            "faq": [
                ("{example_city} में करवा चौथ भारत से अलग तारीख को क्यों है?",
                 "क्योंकि व्रत स्थानीय शाम से जुड़ा है। चतुर्थी तिथि हर जगह एक ही समय-खंड में चलती है, पर भारत से कई घंटे "
                 "पश्चिम के शहर में शाम उस खंड में पहले पड़ती है, इसलिए वहाँ सूर्यास्त के बाद तिथि दिल्ली से एक दिन बाद या पहले चल "
                 "रही हो सकती है।"),
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
            "description": "When is Diwali {year}? The Lakshmi Puja date and time for {n} cities in the USA, Canada, UK, "
                           "Australia and India, in local time.",
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
    "makar_sankranti": {
        "slug": "makar-sankranti",
        "en": {
            "title": "Makar Sankranti {year}: Date and Time by City (USA, Canada, UK, Australia, India)",
            "h1": "Makar Sankranti {year}: date and time in your city",
            "description": "Makar Sankranti {year}, Pongal and Lohri: the date and the moment the Sun enters Makara for {n} "
                           "cities in the USA, Canada, the UK, Australia and India.",
            "intro": [
                "Makar Sankranti is the day the Sun enters Makara, the sidereal Capricorn. The entry is one instant "
                "everywhere, but the day it falls on depends on the city's clock and its sunset: when the Sun enters "
                "Makara after sunset, the festival and its punya kaal, the hours for the holy bath and for giving, move "
                "to the next day. That is why the date can differ between India and a city abroad. Tamil families keep "
                "the same day as Pongal, and Lohri is lit on the evening before.",
                "The table gives, for each city, the day of Makar Sankranti, the local time the Sun enters Makara, and the "
                "day of Lohri. All times are local, with daylight saving allowed for.",
            ],
            "cols": ["City", "Makar Sankranti", "Sun enters Makara", "Lohri"],
            "note": "The Sun's place is sidereal, with the Lahiri ayanamsa. The punya kaal follows the moment of entry; when "
                    "the entry falls after sunset, it is kept from sunrise the next day.",
            "faq": [
                ("Why can Makar Sankranti fall on a different date in {example_city} than in India?",
                 "The Sun enters Makara at one instant worldwide. A city many hours behind India meets that instant "
                 "earlier on its own clock, sometimes on the previous date, and when the entry comes after the city's "
                 "sunset the festival moves to the next day. Either can change the date."),
                ("Is Makar Sankranti always on 14 January?",
                 "No. The moment of entry comes about six hours later each year and moves back with each leap day, so in "
                 "these decades it falls on 14 or 15 January in India, drifting slowly later over the centuries."),
                ("When is Lohri?",
                 "Lohri is lit on the evening before Makar Sankranti, so it moves with it."),
            ],
        },
        "hi": {
            "title": "मकर संक्रांति {year}: तारीख और समय, शहर के अनुसार (अमेरिका, कनाडा, ब्रिटेन, ऑस्ट्रेलिया, भारत)",
            "h1": "मकर संक्रांति {year}: आपके शहर में तारीख और समय",
            "description": "मकर संक्रांति {year}, पोंगल और लोहड़ी: अमेरिका, कनाडा, ब्रिटेन, ऑस्ट्रेलिया और भारत के {n} शहरों में "
                           "तारीख और सूर्य के मकर प्रवेश का स्थानीय समय।",
            "intro": [
                "मकर संक्रांति वह दिन है जब सूर्य निरयन मकर राशि में प्रवेश करता है। यह प्रवेश हर जगह एक ही क्षण होता है, पर वह "
                "किस दिन पड़ता है यह शहर की घड़ी और उसके सूर्यास्त पर निर्भर है: जब सूर्य सूर्यास्त के बाद मकर में प्रवेश करता है, "
                "तो पर्व और उसका पुण्य काल, स्नान और दान का समय, अगले दिन चला जाता है। इसीलिए भारत और विदेश के किसी शहर में "
                "तारीख अलग हो सकती है। तमिल परिवार यही दिन पोंगल के रूप में मनाते हैं, और लोहड़ी इसकी पिछली शाम जलाई जाती है।",
                "तालिका हर शहर के लिए मकर संक्रांति का दिन, सूर्य के मकर प्रवेश का स्थानीय समय और लोहड़ी का दिन देती है। सभी "
                "समय स्थानीय हैं, डेलाइट सेविंग सहित।",
            ],
            "cols": ["शहर", "मकर संक्रांति", "सूर्य का मकर प्रवेश", "लोहड़ी"],
            "note": "सूर्य की स्थिति निरयन है, लाहिड़ी अयनांश के साथ। पुण्य काल प्रवेश के क्षण के बाद आता है; जब प्रवेश सूर्यास्त के "
                    "बाद हो, तो वह अगले दिन सूर्योदय से माना जाता है।",
            "faq": [
                ("{example_city} में मकर संक्रांति भारत से अलग तारीख को क्यों हो सकती है?",
                 "सूर्य पूरे संसार में एक ही क्षण मकर में प्रवेश करता है। भारत से कई घंटे पीछे का शहर उस क्षण को अपनी घड़ी पर पहले "
                 "पाता है, कभी पिछली तारीख को, और यदि प्रवेश शहर के सूर्यास्त के बाद हो तो पर्व अगले दिन चला जाता है। दोनों से "
                 "तारीख बदल सकती है।"),
                ("क्या मकर संक्रांति हमेशा 14 जनवरी को होती है?",
                 "नहीं। प्रवेश का क्षण हर साल लगभग छह घंटे बाद आता है और हर लीप दिन के साथ पीछे लौटता है, इसलिए इन दशकों में भारत "
                 "में यह 14 या 15 जनवरी को पड़ता है, और सदियों में धीरे-धीरे आगे खिसकता है।"),
                ("लोहड़ी कब है?",
                 "लोहड़ी मकर संक्रांति की पिछली शाम जलाई जाती है, इसलिए वह उसी के साथ खिसकती है।"),
            ],
        },
    },
    "maha_shivaratri": {
        "slug": "maha-shivratri",
        "en": {
            "title": "Maha Shivratri {year}: Date and Nishita Puja Time by City (USA, Canada, UK, Australia, India)",
            "h1": "Maha Shivratri {year}: date and nishita puja time in your city",
            "description": "Maha Shivratri {year}: the date and the nishita kaal puja time for {n} cities in the USA, Canada, "
                           "the UK, Australia and India, each in local time.",
            "intro": [
                "Maha Shivratri is kept on the Chaturdashi of the dark fortnight of Magha, which North Indian calendars "
                "call Phalguna, and its central worship is at nishita kaal, the muhurta at the middle of the night. The "
                "day is the one whose midnight muhurta falls while Chaturdashi is in force. Chaturdashi begins and ends at "
                "one instant everywhere, but each city's night is its own, so the date can differ by a day between India "
                "and a city abroad, and even between the east and west coasts of North America.",
                "The table gives, for each city, the date of Maha Shivratri, the nishita puja time during which "
                "Chaturdashi is in force, and the time Chaturdashi ends. The fast is broken the next morning after "
                "sunrise. All times are local, with daylight saving allowed for.",
            ],
            "cols": ["City", "Maha Shivratri", "Nishita puja", "Chaturdashi ends"],
            "note": "Where Chaturdashi holds the midnight muhurta of both nights, the first is taken; where it holds "
                    "neither, the first day it touches.",
            "faq": [
                ("Why is Maha Shivratri on a different date in {example_city} than in India?",
                 "The worship belongs to the middle of the night. Chaturdashi covers the same stretch of time everywhere, "
                 "but midnight comes to each city at a different point in it, so the night it covers can differ from "
                 "Delhi's."),
                ("What is nishita kaal?",
                 "The night is divided into fifteen muhurtas, and nishita is the eighth, the one at its middle. It is "
                 "worked out from each city's own sunset and next sunrise, so it is rarely at midnight on the clock."),
                ("Is this the same as the monthly Shivaratri?",
                 "Masik Shivaratri falls on every dark-fortnight Chaturdashi; Maha Shivratri is the one in Magha "
                 "(Phalguna in the North) and the main one of the year. Each city's page lists every Masik Shivaratri."),
            ],
        },
        "hi": {
            "title": "महाशिवरात्रि {year}: तारीख और निशीथ पूजा का समय, शहर के अनुसार (अमेरिका, कनाडा, ब्रिटेन, ऑस्ट्रेलिया, भारत)",
            "h1": "महाशिवरात्रि {year}: आपके शहर में तारीख और निशीथ पूजा का समय",
            "description": "महाशिवरात्रि {year}: अमेरिका, कनाडा, ब्रिटेन, ऑस्ट्रेलिया और भारत के {n} शहरों के लिए तारीख और निशीथ "
                           "काल की पूजा का समय, स्थानीय समय में।",
            "intro": [
                "महाशिवरात्रि माघ कृष्ण चतुर्दशी को रखी जाती है, जिसे उत्तर भारत के पंचांग फाल्गुन कहते हैं, और इसकी मुख्य पूजा "
                "निशीथ काल में होती है, रात के मध्य का मुहूर्त। दिन वह है जिसकी आधी रात के मुहूर्त में चतुर्दशी चल रही हो। "
                "चतुर्दशी हर जगह एक ही क्षण आरंभ और समाप्त होती है, पर हर शहर की रात अपनी होती है, इसलिए भारत और विदेश के किसी "
                "शहर में, और उत्तर अमेरिका के पूर्वी और पश्चिमी तट के बीच भी, तारीख एक दिन अलग हो सकती है।",
                "तालिका हर शहर के लिए महाशिवरात्रि की तारीख, निशीथ पूजा का वह समय जिसमें चतुर्दशी चल रही हो, और चतुर्दशी के "
                "समाप्त होने का समय देती है। व्रत अगली सुबह सूर्योदय के बाद खोला जाता है। सभी समय स्थानीय हैं, डेलाइट सेविंग सहित।",
            ],
            "cols": ["शहर", "महाशिवरात्रि", "निशीथ पूजा", "चतुर्दशी समाप्त"],
            "note": "जहाँ चतुर्दशी दोनों रातों के मध्य मुहूर्त में हो, वहाँ पहली रात ली गई है; जहाँ किसी में नहीं, वहाँ पहला दिन "
                    "जिसे वह छूती है।",
            "faq": [
                ("{example_city} में महाशिवरात्रि भारत से अलग तारीख को क्यों है?",
                 "पूजा रात के मध्य की है। चतुर्दशी हर जगह एक ही समय-खंड में चलती है, पर हर शहर की आधी रात उस खंड के अलग बिंदु "
                 "पर आती है, इसलिए जिस रात को वह ढकती है वह दिल्ली से अलग हो सकती है।"),
                ("निशीथ काल क्या है?",
                 "रात को पंद्रह मुहूर्तों में बाँटा जाता है, और निशीथ आठवाँ है, रात के मध्य वाला। यह हर शहर के अपने सूर्यास्त और "
                 "अगले सूर्योदय से निकाला जाता है, इसलिए यह घड़ी की आधी रात पर कम ही होता है।"),
                ("क्या यह मासिक शिवरात्रि जैसी ही है?",
                 "मासिक शिवरात्रि हर कृष्ण पक्ष की चतुर्दशी को होती है; महाशिवरात्रि माघ (उत्तर में फाल्गुन) वाली है और वर्ष की "
                 "मुख्य शिवरात्रि है। हर शहर का पृष्ठ हर मासिक शिवरात्रि देता है।"),
            ],
        },
    },
    "holi": {
        "slug": "holi",
        "en": {
            "title": "Holi {year}: Date and Holika Dahan Time by City (USA, Canada, UK, Australia, India)",
            "h1": "Holi {year}: Holika Dahan date and time in your city",
            "description": "Holi {year}: the Holika Dahan date and time, the end of Bhadra and the day of colours for {n} "
                           "cities in the USA, Canada, the UK, Australia and India.",
            "intro": [
                "Holika Dahan, the bonfire, is lit on the evening of Phalguna Purnima, in pradosh kaal after sunset while "
                "Purnima is in force, and Holi, the day of colours, is the next day. The first half of Purnima is Bhadra, "
                "which tradition avoids for the bonfire, so it is lit after Bhadra ends. Purnima begins and ends at one "
                "instant worldwide, but sunset is local, so the date and the time can differ between India and a city "
                "abroad.",
                "The table gives, for each city, the day of Holika Dahan, the part of that evening's pradosh kaal when "
                "Purnima is in force and Bhadra is over, the time Bhadra ends, and the day of Holi. All times are local, "
                "with daylight saving allowed for.",
            ],
            "cols": ["City", "Holika Dahan", "Time to light", "Bhadra ends", "Holi"],
            "note": "Where Purnima is in force in both evenings, the evening it covers more of is taken. Where Bhadra ends "
                    "after pradosh kaal but before midnight, the time is given from the end of Bhadra. Where it lasts past "
                    "midnight, tradition lights the fire in the tail of Bhadra or in pradosh kaal, and practice varies, so "
                    "follow your temple's time.",
            "faq": [
                ("Why is Holi on a different date in {example_city} than in India?",
                 "The bonfire belongs to the evening, and the evening comes to each city at a different point in the "
                 "Purnima tithi. When Purnima begins after sunset in one city and before it in another, the date "
                 "differs, and Holi, the next day, moves with it."),
                ("What is Bhadra and why is it avoided?",
                 "Bhadra is Vishti karana, which falls in the first half of Purnima. Tradition holds it unlucky for "
                 "beginnings, so the bonfire is lit after it ends. When it runs late into the night, communities follow "
                 "the time their temple gives."),
                ("Which day are colours played?",
                 "The morning after Holika Dahan. In many places the day is also called Dhulandi or Rangwali Holi."),
            ],
        },
        "hi": {
            "title": "होली {year}: तारीख और होलिका दहन का समय, शहर के अनुसार (अमेरिका, कनाडा, ब्रिटेन, ऑस्ट्रेलिया, भारत)",
            "h1": "होली {year}: आपके शहर में होलिका दहन की तारीख और समय",
            "description": "होली {year}: अमेरिका, कनाडा, ब्रिटेन, ऑस्ट्रेलिया और भारत के {n} शहरों के लिए होलिका दहन की तारीख और "
                           "समय, भद्रा की समाप्ति और रंगों का दिन।",
            "intro": [
                "होलिका दहन फाल्गुन पूर्णिमा की शाम को, सूर्यास्त के बाद के प्रदोष काल में, पूर्णिमा रहते होता है, और रंगों की "
                "होली अगले दिन। पूर्णिमा का पहला आधा भाग भद्रा है, जिसे परंपरा दहन के लिए टालती है, इसलिए दहन भद्रा समाप्त होने "
                "के बाद होता है। पूर्णिमा पूरे संसार में एक ही क्षण आरंभ और समाप्त होती है, पर सूर्यास्त स्थानीय है, इसलिए भारत "
                "और विदेश के किसी शहर में तारीख और समय अलग हो सकते हैं।",
                "तालिका हर शहर के लिए होलिका दहन का दिन, उस शाम के प्रदोष काल का वह भाग जिसमें पूर्णिमा चल रही हो और भद्रा बीत "
                "चुकी हो, भद्रा समाप्ति का समय और होली का दिन देती है। सभी समय स्थानीय हैं, डेलाइट सेविंग सहित।",
            ],
            "cols": ["शहर", "होलिका दहन", "दहन का समय", "भद्रा समाप्त", "होली"],
            "note": "जहाँ पूर्णिमा दोनों शामों के प्रदोष काल में हो, वहाँ वह शाम ली गई है जिसका अधिक भाग वह ढकती है। जहाँ भद्रा "
                    "प्रदोष काल के बाद पर आधी रात से पहले समाप्त हो, वहाँ समय भद्रा समाप्ति से दिया गया है। जहाँ वह आधी रात के बाद "
                    "तक चले, परंपरा दहन भद्रा पुच्छ में या प्रदोष काल में करती है, और प्रथा अलग-अलग है, इसलिए अपने मंदिर का समय "
                    "मानें।",
            "faq": [
                ("{example_city} में होली भारत से अलग तारीख को क्यों है?",
                 "दहन शाम का है, और शाम हर शहर में पूर्णिमा तिथि के अलग बिंदु पर आती है। जब पूर्णिमा एक शहर में सूर्यास्त के बाद "
                 "और दूसरे में उससे पहले आरंभ होती है, तारीख अलग हो जाती है, और अगले दिन की होली भी उसके साथ खिसकती है।"),
                ("भद्रा क्या है और इसे क्यों टालते हैं?",
                 "भद्रा विष्टि करण है, जो पूर्णिमा के पहले आधे भाग में पड़ता है। परंपरा इसे शुभ आरंभ के लिए अशुभ मानती है, इसलिए "
                 "दहन इसके समाप्त होने के बाद होता है। जब यह रात में देर तक चले, समुदाय अपने मंदिर का बताया समय मानते हैं।"),
                ("रंग किस दिन खेले जाते हैं?",
                 "होलिका दहन के अगले दिन, सुबह। कई जगह इस दिन को धुलंडी या रंगवाली होली भी कहते हैं।"),
            ],
        },
    },
    "navratri": {
        "slug": "navratri",
        "en": {
            "title": "Navratri {year}: Chaitra and Sharad Navratri Dates by City (USA, Canada, UK, Australia, India)",
            "h1": "Navratri {year}: Chaitra and Sharad Navratri dates in your city",
            "description": "Navratri {year}: when Chaitra and Sharad Navratri begin, and Ram Navami, for {n} cities in the "
                           "USA, Canada, UK, Australia and India.",
            "intro": [
                "Navratri, the nine nights of the Goddess, comes twice a year. Chaitra Navratri begins on Chaitra Shukla "
                "Pratipada in spring and ends with Ram Navami; Sharad Navratri begins on Ashwin Shukla Pratipada in "
                "autumn and is followed by Dussehra. Each begins on the day Pratipada is in force at the local sunrise, "
                "with Ghatasthapana that morning, so the first day can differ between India and a city abroad.",
                "The table gives, for each city, the day each Navratri begins and the day of Ram Navami, the Navami "
                "whose midday Navami covers more. The Ashtami, Navami and Dussehra of the autumn Navratri follow rules "
                "about the tithi in force at two sunrises that calendars apply differently, so follow your temple for "
                "those days.",
            ],
            "cols": ["City", "Chaitra Navratri begins", "Ram Navami", "Sharad Navratri begins"],
            "note": "Where Pratipada is in force at neither sunrise, Navratri begins on the day it starts; where a tithi "
                    "is lost or repeated, the nine nights can be eight or ten days.",
            "faq": [
                ("Why does Navratri begin on a different day in {example_city} than in India?",
                 "Pratipada begins at one instant worldwide, but each city meets its own sunrise. When Pratipada begins "
                 "after sunrise in India and before sunrise in a city far to the west, or the other way round, the first "
                 "day differs."),
                ("Is Ram Navami on the same day everywhere?",
                 "No. It is the day whose midday Navami covers, and midday comes at a different moment of the tithi in "
                 "each city: in 2027 several cities in North America and the UK keep it a day before India."),
                ("When is Dussehra?",
                 "After the autumn Navratri, on the Dashami that holds the afternoon. Each city's own page lists it; for "
                 "the Ashtami and Navami days, follow your temple."),
            ],
        },
        "hi": {
            "title": "नवरात्रि {year}: चैत्र और शारदीय नवरात्रि की तारीखें, शहर के अनुसार (अमेरिका, कनाडा, ब्रिटेन, ऑस्ट्रेलिया, भारत)",
            "h1": "नवरात्रि {year}: आपके शहर में चैत्र और शारदीय नवरात्रि की तारीखें",
            "description": "नवरात्रि {year}: अमेरिका, कनाडा, ब्रिटेन, ऑस्ट्रेलिया और भारत के {n} शहरों में चैत्र और शारदीय नवरात्रि "
                           "कब आरंभ होती है, और राम नवमी।",
            "intro": [
                "नवरात्रि, देवी की नौ रातें, वर्ष में दो बार आती है। चैत्र नवरात्रि वसंत में चैत्र शुक्ल प्रतिपदा से आरंभ होकर राम नवमी पर "
                "पूरी होती है; शारदीय नवरात्रि शरद में आश्विन शुक्ल प्रतिपदा से आरंभ होती है और उसके बाद दशहरा आता है। हर नवरात्रि उस "
                "दिन आरंभ होती है जिस दिन स्थानीय सूर्योदय पर प्रतिपदा हो, और उसी सुबह घटस्थापना होती है, इसलिए भारत और विदेश के किसी "
                "शहर में पहला दिन अलग हो सकता है।",
                "तालिका हर शहर के लिए दोनों नवरात्रियों के आरंभ का दिन और राम नवमी का दिन देती है, वह नवमी जिसके मध्याह्न का अधिक भाग "
                "नवमी ढकती है। शारदीय नवरात्रि की अष्टमी, नवमी और दशहरा दो सूर्योदयों पर चल रही तिथि के उन नियमों पर चलते हैं जिन्हें "
                "पंचांग अलग-अलग ढंग से लगाते हैं, इसलिए उन दिनों के लिए अपने मंदिर को मानें।",
            ],
            "cols": ["शहर", "चैत्र नवरात्रि आरंभ", "राम नवमी", "शारदीय नवरात्रि आरंभ"],
            "note": "जहाँ प्रतिपदा किसी भी सूर्योदय पर न हो, वहाँ नवरात्रि उसी दिन आरंभ होती है जिस दिन वह शुरू होती है; जहाँ कोई "
                    "तिथि क्षय या वृद्धि हो, वहाँ नौ रातें आठ या दस दिन की हो सकती हैं।",
            "faq": [
                ("{example_city} में नवरात्रि भारत से अलग दिन क्यों आरंभ होती है?",
                 "प्रतिपदा पूरे संसार में एक ही क्षण आरंभ होती है, पर हर शहर का सूर्योदय अपना है। जब प्रतिपदा भारत में सूर्योदय के बाद "
                 "और पश्चिम के किसी दूर शहर में सूर्योदय से पहले आरंभ हो, या इसके उलट, तो पहला दिन अलग हो जाता है।"),
                ("क्या राम नवमी हर जगह एक ही दिन है?",
                 "नहीं। यह वह दिन है जिसके मध्याह्न को नवमी ढकती है, और मध्याह्न हर शहर में तिथि के अलग क्षण पर आता है: 2027 में उत्तर "
                 "अमेरिका और ब्रिटेन के कई शहर इसे भारत से एक दिन पहले मनाते हैं।"),
                ("दशहरा कब है?",
                 "शारदीय नवरात्रि के बाद, उस दशमी को जो अपराह्न में हो। हर शहर का अपना पृष्ठ इसे देता है; अष्टमी और नवमी के दिनों के "
                 "लिए अपने मंदिर को मानें।"),
            ],
        },
    },
    "raksha_bandhan": {
        "slug": "raksha-bandhan",
        "en": {
            "title": "Raksha Bandhan {year}: Date and Rakhi Time by City (USA, Canada, UK, Australia, India)",
            "h1": "Raksha Bandhan {year}: date and rakhi time in your city",
            "description": "When is Raksha Bandhan {year}? The date and the time to tie rakhi after Bhadra, for {n} cities "
                           "in the USA, Canada, UK, Australia and India.",
            "intro": [
                "Raksha Bandhan falls on Shravana Purnima: the day is the one whose forenoon Purnima holds, or holds more "
                "of where it touches two. The first half of Purnima is Bhadra, which tradition avoids, so rakhi is tied "
                "after Bhadra ends and while Purnima lasts, in daylight or in the evening hours after sunset. Purnima "
                "begins and ends at one instant worldwide, but each city's day is its own, so the date and the time "
                "differ between India and a city abroad.",
                "The table gives, for each city, the day of Raksha Bandhan, the time to tie rakhi (from the end of "
                "Bhadra, or sunrise, until Purnima ends or the evening hours close), the end of Bhadra and the end of "
                "Purnima. All times are local, with daylight saving allowed for.",
            ],
            "cols": ["City", "Raksha Bandhan", "Time to tie rakhi", "Bhadra ends", "Purnima ends"],
            "note": "Where no time is shown, Bhadra lasts until Purnima ends that day: families then follow their "
                    "temple's time.",
            "faq": [
                ("Why is Raksha Bandhan on a different date in {example_city} than in India?",
                 "The day is set by where Purnima falls in each city's own day. For a city many hours behind India, "
                 "Purnima can hold the forenoon of the earlier date, so the festival comes a day before India's."),
                ("What is Bhadra and why is it avoided?",
                 "Bhadra is Vishti karana, the first half of Purnima. Tradition holds it unlucky for tying rakhi, so the "
                 "time given starts when it ends."),
                ("Can rakhi be tied after sunset?",
                 "Yes, in the evening hours after sunset (pradosh kaal) while Purnima lasts, which the time given includes "
                 "when Bhadra ends late in the day."),
            ],
        },
        "hi": {
            "title": "रक्षा बंधन {year}: तारीख और राखी बाँधने का समय, शहर के अनुसार (अमेरिका, कनाडा, ब्रिटेन, ऑस्ट्रेलिया, भारत)",
            "h1": "रक्षा बंधन {year}: आपके शहर में तारीख और राखी बाँधने का समय",
            "description": "रक्षा बंधन {year} कब है? अमेरिका, कनाडा, ब्रिटेन, ऑस्ट्रेलिया और भारत के {n} शहरों के लिए तारीख और भद्रा "
                           "के बाद राखी बाँधने का समय।",
            "intro": [
                "रक्षा बंधन श्रावण पूर्णिमा को होता है: दिन वह है जिसके पूर्वाह्न में पूर्णिमा हो, और दो दिनों को छूने पर जिसका अधिक भाग "
                "वह ढके। पूर्णिमा का पहला आधा भाग भद्रा है, जिसे परंपरा टालती है, इसलिए राखी भद्रा समाप्त होने के बाद और पूर्णिमा रहते "
                "बाँधी जाती है, दिन में या सूर्यास्त के बाद की शाम में। पूर्णिमा पूरे संसार में एक ही क्षण आरंभ और समाप्त होती है, पर हर "
                "शहर का दिन अपना है, इसलिए भारत और विदेश के किसी शहर में तारीख और समय अलग होते हैं।",
                "तालिका हर शहर के लिए रक्षा बंधन का दिन, राखी बाँधने का समय (भद्रा समाप्ति या सूर्योदय से, पूर्णिमा समाप्ति या शाम के "
                "प्रदोष काल के अंत तक), भद्रा की समाप्ति और पूर्णिमा की समाप्ति देती है। सभी समय स्थानीय हैं, डेलाइट सेविंग सहित।",
            ],
            "cols": ["शहर", "रक्षा बंधन", "राखी बाँधने का समय", "भद्रा समाप्त", "पूर्णिमा समाप्त"],
            "note": "जहाँ समय नहीं दिया गया, वहाँ उस दिन भद्रा पूर्णिमा समाप्त होने तक रहती है: तब परिवार अपने मंदिर का समय मानते हैं।",
            "faq": [
                ("{example_city} में रक्षा बंधन भारत से अलग तारीख को क्यों है?",
                 "दिन इस बात से तय होता है कि पूर्णिमा हर शहर के अपने दिन में कहाँ पड़ती है। भारत से कई घंटे पीछे के शहर में पूर्णिमा "
                 "पिछली तारीख के पूर्वाह्न में हो सकती है, इसलिए पर्व भारत से एक दिन पहले आता है।"),
                ("भद्रा क्या है और इसे क्यों टालते हैं?",
                 "भद्रा विष्टि करण है, पूर्णिमा का पहला आधा भाग। परंपरा इसे राखी बाँधने के लिए अशुभ मानती है, इसलिए दिया गया समय इसके "
                 "समाप्त होने से आरंभ होता है।"),
                ("क्या सूर्यास्त के बाद राखी बाँध सकते हैं?",
                 "हाँ, सूर्यास्त के बाद की शाम (प्रदोष काल) में जब तक पूर्णिमा हो; जब भद्रा दिन में देर से समाप्त हो, तो दिया गया समय "
                 "इसे भी शामिल करता है।"),
            ],
        },
    },
    "janmashtami": {
        "slug": "janmashtami",
        "en": {
            "title": "Janmashtami {year}: Date and Midnight Puja Time by City (USA, Canada, UK, Australia, India)",
            "h1": "Krishna Janmashtami {year}: date and midnight puja time in your city",
            "description": "Janmashtami {year}: the night of the fast and the nishita puja time at midnight for {n} cities "
                           "in the USA, Canada, UK, Australia and India.",
            "intro": [
                "Krishna Janmashtami is kept on the Ashtami of the dark fortnight of Bhadrapada, with a fast through the "
                "day and the worship of Krishna's birth at nishita kaal, the muhurta at the middle of the night. The "
                "night is the one whose midnight muhurta Ashtami holds; where it holds both, the later. Because the "
                "puja hour falls after midnight, it belongs to the next calendar date, which is why some calendars print "
                "that date.",
                "The table gives, for each city, the night of Janmashtami, the nishita puja time, and the time Ashtami "
                "ends. This is the date most households and Smarta calendars keep; Vaishnava and ISKCON temples often "
                "keep the following day, so follow your temple if you belong to one.",
            ],
            "cols": ["City", "Janmashtami (night of)", "Nishita puja", "Ashtami ends"],
            "note": "Where Ashtami holds the midnight muhurta of neither night, the later day it touches is taken.",
            "faq": [
                ("Is Janmashtami on the 24th or the 25th?",
                 "The fast and the midnight puja belong to one night. The puja hour falls just after midnight, so "
                 "calendars that print the date of the puja show the next date. The table gives the night, with the puja "
                 "time beside it. Vaishnava and ISKCON temples may keep the next day."),
                ("Why is Janmashtami on a different date in {example_city} than in India?",
                 "Midnight comes to each city at a different point of the Ashtami tithi, so the night it holds can differ "
                 "from Delhi's."),
                ("When is the fast broken?",
                 "Traditionally after the midnight puja, or the next morning after sunrise; follow your family's practice."),
            ],
        },
        "hi": {
            "title": "जन्माष्टमी {year}: तारीख और मध्यरात्रि पूजा का समय, शहर के अनुसार (अमेरिका, कनाडा, ब्रिटेन, ऑस्ट्रेलिया, भारत)",
            "h1": "कृष्ण जन्माष्टमी {year}: आपके शहर में तारीख और मध्यरात्रि पूजा का समय",
            "description": "जन्माष्टमी {year}: अमेरिका, कनाडा, ब्रिटेन, ऑस्ट्रेलिया और भारत के {n} शहरों के लिए व्रत की रात और "
                           "मध्यरात्रि की निशीथ पूजा का समय।",
            "intro": [
                "कृष्ण जन्माष्टमी भाद्रपद कृष्ण अष्टमी को रखी जाती है, दिन भर व्रत और निशीथ काल में, रात के मध्य के मुहूर्त में, कृष्ण "
                "जन्म की पूजा के साथ। रात वह है जिसके मध्य मुहूर्त में अष्टमी हो; दोनों रातों में हो तो बाद वाली। पूजा का समय आधी रात "
                "के बाद पड़ता है, इसलिए वह अगली तारीख में आता है, और इसीलिए कुछ पंचांग वही तारीख छापते हैं।",
                "तालिका हर शहर के लिए जन्माष्टमी की रात, निशीथ पूजा का समय और अष्टमी की समाप्ति देती है। यह वह तारीख है जो अधिकांश "
                "परिवार और स्मार्त पंचांग मानते हैं; वैष्णव और इस्कॉन मंदिर प्रायः अगला दिन मानते हैं, इसलिए यदि आप किसी से जुड़े हैं तो "
                "अपने मंदिर को मानें।",
            ],
            "cols": ["शहर", "जन्माष्टमी (रात)", "निशीथ पूजा", "अष्टमी समाप्त"],
            "note": "जहाँ अष्टमी किसी भी रात के मध्य मुहूर्त में न हो, वहाँ वह बाद वाला दिन लिया गया है जिसे वह छूती है।",
            "faq": [
                ("जन्माष्टमी 24 को है या 25 को?",
                 "व्रत और मध्यरात्रि पूजा एक ही रात के हैं। पूजा का समय आधी रात के ठीक बाद पड़ता है, इसलिए जो पंचांग पूजा की तारीख "
                 "छापते हैं, वे अगली तारीख दिखाते हैं। तालिका रात देती है, साथ में पूजा का समय। वैष्णव और इस्कॉन मंदिर अगला दिन मान "
                 "सकते हैं।"),
                ("{example_city} में जन्माष्टमी भारत से अलग तारीख को क्यों है?",
                 "हर शहर की आधी रात अष्टमी तिथि के अलग बिंदु पर आती है, इसलिए जिस रात को वह ढकती है वह दिल्ली से अलग हो सकती है।"),
                ("व्रत कब खोलें?",
                 "परंपरा से मध्यरात्रि पूजा के बाद, या अगली सुबह सूर्योदय के बाद; अपने परिवार की रीति मानें।"),
            ],
        },
    },
    "ganesh_chaturthi": {
        "slug": "ganesh-chaturthi",
        "en": {
            "title": "Ganesh Chaturthi {year}: Date, Puja Time and Visarjan by City (USA, Canada, UK, Australia, India)",
            "h1": "Ganesh Chaturthi {year}: date, puja time and visarjan in your city",
            "description": "Ganesh Chaturthi {year}: the date, the midday puja time and the Anant Chaturdashi visarjan for "
                           "{n} cities in the USA, Canada, UK, Australia and India.",
            "intro": [
                "Ganesh Chaturthi is kept on the Chaturthi of the bright fortnight of Bhadrapada, with the installation "
                "and worship of Ganesha at madhyahna, the middle part of the day. The day is the one whose madhyahna "
                "Chaturthi holds, or holds more of where it touches two. The festival closes with the visarjan on "
                "Anant Chaturdashi, ten days later.",
                "The table gives, for each city, the day of Ganesh Chaturthi, the part of madhyahna in which Chaturthi "
                "is still in force, and the day of Anant Chaturdashi. Many calendars print the whole madhyahna, which "
                "can run past the end of Chaturthi. All times are local, with daylight saving allowed for.",
            ],
            "cols": ["City", "Ganesh Chaturthi", "Madhyahna puja", "Visarjan (Anant Chaturdashi)"],
            "note": "Where Chaturthi holds the madhyahna of both days, the day it covers more of is taken.",
            "faq": [
                ("Why is Ganesh Chaturthi on a different date in {example_city} than in India?",
                 "The puja belongs to the middle of the day, and midday comes to each city at a different point of the "
                 "Chaturthi tithi. In 2027 cities in North America keep it a day before India."),
                ("Why should the moon not be seen on Ganesh Chaturthi?",
                 "By tradition, seeing the moon that night brings a false accusation (mithya dosha). The moonrise for "
                 "each night is on the city's page."),
                ("When is the visarjan?",
                 "On Anant Chaturdashi, the Chaturdashi of the same fortnight. Families who keep Ganesha for one and a "
                 "half, three, five or seven days immerse him earlier."),
            ],
        },
        "hi": {
            "title": "गणेश चतुर्थी {year}: तारीख, पूजा का समय और विसर्जन, शहर के अनुसार (अमेरिका, कनाडा, ब्रिटेन, ऑस्ट्रेलिया, भारत)",
            "h1": "गणेश चतुर्थी {year}: आपके शहर में तारीख, पूजा का समय और विसर्जन",
            "description": "गणेश चतुर्थी {year}: अमेरिका, कनाडा, ब्रिटेन, ऑस्ट्रेलिया और भारत के {n} शहरों के लिए तारीख, मध्याह्न पूजा "
                           "का समय और अनंत चतुर्दशी का विसर्जन।",
            "intro": [
                "गणेश चतुर्थी भाद्रपद शुक्ल चतुर्थी को रखी जाती है, मध्याह्न में, दिन के मध्य भाग में, गणेश जी की स्थापना और पूजा के "
                "साथ। दिन वह है जिसके मध्याह्न में चतुर्थी हो, और दो दिनों को छूने पर जिसका अधिक भाग वह ढके। पर्व दस दिन बाद अनंत "
                "चतुर्दशी के विसर्जन से पूरा होता है।",
                "तालिका हर शहर के लिए गणेश चतुर्थी का दिन, मध्याह्न का वह भाग जिसमें चतुर्थी अभी चल रही हो, और अनंत चतुर्दशी का दिन देती "
                "है। कई पंचांग पूरा मध्याह्न छापते हैं, जो चतुर्थी समाप्त होने के बाद तक जा सकता है। सभी समय स्थानीय हैं, डेलाइट सेविंग "
                "सहित।",
            ],
            "cols": ["शहर", "गणेश चतुर्थी", "मध्याह्न पूजा", "विसर्जन (अनंत चतुर्दशी)"],
            "note": "जहाँ चतुर्थी दोनों दिनों के मध्याह्न में हो, वहाँ वह दिन लिया गया है जिसका अधिक भाग वह ढकती है।",
            "faq": [
                ("{example_city} में गणेश चतुर्थी भारत से अलग तारीख को क्यों है?",
                 "पूजा दिन के मध्य की है, और मध्याह्न हर शहर में चतुर्थी तिथि के अलग बिंदु पर आता है। 2027 में उत्तर अमेरिका के शहर इसे "
                 "भारत से एक दिन पहले मनाते हैं।"),
                ("गणेश चतुर्थी पर चंद्रमा क्यों नहीं देखना चाहिए?",
                 "परंपरा के अनुसार उस रात चंद्र दर्शन से झूठा कलंक (मिथ्या दोष) लगता है। हर रात का चंद्रोदय शहर के पृष्ठ पर है।"),
                ("विसर्जन कब है?",
                 "अनंत चतुर्दशी को, उसी पक्ष की चतुर्दशी। जो परिवार गणेश जी को डेढ़, तीन, पाँच या सात दिन रखते हैं, वे पहले विसर्जन "
                 "करते हैं।"),
            ],
        },
    },
    "sankashti": {
        "slug": "sankashti-chaturthi",
        "en": {
            "title": "Sankashti Chaturthi {year} Dates and Moonrise Times by City",
            "h1": "Sankashti Chaturthi {year}: dates and moonrise in your city",
            "description": "Sankashti Chaturthi {year}: every date with the moonrise time for {n} cities in the USA, "
                           "Canada, UK, Australia and India, Angarki included.",
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
            "description": "Is today Ekadashi? Every Ekadashi of {year} with the parana time to break the fast, for {n} "
                           "cities in the USA, Canada, UK, Australia and India.",
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
        "description": "How this panchang is worked out: the JPL ephemeris, the Lahiri ayanamsa, sunrise, the Hindu day, "
                       "the muhurtas and the rules that date each festival.",
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
              "part on each weekday, and into fifteen muhurtas, of which Abhijit is the eighth, around midday, except on "
              "Wednesdays, when that muhurta is a Dur Muhurta and Abhijit is not used. The night is divided into fifteen "
              "muhurtas too, and Brahma Muhurta is the second-last before sunrise. Choghadiya divides day and night into "
              "eight parts each: by day the names follow the order of the planetary hours from the weekday's lord; by "
              "night they begin from the lord of the fifth weekday and follow another order. Because all of these are "
              "fractions of the local day, they move with the seasons and with the place."]),
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
              "मुहूर्तों में, जिनमें अभिजित आठवाँ है, दोपहर के आसपास, बुधवार को छोड़कर, जब वह मुहूर्त दुर्मुहूर्त होता है और अभिजित नहीं "
              "लिया जाता। रात भी पंद्रह मुहूर्तों में बँटती है, और ब्रह्म मुहूर्त सूर्योदय से पहले का दूसरा अंतिम है। चौघड़िया दिन और रात को "
              "आठ-आठ भागों में बाँटता है: दिन में नाम वार के स्वामी से होरा के क्रम में चलते हैं; रात में वे पाँचवें वार के स्वामी से आरंभ "
              "होकर दूसरे क्रम में चलते हैं। ये सब स्थानीय दिन के भाग हैं, इसलिए ऋतु और स्थान के साथ बदलते हैं।"]),
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

# The shubh muhurat page of a city, built 16 Nov 2026: the day's general good times, from the times the city page
# already computes, for today, tomorrow and the week. No wedding, griha pravesh or other event muhurat: those need
# rules and checks this site has not made. Descriptions within 155 characters for the longest city name.
MUHURAT = {
    "en": {
        "title": "Shubh Muhurat Today in {city} | Abhijit, Brahma Muhurta, Choghadiya",
        "description": "Shubh muhurat today in {city}: Brahma Muhurta, Abhijit and the good choghadiya, Rahu Kaal "
                       "left out, for today, tomorrow and the week.",
        "h1": "Shubh Muhurat Today in {city}",
        "crumb": "Shubh Muhurat",
        "intro": "The good times of the day in {city}, from {city}'s own sunrise and sunset: Brahma Muhurta before "
                 "dawn, Abhijit around midday, and the Amrit, Shubh and Labh choghadiya, leaving out any that fall in "
                 "Rahu Kaal, Yamaganda or Gulika. Every time is on {city}'s clock, daylight saving included.",
        "now_h": "Right now in {city}",
        "best_h": "Good times",
        "best_note": "Amrit, Shubh and Labh choghadiya, leaving out any that fall in Rahu Kaal, Yamaganda or Gulika. "
                     "Abhijit is given in full, as panchangs print it.",
        "chogh_h": "Choghadiya",
        "week_h": "Brahma Muhurta, Abhijit and Rahu Kaal in {city} this week",
        "year_h": "Muhurat times in {city} through the year",
        "year": "In {year}, Brahma Muhurta in {city} begins as early as {bm_early} ({bm_early_d}) and as late as "
                "{bm_late} ({bm_late_d}). Abhijit, the muhurta around local noon, begins between {ab_early} "
                "({ab_early_d}) and {ab_late} ({ab_late_d}).",
        "dst_yes": "{city} moves its clocks forward on {start} and back on {end} in {year}. The times on this page "
                   "already allow for it: on those days every muhurat moves by an hour on the clock, with the sunrise.",
        "dst_no": "{city} keeps the same clock all year, so its muhurat times move only with the seasons.",
        "events_h": "Weddings, griha pravesh and other ceremonies",
        "events": "This page gives the day's general good times. A muhurat for a wedding, a griha pravesh, a mundan "
                  "or a new vehicle is chosen by many more rules, often with the family's own details, and is not "
                  "given here; families usually ask their own priest.",
        "explain_h": "What these times are",
        "explain": [
            "Brahma Muhurta: the second-last muhurta of the night, ending one muhurta before sunrise; the time "
            "tradition keeps for prayer, meditation and study.",
            "Abhijit Muhurat: the eighth of the day's fifteen muhurtas, around local noon, held good for beginning "
            "important work. It is not used on Wednesdays, when that muhurta is a Dur Muhurta.",
            "Choghadiya: the day and the night, each divided into eight parts. Amrit, Shubh and Labh are good, Chal "
            "(also called Char) is neutral and traditionally used for travel, and Udveg, Kaal and Rog are avoided for "
            "beginnings.",
            "Rahu Kaal, Yamaganda and Gulika: eighths of the day, a different one on each weekday, that tradition "
            "avoids for starting something new.",
        ],
        "faq": [
            ("What is the shubh muhurat today in {city}?",
             "The list at the top of this page: today's Brahma Muhurta, Abhijit Muhurat and the Amrit, Shubh and Labh "
             "choghadiya for {city}, in local time, leaving out any choghadiya that falls in Rahu Kaal, Yamaganda or "
             "Gulika. It changes every day with {city}'s sunrise and sunset."),
            ("Is Abhijit Muhurat used on Wednesday?",
             "No. On a Wednesday the eighth muhurta of the day, the one that is Abhijit on other days, is a Dur "
             "Muhurta, so panchangs give no Abhijit that day."),
            ("When is Brahma Muhurta tomorrow in {city}?",
             "Press Tomorrow at the top of the page, or see the week's table. Brahma Muhurta ends one muhurta before "
             "{city}'s sunrise, so it moves a little every day with the sunrise."),
            ("Which choghadiya is good for travel?",
             "Chal, also called Char, the one tradition names for travel. Amrit, Shubh and Labh are good for most work; "
             "Udveg, Kaal and "
             "Rog are avoided for beginnings."),
            ("Can I begin something in Rahu Kaal if the choghadiya is good?",
             "Many families wait for Rahu Kaal to pass even then, and this page leaves such a choghadiya out of the "
             "good times. The choghadiya tables still show it."),
            ("Does daylight saving change the muhurat times in {city}?", "{dst}"),
        ],
        "labels": {
            "tomorrow": "Tomorrow", "now": "Now", "nowGood": "a good time",
            "nowNeutral": "neutral, traditionally for travel", "nowBad": "avoided for beginnings",
            "nowAvoid": "tradition avoids beginning new work now", "nextGood": "Next good time",
            "noneLeft": "No good time is left before the next sunrise.", "choghWord": "choghadiya",
            "leftOut": "Left out, falling in Rahu Kaal, Yamaganda or Gulika:",
            "hintBrahma": "prayer, meditation and study", "hintAbhijit": "beginning important work",
            "hintAmrit": "all good work", "hintShubh": "worship and ceremonies", "hintLabh": "business and education",
            "colDate": "Date", "colBrahma": "Brahma Muhurta", "colAbhijit": "Abhijit", "colRahu": "Rahu Kaal",
            "noneWed": "none on Wednesday", "shareHeadM": "Shubh muhurat in {city}", "shareGood": "Good choghadiya",
            # labels pass through str.format with the city's words, so the page's own placeholder is doubled
            "tillFmt": "till {{t}}", "stop": ".", "afterFmt": "after {{x}}",
            "clashFmt": "Today Abhijit overlaps {{x}} from {{a}} to {{b}}; families who keep {{x}} begin after it.",
        },
    },
    "hi": {
        "title": "{city} में आज का शुभ मुहूर्त | अभिजित, ब्रह्म मुहूर्त, चौघड़िया",
        "description": "{city} में आज का शुभ मुहूर्त: ब्रह्म मुहूर्त, अभिजित और शुभ चौघड़िया, राहु काल छोड़कर, आज, कल और "
                       "पूरे सप्ताह के लिए, स्थानीय समय में।",
        "h1": "{city} में आज का शुभ मुहूर्त",
        "crumb": "शुभ मुहूर्त",
        "intro": "{city} में दिन के शुभ समय, {city} के अपने सूर्योदय और सूर्यास्त से: भोर से पहले ब्रह्म मुहूर्त, दोपहर के "
                 "आसपास अभिजित, और अमृत, शुभ और लाभ चौघड़िया, उन्हें छोड़कर जो राहु काल, यमगंड या गुलिक में पड़ते हैं। हर "
                 "समय {city} की घड़ी में है, डेलाइट सेविंग सहित।",
        "now_h": "अभी {city} में",
        "best_h": "शुभ समय",
        "best_note": "अमृत, शुभ और लाभ चौघड़िया, उन्हें छोड़कर जो राहु काल, यमगंड या गुलिक में पड़ते हैं। अभिजित पूरा दिया "
                     "गया है, जैसा पंचांग छापते हैं।",
        "chogh_h": "चौघड़िया",
        "week_h": "{city} में इस सप्ताह ब्रह्म मुहूर्त, अभिजित और राहु काल",
        "year_h": "{city} में वर्ष भर मुहूर्त के समय",
        "year": "{year} में {city} में ब्रह्म मुहूर्त सबसे जल्दी {bm_early} ({bm_early_d}) और सबसे देर से {bm_late} "
                "({bm_late_d}) आरंभ होता है। अभिजित, स्थानीय दोपहर के आसपास का मुहूर्त, {ab_early} ({ab_early_d}) से "
                "{ab_late} ({ab_late_d}) के बीच आरंभ होता है।",
        "dst_yes": "{city} में {year} में {start} को घड़ी एक घंटा आगे और {end} को पीछे होती है। इस पृष्ठ के समय इसे पहले "
                   "से मानकर चलते हैं: उन दिनों हर मुहूर्त घड़ी पर एक घंटा खिसकता है, सूर्योदय के साथ।",
        "dst_no": "{city} की घड़ी पूरे वर्ष एक-सी रहती है, इसलिए वहाँ मुहूर्त के समय केवल ऋतु के साथ बदलते हैं।",
        "events_h": "विवाह, गृह प्रवेश और अन्य संस्कार",
        "events": "यह पृष्ठ दिन के सामान्य शुभ समय देता है। विवाह, गृह प्रवेश, मुंडन या नए वाहन का मुहूर्त कई और नियमों से, "
                  "प्रायः परिवार के अपने विवरण के साथ, चुना जाता है, और यहाँ नहीं दिया गया; परिवार प्रायः अपने पुरोहित से "
                  "पूछते हैं।",
        "explain_h": "ये समय क्या हैं",
        "explain": [
            "ब्रह्म मुहूर्त: रात का दूसरा अंतिम मुहूर्त, जो सूर्योदय से एक मुहूर्त पहले समाप्त होता है; परंपरा इसे पूजा, ध्यान "
            "और अध्ययन के लिए रखती है।",
            "अभिजित मुहूर्त: दिन के पंद्रह मुहूर्तों में आठवाँ, स्थानीय दोपहर के आसपास, महत्वपूर्ण काम आरंभ करने के लिए शुभ "
            "माना जाता है। बुधवार को यह नहीं लिया जाता, क्योंकि उस दिन वह मुहूर्त दुर्मुहूर्त है।",
            "चौघड़िया: दिन और रात, हर एक आठ भागों में। अमृत, शुभ और लाभ शुभ हैं, चल (जिसे चर भी कहते हैं) सम है और परंपरा से यात्रा के लिए लिया "
            "जाता है, और उद्वेग, काल और रोग आरंभ के लिए वर्जित हैं।",
            "राहु काल, यमगंड और गुलिक: दिन के आठवें भाग, हर वार को अलग, जिनमें परंपरा कुछ नया आरंभ करने से बचती है।",
        ],
        "faq": [
            ("{city} में आज का शुभ मुहूर्त क्या है?",
             "इस पृष्ठ के ऊपर की सूची: {city} के लिए आज का ब्रह्म मुहूर्त, अभिजित मुहूर्त और अमृत, शुभ और लाभ चौघड़िया, "
             "स्थानीय समय में, उन चौघड़ियों को छोड़कर जो राहु काल, यमगंड या गुलिक में पड़ते हैं। यह {city} के सूर्योदय और "
             "सूर्यास्त के साथ हर दिन बदलती है।"),
            ("क्या बुधवार को अभिजित मुहूर्त लिया जाता है?",
             "नहीं। बुधवार को दिन का आठवाँ मुहूर्त, जो अन्य दिनों अभिजित होता है, दुर्मुहूर्त है, इसलिए पंचांग उस दिन अभिजित "
             "नहीं देते।"),
            ("{city} में कल ब्रह्म मुहूर्त कब है?",
             "पृष्ठ के ऊपर 'कल' दबाएँ, या सप्ताह की तालिका देखें। ब्रह्म मुहूर्त {city} के सूर्योदय से एक मुहूर्त पहले "
             "समाप्त होता है, इसलिए सूर्योदय के साथ हर दिन थोड़ा खिसकता है।"),
            ("यात्रा के लिए कौन-सा चौघड़िया शुभ है?",
             "चल, जिसे चर भी कहते हैं और परंपरा यात्रा के लिए बताती है। अमृत, शुभ और लाभ अधिकतर कामों के लिए शुभ हैं; उद्वेग, काल और रोग "
             "आरंभ के लिए वर्जित हैं।"),
            ("चौघड़िया शुभ हो तो क्या राहु काल में कोई काम आरंभ कर सकते हैं?",
             "बहुत-से परिवार तब भी राहु काल बीतने की प्रतीक्षा करते हैं, और यह पृष्ठ ऐसे चौघड़िया को शुभ समय से छोड़ देता है। "
             "चौघड़िया की तालिकाएँ उसे फिर भी दिखाती हैं।"),
            ("क्या डेलाइट सेविंग से {city} में मुहूर्त के समय बदलते हैं?", "{dst}"),
        ],
        "labels": {
            "tomorrow": "कल", "now": "अभी", "nowGood": "शुभ समय", "nowNeutral": "सम, परंपरा से यात्रा के लिए",
            "nowBad": "आरंभ के लिए वर्जित", "nowAvoid": "परंपरा अभी नया काम आरंभ करने से बचती है",
            "nextGood": "अगला शुभ समय", "noneLeft": "अगले सूर्योदय से पहले कोई शुभ समय शेष नहीं।", "choghWord": "चौघड़िया",
            "leftOut": "राहु काल, यमगंड या गुलिक में पड़ने से छोड़े गए:",
            "hintBrahma": "पूजा, ध्यान और अध्ययन", "hintAbhijit": "महत्वपूर्ण काम का आरंभ", "hintAmrit": "सभी शुभ कार्य",
            "hintShubh": "पूजा और संस्कार", "hintLabh": "व्यापार और शिक्षा",
            "colDate": "तारीख", "colBrahma": "ब्रह्म मुहूर्त", "colAbhijit": "अभिजित", "colRahu": "राहु काल",
            "noneWed": "बुधवार को नहीं", "shareHeadM": "{city} में शुभ मुहूर्त", "shareGood": "शुभ चौघड़िया",
            "tillFmt": "{{t}} तक", "stop": "।", "afterFmt": "{{x}} के बाद",
            "clashFmt": "आज अभिजित {{a}} से {{b}} तक {{x}} से मिलता है; जो परिवार {{x}} मानते हैं, वे उसके बाद आरंभ करते हैं।",
        },
    },
}
