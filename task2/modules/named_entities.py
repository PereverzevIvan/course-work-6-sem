from collections import defaultdict
from modules.lang_tools import nlp_en, nlp_ru, detect_language
from modules.entity_validator import validate_entity
from typing import Dict, Set, List
import re

def split_into_sentences(text: str) -> List[str]:
    """Разбивает текст на предложения"""
    # Используем простой подход с учетом основных разделителей
    sentences = re.split(r'[.!?]+', text)
    return [s.strip() for s in sentences if s.strip()]

def create_named_index(text: str) -> Dict[str, List[str]]:
    """
    Создает именной указатель из текста.
    
    Returns:
        Словарь с категориями сущностей:
        - Персоналии
        - Топонимы
        - Прочее (организации, продукты, события и т.д.)
    """
    result = defaultdict(set)
    sentences = split_into_sentences(text)

    for sentence in sentences:
        if not sentence:
            continue
            
        # Определяем язык предложения
        lang = detect_language(sentence)
        if not lang:
            continue
            
        # Выбираем модель в зависимости от языка
        nlp = nlp_ru if lang == 'ru' else nlp_en
        doc = nlp(sentence)
        
        for ent in doc.ents:
            label = ent.label_
            entity_text = ent.text.strip()

            # Определяем категорию сущности
            if label in {"PER", "PERSON"}:
                category = "Персоналии"
            elif label in {"LOC", "GPE"}:
                category = "Топонимы"
            elif label in {"ORG", "PRODUCT", "EVENT", "WORK_OF_ART", "LAW"}:
                category = "Прочее"
            else:
                continue
                
            # Проверяем валидность сущности
            if validate_entity(entity_text, category):
                result[category].add(entity_text)

    # Преобразуем множества в отсортированные списки
    return {k: sorted(v) for k, v in result.items()}
