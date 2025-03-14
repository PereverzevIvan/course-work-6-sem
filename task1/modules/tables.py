import json
import math
import pandas as pd

# Переменная для хранения названий колонок в csv-файле
columns = [
    "Ранг",
    "Слово",
    "Абсолютная частота",
    "Относительная частота",
    "Нормализованный ранг",
    "Нормализированная частота",
]


def compute_frequency_stats(json_file: str, output_csv: str):
    """Вычисляет частотные характеристики слов из JSON-файла и сохраняет результат в CSV."""

    # Загружаем частотный словарь из JSON
    with open(json_file, "r", encoding="utf-8") as f:
        word_freq = json.load(f)

    # Сортируем слова по убыванию частоты
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

    # Вычисляем общее количество слов в тексте
    total_words = sum(word_freq.values())

    # Формируем таблицу с частотными характеристиками
    data = []
    for rank, (word, freq_abs) in enumerate(sorted_words, start=1):
        freq_rel = freq_abs / total_words  # Относительная частота
        norm_rank = math.log(rank)  # Нормализованный ранг
        norm_freq_rel = math.log(freq_rel)  # Нормализированная относительная частота

        data.append([rank, word, freq_abs, freq_rel, norm_rank, norm_freq_rel])

    # Создаём DataFrame
    df = pd.DataFrame(
        data,
        columns=columns,
    )

    # Сохраняем в CSV
    df.to_csv(output_csv, index=False, encoding="utf-8")

    print(f"Файл {output_csv} успешно создан!")
