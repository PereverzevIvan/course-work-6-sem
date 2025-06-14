import pymorphy3
import spacy
import enchant
import langid

# Инициализируем морфологический анализатор для русского языка
morph = pymorphy3.MorphAnalyzer()

# Загружаем модели для spacy
nlp_en = spacy.load("en_core_web_sm")
nlp_ru = spacy.load("ru_core_news_lg")

# Стоп-слова для отсеивания
spacy_stop_words_en = nlp_en.Defaults.stop_words
spacy_stop_words_ru = nlp_ru.Defaults.stop_words

# Словари для проверки правильности написания слов
en_dict = enchant.Dict("en_US")  # Английский словарь
ru_dict = enchant.Dict("ru_RU")  # Русский словарь


def is_valid_word(word: str) -> bool:
    """
    Проверяет, является ли слово валидным.
    """
    # Проверяем длину
    if len(word) < 2:
        return False
        
    # Проверяем, что слово содержит хотя бы одну букву
    if not any(c.isalpha() for c in word):
        return False
        
    # Проверяем на спецсимволы в начале или конце
    if not (word[0].isalnum() and word[-1].isalnum()):
        return False
        
    return True


def detect_language(word: str) -> str | None:
    """Определяет язык слова ('ru' для русского, 'en' для английского)."""
    if ru_dict.check(word):
        return "ru"
    elif en_dict.check(word):
        return "en"
    return langid.classify(word)[0]


def lemmatize_word(word: str, lang: str) -> str:
    """
    Лемматизирует слово в зависимости от его языка.
    Если слово русское, то используется pymorphy3.
    Если слово английское, то используется spaCy.
    """
    if lang == "ru":
        return morph.parse(word)[0].normal_form  # Лемматизация русского слова
    elif lang == "en":
        doc = nlp_en(word)
        return doc[0].lemma_  # Лемматизация английского слова через spaCy
    return word  # Если язык неизвестен, оставляем слово как есть
