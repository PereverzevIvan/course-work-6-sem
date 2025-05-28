from modules.lang_tools import spacy_stop_words_ru, spacy_stop_words_en
import re
import csv
from itertools import zip_longest
from typing import Dict, List, Any


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


def save_contexts_to_csv(contexts: Dict[str, List[Dict[str, Any]]], output_path: str) -> None:
    """
    Сохраняет контексты n-грамм в CSV файл.
    
    Args:
        contexts: Словарь с контекстами в формате:
            {
                "ngram1": [
                    {
                        "sentence": "Предложение с n-граммой",
                        "context": ["Предложение до", "Предложение после"]
                    },
                    ...
                ],
                ...
            }
        output_path: Путь к выходному CSV файлу
        
    CSV формат:
    N-грамма | Предложение | Контекст до | Контекст после
    """
    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        # Записываем заголовки
        writer.writerow(["N-грамма", "Предложение", "Контекст до", "Контекст после"])
        
        # Для каждой n-граммы
        for ngram, occurrences in contexts.items():
            # Для каждого вхождения n-граммы
            for occurrence in occurrences:
                sentence = occurrence["sentence"]
                context = occurrence["context"]
                
                # Разделяем контекст на "до" и "после"
                context_before = " ".join(context[:len(context)//2])
                context_after = " ".join(context[len(context)//2:])
                
                # Записываем строку
                writer.writerow([
                    ngram,
                    sentence,
                    context_before,
                    context_after
                ])
