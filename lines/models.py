from asyncio.windows_events import NULL

from django.db import models
from accounts.models import Account
from billing.models import Plan

# Create your models here.
class Line(models.Model):
    STATUS_OPTIONS = [
        ('provisioned', 'Provisioned'),
        ('active', 'Active'),
        ('suspended', 'Suspended'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='lines')
    msisdn = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, choices=STATUS_OPTIONS, default='provisioned')
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.msisdn