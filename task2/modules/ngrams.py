from collections import Counter
from nltk import word_tokenize, ngrams, download as nltk_download
from modules.lang_tools import *

nltk_download("punkt_tab")
nltk_download("stopwords")


def is_meaningful_token(token: str) -> bool:
    """Проверка, что токен — это слово без стоп-слов и валидно написан"""
    token = token.strip()
    if not token.isalpha():
        return False
    if not is_valid_word(token):
        return False
    lang = detect_language(token)

    if lang == "en" and token.lower() in spacy_stop_words_en:
        return False
    if lang == "ru" and token.lower() in spacy_stop_words_ru:
        return False
    return True


def normalize_token(token: str) -> str:
    """Лемматизация одного токена с определением языка"""
    lang = detect_language(token)
    if lang is None:
        lang = "en"

    # Решил пока не лемматизировать, так как в задании не сказано
    # return lemmatize_word(token, lang).lower()
    return token.lower()


def extract_lemmas(text: str) -> list[str]:
    """Токенизация + очистка + лемматизация"""
    tokens = word_tokenize(text)
    lemmas = [normalize_token(t) for t in tokens if is_meaningful_token(t)]
    return lemmas


def extract_ngrams(text: str, n: int) -> list[str]:
    """Извлекает n-граммы из лемматизированного текста"""
    lemmas = extract_lemmas(text)
    return [" ".join(gram) for gram in ngrams(lemmas, n)]


def get_top_ngrams(text: str, n: int = 2, top_k: int = 100) -> list[str]:
    """Счётчик наиболее частых n-грамм"""
    grams = extract_ngrams(text, n)
    counter = Counter(grams)
    return [gram for gram, _ in counter.most_common(top_k)]
