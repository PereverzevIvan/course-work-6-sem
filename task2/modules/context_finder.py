"""Модуль для поиска контекста n-грамм в тексте"""
import re
from typing import List, Dict, Tuple
from nltk.tokenize import sent_tokenize
from nltk import download as nltk_download

nltk_download('punkt')

class ContextFinder:
    def __init__(self):
        # Кэш для уже разбитых на предложения текстов
        self._sentences_cache: Dict[str, List[str]] = {}
        
    def _get_sentences(self, text: str) -> List[str]:
        """Разбивает текст на предложения с кэшированием"""
        if text not in self._sentences_cache:
            self._sentences_cache[text] = sent_tokenize(text)
        return self._sentences_cache[text]
    
    def find_ngram_contexts(self, text: str, ngram: str, window_size: int = 1) -> List[Tuple[str, List[str]]]:
        """
        Находит все вхождения n-граммы в тексте и возвращает контекст.
        
        Args:
            text: Исходный текст
            ngram: Искомая n-грамма
            window_size: Количество предложений до и после для контекста
            
        Returns:
            Список кортежей (предложение с n-граммой, контекстные предложения)
        """
        sentences = self._get_sentences(text)
        results = []
        
        # Создаем паттерн для поиска, учитывая возможные вариации регистра
        pattern = r'\b' + re.escape(ngram.lower()) + r'\b'
        
        for i, sentence in enumerate(sentences):
            if re.search(pattern, sentence.lower()):
                # Определяем границы контекстного окна
                start = max(0, i - window_size)
                end = min(len(sentences), i + window_size + 1)
                
                # Собираем контекстные предложения (исключая текущее)
                context = sentences[start:i] + sentences[i+1:end]
                
                results.append((sentence, context))
                
        return results
    
    def find_multiple_ngrams_contexts(self, text: str, ngrams: List[str], window_size: int = 1) -> Dict[str, List[Tuple[str, List[str]]]]:
        """
        Находит контексты для списка n-грамм.
        
        Args:
            text: Исходный текст
            ngrams: Список n-грамм для поиска
            window_size: Количество предложений до и после для контекста
            
        Returns:
            Словарь {n-грамма: [(предложение, контекст), ...]}
        """
        results = {}
        for ngram in ngrams:
            contexts = self.find_ngram_contexts(text, ngram, window_size)
            if contexts:  # Добавляем только если нашли хотя бы одно вхождение
                results[ngram] = contexts
        return results 