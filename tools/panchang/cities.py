"""The places the panchang pages are built for. Coordinates are the city centres; the zone is the IANA name
the page uses to show the city's own clock, daylight saving included."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Place:
    slug: str
    en: str
    hi: str
    country_en: str
    country_hi: str
    lat: float
    lon: float
    tz: str


CITIES = [
    Place("delhi", "Delhi", "दिल्ली", "India", "भारत", 28.6139, 77.2090, "Asia/Kolkata"),
    Place("mumbai", "Mumbai", "मुंबई", "India", "भारत", 19.0760, 72.8777, "Asia/Kolkata"),
    Place("bengaluru", "Bengaluru", "बेंगलुरु", "India", "भारत", 12.9716, 77.5946, "Asia/Kolkata"),
    Place("kolkata", "Kolkata", "कोलकाता", "India", "भारत", 22.5726, 88.3639, "Asia/Kolkata"),
    Place("chennai", "Chennai", "चेन्नई", "India", "भारत", 13.0827, 80.2707, "Asia/Kolkata"),
    Place("hyderabad", "Hyderabad", "हैदराबाद", "India", "भारत", 17.3850, 78.4867, "Asia/Kolkata"),
    Place("ahmedabad", "Ahmedabad", "अहमदाबाद", "India", "भारत", 23.0225, 72.5714, "Asia/Kolkata"),
    Place("jaipur", "Jaipur", "जयपुर", "India", "भारत", 26.9124, 75.7873, "Asia/Kolkata"),
    Place("pune", "Pune", "पुणे", "India", "भारत", 18.5204, 73.8567, "Asia/Kolkata"),
    Place("lucknow", "Lucknow", "लखनऊ", "India", "भारत", 26.8467, 80.9462, "Asia/Kolkata"),
    Place("varanasi", "Varanasi", "वाराणसी", "India", "भारत", 25.3176, 82.9739, "Asia/Kolkata"),
    # United States: the metros with the largest Indian-origin populations (2020 census, combined statistical
    # areas), the highest advertising rates of any market
    Place("new-york", "New York", "न्यूयॉर्क", "United States", "अमेरिका", 40.7128, -74.0060, "America/New_York"),
    Place("new-jersey", "New Jersey (Edison)", "न्यू जर्सी (एडिसन)", "United States", "अमेरिका", 40.5187, -74.4121,
          "America/New_York"),
    Place("san-francisco", "San Francisco (Bay Area)", "सैन फ़्रांसिस्को (बे एरिया)", "United States", "अमेरिका",
          37.7749, -122.4194, "America/Los_Angeles"),
    Place("san-jose", "San Jose (South Bay)", "सैन होज़े (साउथ बे)", "United States", "अमेरिका", 37.3382, -121.8863,
          "America/Los_Angeles"),
    Place("chicago", "Chicago", "शिकागो", "United States", "अमेरिका", 41.8781, -87.6298, "America/Chicago"),
    Place("washington-dc", "Washington, D.C.", "वॉशिंगटन डी.सी.", "United States", "अमेरिका", 38.9072, -77.0369,
          "America/New_York"),
    Place("dallas", "Dallas", "डैलस", "United States", "अमेरिका", 32.7767, -96.7970, "America/Chicago"),
    Place("los-angeles", "Los Angeles", "लॉस एंजेलेस", "United States", "अमेरिका", 34.0522, -118.2437,
          "America/Los_Angeles"),
    Place("houston", "Houston", "ह्यूस्टन", "United States", "अमेरिका", 29.7604, -95.3698, "America/Chicago"),
    Place("philadelphia", "Philadelphia", "फ़िलाडेल्फ़िया", "United States", "अमेरिका", 39.9526, -75.1652, "America/New_York"),
    Place("atlanta", "Atlanta", "अटलांटा", "United States", "अमेरिका", 33.7490, -84.3880, "America/New_York"),
    Place("boston", "Boston", "बोस्टन", "United States", "अमेरिका", 42.3601, -71.0589, "America/New_York"),
    Place("seattle", "Seattle", "सिएटल", "United States", "अमेरिका", 47.6062, -122.3321, "America/Los_Angeles"),
    Place("detroit", "Detroit", "डेट्रॉइट", "United States", "अमेरिका", 42.3314, -83.0458, "America/Detroit"),
    Place("austin", "Austin", "ऑस्टिन", "United States", "अमेरिका", 30.2672, -97.7431, "America/Chicago"),
    Place("phoenix", "Phoenix", "फ़ीनिक्स", "United States", "अमेरिका", 33.4484, -112.0740, "America/Phoenix"),
    Place("sacramento", "Sacramento", "सैक्रामेंटो", "United States", "अमेरिका", 38.5816, -121.4944, "America/Los_Angeles"),
    Place("raleigh", "Raleigh", "रैले", "United States", "अमेरिका", 35.7796, -78.6382, "America/New_York"),
    Place("columbus", "Columbus", "कोलंबस", "United States", "अमेरिका", 39.9612, -82.9988, "America/New_York"),
    Place("charlotte", "Charlotte", "शार्लट", "United States", "अमेरिका", 35.2271, -80.8431, "America/New_York"),
    Place("minneapolis", "Minneapolis", "मिनियापोलिस", "United States", "अमेरिका", 44.9778, -93.2650, "America/Chicago"),
    Place("denver", "Denver", "डेनवर", "United States", "अमेरिका", 39.7392, -104.9903, "America/Denver"),
    Place("orlando", "Orlando", "ऑरलैंडो", "United States", "अमेरिका", 28.5383, -81.3792, "America/New_York"),
    Place("tampa", "Tampa", "टैम्पा", "United States", "अमेरिका", 27.9506, -82.4572, "America/New_York"),
    Place("san-diego", "San Diego", "सैन डिएगो", "United States", "अमेरिका", 32.7157, -117.1611, "America/Los_Angeles"),
    Place("portland", "Portland", "पोर्टलैंड", "United States", "अमेरिका", 45.5152, -122.6784, "America/Los_Angeles"),
    # Canada: the census metropolitan areas by Indian-origin population (2021), with the two Toronto-area cities
    # people name when they search
    Place("toronto", "Toronto", "टोरंटो", "Canada", "कनाडा", 43.6532, -79.3832, "America/Toronto"),
    Place("brampton", "Brampton", "ब्रैम्पटन", "Canada", "कनाडा", 43.7315, -79.7624, "America/Toronto"),
    Place("mississauga", "Mississauga", "मिसिसॉगा", "Canada", "कनाडा", 43.5890, -79.6441, "America/Toronto"),
    Place("vancouver", "Vancouver", "वैंकूवर", "Canada", "कनाडा", 49.2827, -123.1207, "America/Vancouver"),
    Place("surrey", "Surrey", "सरे", "Canada", "कनाडा", 49.1913, -122.8490, "America/Vancouver"),
    Place("calgary", "Calgary", "कैलगरी", "Canada", "कनाडा", 51.0447, -114.0719, "America/Edmonton"),
    Place("edmonton", "Edmonton", "एडमंटन", "Canada", "कनाडा", 53.5461, -113.4938, "America/Edmonton"),
    Place("montreal", "Montreal", "मॉन्ट्रियल", "Canada", "कनाडा", 45.5017, -73.5673, "America/Toronto"),
    Place("winnipeg", "Winnipeg", "विनिपेग", "Canada", "कनाडा", 49.8951, -97.1384, "America/Winnipeg"),
    Place("ottawa", "Ottawa", "ओटावा", "Canada", "कनाडा", 45.4215, -75.6972, "America/Toronto"),
    # United Kingdom: the local authorities with the largest Indian populations (2021 census)
    Place("london", "London", "लंदन", "United Kingdom", "ब्रिटेन", 51.5074, -0.1278, "Europe/London"),
    Place("leicester", "Leicester", "लेस्टर", "United Kingdom", "ब्रिटेन", 52.6369, -1.1398, "Europe/London"),
    Place("birmingham", "Birmingham", "बर्मिंघम", "United Kingdom", "ब्रिटेन", 52.4862, -1.8904, "Europe/London"),
    Place("wolverhampton", "Wolverhampton", "वॉल्वरहैम्पटन", "United Kingdom", "ब्रिटेन", 52.5870, -2.1288, "Europe/London"),
    Place("coventry", "Coventry", "कोवेंट्री", "United Kingdom", "ब्रिटेन", 52.4068, -1.5197, "Europe/London"),
    Place("slough", "Slough", "स्लाउ", "United Kingdom", "ब्रिटेन", 51.5105, -0.5950, "Europe/London"),
    Place("manchester", "Manchester", "मैनचेस्टर", "United Kingdom", "ब्रिटेन", 53.4808, -2.2426, "Europe/London"),
    Place("leeds", "Leeds", "लीड्स", "United Kingdom", "ब्रिटेन", 53.8008, -1.5491, "Europe/London"),
    Place("glasgow", "Glasgow", "ग्लासगो", "United Kingdom", "ब्रिटेन", 55.8642, -4.2518, "Europe/London"),
    # Australia and New Zealand: the capitals, by Indian-born population (2021 and 2023 censuses)
    Place("sydney", "Sydney", "सिडनी", "Australia", "ऑस्ट्रेलिया", -33.8688, 151.2093, "Australia/Sydney"),
    Place("melbourne", "Melbourne", "मेलबर्न", "Australia", "ऑस्ट्रेलिया", -37.8136, 144.9631, "Australia/Melbourne"),
    Place("brisbane", "Brisbane", "ब्रिस्बेन", "Australia", "ऑस्ट्रेलिया", -27.4698, 153.0251, "Australia/Brisbane"),
    Place("perth", "Perth", "पर्थ", "Australia", "ऑस्ट्रेलिया", -31.9523, 115.8613, "Australia/Perth"),
    Place("adelaide", "Adelaide", "एडिलेड", "Australia", "ऑस्ट्रेलिया", -34.9285, 138.6007, "Australia/Adelaide"),
    Place("canberra", "Canberra", "कैनबरा", "Australia", "ऑस्ट्रेलिया", -35.2809, 149.1300, "Australia/Sydney"),
    Place("auckland", "Auckland", "ऑकलैंड", "New Zealand", "न्यूज़ीलैंड", -36.8485, 174.7633, "Pacific/Auckland"),
    # Europe: smaller communities in high-rate markets, one or two cities each
    Place("dublin", "Dublin", "डबलिन", "Ireland", "आयरलैंड", 53.3498, -6.2603, "Europe/Dublin"),
    Place("frankfurt", "Frankfurt", "फ़्रैंकफ़र्ट", "Germany", "जर्मनी", 50.1109, 8.6821, "Europe/Berlin"),
    Place("berlin", "Berlin", "बर्लिन", "Germany", "जर्मनी", 52.5200, 13.4050, "Europe/Berlin"),
    Place("munich", "Munich", "म्यूनिख", "Germany", "जर्मनी", 48.1351, 11.5820, "Europe/Berlin"),
    Place("amsterdam", "Amsterdam", "एम्स्टर्डम", "Netherlands", "नीदरलैंड", 52.3676, 4.9041, "Europe/Amsterdam"),
    Place("the-hague", "The Hague", "द हेग", "Netherlands", "नीदरलैंड", 52.0705, 4.3007, "Europe/Amsterdam"),
    Place("zurich", "Zurich", "ज़्यूरिख", "Switzerland", "स्विट्ज़रलैंड", 47.3769, 8.5417, "Europe/Zurich"),
    # the Gulf and Singapore: large communities, middling advertising rates
    Place("dubai", "Dubai", "दुबई", "United Arab Emirates", "संयुक्त अरब अमीरात", 25.2048, 55.2708, "Asia/Dubai"),
    Place("abu-dhabi", "Abu Dhabi", "अबू धाबी", "United Arab Emirates", "संयुक्त अरब अमीरात", 24.4539, 54.3773, "Asia/Dubai"),
    Place("singapore", "Singapore", "सिंगापुर", "Singapore", "सिंगापुर", 1.3521, 103.8198, "Asia/Singapore"),
]
COUNTRY_ORDER = ["India", "United States", "Canada", "United Kingdom", "Australia", "New Zealand", "Ireland", "Germany",
                 "Netherlands", "Switzerland", "United Arab Emirates", "Singapore"]
