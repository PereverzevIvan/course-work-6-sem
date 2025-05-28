from nltk import pprint
from modules.ngrams import get_top_ngrams
from modules.abbreviations import extract_multilang_abbreviations
from modules import utils
from modules.named_entities import create_named_index
from modules.terms_from_slovnik import extract_top_n_percent_terms
from modules.context_finder import ContextFinder
import os
import json


def process_text(path: str):
    filename = os.path.basename(path).split(".")[0]

    print(f"Processing {filename}")

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

        ngrams = get_top_ngrams(text, 1, 200)
        ngrams = ngrams + get_top_ngrams(text, 2, 200)
        ngrams = ngrams + get_top_ngrams(text, 3, 200)

        utils.write_lines_to_file(list(set(ngrams)), f"./results/ngrams/{filename}.txt")

        # abbrs = extract_multilang_abbreviations(text)
        # utils.write_lines_to_file(
            # list(abbrs), f"./results/abbreviations/{filename}.txt"
        # )

        # name_index = create_named_index(text)
        # utils.save_named_index_to_csv_by_column(
            # name_index, f"./results/named_entities/{filename}.csv"
        # )

        # terms = extract_top_n_percent_terms(
            # f"./assets/slovniks/{filename}.json", f"./results/ngrams/{filename}.txt", 30
        # )

        # utils.write_lines_to_file(terms, f"./results/top_terms/{filename}.txt")

    print("Done")


def find_context_process(text_path: str, ngrams_file_path: str, window_size: int = 1) -> dict:
    """
    Ищет контексты для n-грамм из файла в указанном тексте.
    
    Args:
        text_path: Путь к текстовому файлу
        ngrams_file_path: Путь к файлу со списком n-грамм (одна n-грамма на строку)
        window_size: Размер окна контекста (количество предложений до и после)
        
    Returns:
        Словарь с результатами в формате:
        {
            "ngram1": [
                {
                    "sentence": "Предложение с n-граммой",
                    "context": ["Предложение до", "Предложение после"]
                },
                ...
            ],
            ...
        }
    """
    # Создаем папку для результатов, если её нет
    os.makedirs("./results/contexts", exist_ok=True)
    
    # Читаем n-граммы из файла
    with open(ngrams_file_path, "r", encoding="utf-8") as f:
        ngrams = [line.strip() for line in f if line.strip()]
    
    filename = os.path.basename(text_path).split(".")[0]
    finder = ContextFinder()
    
    with open(text_path, "r", encoding="utf-8") as f:
        text = f.read()
        
        # Получаем контексты
        raw_contexts = finder.find_multiple_ngrams_contexts(text, ngrams, window_size)
        
        # Преобразуем результаты в более удобный формат для JSON
        results = {}
        for ngram, contexts in raw_contexts.items():
            results[ngram] = [
                {
                    "sentence": sentence,
                    "context": context
                }
                for sentence, context in contexts
            ]
        
        # Сохраняем результаты в JSON
        output_path = f"./results/contexts/{filename}_contexts.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
            
        # Сохраняем результаты в CSV
        csv_output_path = f"./results/contexts/{filename}_contexts.csv"
        utils.save_contexts_to_csv(results, csv_output_path)
            
        return results


texts_path = "../texts/txt/"
for i in range(1, 2):
    process_text(f"{texts_path}{i}.txt")
    
    contexts = find_context_process(
        text_path=f"{texts_path}{i}.txt",
        ngrams_file_path=f"./results/ngrams/{i}.txt",
        window_size=1
    )


    
