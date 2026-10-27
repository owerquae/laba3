import os
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from .forms import BookForm, UploadFileForm
from .utils import save_book_to_json, validate_uploaded_file, save_uploaded_file, get_all_files, DATA_DIR

def index(request):
    files = get_all_files()
    return render(request, 'books/index.html', {'files': files})

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            filename = save_book_to_json(form.cleaned_data)
            messages.success(request, f'Книга сохранена: {filename}')
            return redirect('index')
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form})

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            try:
                validate_uploaded_file(file)
                filename = save_uploaded_file(file)
                messages.success(request, f'Файл загружен как {filename}')
                return redirect('index')
            except ValidationError as e:
                messages.error(request, f'Ошибка: {e.message}')
    else:
        form = UploadFileForm()
    return render(request, 'books/upload.html', {'form': form})

def view_file_content(request, filename):
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        messages.error(request, "Файл не найден.")
        return redirect('index')
    with open(filepath, 'r', encoding='utf-8') as f:
        content = json.load(f)
    return render(request, 'books/view_file.html', {'content': content, 'filename': filename})