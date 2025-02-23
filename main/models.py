from email.policy import default
from tabnanny import verbose
from tkinter.constants import CASCADE
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import ForeignKey
from django.utils import timezone
from django.conf import settings

class CustomUser(AbstractUser):
    phone = models.CharField(verbose_name='Телефон', max_length=12)

    def __str__(self):
        return self.username


class Status(models.Model):
    title = models.CharField(max_length=20, verbose_name='Статус')

    def __str__(self):
        return self.title

class Ticket(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Создатель заявки', related_name='ticket_creator')
    title = models.CharField(max_length=255, verbose_name='Название заявки')
    description = models.TextField(verbose_name='Описание заявки')
    category = models.ForeignKey('Categories', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Категория')
    photo = models.ImageField(upload_to='ticket_photos/', verbose_name='Фото проблемы', null=True, blank=True)
    status = models.ForeignKey('Status', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Статус')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')

    def __str__(self):
        return f"{self.title} - {self.creator}"

class Categories(models.Model):
    catgname = models.CharField(max_length=60, blank=False, default="")

    def __str__(self):
        return self.catgname
