from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Account

@receiver(post_save, sender=Account)
def handle_arrears_change(sender, instance, **kwargs):
    if instance.is_in_arrears:
        instance.lines.filter(status='active').update(status='suspended')
    else:
        instance.lines.filter(status='suspended').update(status='active')