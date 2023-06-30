from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Blog
from .middleware import get_current_user

@receiver(pre_save, sender=Blog)
def my_handler(sender, instance, **kwargs):
    if not instance.pk:
        instance.user_admin = get_current_user()
        instance.view_count = 0
