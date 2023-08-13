from django.db import models


# Create your models here.

class Quotes(models.Model):
    # Таблица для хранения цитат
    text = models.TextField()  # текст цитаты
    author = models.CharField(max_length=30)  # автор цитаты

    def __str__(self):
        return f'Text: {self.text[:30]}, Author: {self.author}'


class Pointer(models.Model):
    # в этой таблице будет храниться указатель текущей позиции чтения цитат с сайта
    page = models.SmallIntegerField()  # номер страницы
    quote_num = models.SmallIntegerField()  # номер цитаты на текущей странице

    def __str__(self):
        return f'Page: {self.page}, Quoter number: {self.quote_num}'

