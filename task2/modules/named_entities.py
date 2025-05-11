from collections import defaultdict
from modules.lang_tools import nlp_en, nlp_ru


def create_named_index(text: str) -> dict[str, list[str]]:
    result = defaultdict(set)

    # Обрабатываем обеими моделями
    docs = [nlp_ru(text), nlp_en(text)]

    for doc in docs:
        for ent in doc.ents:
            label = ent.label_

            if label in {"PER", "PERSON"}:
                result["Персоналии"].add(ent.text)
            elif label in {"LOC", "GPE"}:
                result["Топонимы"].add(ent.text)
            elif label in {"ORG", "PRODUCT", "EVENT", "WORK_OF_ART", "LAW"}:
                result["Прочее"].add(ent.text)

    # Преобразуем множества в отсортированные списки
    return {k: sorted(v) for k, v in result.items()}
