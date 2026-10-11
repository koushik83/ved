"""Build the number-grid prashnavali pages (Shiv, Ganesh, Durga, Khatu Shyam)
from the JSON answer sets in tools/prashnavali/.

For each tool it writes the English page, the Hindi page under hi/, and a
markdown copy of each. It never touches any other file. Run from the repo root:

    python tools/build_prashnavali.py

The site's shared navigation (two rows: site links, then the prashnavalis) is
defined here as nav_html() and nav_css() so other scripts can reuse it.
"""
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "tools" / "prashnavali"
SITE = "https://vedprashnavali.com"
TOOLS = ["shiv", "ganesh", "durga", "khatushyam"]

# ----------------------------------------------------------------- navigation

SITE_LINKS = {
    "en": [("/", "🏠 Home", "home"), ("/today", "🌅 Today", ""), ("/jaap", "📿 Jaap", "")],
    "hi": [("/", "🏠 होम", "home"), ("/today", "🌅 आज", ""), ("/jaap", "📿 जप", "")],
}
# (slug, English href, English label, Hindi href, Hindi label)
TOOL_LINKS = [
    ("prash", "/prash", "🕉️ Ram", "/hi/prash", "🕉️ राम शलाका"),
    ("hanumanprash", "/hanumanprash", "⚡ Hanuman", "/hi/hanumanprash", "⚡ हनुमान"),
    ("saibabaprash", "/saibabaprash", "🙏 Sai Baba", "/saibabaprash", "🙏 साईं बाबा"),
    ("shivprash", "/shivprash", "🔱 Shiv", "/hi/shivprash", "🔱 शिव"),
    ("ganeshprash", "/ganeshprash", "🐘 Ganesh", "/hi/ganeshprash", "🐘 गणेश"),
    ("durgaprash", "/durgaprash", "🌺 Durga", "/hi/durgaprash", "🌺 दुर्गा"),
    ("khatushyamprash", "/khatushyamprash", "🏹 Khatu Shyam", "/hi/khatushyamprash", "🏹 खाटू श्याम"),
]


def nav_css():
    return """        .ved-nav { border-bottom: 2px solid #ff9933; padding: 8px 8px 6px; background: #FDF4E7; }
        .ved-nav-row { display: flex; justify-content: center; flex-wrap: wrap; gap: 8px 10px; margin: 0 0 8px; }
        .ved-nav-row:last-child { margin-bottom: 0; }
        .ved-nav a { text-decoration: none; color: #333; padding: 6px 12px; font-size: 14px; white-space: nowrap; border-radius: 20px; background: white; border: 1px solid #ff9933; line-height: 1.4; }
        .ved-nav a.home { font-weight: bold; }
        .ved-nav a[aria-current="page"] { background: #ff9933; color: white; border-color: #ff9933; }
        @media (max-width: 600px) {
            .ved-nav-row.tools { flex-wrap: nowrap; justify-content: flex-start; overflow-x: auto; -webkit-overflow-scrolling: touch; scrollbar-width: none; margin: 0 -8px; padding: 2px 12px 6px; }
            .ved-nav-row.tools::-webkit-scrollbar { display: none; }
        }
"""


def nav_html(lang, active_slug=None, switch=None):
    """The two-row navigation. switch = (href, label) for the other-language page, or None."""
    rows = []
    links = ['<a href="%s"%s>%s</a>' % (h, ' class="home"' if c else "", l) for h, l, c in SITE_LINKS[lang]]
    if switch:
        links.append('<a href="%s" lang="%s">%s</a>' % (switch[0], "hi" if lang == "en" else "en", switch[1]))
    rows.append('        <div class="ved-nav-row">' + "".join(links) + "</div>")
    tools = []
    for slug, en_href, en_label, hi_href, hi_label in TOOL_LINKS:
        href, label = (en_href, en_label) if lang == "en" else (hi_href, hi_label)
        cur = ' aria-current="page"' if slug == active_slug else ""
        tools.append('<a href="%s"%s>%s</a>' % (href, cur, label))
    rows.append('        <div class="ved-nav-row tools">' + "".join(tools) + "</div>")
    label = "Site" if lang == "en" else "साइट"
    return ('    <nav class="ved-nav" aria-label="%s">\n' % label + "\n".join(rows) + "\n    </nav>\n"
            '    <script>(function(){var a=document.querySelector(".ved-nav .tools a[aria-current]");'
            'if(a&&a.scrollIntoView){try{a.scrollIntoView({inline:"center",block:"nearest"});}catch(e){}}})();</script>\n')


# ------------------------------------------------------------------ fragments

RULES = {
    "en": ["Ask one question at a time.", "Do not ask the same question repeatedly.", "No more than three questions in a day.",
           "Read the answer with faith and reflect on it. For important decisions, also use your own judgment."],
    "hi": ["एक समय में एक ही प्रश्न पूछें।", "एक ही प्रश्न को बार-बार न पूछें।", "दिन में तीन से अधिक प्रश्न न पूछें।",
           "उत्तर को श्रद्धा से पढ़ें और उस पर विचार करें। महत्वपूर्ण निर्णयों में अपने विवेक का भी उपयोग करें।"],
}
# The other tools, for the cross-link card on every tool page: slug -> (English href, text, Hindi href, text)
OTHERS = [
    ("prash", "/prash", "Ram Shalaka Prashnavali: 225 letters from Shri Ramcharitmanas leading to nine chaupais",
     "/hi/prash", "राम शलाका प्रश्नावली: श्री रामचरितमानस के 225 अक्षर, नौ चौपाइयाँ"),
    ("hanumanprash", "/hanumanprash", "Hanuman Prashnavali: a chakra of 49 numbers with a yes or no answer",
     "/hi/hanumanprash", "हनुमान प्रश्नावली: 49 अंकों का चक्र, हाँ या नहीं में उत्तर"),
    ("saibabaprash", "/saibabaprash", "Sai Baba Prashnavali: 720 numbered answers",
     "/saibabaprash", "साईं बाबा प्रश्नावली: 720 क्रमांकित उत्तर"),
    ("shivprash", "/shivprash", "Shiv Prashnavali: the nine verses of the Rudrashtakam",
     "/hi/shivprash", "शिव प्रश्नावली: रुद्राष्टक के नौ श्लोक"),
    ("ganeshprash", "/ganeshprash", "Ganesh Prashnavali: the twelve names of Ganesha",
     "/hi/ganeshprash", "गणेश प्रश्नावली: गणेश जी के बारह नाम"),
    ("durgaprash", "/durgaprash", "Durga Prashnavali: the nine forms of Navadurga",
     "/hi/durgaprash", "दुर्गा प्रश्नावली: नवदुर्गा के नौ रूप"),
    ("khatushyamprash", "/khatushyamprash", "Khatu Shyam Prashnavali: eleven names of Shyam Baba",
     "/hi/khatushyamprash", "खाटू श्याम प्रश्नावली: श्याम बाबा के ग्यारह नाम"),
]


def others_html(lang, exclude_slug, inline=False):
    """The cross-link list. inline=True gives a self-styled block for pages without the card CSS."""
    items = []
    for slug, en_href, en_text, hi_href, hi_text in OTHERS:
        if slug == exclude_slug:
            continue
        href, text = (en_href, en_text) if lang == "en" else (hi_href, hi_text)
        name, rest = text.split(": ", 1)
        a_style = ' style="color: #A04000;"' if inline else ""
        items.append('<li><a href="%s"%s>%s</a>: %s</li>' % (href, a_style, name, rest))
    heading = "More prashnavalis on this site" if lang == "en" else "इस साइट की अन्य प्रश्नावलियाँ"
    if inline:
        return ('<div style="max-width: 720px; margin: 24px auto; padding: 16px 20px; background: white; border-radius: 12px; '
                'box-shadow: 0 3px 12px rgba(0,0,0,0.08); text-align: left; font-family: Arial, sans-serif; font-size: 16px; line-height: 1.6; color: #333; box-sizing: border-box;">'
                '<h2 style="color: #D35400; font-size: 21px; margin: 0 0 10px;">%s</h2><ul style="margin: 0; padding-left: 22px;">%s</ul></div>'
                % (heading, "".join(items)))
    return '<section class="card"><h2>%s</h2><ul class="others">%s</ul></section>' % (heading, "".join(items))


LABELS = {
    "en": {"rules": "Rules of the Prashnavali", "faq": "Frequently Asked Questions", "share": "Share on WhatsApp",
           "again": "Ask a new question", "switch": "हिंदी में पढ़ें", "home": "Home", "all": "All %d answers",
           "note": "A prashnavali is a devotional practice. For important decisions use your own judgment and take qualified advice.",
           "privacy": "Privacy Policy", "read_in": "Read in Hindi"},
    "hi": {"rules": "प्रश्नावली के नियम", "faq": "अक्सर पूछे जाने वाले प्रश्न", "share": "WhatsApp पर भेजें",
           "again": "नया प्रश्न पूछें", "switch": "Read in English", "home": "होम", "all": "सभी %d उत्तर",
           "note": "प्रश्नावली एक भक्ति-साधना है। महत्वपूर्ण निर्णयों में अपने विवेक का उपयोग करें और योग्य सलाह लें।",
           "privacy": "गोपनीयता नीति", "read_in": "Read in English"},
}

STYLE = """        body { font-family: Arial, sans-serif; background-color: #FDF4E7; color: #333; margin: 0; padding: 0; line-height: 1.6; }
        .wrap { max-width: 720px; margin: 0 auto; padding: 0 15px 10px; }
        h1 { color: #D35400; font-size: 28px; line-height: 1.3; text-align: center; margin: 25px 0 5px; }
        .card { background: white; border-radius: 12px; box-shadow: 0 3px 12px rgba(0, 0, 0, 0.08); padding: 20px; margin: 20px 0; }
        .card h2 { color: #D35400; font-size: 21px; margin: 0 0 12px; }
        .card h3 { color: #A04000; font-size: 17px; margin: 18px 0 6px; }
        .card a { color: #A04000; }
        .card p { margin: 0 0 12px; }
        .card ul, .card ol { margin: 0 0 12px; padding-left: 22px; }
        .card li { margin-bottom: 6px; }
        .lang-switch { text-align: center; margin: 10px 0 0; font-size: 15px; }
        .lang-switch a { color: #A04000; }
        .hero { display: block; width: 160px; height: 160px; border-radius: 50%%; object-fit: cover; margin: 14px auto 0; box-shadow: 0 3px 12px rgba(0, 0, 0, 0.12); }
        .others li { margin-bottom: 8px; }
        .steps-card { background: #fff8e1; border-left: 5px solid #ff9800; border-radius: 8px; padding: 14px 16px; margin: 16px 0; }
        .steps-card ol { margin: 0; padding-left: 22px; }
        .steps-card li { padding: 3px 0; }
        .grid-wrap { background: white; background-image: linear-gradient(rgba(255,255,255,0.88), rgba(255,255,255,0.88)), url('%(image)s'); background-position: center; background-size: contain; background-repeat: no-repeat; border-radius: 10px; padding: 6px 3px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin: 0 0 14px; box-sizing: border-box; }
        table.grid { width: 100%%; table-layout: fixed; border-collapse: collapse; }
        table.grid td { border: 1px solid #E8E8E8; padding: 12px 0; text-align: center; font-size: 17px; cursor: pointer; }
        table.grid.cols11 td { padding: 10px 0; font-size: 14px; }
        table.grid td:hover { background: #D35400; color: white; }
        .answer { display: none; margin: 0 0 14px; }
        .box { background: white; border: 2px solid #A04000; border-radius: 8px; padding: 12px 14px; margin: 0 0 10px; text-align: left; }
        .box .head { color: #A04000; font-weight: bold; margin-bottom: 4px; }
        .box.verse-box .text { font-size: 20px; line-height: 1.6; color: #5D2E00; }
        .sub { display: block; font-size: 0.8em; color: #8a5a2b; font-weight: normal; }
        .box.good { border-color: #4CAF50; background: #E8F5E9; } .box.good .head { color: #2E7D32; }
        .box.caution { border-color: #FF5733; background: #FFF3EF; } .box.caution .head { color: #D32F2F; }
        .box.wait { border-color: #FB8C00; background: #FFF8E1; } .box.wait .head { color: #E65100; }
        .actions { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin: 6px 0 10px; }
        .btn { display: inline-block; min-height: 44px; box-sizing: border-box; padding: 11px 18px; font-size: 16px; border-radius: 22px; text-decoration: none; cursor: pointer; font-family: inherit; }
        .btn-whatsapp { background: #128C7E; border: 1px solid #128C7E; color: white; }
        .btn-fill { background: #ff9933; border: 1px solid #ff9933; color: white; }
        .answers li { margin-bottom: 12px; } .answers .v { color: #5D2E00; font-weight: bold; }
        .answers .good { color: #2E7D32; } .answers .caution { color: #C62828; } .answers .wait { color: #E65100; }
        [hidden] { display: none !important; }
"""

INSTALL = """    <!-- Install app button -->
    <script>
        let installPrompt;
        window.addEventListener("beforeinstallprompt", (event) => {
          event.preventDefault();
          installPrompt = event;
          if (window.matchMedia("(display-mode: standalone)").matches) { return; }
          let installBtn = document.createElement("button");
          installBtn.innerText = "Install App";
          installBtn.style = `position: fixed; top: 15px; left: 50%; transform: translateX(-50%); padding: 10px 20px; font-size: 16px; background: #FFA726; color: #fff; border: none; cursor: pointer; border-radius: 5px; box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2); transition: background 0.3s, transform 0.2s; z-index: 9999;`;
          document.body.appendChild(installBtn);
          installBtn.addEventListener("mouseover", () => { installBtn.style.background = "#FB8C00"; installBtn.style.transform = "translateX(-50%) scale(1.05)"; });
          installBtn.addEventListener("mouseleave", () => { installBtn.style.background = "#FFA726"; installBtn.style.transform = "translateX(-50%) scale(1)"; });
          installBtn.addEventListener("click", () => {
            installPrompt.prompt();
            installPrompt.userChoice.then((choice) => { if (choice.outcome === "accepted") { installBtn.remove(); } else { installBtn.style.display = "none"; } });
          });
          window.addEventListener("appinstalled", () => { installBtn.remove(); });
        });
    </script>
"""

FOOTER = """    <footer style="text-align: center; padding: 25px 15px; margin-top: 40px; background-color: #FDF4E7; border-top: 2px solid #ff9933; font-family: Arial, sans-serif; font-size: 14px; line-height: 1.9; color: #555;">
        <div>
            <a href="/" style="color: #A04000; text-decoration: none; margin: 0 8px; display: inline-block; white-space: nowrap;">Home</a>
            <a href="/today" style="color: #A04000; text-decoration: none; margin: 0 8px; display: inline-block; white-space: nowrap;">Today's Guidance</a>
            <a href="/jaap" style="color: #A04000; text-decoration: none; margin: 0 8px; display: inline-block; white-space: nowrap;">Jaap Counter</a>
            <a href="/about" style="color: #A04000; text-decoration: none; margin: 0 8px; display: inline-block; white-space: nowrap;">About</a>
            <a href="/contact" style="color: #A04000; text-decoration: none; margin: 0 8px; display: inline-block; white-space: nowrap;">Contact</a>
            <a href="/privacy" style="color: #A04000; text-decoration: none; margin: 0 8px; display: inline-block; white-space: nowrap;">Privacy Policy</a>
            <a href="/terms" style="color: #A04000; text-decoration: none; margin: 0 8px; display: inline-block; white-space: nowrap;">Terms</a>
        </div>
        <div>Ved Prashnavali &middot; Delhi, India &middot; <!--email_off--><a href="mailto:vedicprashnavali@gmail.com" style="color: #A04000; text-decoration: none;">vedicprashnavali@gmail.com</a><!--/email_off--></div>
    </footer>
"""


def strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<br\s*/?>", " ", re.sub(r"<[^>]+>", " ", s))).strip()


def jsonld(obj):
    return json.dumps(obj, ensure_ascii=False)


def grid_html(cells):
    cols = 11 if cells % 11 == 0 else 6
    rows = []
    for r in range(cells // cols):
        tds = "".join('<td data-n="%d">%02d</td>' % (r * cols + c + 1, r * cols + c + 1) for c in range(cols))
        rows.append("<tr>" + tds + "</tr>")
    cls = "grid cols11" if cols == 11 else "grid"
    return '<table class="%s" translate="no"><tbody>%s</tbody></table>' % (cls, "".join(rows))


def page(tool, lang):
    t = tool[lang]
    L = LABELS[lang]
    slug = tool["slug"]
    url = SITE + ("/" if lang == "en" else "/hi/") + slug
    other = SITE + ("/hi/" if lang == "en" else "/") + slug
    switch_href = ("/hi/" if lang == "en" else "/") + slug
    cells = tool["cells"]
    image_url = SITE + tool["image"]
    vlang = tool.get("verse_lang", "sa")   # the language of the verse or name shown: Sanskrit unless the tool says otherwise

    answers_js = [{"verse": a["verse"], "meaning": a[lang]["meaning"], "result": a[lang]["result"],
                   "tag": a[lang]["tag"], "tone": a["tone"]} for a in tool["answers"]]

    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": L["home"], "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": t["breadcrumb"], "item": url}]}

    answers_list = "".join(
        '<li><span class="v" lang="%s">%s</span><br>%s<br><span class="%s">%s (%s)</span></li>'
        % (vlang, a["verse"], html.escape(a[lang]["meaning"]), a["tone"], html.escape(a[lang]["result"]), html.escape(a[lang]["tag"]))
        for a in tool["answers"])
    faq_html = "".join("<h3>%s</h3>\n            <p>%s</p>\n            " % (html.escape(q), html.escape(a)) for q, a in t["faq"])
    steps = "".join("<li>%s</li>" % html.escape(s) for s in t["steps"])
    what = "".join("<p>%s</p>\n            " % html.escape(p) for p in t["what"])
    art = tool.get("article_link", {}).get(lang)
    if art:
        what += '<p><a href="%s"><strong>%s</strong></a></p>\n            ' % (art["href"], html.escape(art["text"]))
    rules = "".join("<li>%s</li>" % html.escape(r) for r in RULES[lang])

    labels_js = {"verse": t["verse_label"], "meaning": t["meaning_label"], "answer": t["answer_label"],
                 "shareText": t["share_text"], "shareTitle": t["share_title"]}

    out = f"""<!DOCTYPE html>
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
    <meta property="og:type" content="website">
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
    <script src="/share-card.js" defer></script>
    <script type="application/ld+json">
    {jsonld(crumbs)}
    </script>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4804498427753837"
     crossorigin="anonymous"></script>
    <script src="/anchor-ad.js" defer></script>
    <script src="/side-ads.js" defer></script>
    <style>
{STYLE % {"image": tool["image"]}}{nav_css()}    </style>
    <script type="application/ld+json">
{jsonld(faq_ld)}
    </script>
</head>
<body>
{nav_html(lang, slug, (switch_href, "हिंदी" if lang == "en" else "English"))}
    <main class="wrap">
        <h1>{html.escape(t["h1"])}<span style="display: block; font-size: 0.68em; margin-top: 4px;">{html.escape(t["subtitle"])}</span></h1>
        <p class="lang-switch"><a href="{switch_href}">{L["read_in"]}</a></p>
        <img class="hero" src="{tool["image"]}" alt="{html.escape(tool.get("image_alt", {}).get(lang, ""), quote=True)}" width="160" height="160">
        <div class="steps-card"><ol>{steps}</ol></div>
        <div class="grid-wrap">{grid_html(cells)}</div>
        <div class="answer" id="result"></div>
        <div class="actions" id="actions" hidden>
            <button type="button" class="btn btn-whatsapp" id="share">{L["share"]}</button>
            <button type="button" class="btn btn-fill" id="again">{L["again"]}</button>
        </div>
        <section class="card">
            <h2>{html.escape(t["what_heading"])}</h2>
            {what}</section>
        <section class="card">
            <h2>{html.escape(t["answers_heading"])}</h2>
            <ol class="answers">{answers_list}</ol>
        </section>
        <section class="card">
            <h2>{L["rules"]}</h2>
            <ul>{rules}</ul>
        </section>
        <section class="card">
            <h2>{L["faq"]}</h2>
            {faq_html}</section>
        {others_html(lang, slug)}
        <section class="card note">
            <p style="font-size: 14px; color: #666; margin: 0 0 8px;">{L["note"]} <a href="/privacy">{L["privacy"]}</a>.</p>
            <p style="font-size: 13px; color: #777; margin: 0;">{html.escape(tool["image_credit"][lang])}</p>
        </section>
    </main>
{FOOTER}    <script>
    (function () {{
        var DATA = {jsonld(answers_js)};
        var L = {jsonld(labels_js)};
        var N = DATA.length, NL = String.fromCharCode(10);
        var PAGE = '{url}', TOOL = '{tool["tool"]}', LANG = '{lang}', IMG = '{tool["image"]}', VLANG = '{vlang}';
        var plain = function (s) {{ return String(s).replace(/<br\\s*\\/?>/g, ' ').replace(/<[^>]+>/g, ' ').replace(/\\s+/g, ' ').trim(); }};
        var result = document.getElementById('result'), chosen = null;
        function show(index) {{
            var d = DATA[index]; chosen = index;
            result.innerHTML = '<div class="box verse-box"><div class="head">' + L.verse + '</div><div class="text" lang="' + VLANG + '">' + d.verse + '</div></div>'
                + '<div class="box"><div class="head">' + L.meaning + '</div><div>' + d.meaning + '</div></div>'
                + '<div class="box ' + d.tone + '"><div class="head">' + L.answer + '</div><div>' + d.result + ' <strong>(' + d.tag + ')</strong></div></div>';
            result.style.display = 'block';
            document.getElementById('actions').hidden = false;
            result.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
            if (typeof window.vedTrack === 'function') {{ window.vedTrack('answer_revealed', {{ tool: TOOL, answer_id: String(index + 1), lang: LANG }}); }}
        }}
        var cells = document.querySelectorAll('table.grid td');
        for (var i = 0; i < cells.length; i++) {{ cells[i].addEventListener('click', function () {{ show((parseInt(this.getAttribute('data-n'), 10) - 1) % N); }}); }}
        document.getElementById('share').addEventListener('click', function () {{
            if (chosen === null) {{ return; }}
            if (typeof window.vedTrack === 'function') {{ window.vedTrack('share', {{ method: 'whatsapp', content_type: TOOL, lang: LANG }}); }}
            var d = DATA[chosen], verse = plain(d.verse);
            var text = L.shareText + NL + NL + verse + NL + d.result + ' (' + d.tag + ')';
            var fallback = function () {{ window.open('https://wa.me/?text=' + encodeURIComponent(text + NL + NL + PAGE)); }};
            if (window.vedShareCard) {{ window.vedShareCard({{ title: L.shareTitle, image: IMG, url: PAGE, text: text, verse: verse, meaning: d.meaning, result: d.result + ' (' + d.tag + ')', tone: d.tone }}).then(function (ok) {{ if (!ok) {{ fallback(); }} }}); }} else {{ fallback(); }}
        }});
        document.getElementById('again').addEventListener('click', function () {{
            result.style.display = 'none'; result.innerHTML = ''; chosen = null; document.getElementById('actions').hidden = true;
            if (typeof window.vedTrack === 'function') {{ window.vedTrack('new_question', {{ tool: TOOL, lang: LANG }}); }}
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }});
    }})();
    </script>

{INSTALL}</body>
</html>
"""
    return out


def markdown(tool, lang):
    t = tool[lang]
    L = LABELS[lang]
    slug = tool["slug"]
    url = SITE + ("/" if lang == "en" else "/hi/") + slug
    other = SITE + ("/hi/" if lang == "en" else "/") + slug
    lines = ["# " + t["title"], "", "Source: " + url, "", "[%s](%s)" % (L["read_in"], other), "",
             "## " + t["what_heading"], ""]
    for p in t["what"]:
        lines += [p, ""]
    art = tool.get("article_link", {}).get(lang)
    if art:
        lines += ["[%s](%s%s)" % (art["text"], SITE, art["href"]), ""]
    lines += ["## " + t["answers_heading"], ""]
    for i, a in enumerate(tool["answers"], 1):
        lines.append("%d. %s. %s %s (%s)" % (i, strip_tags(a["verse"]), a[lang]["meaning"], a[lang]["result"], a[lang]["tag"]))
    lines += ["", "## " + L["rules"], ""] + ["- " + r for r in RULES[lang]] + ["", "## " + L["faq"], ""]
    for q, a in t["faq"]:
        lines += ["### " + q, "", a, ""]
    lines += ["## " + ("More prashnavalis on this site" if lang == "en" else "इस साइट की अन्य प्रश्नावलियाँ"), ""]
    for o_slug, en_href, en_text, hi_href, hi_text in OTHERS:
        if o_slug != slug:
            href, text = (en_href, en_text) if lang == "en" else (hi_href, hi_text)
            lines.append("- %s %s" % (text, SITE + href))
    lines.append("")
    lines += [L["note"] + " [%s](%s/privacy)." % (L["privacy"], SITE), "", tool["image_credit"][lang], ""]
    return "\n".join(lines)


def build():
    written = []
    for name in TOOLS:
        tool = json.loads((DATA / f"{name}.json").read_text(encoding="utf-8"))
        assert tool["cells"] % len(tool["answers"]) == 0, name
        for lang in ("en", "hi"):
            folder = ROOT if lang == "en" else ROOT / "hi"
            (folder / f"{tool['slug']}.html").write_text(page(tool, lang), encoding="utf-8")
            (folder / f"{tool['slug']}.md").write_text(markdown(tool, lang), encoding="utf-8")
            written.append(str((folder / f"{tool['slug']}.html").relative_to(ROOT)))
    return written


if __name__ == "__main__":
    for w in build():
        print("wrote", w)
