"""The words of the panchang in English and Hindi, indexed the way engine.py counts them."""

TITHI = {
    "en": ["Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi", "Saptami", "Ashtami", "Navami",
           "Dashami", "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima",
           "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi", "Saptami", "Ashtami", "Navami",
           "Dashami", "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Amavasya"],
    "hi": ["प्रतिपदा", "द्वितीया", "तृतीया", "चतुर्थी", "पञ्चमी", "षष्ठी", "सप्तमी", "अष्टमी", "नवमी",
           "दशमी", "एकादशी", "द्वादशी", "त्रयोदशी", "चतुर्दशी", "पूर्णिमा",
           "प्रतिपदा", "द्वितीया", "तृतीया", "चतुर्थी", "पञ्चमी", "षष्ठी", "सप्तमी", "अष्टमी", "नवमी",
           "दशमी", "एकादशी", "द्वादशी", "त्रयोदशी", "चतुर्दशी", "अमावस्या"],
}
PAKSHA = {"en": {"shukla": "Shukla Paksha", "krishna": "Krishna Paksha"},
          "hi": {"shukla": "शुक्ल पक्ष", "krishna": "कृष्ण पक्ष"}}
NAKSHATRA = {
    "en": ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha",
           "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha",
           "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishtha", "Shatabhisha",
           "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"],
    "hi": ["अश्विनी", "भरणी", "कृत्तिका", "रोहिणी", "मृगशिरा", "आर्द्रा", "पुनर्वसु", "पुष्य", "आश्लेषा",
           "मघा", "पूर्वाफाल्गुनी", "उत्तराफाल्गुनी", "हस्त", "चित्रा", "स्वाति", "विशाखा", "अनुराधा",
           "ज्येष्ठा", "मूल", "पूर्वाषाढ़ा", "उत्तराषाढ़ा", "श्रवण", "धनिष्ठा", "शतभिषा",
           "पूर्वाभाद्रपद", "उत्तराभाद्रपद", "रेवती"],
}
YOGA = {
    "en": ["Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda", "Sukarma", "Dhriti", "Shula",
           "Ganda", "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata", "Variyana",
           "Parigha", "Shiva", "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma", "Indra", "Vaidhriti"],
    "hi": ["विष्कुम्भ", "प्रीति", "आयुष्मान", "सौभाग्य", "शोभन", "अतिगण्ड", "सुकर्मा", "धृति", "शूल",
           "गण्ड", "वृद्धि", "ध्रुव", "व्याघात", "हर्षण", "वज्र", "सिद्धि", "व्यतीपात", "वरीयान",
           "परिघ", "शिव", "सिद्ध", "साध्य", "शुभ", "शुक्ल", "ब्रह्म", "इन्द्र", "वैधृति"],
}
# karana by half-tithi index 0..59: Kimstughna first, the seven movable ones eight times, then the three fixed
_MOVABLE = {"en": ["Bava", "Balava", "Kaulava", "Taitila", "Garaja", "Vanija", "Vishti"],
            "hi": ["बव", "बालव", "कौलव", "तैतिल", "गर", "वणिज", "विष्टि"]}
_FIXED = {"en": {0: "Kimstughna", 57: "Shakuni", 58: "Chatushpada", 59: "Naga"},
          "hi": {0: "किंस्तुघ्न", 57: "शकुनि", 58: "चतुष्पाद", 59: "नाग"}}


def karana(index: int, lang: str) -> str:
    if index in _FIXED[lang]:
        return _FIXED[lang][index]
    return _MOVABLE[lang][(index - 1) % 7]


MONTH = {
    "en": ["Chaitra", "Vaishakha", "Jyeshtha", "Ashadha", "Shravana", "Bhadrapada", "Ashwina", "Kartika",
           "Margashirsha", "Pausha", "Magha", "Phalguna"],
    "hi": ["चैत्र", "वैशाख", "ज्येष्ठ", "आषाढ़", "श्रावण", "भाद्रपद", "आश्विन", "कार्तिक",
           "मार्गशीर्ष", "पौष", "माघ", "फाल्गुन"],
}
ADHIKA = {"en": "Adhika ", "hi": "अधिक "}
RASHI = {
    "en": ["Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya", "Tula", "Vrishchika", "Dhanu", "Makara",
           "Kumbha", "Meena"],
    "hi": ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुम्भ", "मीन"],
}
# Python weekday Mon=0 .. Sun=6
WEEKDAY = {
    "en": ["Somawara", "Mangalawara", "Budhawara", "Guruwara", "Shukrawara", "Shaniwara", "Raviwara"],
    "hi": ["सोमवार", "मंगलवार", "बुधवार", "गुरुवार", "शुक्रवार", "शनिवार", "रविवार"],
    "civil": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
}
# sidereal solar month index 0=Mesha -> season (two rashis each) and ayana
RITU = {
    "en": ["Vasanta", "Grishma", "Varsha", "Sharad", "Hemanta", "Shishira"],
    "hi": ["वसन्त", "ग्रीष्म", "वर्षा", "शरद", "हेमन्त", "शिशिर"],
}
AYANA = {"en": ["Uttarayana", "Dakshinayana"], "hi": ["उत्तरायण", "दक्षिणायन"]}
CHOGHADIYA = {
    "en": {"udveg": "Udveg", "chal": "Chal", "labh": "Labh", "amrit": "Amrit", "kaal": "Kaal", "shubh": "Shubh",
           "rog": "Rog"},
    "hi": {"udveg": "उद्वेग", "chal": "चल", "labh": "लाभ", "amrit": "अमृत", "kaal": "काल", "shubh": "शुभ", "rog": "रोग"},
}
# good, neutral or bad, for the colour of a choghadiya cell
CHOGHADIYA_TONE = {"amrit": "good", "shubh": "good", "labh": "good", "chal": "neutral", "udveg": "bad", "kaal": "bad",
                   "rog": "bad"}


def ritu(sun_rashi: int) -> int:
    return (sun_rashi // 2) % 6


def ayana(sun_rashi: int) -> int:
    """Uttarayana from Makara (9) to Mithuna (2), Dakshinayana from Karka (3) to Dhanu (8)."""
    return 1 if 3 <= sun_rashi <= 8 else 0
