from typing import Dict, List
from modules import utils
from modules.lang_utils import detect_language, lemmatize_word


def save_lemmas_info(input_file: str, lemma_and_forms_file: str, slovnik_file: str):
    lemmas: List[str] = []  # Все леммы для  формирования частотного словника
    lemma_dict: Dict[str, List[str]] = {}  # Для хранения лемм и их словоформ

    text = utils.read_text_file(input_file)
    text = utils.clean_text(text)
    words = utils.tokenize(text)
    words = utils.clean_words(words)

    for word in words:
        lang = detect_language(word)
        if not lang:
            continue

        lemma = lemmatize_word(word, lang)
        lemmas.append(lemma)

        if lemma not in lemma_dict:
            lemma_dict[lemma] = []

        if word not in lemma_dict[lemma]:
            lemma_dict[lemma].append(word)

    counted_lemmas = utils.count_word_frequencies(lemmas)

    utils.save_data_to_json(counted_lemmas, slovnik_file)
    utils.save_data_to_json(lemma_dict, lemma_and_forms_file)

    print(f"Словарь лемм и словоформ {input_file} успешно создан!")
