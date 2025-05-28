"""Модуль для конвертации PDF в TXT с учетом колонок"""
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTTextBox, LAParams
import re
from typing import List, Tuple
from modules.lang_tools import is_valid_word, detect_language
import os

class PDFConverter:
    def __init__(self):
        self.valid_single_chars = {'а', 'и', 'в', 'к', 'о', 'с', 'у', 'я'}
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Извлекает текст из PDF с учетом колонок.
        """
        text_blocks = []
        
        # Настраиваем параметры для учета колонок
        laparams = LAParams(
            line_margin=0.5,
            word_margin=0.1,
            boxes_flow=0.5,
            detect_vertical=True,
            all_texts=True
        )
        
        # Извлекаем страницы и текстовые блоки
        for page_layout in extract_pages(pdf_path, laparams=laparams):
            page_blocks = self._process_page(page_layout)
            text_blocks.extend(page_blocks)
        
        # Объединяем и чистим текст
        full_text = self._join_blocks(text_blocks)
        clean_text = self._clean_text(full_text)
        
        return clean_text
        
    def _process_page(self, page_layout) -> List[str]:
        """Обрабатывает одну страницу PDF"""
        page_blocks = []
        
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                x0, y0, x1, y1 = element.bbox
                text = element.get_text().strip()
                if text:
                    # Инвертируем y для правильной сортировки сверху вниз
                    page_blocks.append((x0, -y0, text))
        
        # Сортируем блоки сначала по строкам (y), потом по колонкам (x)
        page_blocks.sort(key=lambda b: (int(b[1]/10), b[0]))
        
        return [block[2] for block in page_blocks]
        
    def _join_blocks(self, blocks: List[str]) -> str:
        """Объединяет текстовые блоки в единый текст"""
        text = '\n'.join(blocks)
        # Удаляем множественные пробелы и переносы строк
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n', text)
        return text.strip()
        
    def _clean_text(self, text: str) -> str:
        """Очищает текст от артефактов и восстанавливает разорванные слова"""
        # Заменяем переносы слов
        text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)
        
        words = text.split()
        cleaned_words = []
        i = 0
        
        while i < len(words):
            word = words[i]
            
            # Пропускаем одиночные символы, кроме валидных
            if len(word) == 1 and word.lower() not in self.valid_single_chars:
                i += 1
                continue
            
            # Пытаемся объединить короткие части слов
            if i < len(words) - 1:
                next_word = words[i + 1]
                if len(word) <= 3 and len(next_word) <= 3:
                    combined = word + next_word
                    # Проверяем валидность объединенного слова
                    if is_valid_word(combined):
                        cleaned_words.append(combined)
                        i += 2
                        continue
            
            cleaned_words.append(word)
            i += 1
        
        return ' '.join(cleaned_words)
        
    def convert_pdf_to_txt(self, pdf_path: str, output_dir: str) -> str:
        """
        Конвертирует PDF в TXT с сохранением результата.
        
        Args:
            pdf_path: Путь к PDF файлу
            output_dir: Директория для сохранения результата
            
        Returns:
            Путь к созданному TXT файлу
        """
        # Создаем директорию, если её нет
        os.makedirs(output_dir, exist_ok=True)
        
        # Извлекаем текст
        text = self.extract_text_from_pdf(pdf_path)
        
        # Формируем путь для выходного файла
        filename = os.path.splitext(os.path.basename(pdf_path))[0]
        output_path = os.path.join(output_dir, f"{filename}.txt")
        
        # Сохраняем результат
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
            
        return output_path 