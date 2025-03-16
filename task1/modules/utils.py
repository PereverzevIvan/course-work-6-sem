import json
import re
from typing import Any, Dict, List
from collections import Counter
from modules.lang_utils import stop_words_en, stop_words_ru, is_valid_word

# В этом файле хранятся функции, которые могут быть переиспользованы в других модулях


def clean_text(text: str):
    """Очищает текст: приводит к нижнему регистру, убирает знаки препинания (кроме дефиса)."""

    text = text.lower()
    # Убираем знаки препинания, кроме дефиса
    text = re.sub(r"[^\w\s-]", "", text)

    return text


def clean_words(words: List[str]):
    """Удаляет все стоп-слова."""
    filter_func = lambda word: all(
        [
            word not in stop_words_en,
            word not in stop_words_ru,
            # is_valid_word(word),  # проверка правильности слова (читай описание)
        ]
    )

    return list(filter(filter_func, words))


def tokenize(text: str):
    """Разбивает текст на слова."""
    return text.split()


def count_word_frequencies(words: List[str]):
    """Считает частоту слов в списке."""
    return Counter(words)


def save_data_to_json(data: Dict[Any, Any], output_path: str):
    """Сохраняет данные в JSON-файл."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def read_text_file(file_path: str):
    """Читает текстовый файл и возвращает его содержимое."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
