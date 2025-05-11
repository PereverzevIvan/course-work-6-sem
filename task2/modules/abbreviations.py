import re
from modules.lang_tools import ru_dict, en_dict


def extract_multilang_abbreviations(text: str) -> set[str]:
    """
    Ищет аббревиатуры в тексте на русском и английском языке.
    Учитывает слова в скобках и все заглавные слова 2–10 букв.
    """
    potential_abbrs = set()

    # 1. Аббревиатуры: последовательности заглавных букв (латиница и кириллица)
    pattern = r"\b[А-ЯA-Z]{2,10}\b"
    matches = re.findall(pattern, text)
    potential_abbrs.update(matches)

    # 2. Аббревиатуры в скобках
    bracket_matches = re.findall(r"\(([А-ЯA-Z]{2,10})\)", text)
    potential_abbrs.update(bracket_matches)

    # 3. Фильтрация: не обычные слова
    filtered = set()
    for abbr in potential_abbrs:
        lower = abbr.lower()
        if not (ru_dict.check(lower) or en_dict.check(lower)):
            filtered.add(abbr)

    return filtered
