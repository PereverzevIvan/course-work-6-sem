from modules import slovnik, tables, graphics
import os

txt_dir = "../texts/txt/"
result_dir = "./results"
slovniks_dir = result_dir + "/slovniks/"
tables_dir = result_dir + "/tables/"
common_graphics_dir = result_dir + "/graphics/common"
normalize_graphics_dir = result_dir + "/graphics/normalize/"


def process_files(folder_path):
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
        slovnik_file = os.path.join(slovniks_dir, txt_file.replace(".txt", ".json"))
        table_file = os.path.join(tables_dir, txt_file.replace(".txt", ".csv"))
        common_graphic_file = os.path.join(
            common_graphics_dir, txt_file.replace(".txt", ".png")
        )
        normalize_graphic_file = os.path.join(
            normalize_graphics_dir, txt_file.replace(".txt", ".png")
        )

        slovnik.create_slovnik(full_path, slovnik_file)
        tables.compute_frequency_stats(slovnik_file, table_file)
        graphics.plot_frequency_distribution(table_file, common_graphic_file)
        graphics.plot_normalize_frequency_distribution(
            table_file, normalize_graphic_file
        )

    print("Обработка файлов завершена.")


if __name__ == "__main__":
    process_files(txt_dir)
