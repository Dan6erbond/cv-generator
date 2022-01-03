strings = {
    "education": {
        "en": "Education",
        "de": "Ausbildung",
    },
    "profile": {
        "en": "Profile",
        "de": "Profil",
    },
    "contact": {
        "en": "Contact",
        "de": "Kontakt",
    },
    "languages": {
        "en": "Languages",
        "de": "Sprachen",
    },
    "experience": {
        "en": "Experience",
        "de": "Erfahrung",
    },
    "watermark": {
        "en": "This CV was generated using CV-Generator by RaviAnand Mohabir.",
        "de": "Dieses CV wurde mit CV-Generator von RaviAnand Mohabir generiert.",
    },
}


def resolve_string(value: dict | str, lang: str, default_lang: str = "en") -> str:
    if isinstance(value, dict):
        return value.get(lang, value.get(default_lang, ""))
    else:
        return value
