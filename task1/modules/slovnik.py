import re
import json
from collections import Counter
from typing import List
from modules.stop_words import stop_words


def clean_text(text: str) -> str:
    """Очищает текст: приводит к нижнему регистру, убирает знаки препинания (кроме дефиса) и цифры."""

    text = text.lower()

    # Убираем знаки препинания, кроме дефиса
    text = re.sub(r"[^\w\s-]", "", text)

    return text


def clean_words(words: List[str]):
    filtered_words = list(filter(lambda word: word not in stop_words, words))
    return filtered_words


def tokenize(text: str):
    """Разбивает текст на слова."""
    return text.split()


def read_text_file(file_path: str):
    """Читает текстовый файл и возвращает его содержимое."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def save_json(data: Counter[str], output_path: str):
    """Сохраняет данные в JSON-файл."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def count_word_frequencies(words: List[str]):
    """Считает частоту слов в списке."""
    return Counter(words)


def create_slovnik(src: str, dest: str):
    text = read_text_file(src)
    text = clean_text(text)

    words = tokenize(text)
    words = clean_words(words)

    words_frequencies = count_word_frequencies(words)
    save_json(words_frequencies, dest)
