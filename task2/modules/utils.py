from modules.lang_tools import spacy_stop_words_ru, spacy_stop_words_en
import re
import csv
from itertools import zip_longest


def clean_text(text: str):
    """Очищает текст: убирает знаки препинания (кроме дефиса)."""

    # Убираем знаки препинания, кроме дефиса
    text = re.sub(r"[^\w\s-]", "", text)

    return text


def write_lines_to_file(lines: list[str], filename: str) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")


def save_named_index_to_csv_by_column(
    index: dict[str, list[str]], filename: str
) -> None:
    # Сортируем ключи, чтобы порядок был стабильным
    types = sorted(index.keys())

    # Собираем строки, выравнивая по самой длинной колонке
    rows = zip_longest(*(index[t] for t in types), fillvalue="")

    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(types)  # Заголовки колонок

        for row in rows:
            writer.writerow(row)
