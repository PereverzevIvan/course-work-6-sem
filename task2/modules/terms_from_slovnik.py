import json
from typing import List


def extract_top_n_percent_terms(
    json_path: str, ngram_path: str, percent: int = 20
) -> List[str]:
    # 1. Загрузить словарь
    with open(json_path, "r", encoding="utf-8") as f:
        freq_dict = json.load(f)

    # 2. Загрузить n-граммы
    with open(ngram_path, "r", encoding="utf-8") as f:
        ngrams = [line.strip().lower() for line in f if line.strip()]

    # 3. Найти слова, которые встречаются хотя бы в одной n-грамме (как подстрока)
    matched_words = {}
    for word, freq in freq_dict.items():
        word_lower = word.lower()
        if any(word_lower in ngram for ngram in ngrams):
            matched_words[word] = freq

    # 4. Отсортировать по частоте и взять верхние 20%
    sorted_words = sorted(matched_words.items(), key=lambda x: x[1], reverse=True)
    top_n_percent_count = max(1, len(sorted_words) * percent // 100)
    top_terms = [word for word, _ in sorted_words[:top_n_percent_count]]

    return top_terms
