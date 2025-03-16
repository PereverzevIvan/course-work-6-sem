from modules.lang_utils import detect_language
from modules import utils
from googletrans import Translator

# Инициализируем переводчик
translator = Translator()


def translate_word(word: str) -> list:
    """Переводит английское слово на русский (не более 3 вариантов)."""
    try:
        translation = translator.translate(word, src="en", dest="ru")
        translations = translation.text.split(", ")[:3]  # Ограничиваем до 3 переводов
        return translations
    except Exception as e:
        print(f"Ошибка перевода '{word}': {e}")
        return []


def generate_translation_dict(input_file: str, output_file: str):
    """Принимает на вход файл, считывает из него все слова и создаёт словарь переводов для английских слов."""
    translation_dict = {}

    text = utils.read_text_file(input_file)
    text = utils.clean_text(text)
    words = utils.tokenize(text)
    words = utils.clean_words(words)

    for word in words:
        if detect_language(word) == "en":
            translations = translate_word(word)
            if translations:
                translation_dict[word] = translations

    # Сохраняем словарь переводов в JSON
    utils.save_data_to_json(translation_dict, output_file)
