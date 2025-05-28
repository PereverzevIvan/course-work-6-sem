from ruwordnet import RuWordNet
from typing import List, Set

class WordNetValidator:
    def __init__(self):
        self.wn = RuWordNet()
        self._valid_terms_cache: Set[str] = set()
    
    def is_valid_term(self, term: str) -> bool:
        """Проверяет, является ли термин или словосочетание значащим через RuWordNet"""
        if term in self._valid_terms_cache:
            return True
            
        # Проверяем, есть ли точное совпадение в RuWordNet
        senses = self.wn.get_senses(term.upper())
        if senses:
            self._valid_terms_cache.add(term)
            return True
            
        # Для многословных терминов проверяем каждое слово
        words = term.split()
        if len(words) > 1:
            # Проверяем каждое слово
            valid_words = 0
            for word in words:
                if self.wn.get_senses(word.upper()):
                    valid_words += 1
            
            # Если большинство слов найдено в WordNet, считаем термин валидным
            if valid_words >= len(words) / 2:
                self._valid_terms_cache.add(term)
                return True
        
        return False

    def filter_valid_ngrams(self, ngrams: List[str]) -> List[str]:
        """Фильтрует список n-грамм, оставляя только значащие термины"""
        return [ngram for ngram in ngrams if self.is_valid_term(ngram)] 