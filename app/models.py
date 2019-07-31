from django.db import models
from decimal import Decimal
# Create your models here.


class env_info(models.Model):
    name = models.CharField(max_length=100)
    temperature = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'))
    humidity = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'))
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return self.name
