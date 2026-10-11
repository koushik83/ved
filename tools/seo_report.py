"""Monthly Search Console report for the prashnavali query families.

Export the Performance report from Search Console (last 28 days, Search type
Web) and put its CSV files in a folder: Queries.csv and Pages.csv are the two
it uses. Then:

    python tools/seo_report.py <folder> [--floor 5]

For each family in tools/seo/families.json it prints the top queries by
impressions with average position and clicks, the family's pages with their
position, the striking-distance queries (position 4 to 20 with impressions at
or above the floor), and the query words that appear in none of the family's
page titles, H1s or FAQ questions. The folder is copied under
tools/seo/snapshots/<date>/ so the next run can show movement against it.
"""
import csv
import datetime
import json
import pathlib
import re
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
FAMILIES = json.loads((ROOT / "tools" / "seo" / "families.json").read_text(encoding="utf-8"))
SNAP = ROOT / "tools" / "seo" / "snapshots"


def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    out = []
    for r in rows:
        key = next((k for k in r if k.lower().startswith("top ")), None)
        if not key:
            continue
        def num(v):
            v = str(v or "").replace("%", "").replace(",", "").strip()
            try:
                return float(v)
            except ValueError:
                return 0.0
        out.append({"name": r[key].strip(), "clicks": num(r.get("Clicks")), "impressions": num(r.get("Impressions")),
                    "ctr": num(r.get("CTR")), "position": num(r.get("Position"))})
    return out


def family_of(query):
    q = query.lower()
    for fam, spec in FAMILIES.items():
        if fam.startswith("_"):
            continue
        if any(w in q for w in spec["words"]):
            return fam
    return None


def page_text(path):
    """Title, H1 and FAQ questions of a page on disk, lower-cased, for the coverage check."""
    f = ROOT / (path.strip("/") + ".html")
    if not f.exists():
        return ""
    s = f.read_text(encoding="utf-8", errors="replace")
    parts = re.findall(r"<title>(.*?)</title>", s, re.S) + re.findall(r"<h1[^>]*>(.*?)</h1>", s, re.S) + re.findall(r"<h3>(.*?)</h3>", s, re.S)
    return re.sub(r"<[^>]+>", " ", " ".join(parts)).lower()


def previous_snapshot():
    if not SNAP.exists():
        return None
    dirs = sorted(d for d in SNAP.iterdir() if d.is_dir())
    return dirs[-1] if dirs else None


def main(folder, floor):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")   # Devanagari queries on a Windows console
    except AttributeError:
        pass
    folder = pathlib.Path(folder)
    queries = read_csv(folder / "Queries.csv") if (folder / "Queries.csv").exists() else []
    pages = read_csv(folder / "Pages.csv") if (folder / "Pages.csv").exists() else []
    prev = previous_snapshot()
    prev_pages = {}
    if prev and (prev / "Pages.csv").exists():
        prev_pages = {p["name"]: p for p in read_csv(prev / "Pages.csv")}

    for fam, spec in FAMILIES.items():
        if fam.startswith("_"):
            continue
        fq = sorted((q for q in queries if family_of(q["name"]) == fam), key=lambda q: -q["impressions"])
        print("\n=== %s: %d queries, %d impressions, %d clicks" % (fam, len(fq), sum(q["impressions"] for q in fq), sum(q["clicks"] for q in fq)))
        print("-- pages (position now, previous)")
        for path in spec["pages"]:
            url = "https://vedprashnavali.com" + path
            row = next((p for p in pages if p["name"].rstrip("/") == url), None)
            old = prev_pages.get(url)
            print("   %-40s %s %s" % (path, ("pos %.1f, %d impr, %d clicks" % (row["position"], row["impressions"], row["clicks"])) if row else "no data",
                                      ("(was %.1f)" % old["position"]) if old else ""))
        print("-- top queries")
        for q in fq[:12]:
            print("   %-45s impr %5d  pos %5.1f  clicks %3d" % (q["name"][:45], q["impressions"], q["position"], q["clicks"]))
        print("-- striking distance (position 4 to 20, impressions >= %d)" % floor)
        for q in fq:
            if 4 <= q["position"] <= 20 and q["impressions"] >= floor:
                print("   %-45s impr %5d  pos %5.1f" % (q["name"][:45], q["impressions"], q["position"]))
        covered = " ".join(page_text(p) for p in spec["pages"])
        missing = sorted({w for q in fq if q["impressions"] >= floor for w in re.findall(r"[\wऀ-ॿ]+", q["name"].lower())
                          if len(w) > 2 and w not in covered})
        print("-- query words not in any title, H1 or FAQ of these pages:", ", ".join(missing) if missing else "none")

    other = [q for q in queries if family_of(q["name"]) is None]
    print("\n=== outside the four families: %d queries, %d impressions" % (len(other), sum(q["impressions"] for q in other)))

    stamp = datetime.date.today().isoformat()
    dest = SNAP / stamp
    dest.mkdir(parents=True, exist_ok=True)
    for name in ("Queries.csv", "Pages.csv"):
        if (folder / name).exists():
            shutil.copy(folder / name, dest / name)
    print("\nsnapshot saved under", dest.relative_to(ROOT))


if __name__ == "__main__":
    args = sys.argv[1:]
    floor = 5
    if "--floor" in args:
        i = args.index("--floor")
        floor = int(args[i + 1])
        del args[i:i + 2]
    if not args:
        print(__doc__)
        sys.exit(2)
    main(args[0], floor)
