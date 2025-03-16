from modules import utils


def generate_reverse_dict(input_file: str, output_file: str):
    """Создаёт обратный словарь из текста."""
    text = utils.read_text_file(input_file)
    text = utils.clean_text(text)
    words = utils.tokenize(text)
    words = utils.clean_words(words)

    words = list(set(words))  # удаляем дубликаты

    # Сортируем по последним буквам
    reversed_words = sorted(words, key=lambda word: word[::-1])

    # Записываем результат
    with open(output_file, "w", encoding="utf-8") as file:
        for word in reversed_words:
            file.write(word + "\n")

    print(f"Обратный словарь сохранён в {output_file}")
