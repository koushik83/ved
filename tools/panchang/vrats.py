"""Fasts and festivals for a city: which civil day each falls on, and the moment that decides it.

Works from the cached astronomy (the Sky's tithi, nakshatra and sankranti changes; the city's sunrises, sunsets and
moonrises), all as UTC epoch seconds, so it needs no ephemeris at run time.

The rule of a tithi-bound observance names the lunar month (amanta reckoning), the paksha, the tithi, and the part
of the Hindu day in which the tithi must be in force (the "kala"): sunrise, the forenoon, midday, the afternoon,
the evening after sunset, midnight, or moonrise. When the tithi is in force at that part on two consecutive days,
or on neither, the rule's preference decides: the earlier day or the later. These preferences were set by matching
published panchangs over several cities and both years of data; where they follow a convention rather than first
principles, the comment says so.
"""
from __future__ import annotations

import bisect
import datetime as dt
import json
import pathlib
from dataclasses import dataclass, field
from zoneinfo import ZoneInfo

HERE = pathlib.Path(__file__).resolve().parent
CACHE_DIR = HERE / "cache"
MINUTE = 60
MUHURTA_ARUNODAYA = 96 * MINUTE          # four ghatis before sunrise
PRADOSH_LENGTH = 144 * MINUTE            # three muhurtas after sunset


def sky_cache(first: dt.date, last: dt.date) -> dict:
    """The Sky's change lists as epochs, computed once per span and kept beside the city caches."""
    path = CACHE_DIR / f"sky-{first}-{last}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    from . import engine  # the only place this module touches the ephemeris
    sky = engine.Sky(first, last)
    stamp = lambda t: int(t.utc_datetime().timestamp())  # noqa: E731
    payload = {k: [[stamp(t), v] for t, v in getattr(sky, k)] for k in ("tithi", "nakshatra", "yoga", "sankranti")}
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")
    return payload


class Almanac:
    """A city's clock, sunrises and the sky's changes, with the questions the rules ask of them."""

    def __init__(self, sky: dict, events: dict, tz: str):
        self.zone = ZoneInfo(tz)
        self.changes = {k: ([e for e, _ in v], [x for _, x in v]) for k, v in sky.items()}
        self.sunrises = events["sunrise"]
        self.sunsets = events["sunset"]
        self.moonrises = events["moonrise"]
        self.new_moons = [e for e, v in sky["tithi"] if v == 0]

    # ---- the sky
    def _at(self, key, epoch, modulus):
        times, values = self.changes[key]
        i = bisect.bisect_right(times, epoch) - 1
        if i < 0:
            return (values[0] - 1) % modulus
        return values[i]

    def tithi_at(self, epoch):
        return self._at("tithi", epoch, 30)

    def nakshatra_at(self, epoch):
        return self._at("nakshatra", epoch, 27)

    def sun_rashi_at(self, epoch):
        return self._at("sankranti", epoch, 12)

    def tithi_bounds(self, epoch):
        """(begin, end) of the tithi in force at epoch."""
        times, _ = self.changes["tithi"]
        i = bisect.bisect_right(times, epoch) - 1
        begin = times[i] if i >= 0 else None
        end = times[i + 1] if i + 1 < len(times) else None
        return begin, end

    def sankrantis(self, rashi):
        times, values = self.changes["sankranti"]
        return [t for t, v in zip(times, values) if v == rashi]

    # ---- the city's days
    def local_date(self, epoch) -> dt.date:
        return dt.datetime.fromtimestamp(epoch, self.zone).date()

    def sunrise_on(self, date: dt.date):
        start = int(dt.datetime.combine(date, dt.time(), self.zone).timestamp())
        i = bisect.bisect_left(self.sunrises, start)
        if i < len(self.sunrises) and self.local_date(self.sunrises[i]) == date:
            return self.sunrises[i]
        return None

    def day(self, date: dt.date):
        """(sunrise, sunset, next sunrise) of the Hindu day that begins on this civil date."""
        s = self.sunrise_on(date)
        s2 = self.sunrise_on(date + dt.timedelta(days=1))
        if s is None or s2 is None:
            return None
        j = bisect.bisect_right(self.sunsets, s)
        return s, self.sunsets[j], s2

    def moonrise_in(self, start, end):
        i = bisect.bisect_left(self.moonrises, start)
        if i < len(self.moonrises) and self.moonrises[i] < end:
            return self.moonrises[i]
        return None

    def windows(self, s, ss, s2):
        """The parts of the Hindu day the rules name, as (start, end) epochs or an instant."""
        d, n = ss - s, s2 - ss
        mid_night = ss + n / 2
        return {
            "sunrise": (s, s),
            "arunodaya": (s - MUHURTA_ARUNODAYA, s - MUHURTA_ARUNODAYA),
            "pratah": (s, s + d / 5),
            "purvahna": (s + d / 5, s + 2 * d / 5),
            "madhyahna": (s + 2 * d / 5, s + 3 * d / 5),
            "aparahna": (s + 3 * d / 5, s + 4 * d / 5),
            "sayahna": (s + 4 * d / 5, ss),
            "sunset": (ss, ss),
            "pradosh": (ss, ss + PRADOSH_LENGTH),
            "nishita": (mid_night - n / 30, mid_night + n / 30),
        }

    # ---- the lunar month
    def lunar_month(self, epoch):
        """(amanta month index 0=Chaitra, adhika, start new moon, end new moon) for the month containing epoch."""
        i = bisect.bisect_right(self.new_moons, epoch) - 1
        if i < 0 or i + 1 >= len(self.new_moons):
            return None
        start, end = self.new_moons[i], self.new_moons[i + 1]
        times, values = self.changes["sankranti"]
        inside = [v for t, v in zip(times, values) if start < t <= end]
        if inside:
            return inside[0], False, start, end
        after = [v for t, v in zip(times, values) if t > end]
        return (after[0] if after else None), True, start, end

    def months(self, first_epoch, last_epoch):
        """Every lunar month overlapping the span: [(index, adhika, start, end), ...]."""
        out = []
        for i in range(len(self.new_moons) - 1):
            start, end = self.new_moons[i], self.new_moons[i + 1]
            if end < first_epoch or start > last_epoch:
                continue
            m = self.lunar_month(start + 1)
            if m and m[0] is not None:
                out.append(m)
        return out


# ------------------------------------------------------------------ deciding the day

def tithi_interval(alm: Almanac, month_start, month_end, tithi_index):
    """(begin, end) of the given tithi (0..29) within the lunar month, or None if it is skipped."""
    times, values = alm.changes["tithi"]
    for t, v in zip(times, values):
        if month_start <= t < month_end and v == tithi_index:
            j = times.index(t)
            return t, times[j + 1] if j + 1 < len(times) else None
    return None


def in_force(window, begin, end):
    a, b = window
    if a == b:
        return begin <= a < end
    return a < end and begin < b


def decide(alm: Almanac, begin, end, kala, prefer="purva", fallback=None):
    """The civil date the observance falls on, and the Hindu day's (s, ss, s2), from where the tithi is in force.

    Candidates are the Hindu days the tithi touches. The one whose kala holds the tithi wins; with two, `prefer`
    decides: "purva" the earlier, "para" the later, "more" the day on which the tithi covers more of the window.
    With none, `fallback` decides: "purva" or "para" for the earlier or later day, "sunrise" for the day the tithi
    is in force at sunrise (else the earlier), None for `prefer`. The kalas "begins" and "ends" are the civil days
    of the tithi's own boundaries, "midnight" the instant halfway through the night."""
    if kala in ("begins", "ends"):
        date = alm.local_date(begin if kala == "begins" else end)
        return date, alm.day(date)
    first = alm.local_date(begin)
    candidates = []
    for k in range(-1, 3):
        date = first + dt.timedelta(days=k)
        d = alm.day(date)
        if d and d[0] < end and begin < d[2]:
            candidates.append((date, d))
    if not candidates:
        return None, None
    hits = []
    for date, (s, ss, s2) in candidates:
        overlap = 0.0
        if kala == "moonrise":
            m = alm.moonrise_in(s, s2)
            ok = m is not None and begin <= m < end
        elif kala == "midnight":
            mid = ss + (s2 - ss) / 2
            ok = begin <= mid < end
        else:
            if kala.startswith("pradosh") and kala != "pradosh":
                window = (ss, ss + int(kala[len("pradosh"):]) * MINUTE)
            else:
                window = alm.windows(s, ss, s2)[kala]
            ok = in_force(window, begin, end)
            overlap = max(0.0, min(window[1], end) - max(window[0], begin))
        if ok:
            hits.append((date, (s, ss, s2), overlap))
    if len(hits) == 1:
        return hits[0][:2]
    if hits:
        if prefer == "more":
            return max(hits, key=lambda h: h[2])[:2]
        return hits[0][:2] if prefer == "purva" else hits[-1][:2]
    rule = fallback or prefer
    if rule == "sunrise":
        at_sunrise = [c for c in candidates if begin <= c[1][0] < end]
        return at_sunrise[0] if at_sunrise else candidates[0]
    return candidates[0] if rule == "purva" else candidates[-1]


@dataclass
class Rule:
    key: str
    en: str
    hi: str
    month: int | None          # amanta month index, None for every month
    paksha: str                # "s" or "k"
    tithi: int                 # 1..15 within the paksha (15 = Purnima or Amavasya)
    kala: str
    prefer: str = "purva"
    kind: str = "festival"     # "festival" or "vrat"
    extra: dict = field(default_factory=dict)
    fallback: str | None = None

    @property
    def index(self):
        return self.tithi - 1 + (0 if self.paksha == "s" else 15)


@dataclass
class Observance:
    key: str
    date: dt.date
    kind: str
    en: str
    hi: str
    details: dict = field(default_factory=dict)      # epochs and texts the page shows


# the monthly vrats, every lunar month. Each rule was chosen by matching the published lists for nine cities over
# fourteen months (the agreement is noted); the preferences are conventions those lists follow.
MONTHLY = [
    # Chaturthi at moonrise; on two evenings the first; on none, the later day (70 of 70)
    Rule("sankashti", "Sankashti Chaturthi", "संकष्टी चतुर्थी", None, "k", 4, "moonrise", "purva", "vrat", fallback="para"),
    # Chaturthi in the midday fifth; the day it covers more of it (74 of 74)
    Rule("vinayaka", "Vinayaka Chaturthi", "विनायक चतुर्थी", None, "s", 4, "madhyahna", "more", "vrat"),
    # Trayodashi in the three muhurtas after sunset, the later day (69 of 70); in the dark half, at sunset (74 of 75)
    Rule("pradosh_s", "Pradosh Vrat", "प्रदोष व्रत", None, "s", 13, "pradosh", "para", "vrat", fallback="sunrise"),
    Rule("pradosh_k", "Pradosh Vrat", "प्रदोष व्रत", None, "k", 13, "sunset", "purva", "vrat"),
    # Chaturdashi at midnight, the later night (74 of 75)
    Rule("shivaratri", "Masik Shivaratri", "मासिक शिवरात्रि", None, "k", 14, "nishita", "para", "vrat"),
    # the tithi days (sunrise) and the fasting days: Purnima at midday, Amavasya covering more of the afternoon
    Rule("purnima", "Purnima", "पूर्णिमा", None, "s", 15, "sunrise", "purva", "vrat"),
    Rule("purnima_vrat", "Purnima Vrat", "पूर्णिमा व्रत", None, "s", 15, "madhyahna", "purva", "vrat", fallback="sunrise"),
    Rule("amavasya", "Amavasya", "अमावस्या", None, "k", 15, "sunrise", "purva", "vrat"),
    Rule("darsha_amavasya", "Darsha Amavasya", "दर्श अमावस्या", None, "k", 15, "aparahna", "more", "vrat"),
    Rule("durgashtami", "Masik Durgashtami", "मासिक दुर्गाष्टमी", None, "s", 8, "sunrise", "purva", "vrat"),
    Rule("kalashtami", "Kalashtami", "कालाष्टमी", None, "k", 8, "pradosh", "more", "vrat"),
]

# Ekadashi names by purnimanta month and paksha: Krishna paksha names belong to the following amanta month's name
EKADASHI_NAMES = {
    (0, "s"): ("Kamada", "कामदा"), (1, "k"): ("Varuthini", "वरूथिनी"), (1, "s"): ("Mohini", "मोहिनी"),
    (2, "k"): ("Apara", "अपरा"), (2, "s"): ("Nirjala", "निर्जला"), (3, "k"): ("Yogini", "योगिनी"),
    (3, "s"): ("Devshayani", "देवशयनी"), (4, "k"): ("Kamika", "कामिका"), (4, "s"): ("Shravana Putrada", "श्रावण पुत्रदा"),
    (5, "k"): ("Aja", "अजा"), (5, "s"): ("Parivartini", "परिवर्तिनी"), (6, "k"): ("Indira", "इन्दिरा"),
    (6, "s"): ("Papankusha", "पापांकुशा"), (7, "k"): ("Rama", "रमा"), (7, "s"): ("Devutthana", "देवउठनी"),
    (8, "k"): ("Utpanna", "उत्पन्ना"), (8, "s"): ("Mokshada", "मोक्षदा"), (9, "k"): ("Saphala", "सफला"),
    (9, "s"): ("Pausha Putrada", "पौष पुत्रदा"), (10, "k"): ("Shattila", "षट्तिला"), (10, "s"): ("Jaya", "जया"),
    (11, "k"): ("Vijaya", "विजया"), (11, "s"): ("Amalaki", "आमलकी"), (0, "k"): ("Papmochani", "पापमोचनी"),
}

# the festivals of the year, by amanta month (0 = Chaitra), paksha and tithi. The kala is the classical one; where
# the published panchangs' own city pages were compared (five cities, 2026-27), the agreement is noted, and the
# preference is the one those pages follow. "more": the day the tithi covers more of the window.
ANNUAL = [
    Rule("vasant_panchami", "Vasant Panchami", "वसंत पंचमी", 10, "s", 5, "purvahna"),                        # 5 of 5
    Rule("ratha_saptami", "Ratha Saptami", "रथ सप्तमी", 10, "s", 7, "sunrise"),                             # 5 of 5
    Rule("magha_purnima", "Magha Purnima", "माघ पूर्णिमा", 10, "s", 15, "sunrise"),
    Rule("maha_shivaratri", "Maha Shivaratri", "महाशिवरात्रि", 10, "k", 14, "nishita"),                     # 5 of 5
    Rule("holika_dahan", "Holika Dahan", "होलिका दहन", 11, "s", 15, "pradosh", "more"),                     # 5 of 5
    Rule("chaitra_navratri", "Chaitra Navratri begins", "चैत्र नवरात्रि आरंभ", 0, "s", 1, "sunrise"),
    Rule("ugadi", "Ugadi / Gudi Padwa", "उगादि / गुड़ी पड़वा", 0, "s", 1, "sunrise"),                        # 5 of 5
    Rule("gangaur", "Gangaur", "गणगौर", 0, "s", 3, "sunrise"),                                              # 5 of 5
    Rule("ram_navami", "Ram Navami", "राम नवमी", 0, "s", 9, "madhyahna", "more"),                            # 5 of 5
    Rule("hanuman_jayanti", "Hanuman Jayanti", "हनुमान जयंती", 0, "s", 15, "sunrise"),                      # 5 of 5
    Rule("akshaya_tritiya", "Akshaya Tritiya", "अक्षय तृतीया", 1, "s", 3, "purvahna"),                       # 5 of 5
    Rule("narasimha_jayanti", "Narasimha Jayanti", "नृसिंह जयंती", 1, "s", 14, "sayahna"),
    Rule("buddha_purnima", "Buddha Purnima", "बुद्ध पूर्णिमा", 1, "s", 15, "sunrise"),                      # 5 of 5
    Rule("vat_savitri", "Vat Savitri Vrat", "वट सावित्री व्रत", 1, "k", 15, "sunrise"),
    Rule("ganga_dussehra", "Ganga Dussehra", "गंगा दशहरा", 2, "s", 10, "sunrise"),                          # 5 of 5
    Rule("vat_purnima", "Vat Purnima Vrat", "वट पूर्णिमा व्रत", 2, "s", 15, "sunrise"),
    Rule("rath_yatra", "Jagannath Rath Yatra", "जगन्नाथ रथ यात्रा", 3, "s", 2, "sunrise"),
    Rule("guru_purnima", "Guru Purnima", "गुरु पूर्णिमा", 3, "s", 15, "sunrise"),                           # 5 of 5
    Rule("hariyali_teej", "Hariyali Teej", "हरियाली तीज", 4, "s", 3, "sunrise"),
    Rule("nag_panchami", "Nag Panchami", "नाग पंचमी", 4, "s", 5, "sunrise"),                                # 5 of 5
    Rule("raksha_bandhan", "Raksha Bandhan", "रक्षा बंधन", 4, "s", 15, "purvahna", "more"),                  # 5 of 5
    Rule("kajari_teej", "Kajari Teej", "कजरी तीज", 4, "k", 3, "sunrise"),
    Rule("janmashtami", "Krishna Janmashtami", "कृष्ण जन्माष्टमी", 4, "k", 8, "nishita", "para"),
    Rule("hartalika_teej", "Hartalika Teej", "हरतालिका तीज", 5, "s", 3, "pratah"),
    Rule("ganesh_chaturthi", "Ganesh Chaturthi", "गणेश चतुर्थी", 5, "s", 4, "madhyahna", "more"),            # 5 of 5
    Rule("rishi_panchami", "Rishi Panchami", "ऋषि पंचमी", 5, "s", 5, "madhyahna", "more"),                   # 5 of 5
    Rule("radha_ashtami", "Radha Ashtami", "राधा अष्टमी", 5, "s", 8, "madhyahna", "para"),                   # 5 of 5
    Rule("anant_chaturdashi", "Anant Chaturdashi", "अनंत चतुर्दशी", 5, "s", 14, "sunrise"),                  # 5 of 5
    Rule("pitru_paksha", "Pitru Paksha begins", "पितृ पक्ष आरंभ", 5, "s", 15, "aparahna", "more"),
    Rule("sarva_pitru_amavasya", "Sarva Pitru Amavasya", "सर्व पितृ अमावस्या", 5, "k", 15, "aparahna", "more"),
    Rule("sharad_navratri", "Sharad Navratri begins", "शारदीय नवरात्रि आरंभ", 6, "s", 1, "sunrise"),
    Rule("durga_ashtami", "Durga Ashtami", "दुर्गा अष्टमी", 6, "s", 8, "sunrise"),
    Rule("maha_navami", "Maha Navami", "महा नवमी", 6, "s", 9, "sunrise"),
    Rule("dussehra", "Dussehra", "दशहरा", 6, "s", 10, "aparahna", "more"),
    Rule("sharad_purnima", "Sharad Purnima", "शरद पूर्णिमा", 6, "s", 15, "nishita", "para"),
    # the day of the fast is the one the published Karwa Chauth pages give, Chaturthi in the evening after sunset;
    # the moon of that evening is shown (5 of 5)
    Rule("karwa_chauth", "Karwa Chauth", "करवा चौथ", 6, "k", 4, "pradosh", "more", extra={"moonrise": True}),
    Rule("ahoi_ashtami", "Ahoi Ashtami", "अहोई अष्टमी", 6, "k", 8, "pradosh", "more"),                       # 5 of 5
    Rule("dhanteras", "Dhanteras", "धनतेरस", 6, "k", 13, "pradosh", "more"),
    Rule("narak_chaturdashi", "Narak Chaturdashi", "नरक चतुर्दशी", 6, "k", 14, "arunodaya", "para"),         # 10 of 10
    Rule("diwali", "Diwali", "दीपावली", 6, "k", 15, "pradosh", "more"),                                     # 10 of 10
    Rule("govardhan", "Govardhan Puja", "गोवर्धन पूजा", 7, "s", 1, "aparahna", "para", fallback="sunrise"),  # 10 of 10
    Rule("bhai_dooj", "Bhai Dooj", "भाई दूज", 7, "s", 2, "aparahna", "more"),                                # 8 of 8
    Rule("chhath", "Chhath Puja", "छठ पूजा", 7, "s", 6, "sunrise"),                                         # 10 of 10
    Rule("gopashtami", "Gopashtami", "गोपाष्टमी", 7, "s", 8, "sunrise"),                                     # 10 of 10
    Rule("akshaya_navami", "Akshaya Navami", "अक्षय नवमी", 7, "s", 9, "sunrise"),                            # 10 of 10
    Rule("tulsi_vivah", "Tulsi Vivah", "तुलसी विवाह", 7, "s", 12, "sunrise"),                                # 10 of 10
    Rule("kartik_purnima", "Kartik Purnima / Dev Deepawali", "कार्तिक पूर्णिमा / देव दीपावली", 7, "s", 15, "sunrise"),
    Rule("gita_jayanti", "Gita Jayanti", "गीता जयंती", 8, "s", 11, "sunrise"),   # replaced by the Ekadashi rule below
    Rule("dattatreya_jayanti", "Dattatreya Jayanti", "दत्तात्रेय जयंती", 8, "s", 15, "pradosh", "more"),
]


def ekadashi(alm: Almanac, month_start, month_end, month_index, paksha):
    """The Smarta and Vaishnava Ekadashi days of one paksha, with the parana (fast-breaking) window.

    Smarta: the day Ekadashi is in force at sunrise; on two such days the later; on none, the day after the tithi.
    Vaishnava: the same, unless Dashami is still in force at arunodaya (four ghatis before sunrise), when the fast
    moves to the next day. Parana: on the following day, after sunrise and after the first quarter of Dwadashi
    (Hari Vasara), within the first fifth of the day where the tithi allows, else before Dwadashi ends."""
    index = 10 if paksha == "s" else 25
    span = tithi_interval(alm, month_start, month_end, index)
    if not span or span[1] is None:
        return []
    begin, end = span
    smarta, hd = decide(alm, begin, end, "sunrise", prefer="para")
    if smarta is None or hd is None:
        return []
    # the fast is broken in Dwadashi the next morning: when Dwadashi is over before that sunrise, the fast moves
    # a day earlier, to the day Ekadashi began (the published panchangs all do this)
    after = alm.day(smarta + dt.timedelta(days=1))
    if after and alm.tithi_at(after[0]) == (index + 2) % 30 and alm.local_date(begin) < smarta:
        smarta -= dt.timedelta(days=1)
        hd = alm.day(smarta) or hd
    s = hd[0]
    dashami_at_arunodaya = alm.tithi_at(s - MUHURTA_ARUNODAYA) == index - 1
    vaishnava = smarta + dt.timedelta(days=1) if dashami_at_arunodaya else smarta
    name_month = month_index if paksha == "s" else (month_index + 1) % 12
    en, hi = EKADASHI_NAMES[(name_month, paksha)]
    out = []
    for date, label_en, label_hi in ((smarta, en + " Ekadashi", hi + " एकादशी"),
                                     (vaishnava, "Vaishnava " + en + " Ekadashi", "वैष्णव " + hi + " एकादशी")):
        if date == smarta and date == vaishnava and label_en.startswith("Vaishnava"):
            continue
        nxt = alm.day(date + dt.timedelta(days=1))
        details: dict = {"tithi_begins": begin, "tithi_ends": end}
        if nxt:
            ns, nss, _ = nxt
            d_begin, d_end = end, alm.tithi_bounds(end + 1)[1]        # Dwadashi follows Ekadashi
            if d_end is None:
                d_end = d_begin + 86400
            hari_vasara_end = d_begin + (d_end - d_begin) / 4
            pratah_end = ns + (nss - ns) / 5
            start = max(ns, hari_vasara_end)
            finish = pratah_end if start < pratah_end else d_end
            if d_end < start:                            # Dwadashi over before sunrise: break the fast at sunrise
                start, finish = ns, pratah_end
            details["parana"] = (int(start), int(min(finish, d_end) if finish > start else finish))
            details["dwadashi_ends"] = int(d_end)
        out.append(Observance("ekadashi" if date == smarta else "ekadashi_vaishnava", date, "vrat", label_en, label_hi, details))
        if smarta == vaishnava:
            break
    return out


def observances(alm: Almanac, first: dt.date, last: dt.date) -> list[Observance]:
    first_epoch = int(dt.datetime.combine(first, dt.time(), alm.zone).timestamp())
    last_epoch = int(dt.datetime.combine(last + dt.timedelta(days=1), dt.time(), alm.zone).timestamp())
    out: list[Observance] = []
    for month, adhika, m_start, m_end in alm.months(first_epoch - 40 * 86400, last_epoch + 40 * 86400):
        rules = list(MONTHLY) + ([] if adhika else [r for r in ANNUAL if r.month == month])
        for rule in rules:
            span = tithi_interval(alm, m_start, m_end, rule.index)
            if not span or span[1] is None:
                continue
            begin, end = span
            date, hd = decide(alm, begin, end, rule.kala, rule.prefer, rule.fallback)
            if date is None or hd is None:
                continue
            details = {"tithi_begins": begin, "tithi_ends": end}
            s, ss, s2 = hd
            if rule.kala == "moonrise" or rule.extra.get("moonrise"):
                m = alm.moonrise_in(s, s2)
                details["moonrise"] = m
                details["fast"] = (s, m) if m else None
            if rule.kala in ("madhyahna", "pradosh", "nishita"):        # the kalas that are puja windows
                a, b = alm.windows(s, ss, s2)[rule.kala]
                lo, hi = max(a, begin), min(b, end)
                if hi > lo:
                    details["window"] = (int(lo), int(hi))
            if rule.key == "sankashti" and date.weekday() == 1:
                details["angarki"] = True
            out.append(Observance(rule.key, date, rule.kind, rule.en, rule.hi, details))
        for paksha in ("s", "k"):
            out.extend(ekadashi(alm, m_start, m_end, month, paksha))
    # the solar festivals: Makar Sankranti and the day before it (Lohri), Mesha Sankranti (Baisakhi)
    for rashi, key, en, hi in ((9, "makar_sankranti", "Makar Sankranti / Pongal", "मकर संक्रांति / पोंगल"),
                               (0, "baisakhi", "Baisakhi / Mesha Sankranti", "बैसाखी / मेष संक्रांति")):
        for t in alm.sankrantis(rashi):
            date = alm.local_date(t)
            d = alm.day(date)
            if d and t > d[1]:                        # after sunset: the punya kala falls on the next day
                date += dt.timedelta(days=1)
            out.append(Observance(key, date, "festival", en, hi, {"sankranti": t}))
            if key == "makar_sankranti":
                out.append(Observance("lohri", date - dt.timedelta(days=1), "festival", "Lohri", "लोहड़ी", {}))
    # Holi is the day after Holika Dahan; Gita Jayanti is Mokshada Ekadashi itself, so it follows the Ekadashi rule
    for o in [o for o in out if o.key == "holika_dahan"]:
        out.append(Observance("holi", o.date + dt.timedelta(days=1), "festival", "Holi", "होली", {}))
    out = [o for o in out if o.key != "gita_jayanti"]
    for o in [o for o in out if o.key == "ekadashi" and o.en.startswith("Mokshada")]:
        out.append(Observance("gita_jayanti", o.date, "festival", "Gita Jayanti", "गीता जयंती", dict(o.details)))
    out = [o for o in out if first <= o.date <= last]
    out.sort(key=lambda o: (o.date, o.kind != "festival", o.en))
    return out


def load_city(slug: str, tz: str, first: dt.date, last: dt.date) -> Almanac:
    """The almanac for a city whose astronomy is already cached by the page builder."""
    city = json.loads((CACHE_DIR / f"{slug}-{first}-{last}.json").read_text(encoding="utf-8"))
    return Almanac(sky_cache(first, last), city["events"], tz)
