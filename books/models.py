from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    author = models.CharField(max_length=100, verbose_name="Автор")
    year = models.IntegerField(verbose_name="Год издания")
    pages = models.IntegerField(verbose_name="Количество страниц")

    def __str__(self):
        return self.title