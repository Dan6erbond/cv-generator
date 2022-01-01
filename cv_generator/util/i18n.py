def resolve_string(value: dict | str, lang: str) -> str:
    if isinstance(value, dict):
        return value[lang]
    else:
        return value
