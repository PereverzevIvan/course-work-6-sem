from modules import utils


def create_slovnik(src: str, dest: str):
    """Принимает на вход файл, считывает в нем все слова, и создает словник,
    в котором перечислены слова и частоты их встречи в тексте
    """
    text = utils.read_text_file(src)
    text = utils.clean_text(text)
    words = utils.tokenize(text)
    words = utils.clean_words(words)

    words_frequencies = utils.count_word_frequencies(words)
    utils.save_data_to_json(words_frequencies, dest)
