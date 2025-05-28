import json
import csv

# Открываем JSON
with open("../results/translate/4.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Пишем CSV
with open("./output_4.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["key", "value"])
    for key, values in data.items():
        for value in values:  # если в списке больше одного значения
            writer.writerow([key, value])
