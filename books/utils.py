import json
import os
import uuid
from django.conf import settings
from django.core.exceptions import ValidationError

DATA_DIR = os.path.join(settings.MEDIA_ROOT, 'data_files')

def ensure_dir_exists():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def save_book_to_json(data):
    ensure_dir_exists()
    filename = f"book_{uuid.uuid4().hex[:8]}.json"
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return filename

def validate_uploaded_file(uploaded_file):
    if not uploaded_file.name.endswith('.json'):
        raise ValidationError("Поддерживаются только файлы формата JSON.")
    try:
        content = uploaded_file.read().decode('utf-8')
        data = json.loads(content)
        if isinstance(data, dict):
            required_keys = ['title', 'author', 'year', 'pages']
            if not all(key in data for key in required_keys):
                raise ValidationError("Неверная структура JSON: отсутствуют поля.")
    except json.JSONDecodeError:
        raise ValidationError("Файл не является валидным JSON.")
    except Exception as e:
        raise ValidationError(f"Ошибка: {str(e)}")
    uploaded_file.seek(0)
    return True

def save_uploaded_file(uploaded_file):
    ensure_dir_exists()
    filename = f"uploaded_{uuid.uuid4().hex[:8]}.json"
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return filename

def get_all_files():
    ensure_dir_exists()
    return [f for f in os.listdir(DATA_DIR) if f.endswith('.json')]