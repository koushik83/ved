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
    Place("new-york", "New York", "न्यूयॉर्क", "United States", "अमेरिका", 40.7128, -74.0060, "America/New_York"),
    Place("new-jersey", "New Jersey (Edison)", "न्यू जर्सी (एडिसन)", "United States", "अमेरिका", 40.5187, -74.4121,
          "America/New_York"),
    Place("chicago", "Chicago", "शिकागो", "United States", "अमेरिका", 41.8781, -87.6298, "America/Chicago"),
    Place("dallas", "Dallas", "डैलस", "United States", "अमेरिका", 32.7767, -96.7970, "America/Chicago"),
    Place("houston", "Houston", "ह्यूस्टन", "United States", "अमेरिका", 29.7604, -95.3698, "America/Chicago"),
    Place("atlanta", "Atlanta", "अटलांटा", "United States", "अमेरिका", 33.7490, -84.3880, "America/New_York"),
    Place("san-francisco", "San Francisco (Bay Area)", "सैन फ़्रांसिस्को (बे एरिया)", "United States", "अमेरिका",
          37.7749, -122.4194, "America/Los_Angeles"),
    Place("los-angeles", "Los Angeles", "लॉस एंजेलेस", "United States", "अमेरिका", 34.0522, -118.2437,
          "America/Los_Angeles"),
    Place("seattle", "Seattle", "सिएटल", "United States", "अमेरिका", 47.6062, -122.3321, "America/Los_Angeles"),
    Place("toronto", "Toronto", "टोरंटो", "Canada", "कनाडा", 43.6532, -79.3832, "America/Toronto"),
    Place("vancouver", "Vancouver", "वैंकूवर", "Canada", "कनाडा", 49.2827, -123.1207, "America/Vancouver"),
    Place("calgary", "Calgary", "कैलगरी", "Canada", "कनाडा", 51.0447, -114.0719, "America/Edmonton"),
    Place("london", "London", "लंदन", "United Kingdom", "ब्रिटेन", 51.5074, -0.1278, "Europe/London"),
    Place("leicester", "Leicester", "लेस्टर", "United Kingdom", "ब्रिटेन", 52.6369, -1.1398, "Europe/London"),
    Place("birmingham", "Birmingham", "बर्मिंघम", "United Kingdom", "ब्रिटेन", 52.4862, -1.8904, "Europe/London"),
    Place("sydney", "Sydney", "सिडनी", "Australia", "ऑस्ट्रेलिया", -33.8688, 151.2093, "Australia/Sydney"),
    Place("melbourne", "Melbourne", "मेलबर्न", "Australia", "ऑस्ट्रेलिया", -37.8136, 144.9631, "Australia/Melbourne"),
    Place("dubai", "Dubai", "दुबई", "United Arab Emirates", "संयुक्त अरब अमीरात", 25.2048, 55.2708, "Asia/Dubai"),
    Place("singapore", "Singapore", "सिंगापुर", "Singapore", "सिंगापुर", 1.3521, 103.8198, "Asia/Singapore"),
]
COUNTRY_ORDER = ["India", "United States", "Canada", "United Kingdom", "Australia", "United Arab Emirates", "Singapore"]
