from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import AdminAccessLog, AdminNotification

@receiver(user_logged_in)
def log_admin_access(sender, request, user, **kwargs):
    """Смотрим на запрос к админке"""
    if request.path.startswith('/admin/'):
        log = AdminAccessLog.objects.create(user=user)
        text = f"Дата: {log.access_time.strftime('%Y-%m-%d %H:%M:%S')} \nПользователь {user.username}"
        AdminNotification.objects.create(text=text)  # Если вход был удачным, записываем в модель-костыль.
