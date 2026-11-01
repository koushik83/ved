"""The panchang engine: the five limbs and a day's timings, from the JPL ephemeris.

Everything here is astronomy and arithmetic; the words are in names.py and the pages in
tools/build_panchang.py. The conventions, stated once:

- Positions are geocentric apparent, referred to the mean ecliptic and equinox of date.
- Sidereal longitudes subtract the Lahiri (Chitrapaksha) ayanamsa, defined the way Swiss Ephemeris
  defines it: 23 deg 14' 43.88" at 1956 March 21.0 ET on the mean equinox, carried through time as a
  fixed direction in space.
- A tithi is 12 degrees of moon-minus-sun elongation, a karana 6, a nakshatra and a yoga 13 deg 20'.
- The Hindu day runs from sunrise to the next sunrise. A day lists the element in force at sunrise and
  every change up to the next sunrise.
- Sunrise and sunset are the moments the Sun's centre is SUN_HORIZON degrees above the geometric
  horizon; MOON_HORIZON likewise for the Moon. Both values were chosen by matching published panchangs
  for many cities and dates, not assumed.
- Rahu Kaal, Yamaganda and Gulika are eighths of the day (sunrise to sunset); Abhijit is the eighth of
  the fifteen day muhurtas; Brahma Muhurta the second-last of the fifteen night muhurtas before sunrise;
  Choghadiya eighths of the day and of the night.

The ephemeris file (de421.bsp, 17 MB, 1900-2050) lives in tools/panchang/ephem/ and is not committed.
"""
from __future__ import annotations

import datetime as dt
import math
import pathlib
from dataclasses import dataclass
from typing import Any
from zoneinfo import ZoneInfo

import numpy as np
from skyfield import almanac
from skyfield.api import Loader, wgs84
from skyfield.functions import mxv
from skyfield.nutationlib import iau2000b_radians, mean_obliquity
from skyfield.precessionlib import compute_precession

HERE = pathlib.Path(__file__).resolve().parent
EPHEM_DIR = HERE / "ephem"
EPHEM_FILE = "de421.bsp"
EPHEM_URL = "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/a_old_versions/de421.bsp"

ASEC2RAD = math.pi / (180.0 * 3600.0)
TITHI_DEG, KARANA_DEG, PART27_DEG, RASHI_DEG = 12.0, 6.0, 360.0 / 27.0, 30.0

# Lahiri's ayanamsa: 23 deg 15' 00.658" at 1956 March 21.0 ET, the value the Indian panchangs carry forward.
# (Swiss Ephemeris subtracts 16.78" here for the nutation of that day; the published panchangs do not, and
# the difference is 30 seconds in a nakshatra's end time.)
LAHIRI_T0 = 2435553.5
LAHIRI_AT_T0 = 23.250182778

# Set by matching published panchangs. Sun: upper limb with refraction is -0.8333; centre without
# refraction is 0.0. The Moon's is for its topocentric centre.
SUN_HORIZON = -0.8333
MOON_HORIZON = 0.0

_loaded: dict = {}


def _sky():
    """The timescale, ephemeris and bodies, loaded once."""
    if not _loaded:
        if not (EPHEM_DIR / EPHEM_FILE).exists():
            raise SystemExit(f"missing {EPHEM_DIR / EPHEM_FILE}: download it from {EPHEM_URL}")
        load = Loader(str(EPHEM_DIR), verbose=False)
        ts = load.timescale()
        eph = load(EPHEM_FILE)
        _loaded.update(ts=ts, eph=eph, earth=eph["earth"], sun=eph["sun"], moon=eph["moon"])
    return _loaded


# ---------------------------------------------------------------- longitudes

def mean_ecliptic_longitude(body, t):
    """Geocentric apparent ecliptic longitude on the mean ecliptic and equinox of date, in degrees."""
    s = _sky()
    v = s["earth"].at(t).observe(s[body]).apparent().position.au       # ICRS, shape (3,) or (3, n)
    v = mxv(compute_precession(t.tdb), v)                               # mean equator and equinox of date
    eps = mean_obliquity(t.tdb) * ASEC2RAD
    x, y, z = v
    y2 = y * np.cos(eps) + z * np.sin(eps)                              # mean ecliptic of date
    return np.degrees(np.arctan2(y2, x)) % 360.0


def lahiri_ayanamsa(jd_tdb):
    """The Lahiri ayanamsa in degrees on the mean equinox of date, for a float or array of TDB Julian dates.

    The sidereal zero point sits at tropical longitude LAHIRI_AT_T0 on the mean ecliptic of the epoch; it is a
    fixed direction in space, so its tropical longitude on the mean ecliptic of any date is the ayanamsa then."""
    lon0 = math.radians(LAHIRI_AT_T0)
    v = np.array([math.cos(lon0), math.sin(lon0), 0.0])                 # the sidereal zero point, ecliptic of T0
    e0 = mean_obliquity(LAHIRI_T0) * ASEC2RAD
    v = np.array([v[0], v[1] * math.cos(e0) - v[2] * math.sin(e0), v[1] * math.sin(e0) + v[2] * math.cos(e0)])
    v = compute_precession(LAHIRI_T0).T @ v                             # to ICRS
    jd = np.asarray(jd_tdb, dtype=float)
    P = compute_precession(jd)
    w = mxv(P, v if jd.ndim == 0 else np.repeat(v[:, None], jd.size, axis=1))
    eps = mean_obliquity(jd) * ASEC2RAD
    x, y, z = w
    y2 = y * np.cos(eps) + z * np.sin(eps)
    return np.degrees(np.arctan2(y2, x)) % 360.0


def true_ayanamsa(t):
    """The ayanamsa on the true equinox of date (mean plus the nutation in longitude): the figure panchangs print."""
    dpsi, _ = iau2000b_radians(t)
    return float(lahiri_ayanamsa(t.tdb) + math.degrees(dpsi))


def sidereal_longitude(body, t):
    return (mean_ecliptic_longitude(body, t) - lahiri_ayanamsa(t.tdb)) % 360.0


def elongation(t):
    """Moon minus Sun, 0 to 360 degrees: the tithi's measure. The ayanamsa cancels."""
    return (mean_ecliptic_longitude("moon", t) - mean_ecliptic_longitude("sun", t)) % 360.0


def _discrete(fn, step_days):
    fn.step_days = step_days
    return fn


tithi_of = _discrete(lambda t: np.floor(elongation(t) / TITHI_DEG).astype(int), 0.25)
karana_of = _discrete(lambda t: np.floor(elongation(t) / KARANA_DEG).astype(int), 0.1)
nakshatra_of = _discrete(lambda t: np.floor(sidereal_longitude("moon", t) / PART27_DEG).astype(int), 0.25)
yoga_of = _discrete(lambda t: np.floor(((sidereal_longitude("moon", t) + sidereal_longitude("sun", t)) % 360.0)
                                        / PART27_DEG).astype(int), 0.25)
sun_rashi_of = _discrete(lambda t: np.floor(sidereal_longitude("sun", t) / RASHI_DEG).astype(int), 2.0)
moon_rashi_of = _discrete(lambda t: np.floor(sidereal_longitude("moon", t) / RASHI_DEG).astype(int), 0.5)


def changes(fn, t0, t1):
    """Every moment in (t0, t1) the integer-valued fn changes: a list of (time, new value)."""
    times, values = almanac.find_discrete(t0, t1, fn)
    return list(zip(times, [int(v) for v in values])) if len(times) else []


# ---------------------------------------------------------------- places and days

@dataclass(frozen=True)
class City:
    slug: str
    lat: float
    lon: float
    tz: str
    elevation_m: float = 0.0

    @property
    def zone(self):
        return ZoneInfo(self.tz)


def _local(t, city: City) -> dt.datetime:
    return t.utc_datetime().astimezone(city.zone)


def _events(observer, body, t0, t1, finder, horizon):
    times, ok = finder(observer, body, t0, t1, horizon_degrees=horizon)
    return [t for t, good in zip(times, ok) if good]


def _by_date(times, city):
    out: dict[dt.date, list] = {}
    for t in times:
        out.setdefault(_local(t, city).date(), []).append(t)
    return out


def _span(items, value_at_start, t_start, t_end):
    """The element in force at t_start and each change before t_end: [(index, end time or None), ...]."""
    out = []
    current = value_at_start
    for t, new in items:
        if t.tt <= t_start.tt or t.tt >= t_end.tt:
            continue
        out.append((current, t))
        current = new
    out.append((current, None))
    return out


def _part(start, end, n, k):
    """The k-th (1-based) of n equal parts between two times, as (start, end) datetimes."""
    d = (end - start) / n
    return start + d * (k - 1), start + d * k


# segment numbers (1-based of 8) by Python weekday Mon=0 .. Sun=6
RAHU = {6: 8, 0: 2, 1: 7, 2: 5, 3: 6, 4: 4, 5: 3}
YAMAGANDA = {6: 5, 0: 4, 1: 3, 2: 2, 3: 1, 4: 7, 5: 6}
GULIKA = {6: 7, 0: 6, 1: 5, 2: 4, 3: 3, 4: 2, 5: 1}
# choghadiya: the cyclic order of the seven, then the first of the day and of the night by weekday
CHOGHADIYA_ORDER = ["udveg", "chal", "labh", "amrit", "kaal", "shubh", "rog"]
CHOGHADIYA_DAY_FIRST = {6: "udveg", 0: "amrit", 1: "rog", 2: "labh", 3: "shubh", 4: "chal", 5: "kaal"}
CHOGHADIYA_NIGHT_FIRST = {6: "shubh", 0: "chal", 1: "kaal", 2: "udveg", 3: "amrit", 4: "rog", 5: "labh"}


def _choghadiya(start, end, first):
    i = CHOGHADIYA_ORDER.index(first)
    out = []
    for k in range(8):
        a, b = _part(start, end, 8, k + 1)
        out.append((CHOGHADIYA_ORDER[(i + k) % 7], a, b))
    return out


class Sky:
    """Everything that does not depend on the city, computed once for a padded span of dates."""

    def __init__(self, first: dt.date, last: dt.date):
        s = _sky()
        ts = s["ts"]
        self.ts = ts
        pad0 = ts.utc(first.year, first.month, first.day) - 400      # back to the previous Chaitra at least
        pad1 = ts.utc(last.year, last.month, last.day) + 40
        self.tithi = changes(tithi_of, pad0, pad1)
        self.karana = changes(karana_of, pad0, pad1)
        self.nakshatra = changes(nakshatra_of, pad0, pad1)
        self.yoga = changes(yoga_of, pad0, pad1)
        self.sankranti = changes(sun_rashi_of, pad0, pad1)
        self.new_moons = [t for t, v in self.tithi if v == 0]
        self.mesha = [t for t, v in self.sankranti if v == 0]

    def lunar_month(self, t):
        """(amanta month index 0=Chaitra, adhika flag, start new moon, end new moon) for the month containing t."""
        before = [m for m in self.new_moons if m.tt <= t.tt]
        after = [m for m in self.new_moons if m.tt > t.tt]
        if not before or not after:
            raise ValueError("outside the computed span")
        start, end = before[-1], after[0]
        inside = [(ti, v) for ti, v in self.sankranti if start.tt < ti.tt <= end.tt]
        if inside:
            return inside[0][1], False, start, end                # Mesha sankranti inside -> Chaitra
        following = [v for ti, v in self.sankranti if ti.tt > end.tt]
        return following[0], True, start, end                     # no sankranti: adhika, named for the next

    def vikram_year(self, t):
        """Vikram Samvat at t: 57 plus the Gregorian year of the latest Chaitra Shukla 1 at or before t."""
        starts = []
        for m in self.mesha:
            before = [n for n in self.new_moons if n.tt <= m.tt]
            if before:
                starts.append(before[-1])
        past = [c for c in starts if c.tt <= t.tt]
        if not past:
            raise ValueError("outside the computed span")
        return _utc_year(past[-1]) + 57


def _utc_year(t):
    return t.utc_datetime().year


class Place:
    """One city's sunrises, sunsets, moonrises and moonsets over the span, and its days."""

    def __init__(self, sky: Sky, city: City, first: dt.date, last: dt.date):
        s = _sky()
        self.sky, self.city = sky, city
        observer = s["earth"] + wgs84.latlon(city.lat, city.lon, elevation_m=city.elevation_m)
        z = city.zone
        t0 = sky.ts.from_datetime(dt.datetime.combine(first - dt.timedelta(days=2), dt.time(), z))
        t1 = sky.ts.from_datetime(dt.datetime.combine(last + dt.timedelta(days=2), dt.time(), z))
        self.sunrise = _by_date(_events(observer, s["sun"], t0, t1, almanac.find_risings, SUN_HORIZON), city)
        self.sunset = _by_date(_events(observer, s["sun"], t0, t1, almanac.find_settings, SUN_HORIZON), city)
        # the Moon's events are listed in time order and taken per Hindu day, sunrise to the next sunrise
        self.moonrises = _events(observer, s["moon"], t0, t1, almanac.find_risings, MOON_HORIZON)
        self.moonsets = _events(observer, s["moon"], t0, t1, almanac.find_settings, MOON_HORIZON)

    def one(self, date: dt.date, key):
        found = getattr(self, key).get(date, [])
        return found[0] if found else None

    @staticmethod
    def _within(events, start, end):
        """The first event at or after start and before end, or None (a Hindu day can lack a moonrise)."""
        for t in events:
            if start.tt <= t.tt < end.tt:
                return t
        return None

    def day(self, date: dt.date) -> dict:
        sky, city = self.sky, self.city
        sunrise = self.one(date, "sunrise")
        sunset = self.one(date, "sunset")
        next_sunrise = self.one(date + dt.timedelta(days=1), "sunrise")
        prev_sunset = self.one(date - dt.timedelta(days=1), "sunset")
        if sunrise is None or sunset is None or next_sunrise is None or prev_sunset is None:
            raise ValueError(f"no sunrise or sunset on {date} at {city.slug}")
        # Every duration is worked out in UTC: two datetimes carrying the same local zone subtract as wall-clock
        # values in Python, which is an hour wrong across a daylight-saving change. The city's clock is applied last.
        utc = lambda t: t.utc_datetime()  # noqa: E731
        sr, ss, nsr, pss = (utc(x) for x in (sunrise, sunset, next_sunrise, prev_sunset))
        moonrise = self._within(self.moonrises, sunrise, next_sunrise)
        moonset = self._within(self.moonsets, sunrise, next_sunrise)
        at = lambda fn: int(fn(sunrise))  # noqa: E731

        def span(items, fn):
            return [(i, utc(t) if t is not None else None) for i, t in _span(items, at(fn), sunrise, next_sunrise)]

        month, adhika, _, _ = sky.lunar_month(sunrise)
        tithis = span(sky.tithi, tithi_of)
        paksha = "shukla" if tithis[0][0] < 15 else "krishna"
        vikram = sky.vikram_year(sunrise)
        wd = date.weekday()
        day_muhurta = (ss - sr) / 15
        night_muhurta = (sr - pss) / 15
        rows = {
            "date": date.isoformat(),
            "weekday": wd,
            "sunrise": sr, "sunset": ss, "next_sunrise": nsr,
            "moonrise": utc(moonrise) if moonrise is not None else None,
            "moonset": utc(moonset) if moonset is not None else None,
            "tithi": tithis,
            "nakshatra": span(sky.nakshatra, nakshatra_of),
            "yoga": span(sky.yoga, yoga_of),
            "karana": span(sky.karana, karana_of),
            "paksha": paksha,
            "amanta_month": month, "adhika": adhika,
            # Purnimanta: the Krishna half belongs to the following month, except that an adhika month is the
            # same span in both reckonings, new moon to new moon, as the North Indian panchangs print it
            "purnimanta_month": month if (paksha == "shukla" or adhika) else (month + 1) % 12,
            "purnimanta_adhika": adhika,
            "vikram": vikram, "shaka": vikram - 135,
            "gujarati": vikram - 1 if month < 7 else vikram,
            "sun_rashi": at(sun_rashi_of), "moon_rashi": at(moon_rashi_of),
            "rahu": _part(sr, ss, 8, RAHU[wd]),
            "yamaganda": _part(sr, ss, 8, YAMAGANDA[wd]),
            "gulika": _part(sr, ss, 8, GULIKA[wd]),
            "abhijit": (sr + day_muhurta * 7, sr + day_muhurta * 8),
            "brahma": (sr - night_muhurta * 2, sr - night_muhurta),
            "choghadiya_day": _choghadiya(sr, ss, CHOGHADIYA_DAY_FIRST[wd]),
            "choghadiya_night": _choghadiya(ss, nsr, CHOGHADIYA_NIGHT_FIRST[wd]),
            "day_length": ss - sr,
            "ayanamsa": true_ayanamsa(sunrise),
            # sidereal longitudes at sunrise, for the page's drawing of the sky
            "sun_lon": float(sidereal_longitude("sun", sunrise)),
            "moon_lon": float(sidereal_longitude("moon", sunrise)),
        }
        return _localize(rows, city.zone)


def _localize(value: Any, zone) -> Any:
    """Every datetime inside value, however nested, moved onto the city's clock."""
    if isinstance(value, dt.datetime):
        return value.astimezone(zone)
    if isinstance(value, dict):
        return {k: _localize(v, zone) for k, v in value.items()}
    if isinstance(value, tuple):
        return tuple(_localize(v, zone) for v in value)
    if isinstance(value, list):
        return [_localize(v, zone) for v in value]
    return value


def compute(city: City, first: dt.date, last: dt.date, sky: Sky | None = None) -> list[dict]:
    sky = sky or Sky(first, last)
    place = Place(sky, city, first, last)
    out = []
    d = first
    while d <= last:
        out.append(place.day(d))
        d += dt.timedelta(days=1)
    return out
