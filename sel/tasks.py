"""
CELERY WORKER MANAGE COMMAND:
celery -A core worker -l INFO

START CELERY BEAT SERVICE:
celery -A core beat

EMBED BEAT INSIDE THE WORKER:
celery -A core worker -B
celery -A core worker -B -l INFO

EXAMPLE:
m = mul.apply_async(kwargs={"x": 2, "y": 30}, eta=datetime.datetime.utcnow())
m = mul.apply_async(kwargs={"x": 2, "y": 30}, eta=timezone.now()+timezone.timedelta(seconds=10))

"""

# Create your tasks here

# from demoapp.models import Widget

import requests
from bs4 import BeautifulSoup

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from .models import Quotes, Pointer


@shared_task
def send_postponed_email(*args, **kwargs):
    return send_mail


@shared_task
def grab_quotes(url, quote_qty=5):
    def get_page(page):
        """
        Получить html - страницу с номером page
        :param page: номер страницы
        :return: страницу как текст
        """
        nonlocal url
        header = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0',
            'Accept':
                'application/font-woff2;q=1.0,application/font-woff;q=0.9,*/*;q=0.8'
        }
        full_url = url + f'page/{page}/'  # получить полный url: базовый + номер страницы
        response = requests.get(full_url, headers=header)  # загрузить страницу
        if response.status_code == 200:  # если успешно
            return response.text  # получить страницу как текст
        else:
            return None

    def get_all_quotes_on_page(html) -> list[tuple]:
        """
        Получить все цитаты на странице
        :param html: страница как текст
        :return: список кортежей (цитата, автор)
        """
        result = []
        soup = BeautifulSoup(html, 'html.parser')  # загрузить страницу в парсер
        quote_list = soup.find_all(name='div', attrs={'class': 'quote'})  # найти все цитаты
        for quote in quote_list:
            # сформировать список кортежей (цитата, автор)
            result.append(
                (quote.find(name='span', attrs={'itemprop': 'text'}).text,
                 quote.find(name='small', attrs={'itemprop': 'author'}).text,)
            )
        return result

    # позицию чтения цитаты храним в базе данных в таблице Pointer
    if not Pointer.objects.first():  # если в базе нет сохраненной позиции
        Pointer.objects.create(page=1, quote_num=1)  # создаем запись, указывающую на 1-ю цитату на 1-й странице
    pointer = Pointer.objects.first()  # присваиваем значение текущей позиции чтения переменной

    result = []
    quotes_need_read_on_page = quote_qty  # установить кол-во цитат, которые нужно считать на текущей странице
    success = False  # сбросить флаг успешного окончания процесса

    while not success:
        html = get_page(page=pointer.page)  # прочитать страницу
        quotes = get_all_quotes_on_page(html)  # прочитать все цитаты со страницы
        if not quotes:  # если более нет цитат
            send_mail(  # отправить e-mail с уведомлением на адрес админа
                subject='The END achieved!',
                message='There are no quotes left!',
                from_email=settings.NO_REPLY_EMAIL,
                recipient_list=['admin@example.com', ]
            )
            break

        start = pointer.quote_num - 1  # установить номер первой цитаты, которую нужно прочесть
        finish = start + quotes_need_read_on_page  # установить номер последней цитаты, которую нужно прочесть
        quotes_for_add = quotes[start:finish]  # выделить из списка всех цитат на странице только те, что нужны
        result.extend(quotes_for_add)  # добавить к результату
        quotes_been_read = len(quotes_for_add)  # сколько было прочитано цитат с текущей страницы?
        pointer.quote_num += quotes_been_read  # сдвинуть позицию чтения на количество прочитанных цитат

        if quotes_been_read < quotes_need_read_on_page:  # если с текущей страницы было прочитано меньше цитат, чем требовалось
            pointer.page += 1  # установить позицию чтения на начало следующей страницы
            pointer.quote_num = 1
            quotes_need_read_on_page -= quotes_been_read  # Установить количество цитат,
                                                          # которые осталось прочесть в текущем цикле чтения.
                                                          # Вернуться в начало цикла чтения
        else:  # если прочитали сколько требовалось
            success = True  # установить флаг успешного окончания процесса
            if pointer.quote_num > len(quotes):  # если на текущей странице не осталось непрочитанных цитат,
                pointer.page += 1  # установить позицию чтения на начало следующей страницы
                pointer.quote_num = 1

    pointer.save()  # сохранить позицию чтения в базу данных Pointer
    Quotes.objects.bulk_create(  # записываем полученные цитаты в базу данных Quotes
        (
            Quotes(
                text=quote[0],  # цитата
                author=quote[1]  # автор
            ) for quote in result  # result - это список кортежей (цитата, автор)
        )
    )
    return
