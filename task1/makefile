run: clean base lemmas

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

test:
	@python ./test.py

clean:
	@rm -rf ./results

PHONY: run clean
