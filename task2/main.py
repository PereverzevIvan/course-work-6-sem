from nltk import pprint
from modules.ngrams import get_top_ngrams
from modules.abbreviations import extract_multilang_abbreviations
from modules import utils
from modules.named_entities import create_named_index
from modules.terms_from_slovnik import extract_top_n_percent_terms
import os


def process_text(path: str):
    filename = os.path.basename(path).split(".")[0]

    print(f"Processing {filename}")

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

        ngrams = get_top_ngrams(text, 1, 35)
        ngrams = ngrams + get_top_ngrams(text, 2, 35)
        ngrams = ngrams + get_top_ngrams(text, 3, 35)

        utils.write_lines_to_file(list(set(ngrams)), f"./results/ngrams/{filename}.txt")

        abbrs = extract_multilang_abbreviations(text)
        utils.write_lines_to_file(
            list(abbrs), f"./results/abbreviations/{filename}.txt"
        )

        name_index = create_named_index(text)
        utils.save_named_index_to_csv_by_column(
            name_index, f"./results/named_entities/{filename}.csv"
        )

        terms = extract_top_n_percent_terms(
            f"./assets/slovniks/{filename}.json", f"./results/ngrams/{filename}.txt", 30
        )

        utils.write_lines_to_file(terms, f"./results/top_terms/{filename}.txt")

    print("Done")


texts_path = "../texts/txt/"
for i in range(1, 5):
    process_text(f"{texts_path}{i}.txt")
