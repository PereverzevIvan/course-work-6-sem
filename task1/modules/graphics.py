import pandas as pd
import matplotlib.pyplot as plt


def plot_frequency_distribution(input_file, output_file):
    """Создает график изменения частот в соответствии с рангами и сохраняет его в файловой системе"""
    # Загрузка данных из CSV файла
    df = pd.read_csv(input_file)

    # Построение ступенчатой функции распределения частот
    plt.figure(figsize=(10, 6))
    plt.step(
        df["Абсолютная частота"],
        df["Ранг"],
        where="post",
        label="Ступенчатая функция распределения",
    )

    plt.xlabel("Абсолютная частота")
    plt.ylabel("Ранг слова")
    plt.title(
        f"Ступенчатая функция распределения частот для данных из файла {input_file}"
    )

    plt.grid()
    plt.legend()

    # Сохранение графика
    plt.savefig(output_file)
    plt.close()  # Закрываем график для освобождения памяти
    print(f"График сохранен в: {output_file}")


def plot_normalize_frequency_distribution(input_file, output_file):
    """Создает график изменения нормализованных частот в соответствии с нормализованными рангами и сохраняет его в файловой системе"""
    # Загрузка данных из CSV файла
    df = pd.read_csv(input_file)

    # Построение графика распределения частот
    plt.figure(figsize=(10, 6))
    plt.plot(
        df["Нормализованный ранг"],
        df["Нормализированная частота"],
        label="Нормализованная частота",
    )
    plt.xlabel("Нормализованный ранг слова")
    plt.ylabel("Нормализованная относительная частота слова")
    plt.title(f"Нормализированное распределение частот слов для файла {input_file}")

    plt.grid()
    plt.legend()

    # Сохранение графика
    plt.savefig(output_file)
    plt.close()  # Закрываем график для освобождения памяти
    print(f"Нормализованный График сохранен в: {output_file}")
