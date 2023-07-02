from mailing.models import NULLABLE
from datetime import date
from django.db.models import *


class Blog(Model):
    heading = CharField(max_length=255, unique=True, verbose_name='Заголовок')
    content = TextField(verbose_name='Cодержимое статьи')
    image = ImageField(upload_to='blog_images', verbose_name='Изображение', **NULLABLE)
    views_count = IntegerField(max_length=15, default=0, verbose_name='Количество просмотров')
    publicate_date = DateField(default=date.today, verbose_name='Количество просмотров')

    def __str__(self):
        return self.heading

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'


