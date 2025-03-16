# Осторожно: из-за операции translate может работать очень долго
run: base lemmas translate poetry

# Запуск кода для выполнения основного задания, а также создание каталогов для хранения результатов
base:
	@mkdir -p \
		./results/slovniks/base \
		./results/graphics/base/normalize \
		./results/graphics/base/common \
		./results/tables/base \

	@python ./base.py

# Запуск кода для выполнения первого дополнительного задания, а также создание каталогов для хранения результатов
lemmas:
	@mkdir -p \
		./results/lemmas \
		./results/slovniks/lemmas \
		./results/graphics/lemmas/normalize \
		./results/graphics/lemmas/common \
		./results/tables/lemmas

	@python ./lemmas.py

# Запуск кода для выполнения второго дополнительного задания, а также создание каталогов для хранения результатов
# Осторожно: из-за запросов к внешнему api может работать очень медленно
translate:
	@mkdir -p \
		./results/translate

	@python ./translate.py

# Запуск кода для выполнения третьего дополнительного задания, а также создание каталогов для хранения результатов
poetry:
	@mkdir -p \
		./results/poetry

	@python ./poetry.py

# Для тестирования новых функций, чтобы не запускать сразу все модули
test:
	@python ./test.py

# Очистка удаление всех созданных ранее результатов
clean:
	@rm -rf ./results

