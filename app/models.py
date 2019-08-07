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

class Rfid(models.Model):
    R_id = models.CharField(max_length=20)
    name = models.CharField(max_length=20, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return self.R_id

class pet_info(models.Model):
    r_id = models.ForeignKey(Rfid,on_delete=models.CASCADE)
    water_drink = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'))
    food_eat = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'))
    updated_at = models.DateTimeField(auto_now_add=True)

class user_setting(models.Model):
    r_id = models.ForeignKey(Rfid,on_delete=models.CASCADE)
    user_water_setting = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'))
    user_food_setting = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'))
    updated_at = models.DateTimeField(auto_now_add=True)
