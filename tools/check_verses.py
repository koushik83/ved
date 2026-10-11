"""Check every Devanagari verse in the answer sets and articles against the
source texts fetched from Wikisource and Wikipedia (a folder of .txt files
passed as the first argument). A verse passes when its text, with whitespace,
dandas and verse numbers stripped, appears in some source file the same way.

Known edition variants are listed in ALLOWED, with the reading the source
has; anything else that does not match is reported and the exit code is 1.

    python tools/check_verses.py <folder with the fetched source texts>
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
FILES = [ROOT / "tools" / "prashnavali" / n for n in ("shiv.json", "ganesh.json", "durga.json")] + \
        [ROOT / "tools" / "articles" / n for n in ("rudrashtakam.json", "navadurga.json", "sankat-nashan.json")]

# verse fragment as printed here -> the source edition's reading (scan or edition variants)
ALLOWED = {
    "भक्तावासं स्मरेन्नित्यमायुःकामार्थसिद्धये": "भक्तावासं स्मरेनित्यमायुकामार्थसिद्धये",
    "गजवक्त्रं चतुर्थकम्": "गजवक्र चतुर्थकम्",
    "लम्बोदरं पञ्चमं च": "लम्बोदरं पञ्चमै च",
    "सप्तमं विघ्नराजेन्द्रं धूम्रवर्णं तथाष्टमम्": "सप्तमं विघ्नराजं च धूम्रवर्ण तथाष्टमम्",
    "नवमं भालचन्द्रं च": "नवमं फालचन्द्रं च",
    "एकादशं गणपतिं द्वादशं": "एकादशं गणपति द्वादशं",
    "द्वादशैतानि नामानि त्रिसन्ध्यं यः पठेन्नरः": "द्वादशेतानि नामानि त्रिसन्ध्यं य: पठेन्नरः",
    "न च विघ्नभयं तस्य": "नव विघ्नभयं तस्य",
    "जपेद्गणपतिस्तोत्रं षड्भिर्मासैः फलं लभेत्": "जपेद्गणपतिस्तोत्रं षभिर्मासै: फलं लभेत्",
    "कूष्माण्डा शुभदास्तु मे": "कूष्माण्डा शुभदाऽस्तु मे",
    "शुभदास्तु सदा देवी स्कन्दमाता": "शुभदाऽस्तु सदा देवी स्कन्दमाता",
    "कात्यायनी शुभं दद्याद्देवी दानवघातिनी": "कात्यायनी शुभं दद्याद्देवी दानव-घातिनी",
    "महागौरी शुभं दद्यान्महादेवप्रमोददा": "महागौरी शुभं दद्यान्महादेव-प्रमोद-दा",
    "सिद्धगन्धर्वयक्षाद्यैरसुरैरमरैरपि": "सिद्धगन्धर्व-यक्षाद्यैरसुरैरमरैरपि",
    # the Navadurga page on Hindi Wikipedia prints a typo (केर्) where the instrumental कैर् is standard;
    # the Chandraghanta page itself has कैर्युता
    "पिण्डजप्रवरारूढा चण्डकोपास्त्रकैर्युता": "पिण्डजप्रवरारूढा चण्डकोपास्त्रकेर्युता",
    # OCR slip in the Wikisource scan (लमते for लभते)
    "धनार्थी लभते धनम्": "धनार्थी लमते धनम्",
}


def norm(s):
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"[॥।।॥|]", " ", s)
    s = re.sub(r"[०-९0-9]+", " ", s)
    s = s.replace("‍", "").replace("‌", "").replace(" ", " ")
    s = re.sub(r"[\s\-‌‍]+", "", s)
    return s


def main(src_dir):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    sources = "".join(norm(p.read_text(encoding="utf-8", errors="replace")) for p in pathlib.Path(src_dir).glob("*.txt"))
    allowed = {norm(k): norm(v) for k, v in ALLOWED.items()}
    bad = []
    checked = 0
    for f in FILES:
        data = json.loads(f.read_text(encoding="utf-8"))
        items = data["answers"] if "answers" in data else data["verses"]
        for item in items:
            text = item.get("verse", item.get("text", ""))
            # drop the name/epithet line of the Ganesh entries, keep the quoted half-line; articles keep whole verses
            parts = re.split(r"<br\s*/?>", text)
            for part in parts:
                plain = re.sub(r"<[^>]+>", " ", part)
                if not re.search(r"[ऀ-ॿ]", plain):
                    continue
                for piece in re.split(r"[।॥]", plain):
                    n = norm(piece)
                    if len(n) < 8 or " " not in piece.strip():
                        continue   # too short, or a bare name rather than a verse line
                    checked += 1
                    if n in sources:
                        continue
                    alt = next((v for k, v in allowed.items() if k in n or n in k), None)
                    if alt and alt in sources:
                        continue
                    bad.append((f.name, piece.strip()))
    print("checked %d verse lines" % checked)
    for name, piece in bad:
        print("NOT IN SOURCES:", name, piece)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
