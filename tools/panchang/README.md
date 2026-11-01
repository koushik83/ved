# The panchang generator

The pages under `/panchang/` and `/hi/panchang/` hold the Hindu almanac for each city in `cities.py`, from a first
date to a last date, as one data file per city (`panchang/data/<slug>.json`) that the page reads for the day it is
opened on. Rebuild them before the data runs out, each November for the whole of the year after next:

    .venv\Scripts\python tools\build_panchang.py --first 2027-11-01 --last 2028-12-31

The build needs the site's own environment (`python -m venv .venv`, then `pip install skyfield tzdata`) and the
JPL ephemeris `tools/panchang/ephem/de421.bsp`, 17 MB, downloaded from
<https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/a_old_versions/de421.bsp>; it covers 1900 to 2050
and is not committed. A full build of thirty cities takes a few minutes.

What the engine does and the conventions it follows are stated at the top of `engine.py`. The words are in
`names.py`, the places in `cities.py`, the page and its text in `../build_panchang.py`, and the behaviour in the
browser in `/panchang.js`. Adding a city is one line in `cities.py` and a rebuild.

Before shipping a rebuild, compare a handful of dates and cities against a published panchang: sunrise, moonrise,
the tithi and nakshatra end times, Rahu Kaal. Agreement to the minute is expected; a difference of about a minute on
the tithi and nakshatra ends against some published panchangs is known and is on their side (the new and full moons
here agree with the astronomical almanac to within seconds).
