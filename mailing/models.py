from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.db.models import *


NULLABLE = {'null': True, 'blank': True}


class Client(Model):
    email = EmailField(verbose_name='Электронная почта', unique=True)
    fio = CharField(max_length=100, verbose_name='ФИО')
    comment = TextField(verbose_name='Комментарий', **NULLABLE)
    active_flg = BooleanField(verbose_name='Активный', default=True)
    last_mailing_dttm = DateTimeField(verbose_name='Дата и время последней рассылки', default=datetime.now)
    author = ForeignKey("mailing.User", on_delete=CASCADE, verbose_name='Автор', **NULLABLE)

    def __str__(self):
        return f"{self.fio} - {self.email}"

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def delete(self, *args, **kwargs):
        self.active_flg = False
        self.save()


class Mailing(Model):
    REGULARITY = (
        (1, 'Раз в день'),
        (7, 'Раз в неделю'),
        (30, 'Раз в месяц'),
    )

    STATUS = (
        ('created', 'Создана'),
        ('completed', 'Завершена'),
        ('launched', 'Запущена'),
    )

    name = CharField(max_length=150, verbose_name='Наименование рассылки', unique=True)
    time = TimeField(verbose_name='Время рассылки', default='00:00:00', **NULLABLE)
    regularity = IntegerField(verbose_name='Периодичность', choices=REGULARITY, default=REGULARITY[0][0])
    status = CharField(max_length=20, verbose_name='Cтатус рассылки', choices=STATUS, default=STATUS[0][0])
    client = ManyToManyField(Client, verbose_name='Клиент', blank=True)
    active_flg = BooleanField(verbose_name='Активный', default=True)
    author = ForeignKey("mailing.User", on_delete=CASCADE, verbose_name='Автор', **NULLABLE)

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            ('setting_the_mailing_status', 'Сan set mailing status'),
        ]


    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.active_flg = False
        self.save()


class MailingMessage(Model):
    topic = CharField(max_length=200, verbose_name='Тема письма', **NULLABLE)
    text = TextField(verbose_name='Текст письма')
    mailing = ForeignKey(Mailing, on_delete=CASCADE, blank=True, related_name='messages')

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
    mailing = ForeignKey(Mailing, on_delete=CASCADE, verbose_name='Рассылка')
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
        permissions = [
            ('setting_the_user_status', 'Сan set user status'),
        ]

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Необходимо указать email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперюзер должен иметь is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперюзер должен иметь is_superuser=True")

        return self._create_user(email, password, **extra_fields)