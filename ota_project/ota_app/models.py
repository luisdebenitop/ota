from django.db import models
from django.utils.crypto import get_random_string


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    company_name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    invoice_currency = models.CharField(max_length=3)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    invoiced_user = models.ForeignKey(User, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=5, unique=True)
    invoiced_amount = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_date = models.DateField()
    is_paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.invoice_number = "OTA-" + get_random_string(
                length=5, allowed_chars="0123456789"
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice_number
