from django.contrib.auth.models import AbstractUser
from django.db.models import *


NULLABLE = {'null': True, 'blank': True}


class Client(Model):
    email = EmailField(verbose_name='Электронная почта')
    fio = CharField(max_length=100, verbose_name='ФИО')
    comment = TextField(verbose_name='Комментарий', **NULLABLE)

    def __str__(self):
        return f"{self.fio} - {self.email}"

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Mailing(Model):
    REGULARITY = (
        ('once a day', 'Раз в день'),
        ('once a week', 'Раз в неделю'),
        ('once a month', 'Раз в месяц'),
    )

    STATUS = (
        ('created', 'Создана'),
        ('completed', 'Завершена'),
        ('launched', 'Запущена'),
    )

    name = CharField(max_length=150, verbose_name='Наименование рассылки', unique=True)
    time = TimeField(verbose_name='Время рассылки', default='00:00:00', **NULLABLE)
    regularity = CharField(max_length=20, verbose_name='Периодичность', choices=REGULARITY, default=REGULARITY[0][0])
    status = CharField(max_length=20, verbose_name='Cтатус рассылки', choices=STATUS, default=STATUS[0][0])
    client = ManyToManyField(Client, verbose_name='Клиент')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingMessage(Model):
    topic = CharField(max_length=200, verbose_name='Тема письма', **NULLABLE)
    text = TextField(verbose_name='Текст письма')
    mailing = OneToOneField(Mailing, to_field='id', on_delete=CASCADE)

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = 'Сообщение для рассылки'
        verbose_name_plural = 'Сообщения для рассылок'


class MailingTrying(Model):
    STATUS = (
        ('success', 'Успешно отправлено'),
        ('error', 'Ошибка при отправке')
    )

    trying_date = DateTimeField(verbose_name='Дата и время попытки рассылки')
    mailing = ForeignKey(Mailing, to_field='id', on_delete=CASCADE)
    status = CharField(max_length=10, verbose_name='Статус отправки', choices=STATUS)
    server_response = TextField(verbose_name='Ответ сервера', **NULLABLE)

    def __str__(self):
        return f"{self.trying_date} - {self.STATUS}"

    class Meta:
        verbose_name = 'Попытка отправки письма'
        verbose_name_plural = 'Попытки отправок писем'


class User(AbstractUser):
    username = None
    email = EmailField(unique=True, verbose_name='email')
    avatar = ImageField(upload_to='media/avatars', verbose_name='Аватар', **NULLABLE)
    phone_number = CharField(max_length=20, verbose_name='Номер телефона', **NULLABLE)
    country = CharField(max_length=100, verbose_name='Страна')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'