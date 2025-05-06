from django.db import models
from django.contrib.auth.models import User


class AdminAccessLog(models.Model):
    """Модель входов в админку."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_time = models.DateTimeField(auto_now_add=True)


class TelegramSubscriber(models.Model):
    """Модель подписчиков на бота."""
    chat_id = models.BigIntegerField(unique=True)


class AdminNotification(models.Model):
    """Модель-костыль, что бы бот каждый раз рассылал сообщения, а не падал после первой отправки."""
    text = models.TextField()
    sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
