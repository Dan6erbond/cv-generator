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
    }
}


def resolve_string(value: dict | str, lang: str) -> str:
    if isinstance(value, dict):
        return value[lang]
    else:
        return value
