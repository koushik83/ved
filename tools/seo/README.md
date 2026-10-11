# The Search Console loop

Goal set on 2026-10-11: each of the four new prashnavalis in the top 3 for its
query family within four months. The families and their pages are in
`families.json`. This is the monthly procedure that moves positions.

## Now, once

1. Search Console, Sitemaps: submit `https://vedprashnavali.com/sitemap.xml`.
2. URL Inspection, Request indexing, for each of the sixteen new URLs: the four
   tool pages and four articles, in English and under `/hi/`.

## Every month

1. Search Console, Performance, Search results. Date: last 28 days. Search
   type: Web. Export, and unzip; the two files that matter are `Queries.csv`
   and `Pages.csv`.
2. Run, from the repo root:

       python tools/seo_report.py <folder with the two CSVs>

   It prints, per family: the family's pages with their position and the
   previous month's, the top queries, the striking-distance queries (position
   4 to 20) and the query words that none of the family's titles, H1s or FAQs
   contain. The input is copied under `snapshots/<date>/` for next month's
   comparison. Commit the snapshot.
3. Act on it, in this order:
   - A query word missing from the pages: add it to a FAQ question or the
     opening paragraph in the tool's JSON (`tools/prashnavali/`) or the
     article's JSON (`tools/articles/`), regenerate, commit. FAQs can change
     any month.
   - A striking-distance query with real impressions: make sure the exact
     phrase is in the title or H1 of the page that should rank for it. Rewrite
     a title at most once a month, and never within the first 28 days of data
     for that page; a title change resets the signal.
   - A page that lost position against the snapshot: check it still loads,
     still has its hreflang pair, and that no other page on the site now
     targets the same phrase.
4. Regenerate after any JSON change:

       python tools/build_prashnavali.py
       python tools/build_articles.py
       python tools/check_verses.py <folder of fetched source texts>

The first export, in week 2 after indexing, is the baseline; do not change
titles on it. Position 3 is measured on the family's main query (for example
"shiv prashnavali" and "शिव प्रश्नावली"), with the article pages ranking for
the text queries ("rudrashtakam with meaning") feeding the tool.

## What is outside this loop

Links from other sites, mentions in forums and videos, and shares. Those are
what separate position 5 from position 2 on the harder families, and they are
not something the pages can do for themselves.
