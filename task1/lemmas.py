from modules import slovnik, tables, graphics, lemmas
import os

txt_dir = "../texts/txt/"
result_dir = "./results"
lemmas_dir = result_dir + "/lemmas/"
slovniks_dir = result_dir + "/slovniks/lemmas/"
tables_dir = result_dir + "/tables/lemmas/"
common_graphics_dir = result_dir + "/graphics/lemmas/common"
normalize_graphics_dir = result_dir + "/graphics/lemmas/normalize/"


def process_files(folder_path):
    """Принимает на вход папку каталог, в котором хранятся файлы для обработки,
    создает для них словники лемм, таблицы с частотными характеристиками, графики изменения частоты.
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
        full_path = os.path.join(folder_path, txt_file)
        lemma_and_forms_file = os.path.join(
            lemmas_dir, txt_file.replace(".txt", ".json")
        )
        slovnik_file = os.path.join(slovniks_dir, txt_file.replace(".txt", ".json"))
        table_file = os.path.join(tables_dir, txt_file.replace(".txt", ".csv"))
        common_graphic_file = os.path.join(
            common_graphics_dir, txt_file.replace(".txt", ".png")
        )
        normalize_graphic_file = os.path.join(
            normalize_graphics_dir, txt_file.replace(".txt", ".png")
        )

        lemmas.save_lemmas_info(full_path, lemma_and_forms_file, slovnik_file)
        tables.compute_frequency_stats(slovnik_file, table_file)
        graphics.plot_frequency_distribution(table_file, common_graphic_file)
        graphics.plot_normalize_frequency_distribution(
            table_file, normalize_graphic_file
        )

    print("Обработка файлов завершена.")


process_files(txt_dir)
