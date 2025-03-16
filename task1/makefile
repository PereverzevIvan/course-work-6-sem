# Осторожно: из-за операции translate может работать очень долго
run: base lemmas translate poetry

base:
	@mkdir -p \
		./results/slovniks/base \
		./results/graphics/base/normalize \
		./results/graphics/base/common \
		./results/tables/base \

	@python ./base.py

lemmas:
	@mkdir -p \
		./results/lemmas \
		./results/slovniks/lemmas \
		./results/graphics/lemmas/normalize \
		./results/graphics/lemmas/common \
		./results/tables/lemmas

	@python ./lemmas.py

# Осторожно: из-за запросов к внешнему api может работать очень медленно
translate:
	@mkdir -p \
		./results/translate

	@python ./translate.py

poetry:
	@mkdir -p \
		./results/poetry

	@python ./poetry.py

test:
	@python ./test.py

clean:
	@rm -rf ./results

PHONY: run clean
