from django.db import models
from accounts.models import Account
from django.utils import timezone

# Create your models here.
class Plan(models.Model):
    name = models.CharField(max_length=255)
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Invoice(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='invoices')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)

    @property
    def is_overdue(self):
        return not self.is_paid and self.due_date < timezone.now().date()

    def __str__(self):
        return f"Invoice {self.id} - {self.account.name}"