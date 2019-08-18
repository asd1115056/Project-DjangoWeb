from django.db import models
from decimal import Decimal

class env_info(models.Model):
    name = models.CharField(max_length=100)
    temperature = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'))
    humidity = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'))
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
       return self.name

class Tag_Info(models.Model):
    CHOICE = ((1, 'Cat'),
        (2, 'Dog'),)
    cat = ((2.5, 'Kitten'),
        (1.4, 'Neutered'),
        (1.2, 'Intact'),
        (1.0, 'Inactive/obese prone'),
        (0.95, 'Weight loss'),)
    dog = ((3, '0-4 months'),
        (2, '4 months to adult'),
        (1.6, 'Neutered'),
        (1.8, 'Intact'),
        (1.3, 'Inactive/obese prone'),
        (1.0, 'Weight loss'),
        (1.5, 'Weight gain'),
        (3.5, 'Active, working dogs'),)
    Tag = models.CharField(max_length = 20)
    nickname = models.CharField(max_length=20, null=True, blank=True,default='Null')
    category = models.SmallIntegerField(choices = CHOICE, null = True, blank = True,default=0)
    cat_statue = models.FloatField(choices = cat, null=True, blank=True,default=0)
    dog_statue = models.FloatField(choices = dog, null = True, blank = True,default=0)
    per = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'), null=True, blank=True)
    weight = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'), null=True, blank=True)
    suggest_water_drinking_daily = models.DecimalField(max_digits = 6,decimal_places = 2,default = Decimal('0.00'), null = True, blank = True)
    suggest_feed_amount_daily = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'), null=True, blank=True)
    updated_at = models.DateTimeField(auto_now = True)
    def __str__(self):
       return self.Tag

class pet_info(models.Model):
    Tag = models.ForeignKey(Tag_Info,on_delete=models.CASCADE)
    water_drink = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'))
    food_eat = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'))
    updated_at = models.DateTimeField(auto_now=True)


class user_setting(models.Model):
    Tag = models.ForeignKey(Tag_Info,on_delete=models.CASCADE)
    user_water_setting_daily = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'))
    user_food_setting_daily = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'))
    updated_at = models.DateTimeField(auto_now=True)

