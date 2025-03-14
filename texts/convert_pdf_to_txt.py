import pdfplumber
import re
import os


def clean_text(text):
    """Очищает текст от переносов слов и лишних разрывов строк."""
    # Соединяем слова, разорванные дефисом на переносе строки (сло-\nво -> слово)
    text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)

    # Убираем лишние разрывы строк, заменяя их пробелами (но не между пунктами списка и заголовками)
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

    return text


def extract_text_from_pdf(pdf_path):
    full_text = []
    previous_page_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Проверяем, есть ли текст на странице
            current_page_text = page.extract_text()
            if not current_page_text:
                continue  # Пропускаем пустые страницы

            cleaned_text = clean_text(current_page_text)

            # Обрабатываем переносы слов между страницами
            if previous_page_text:
                match = re.search(r"(\w+)-$", previous_page_text)
                if match:
                    unfinished_word = match.group(1)
                    cleaned_text = re.sub(
                        rf"^{unfinished_word}(\w+)", rf"\1", cleaned_text
                    )

            full_text.append(cleaned_text)
            previous_page_text = current_page_text

    return "\n".join(full_text)


def save_text_to_file(text, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)


def process_pdfs(input_folder, output_folder):
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            txt_path = os.path.join(output_folder, filename.replace(".pdf", ".txt"))

            parsed_text = extract_text_from_pdf(pdf_path)
            save_text_to_file(parsed_text, txt_path)

            print(f"Обработанный текст {filename} сохранён в {txt_path}")


# Использование:
input_folder = "./pdf/"  # Укажи путь к папке с PDF-файлами
output_folder = "./txt/"  # Укажи путь к папке для сохранения текстовых файлов

# Создаём папку для вывода, если она не существует
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

process_pdfs(input_folder, output_folder)
