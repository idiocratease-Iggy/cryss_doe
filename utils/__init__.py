import unicodedata


def normalize(name: str) -> str:
    """
    Canonical solvent/component name normalisation:
    - Unicode NFC
    - Strip whitespace
    - Replace non-breaking spaces
    """
    if not isinstance(name, str):
        return name

    s = unicodedata.normalize("NFC", name)
    s = s.replace("\u00A0", " ")
    s = s.strip()
    return s
