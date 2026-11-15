"""Keep sitemap.xml in step with the pages: every page listed, nothing listed that is gone, and each lastmod the
date the page last changed.

Run from the repo root after any page is built or edited, and before committing:

    python -B tools/update_sitemap.py           # rewrite sitemap.xml where it is out of step
    python -B tools/update_sitemap.py --check   # say what is out of step and exit 1, writing nothing

A page is every .html file git tracks or would track, except 404.html and any page marked noindex. Its lastmod is
the date of the last commit that changed it, or today when it has changes not yet committed, so a rebuild that
leaves a page byte-for-byte the same leaves its date alone. Other files the sitemap lists (the PDFs) stay while they
exist and are dated the same way. Entries keep their order, change frequency and priority; a new page is added at
the end with the frequency and priority its generator passes in `hints`, or monthly and 0.7.
"""
from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import re
import subprocess
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = "https://vedprashnavali.com"
SITEMAP = ROOT / "sitemap.xml"
DEFAULT = ("monthly", "0.7")
NOT_PAGES = {"404.html"}
URL_RE = re.compile(r"<url>\s*<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>\s*<changefreq>([^<]+)</changefreq>\s*"
                    r"<priority>([^<]+)</priority>\s*</url>")
NOINDEX_RE = re.compile(r"<meta[^>]+name=[\"']robots[\"'][^>]+noindex", re.I)


def _git(*args: str) -> str:
    return subprocess.run(["git", "-c", "core.quotePath=false", "-C", str(ROOT), *args], capture_output=True,
                          text=True, encoding="utf-8", check=True).stdout


def url_of(rel: str) -> str:
    """The clean address a file is served at: index.html is /, x/index.html is /x/, a.html is /a."""
    if rel.endswith(".html"):
        stem = rel[: -len(".html")]
        if stem == "index":
            return SITE + "/"
        if stem.endswith("/index"):
            return SITE + "/" + stem[: -len("index")]
        return SITE + "/" + stem
    return SITE + "/" + rel


def file_of(url: str) -> str | None:
    """The file behind an address the sitemap lists, or None when there is none."""
    path = url[len(SITE):].lstrip("/") if url.startswith(SITE) else None
    if path is None:
        return None
    for rel in (path, (path + "index.html") if path.endswith("/") or not path else None, path + ".html"):
        if rel and (ROOT / rel).is_file():
            return rel
    return None


def pages() -> list[str]:
    """Every page the site serves for search: tracked or new .html files, less 404 and noindex pages."""
    out = []
    for rel in _git("ls-files", "--cached", "--others", "--exclude-standard", "--", "*.html").splitlines():
        if rel in NOT_PAGES or not (ROOT / rel).is_file():
            continue
        text = (ROOT / rel).read_text(encoding="utf-8", errors="replace")
        head = text[: text.find("</head>")] if "</head>" in text else text
        if not NOINDEX_RE.search(head):
            out.append(rel)
    return sorted(set(out))


def change_dates(today: dt.date) -> dict[str, str]:
    """The date each file last changed: today for uncommitted changes, else its last commit's date."""
    dates: dict[str, str] = {}
    date = None
    for line in _git("log", "--format=@@%cs", "--name-only").splitlines():
        if line.startswith("@@"):
            date = line[2:]
        elif line and line not in dates and date:
            dates[line] = date
    tokens = _git("status", "--porcelain", "-z", "--untracked-files=all").split("\0")
    i = 0
    while i < len(tokens):
        entry = tokens[i]
        i += 1
        if len(entry) < 4:
            continue
        dates[entry[3:]] = today.isoformat()
        if "R" in entry[:2] or "C" in entry[:2]:
            i += 1  # a rename or copy names its old path next
    return dates


def update(hints: dict[str, tuple[str, str]] | None = None, today: dt.date | None = None,
           write: bool = True) -> dict:
    """Bring sitemap.xml in step. hints: {url: (changefreq, priority)} for pages a generator adds."""
    today = today or dt.date.today()
    hints = hints or {}
    raw = SITEMAP.read_bytes().decode("utf-8")
    nl = "\r\n" if "\r\n" in raw else "\n"
    text = raw.replace("\r\n", "\n")
    entries = [list(m) for m in URL_RE.findall(text)]
    if len(entries) != text.count("<url>"):
        raise SystemExit("sitemap.xml has an entry this tool does not read (an extra tag?); update it by hand")
    dates = change_dates(today)
    wanted = {url_of(rel): rel for rel in pages()}
    report: dict[str, Any] = {"added": [], "removed": [], "redated": []}
    kept, seen = [], set()
    for loc, lastmod, freq, prio in entries:
        if loc in seen:
            report["removed"].append(loc)
            continue
        seen.add(loc)
        rel = wanted.get(loc)
        if rel is None:
            other = file_of(loc)
            rel = other if other and not other.endswith(".html") else None
        if rel is None:
            report["removed"].append(loc)
            continue
        new = dates.get(rel, lastmod)
        if new != lastmod:
            report["redated"].append((loc, lastmod, new))
        kept.append((loc, new, freq, prio))
    new_urls = [u for u in hints if u in wanted and u not in seen]
    new_urls += sorted(u for u in wanted if u not in seen and u not in hints)
    for loc in new_urls:
        freq, prio = hints.get(loc, DEFAULT)
        kept.append((loc, dates.get(wanted[loc], today.isoformat()), freq, prio))
        report["added"].append(loc)
    body = "".join(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lastmod}</lastmod>\n"
                   f"    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>\n  </url>\n"
                   for loc, lastmod, freq, prio in kept)
    out = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "</urlset>")
    if text.endswith("\n"):
        out += "\n"
    report["changed"] = out != text
    report["entries"] = len(kept)
    if write and report["changed"]:
        SITEMAP.write_bytes(out.replace("\n", nl).encode("utf-8"))
    return report


def describe(report: dict) -> str:
    lines = [f"{report['entries']} entries; {len(report['added'])} added, {len(report['removed'])} removed, "
             f"{len(report['redated'])} redated"]
    lines += [f"  added    {u}" for u in report["added"][:20]]
    lines += [f"  removed  {u}" for u in report["removed"][:20]]
    moves: dict[tuple[str, str], int] = {}
    for _, old, new in report["redated"]:
        moves[(old, new)] = moves.get((old, new), 0) + 1
    lines += [f"  redated  {n} from {old} to {new}" for (old, new), n in sorted(moves.items())]
    return "\n".join(lines)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Keep sitemap.xml in step with the pages.")
    ap.add_argument("--check", action="store_true", help="report only; exit 1 if the sitemap is out of step")
    a = ap.parse_args()
    r = update(write=not a.check)
    print(describe(r))
    if a.check and r["changed"]:
        raise SystemExit(1)
