from django.db import models

# Create your models here.
class Account(models.Model):
    STATUS_OPTIONS = [
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('closed', 'Closed'),
    ]

    name = models.CharField(max_length=123)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=21)
    status = models.CharField(max_length=10, choices=STATUS_OPTIONS, default='active')
    is_in_arrears = models.BooleanField(default=False)

    def __str__(self):
        return self.name