from collections import Counter
from nltk import word_tokenize, ngrams, download as nltk_download
from modules.lang_tools import *
from modules.wordnet_validator import WordNetValidator
from modules.custom_stopwords import CUSTOM_STOPWORDS

nltk_download("punkt_tab")
nltk_download("stopwords")

_wordnet_validator = WordNetValidator()


def is_meaningful_token(token: str) -> bool:
    """Проверка, что токен — это слово без стоп-слов и валидно написан"""
    token = token.strip().lower()
    if not token.isalpha():
        return False
    if not is_valid_word(token):
        return False
    if token in CUSTOM_STOPWORDS:  # Проверка на пользовательские стоп-слова
        return False
        
    lang = detect_language(token)
    if lang == "en" and token in spacy_stop_words_en:
        return False
    if lang == "ru" and token in spacy_stop_words_ru:
        return False
    return True


def is_meaningful_ngram(ngram: str) -> bool:
    """Проверка, что n-грамма не содержит стоп-слов"""
    words = ngram.split()
    return all(is_meaningful_token(word) for word in words)


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
    ngrams_list = [" ".join(gram) for gram in ngrams(lemmas, n)]
    # Фильтруем n-граммы, содержащие стоп-слова
    return [gram for gram in ngrams_list if is_meaningful_ngram(gram)]


def get_top_ngrams(text: str, n: int = 2, top_k: int = 100) -> list[str]:
    """Счётчик наиболее частых n-грамм с проверкой через RuWordNet"""
    grams = extract_ngrams(text, n)
    # Фильтруем n-граммы через WordNet
    valid_grams = _wordnet_validator.filter_valid_ngrams(grams)
    counter = Counter(valid_grams)
    return [gram for gram, _ in counter.most_common(top_k)]
