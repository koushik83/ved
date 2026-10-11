"""Build the supporting articles (the text behind each prashnavali) from the
JSON files in tools/articles/. Each article is written in English and Hindi,
with a markdown copy of each, and links to its prashnavali. Run from the repo
root:

    python tools/build_articles.py

The navigation, footer and install button come from build_prashnavali.py so
the pages match the rest of the site.
"""
import html
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_prashnavali import FOOTER, INSTALL, SITE, jsonld, nav_css, nav_html, strip_tags  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "tools" / "articles"
ARTICLES = ["rudrashtakam", "navadurga", "sankat-nashan", "khatu-shyam"]

LABELS = {
    "en": {"home": "Home", "faq": "Frequently Asked Questions", "read_in": "Read in Hindi", "privacy": "Privacy Policy",
           "note": "The verses are traditional texts; the explanations are the site's own words, offered for reflection, not as a guarantee of any outcome."},
    "hi": {"home": "होम", "faq": "अक्सर पूछे जाने वाले प्रश्न", "read_in": "Read in English", "privacy": "गोपनीयता नीति",
           "note": "श्लोक पारम्परिक पाठ हैं; व्याख्याएँ साइट के अपने शब्द हैं, चिंतन के लिए, किसी परिणाम की गारंटी के रूप में नहीं।"},
}

STYLE = """        body { font-family: Arial, sans-serif; background-color: #FDF4E7; color: #333; margin: 0; padding: 0; line-height: 1.7; }
        .wrap { max-width: 720px; margin: 0 auto; padding: 0 15px 10px; }
        h1 { color: #D35400; font-size: 28px; line-height: 1.3; text-align: center; margin: 25px 0 5px; }
        .lang-switch { text-align: center; margin: 10px 0 0; font-size: 15px; }
        .lang-switch a { color: #A04000; }
        .hero { display: block; width: 160px; height: 160px; border-radius: 50%%; object-fit: cover; margin: 14px auto 0; box-shadow: 0 3px 12px rgba(0, 0, 0, 0.12); }
        .card { background: white; border-radius: 12px; box-shadow: 0 3px 12px rgba(0, 0, 0, 0.08); padding: 20px; margin: 20px 0; }
        .card h2 { color: #D35400; font-size: 22px; margin: 0 0 12px; }
        .card h3 { color: #A04000; font-size: 18px; margin: 18px 0 6px; }
        .card a { color: #A04000; }
        .card p { margin: 0 0 12px; font-size: 17px; }
        .card ul, .card ol { margin: 0 0 12px; padding-left: 22px; }
        .card li { margin-bottom: 6px; }
        .intro p { font-size: 17px; margin: 14px 0; }
        .verse { background: white; border: 2px solid #A04000; border-radius: 8px; padding: 12px 14px; margin: 0 0 14px; }
        .verse .head { color: #A04000; font-weight: bold; margin-bottom: 4px; }
        .verse .text { font-size: 20px; line-height: 1.6; color: #5D2E00; margin-bottom: 8px; }
        .verse .meaning { font-size: 16px; }
        .cta { text-align: center; margin: 18px 0; }
        .btn { display: inline-block; min-height: 44px; box-sizing: border-box; padding: 11px 22px; font-size: 17px; border-radius: 22px; text-decoration: none; background: #ff9933; color: white; border: 1px solid #ff9933; font-weight: bold; }
        [hidden] { display: none !important; }
"""


def paras(items):
    return "".join("<p>%s</p>\n" % html.escape(p) for p in items)


def page(a, lang):
    t = a[lang]
    L = LABELS[lang]
    slug = a["slug"]
    url = SITE + ("/" if lang == "en" else "/hi/") + slug
    switch_href = ("/hi/" if lang == "en" else "/") + slug
    tool_href = ("/" if lang == "en" else "/hi/") + a["tool_slug"]
    if a.get("tool_english_only"):
        tool_href = "/" + a["tool_slug"]
    vlang = a.get("verse_lang", "sa")
    image_url = SITE + a["image"]
    alt = a.get("image_alt", {}).get(lang, "")

    verses_html = ""
    for i, v in enumerate(a["verses"], 1):
        head = v.get(lang, {}).get("title") or ("%s %d" % (t["verse_word"], i))
        verses_html += ('<div class="verse"><div class="head">%s</div><div class="text" lang="%s">%s</div>'
                        '<div class="meaning">%s</div></div>\n'
                        % (html.escape(head), vlang, v["text"], html.escape(v[lang]["meaning"])))

    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in t["faq"]]}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": L["home"], "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": t["breadcrumb"], "item": url}]}
    article_ld = {"@context": "https://schema.org", "@type": "Article", "headline": t["h1"], "description": t["description"],
                  "image": image_url, "datePublished": a["date_published"], "dateModified": a.get("date_modified", a["date_published"]),
                  "inLanguage": lang, "mainEntityOfPage": url,
                  "author": {"@type": "Organization", "name": "Ved Prashnavali", "url": SITE + "/"},
                  "publisher": {"@type": "Organization", "name": "Ved Prashnavali", "url": SITE + "/",
                                "logo": {"@type": "ImageObject", "url": SITE + "/favicon/android-chrome-512x512.png"}}}
    faq_html = "".join("<h3>%s</h3>\n            <p>%s</p>\n            " % (html.escape(q), html.escape(ans)) for q, ans in t["faq"])
    cta = '<p class="cta"><a class="btn" href="%s">%s</a></p>' % (tool_href, html.escape(t["cta"]))

    sections = ""
    for sec in t["sections"]:
        sections += '        <section class="card">\n            <h2>%s</h2>\n            %s        </section>\n' % (html.escape(sec["heading"]), paras(sec["paragraphs"]).replace("\n", "\n            "))

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(t["title"])}</title>
    <link rel="canonical" href="{url}" />
    <link rel="alternate" hreflang="en" href="{SITE}/{slug}" />
    <link rel="alternate" hreflang="hi" href="{SITE}/hi/{slug}" />
    <link rel="alternate" hreflang="x-default" href="{SITE}/{slug}" />
    <link rel="apple-touch-icon" sizes="180x180" href="/favicon/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon/favicon-16x16.png">
    <link rel="manifest" href="/favicon/site.webmanifest">
    <meta name="description" content="{html.escape(t["description"], quote=True)}">
    <meta property="og:title" content="{html.escape(t["title"], quote=True)}">
    <meta property="og:description" content="{html.escape(t["description"], quote=True)}">
    <meta property="og:url" content="{url}">
    <meta property="og:type" content="article">
    <meta property="og:image" content="{image_url}">
    <meta name="twitter:card" content="summary_large_image">

    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-32DZ0S3QTT"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'G-32DZ0S3QTT');
    </script>
    <script src="/app-events.js" defer></script>
    <script type="application/ld+json">
    {jsonld(crumbs)}
    </script>
    <script type="application/ld+json">
    {jsonld(article_ld)}
    </script>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4804498427753837"
     crossorigin="anonymous"></script>
    <script src="/anchor-ad.js" defer></script>
    <script src="/side-ads.js" defer></script>
    <style>
{STYLE % {}}{nav_css()}    </style>
    <script type="application/ld+json">
{jsonld(faq_ld)}
    </script>
</head>
<body>
{nav_html(lang, a["tool_slug"], (switch_href, "हिंदी" if lang == "en" else "English"))}
    <main class="wrap">
        <h1>{html.escape(t["h1"])}</h1>
        <p class="lang-switch"><a href="{switch_href}">{L["read_in"]}</a></p>
        <img class="hero" src="{a["image"]}" alt="{html.escape(alt, quote=True)}" width="160" height="160">
        <div class="intro">
{paras(t["intro"])}        </div>
        {cta}
        <section class="card">
            <h2>{html.escape(t["verses_heading"])}</h2>
{verses_html}        </section>
{sections}        <section class="card">
            <h2>{L["faq"]}</h2>
            {faq_html}</section>
        <div class="intro">
{paras(t["closing"])}        </div>
        {cta}
        <section class="card">
            <p style="font-size: 14px; color: #666; margin: 0 0 8px;">{L["note"]} <a href="/privacy">{L["privacy"]}</a>.</p>
            <p style="font-size: 13px; color: #777; margin: 0;">{html.escape(a["image_credit"][lang])}</p>
        </section>
    </main>
{FOOTER}
{INSTALL}</body>
</html>
"""


def markdown(a, lang):
    t = a[lang]
    L = LABELS[lang]
    slug = a["slug"]
    url = SITE + ("/" if lang == "en" else "/hi/") + slug
    other = SITE + ("/hi/" if lang == "en" else "/") + slug
    tool = SITE + ("/" if lang == "en" or a.get("tool_english_only") else "/hi/") + a["tool_slug"]
    lines = ["# " + t["title"], "", "Source: " + url, "", "[%s](%s)" % (L["read_in"], other), ""]
    lines += t["intro"] + ["", "[%s](%s)" % (t["cta"], tool), "", "## " + t["verses_heading"], ""]
    for i, v in enumerate(a["verses"], 1):
        head = v.get(lang, {}).get("title") or ("%s %d" % (t["verse_word"], i))
        lines += ["### " + head, "", strip_tags(v["text"]), "", v[lang]["meaning"], ""]
    for sec in t["sections"]:
        lines += ["## " + sec["heading"], ""] + [p + "\n" for p in sec["paragraphs"]]
    lines += ["## " + L["faq"], ""]
    for q, ans in t["faq"]:
        lines += ["### " + q, "", ans, ""]
    lines += t["closing"] + ["", "[%s](%s)" % (t["cta"], tool), "", L["note"], "", a["image_credit"][lang], ""]
    return "\n".join(lines)


def build():
    written = []
    for name in ARTICLES:
        a = json.loads((DATA / f"{name}.json").read_text(encoding="utf-8"))
        for lang in ("en", "hi"):
            folder = ROOT if lang == "en" else ROOT / "hi"
            (folder / f"{a['slug']}.html").write_text(page(a, lang), encoding="utf-8")
            (folder / f"{a['slug']}.md").write_text(markdown(a, lang), encoding="utf-8")
            written.append(str((folder / f"{a['slug']}.html").relative_to(ROOT)))
    return written


if __name__ == "__main__":
    for w in build():
        print("wrote", w)
