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
    "language_codes": {
        "en": {
            "en": "English",
            "de": "Englisch",
        },
        "de": {
            "en": "German",
            "de": "Deutsch",
        },
    },
    "language_level": {
        "native/bilingual": {
            "en": "Native/Bilingual",
            "de": "Muttersprache/Zweisprachig",
        },
    },
    "projects": {
        "en": "Projects",
        "de": "Projekte",
    },
}


def resolve_string(value: dict | str, lang: str, default_lang: str = "en") -> str:
    if isinstance(value, dict):
        return value.get(
            lang,
            value.get(
                default_lang,
                value[list(value.keys())[0]] if value else "",
            ),
        )
    else:
        return value
