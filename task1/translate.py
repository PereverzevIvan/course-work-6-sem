import os
from modules.translate import generate_translation_dict

txt_dir = "../texts/txt/"
result_dir = "./results"
translate_dir = result_dir + "/translate/"


def process_files(folder_path):
    """Принимает на вход папку каталог, в котором хранятся файлы для обработки,
    считывает из них все слова и создает словари с переводом английских слов.
    """

    # Проверка, существует ли папка
    if not os.path.exists(folder_path):
        print(f"Папка '{folder_path}' не найдена.")
        return

    # Получение списка всех файлов в папке
    txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

    # Проверка наличия файлов формата .txt
    if not txt_files:
        print("В папке нет файлов формата .txt.")
        return

    # Обработка каждого файла
    for txt_file in txt_files:
        # Получение полного пути к файлу
        full_path = os.path.join(folder_path, txt_file)
        translate_file = os.path.join(translate_dir, txt_file.replace(".txt", ".json"))
        generate_translation_dict(full_path, translate_file)

    print("Перевод файлов завершен.")


confirm = input(
    "Осторожно: данный скрипт обращается к внешнему API, из-за чего может работать очень долго.\n"
    "Если действительно хотите заново перевести все файлы, то напишите слово 'yes': "
)
if confirm == "yes":
    process_files(txt_dir)
else:
    print("Перевод слов в текстах отменен")
