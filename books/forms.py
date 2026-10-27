from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'year', 'pages']

class UploadFileForm(forms.Form):
    file = forms.FileField(label="Выберите файл (JSON)")