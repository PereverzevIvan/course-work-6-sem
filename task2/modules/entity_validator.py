"""Модуль для валидации именованных сущностей"""
import re
from typing import Optional

# Известные организации и их части
KNOWN_ORGS = {
    'мгту', 'бауман', 'следственный комитет', 'университет',
    'академия', 'институт', 'department', 'university'
}

# Известные локации
KNOWN_LOCATIONS = {
    'москва', 'россия', 'russian federation', 'российская федерация',
    'moscow', 'russia'
}

# Маркеры, которые указывают на невалидные сущности
INVALID_MARKERS = {
    'http', 'www', '@', '.ru', '.com', '.org', '.net',
    'рис', 'fig', 'таб', 'tab', 'стр', 'page'
}

def normalize_text(text: str) -> str:
    """Нормализует текст для проверок"""
    return text.lower().strip()

def is_valid_entity(ent_text: str) -> bool:
    """Базовая проверка валидности именованной сущности"""
    text = normalize_text(ent_text)
    
    # Проверка длины
    if len(text) < 2:
        return False
    
    # Проверка на цифры и спецсимволы в начале или конце
    if re.match(r'^[\d\W]|[\d\W]$', text):
        return False
    
    # Проверка на невалидные маркеры
    if any(marker in text for marker in INVALID_MARKERS):
        return False
    
    # Проверка на одиночные буквы и сокращения
    words = text.split()
    if any(len(word) < 2 for word in words):
        return False
    
    return True

def validate_entity(ent_text: str, ent_type: str) -> bool:
    """Проверяет сущность на валидность с учетом её типа"""
    if not is_valid_entity(ent_text):
        return False
        
    text = normalize_text(ent_text)
    
    if ent_type == "Топонимы":
        # Проверяем через известные локации
        return any(loc in text for loc in KNOWN_LOCATIONS)
        
    elif ent_type == "Прочее":
        # Проверяем через известные организации
        return any(org in text for org in KNOWN_ORGS)
        
    elif ent_type == "Персоналии":
        # Для персоналий проверяем наличие хотя бы двух слов 
        # или одного слова с заглавной буквы длиннее 5 символов
        words = ent_text.split()
        if len(words) >= 2:
            return True
        return len(ent_text) > 5 and ent_text[0].isupper()
    
    return False 