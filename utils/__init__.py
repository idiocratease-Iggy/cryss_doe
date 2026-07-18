import unicodedata


def normalize(name: str) -> str:
    """
    Canonical solvent/component name normalisation:
    - Unicode NFC
    - Strip whitespace
    - Replace non-breaking spaces

    Normalizes solvent/component names to avoid Excel Unicode inconsistencies
    (NBSP, combining accents, stray whitespace). Ensures consistent matching across
    descriptor matrices, picker lists, and PCA.”
    """
    if not isinstance(name, str):
        return name

    s = unicodedata.normalize("NFC", name)
    s = s.replace("\u00A0", " ")
    s = s.strip()
    return s
