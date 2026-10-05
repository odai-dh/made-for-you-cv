"""
cv_common.py: shared helpers for fill_template.py and build_docx.py.

Section labels per language, localized dates, and section ordering. Standard
library only.
"""

import datetime
import re

DEFAULT_ORDER = ["experience", "projects", "education", "skills", "languages"]

# label keys: PROFILE EXPERIENCE PROJECTS SELECTED_PROJECTS EDUCATION SKILLS LANGUAGES CONTACT
LABELS = {
    "en": ("Profile", "Experience", "Projects", "Selected Projects", "Education", "Skills", "Languages", "Contact"),
    "sv": ("Profil", "Erfarenhet", "Projekt", "Utvalda projekt", "Utbildning", "Kompetenser", "Språk", "Kontakt"),
    "da": ("Profil", "Erfaring", "Projekter", "Udvalgte projekter", "Uddannelse", "Kompetencer", "Sprog", "Kontakt"),
    "nb": ("Profil", "Erfaring", "Prosjekter", "Utvalgte prosjekter", "Utdanning", "Kompetanse", "Språk", "Kontakt"),
    "de": ("Profil", "Berufserfahrung", "Projekte", "Ausgewählte Projekte", "Ausbildung", "Kenntnisse", "Sprachen", "Kontakt"),
    "nl": ("Profiel", "Werkervaring", "Projecten", "Geselecteerde projecten", "Opleiding", "Vaardigheden", "Talen", "Contact"),
    "fr": ("Profil", "Expérience", "Projets", "Projets sélectionnés", "Formation", "Compétences", "Langues", "Contact"),
}
LABEL_KEYS = ("PROFILE", "EXPERIENCE", "PROJECTS", "SELECTED_PROJECTS", "EDUCATION", "SKILLS", "LANGUAGES", "CONTACT")

MONTHS = {
    "en": "January February March April May June July August September October November December".split(),
    "sv": "januari februari mars april maj juni juli augusti september oktober november december".split(),
    "da": "januar februar marts april maj juni juli august september oktober november december".split(),
    "nb": "januar februar mars april mai juni juli august september oktober november desember".split(),
    "de": "Januar Februar März April Mai Juni Juli August September Oktober November Dezember".split(),
    "nl": "januari februari maart april mei juni juli augustus september oktober november december".split(),
    "fr": "janvier février mars avril mai juin juillet août septembre octobre novembre décembre".split(),
}
# {d} {month} {y}; German uses "5. Oktober 2026", everything else "5 October 2026".
DATE_FORMAT = {"de": "{d}. {month} {y}"}

ALIASES = {"no": "nb", "nn": "nb"}


def normalize_lang(value):
    """'sv-SE' -> 'sv', 'no' -> 'nb'. Returns (code, known)."""
    code = (value or "en").strip().lower().replace("_", "-").split("-")[0] or "en"
    code = ALIASES.get(code, code)
    return (code, True) if code in LABELS else (code, False)


def labels_for(lang):
    code, known = normalize_lang(lang)
    values = LABELS[code if known else "en"]
    return {f"H_{k}": v for k, v in zip(LABEL_KEYS, values)}


def localize_date(value, lang):
    """Localize an ISO date (YYYY-MM-DD). Empty -> today. Anything else is returned unchanged."""
    code, known = normalize_lang(lang)
    code = code if known else "en"
    value = (value or "").strip()
    if not value:
        d = datetime.date.today()
    else:
        m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", value)
        if not m:
            return value
        d = datetime.date(int(m[1]), int(m[2]), int(m[3]))
    fmt = DATE_FORMAT.get(code, "{d} {month} {y}")
    return fmt.format(d=d.day, month=MONTHS[code][d.month - 1], y=d.year)


def parse_order(value):
    """'education, projects' or a list -> validated list of section names."""
    if not value:
        return []
    if isinstance(value, str):
        items = [x.strip().lower() for x in value.split(",")]
    else:
        items = [str(x).strip().lower() for x in value]
    out = []
    for it in items:
        if it in DEFAULT_ORDER and it not in out:
            out.append(it)
    return out


def full_order(value):
    """Requested sections first, then the rest in default order."""
    first = parse_order(value)
    return first + [s for s in DEFAULT_ORDER if s not in first]
