from django.db import models
from decimal import Decimal
import django.utils.timezone as timezone


class device_info(models.Model):
    device_name = models.CharField(max_length=100,null=True, blank=True) #LOCATION_NAME
    mac = models.CharField(max_length=100) #ID
    updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
       return self.mac
    def natural_key(self):
       return (self.mac)

class env_info(models.Model):
    mac = models.ForeignKey(device_info,on_delete=models.CASCADE)
    temperature = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'))
    humidity = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'))
    updated_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

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
    nickname = models.CharField(max_length=20,null=True, blank=True)
    category = models.SmallIntegerField(choices = CHOICE, null = True, blank = True,default=0)
    cat_statue = models.DecimalField(choices = cat, null=True, blank=True,max_digits=6,decimal_places=2,default=Decimal('0.00'))
    dog_statue = models.DecimalField(choices = dog, null = True, blank = True,max_digits=6,decimal_places=2,default=Decimal('0.00'))
    per = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'), null=True, blank=True)
    weight = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'), null=True, blank=True)
    suggest_water_drinking_daily = models.DecimalField(max_digits = 6,decimal_places = 2,default = Decimal('0.00'), null = True, blank = True)
    suggest_feed_amount_daily = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'), null=True, blank=True)
    user_water_drinking_setting_daily = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'), null=True, blank=True)
    user_feed_amount_setting_daily = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'), null=True, blank=True)
    updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
       return self.Tag
    def natural_key(self):
        return (self.Tag)

class pet_info(models.Model):
    Tag = models.ForeignKey(Tag_Info,on_delete=models.CASCADE)
    mac = models.ForeignKey(device_info,on_delete=models.CASCADE)
    water_drink = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'),null=True, blank=True)
    food_eat = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'),null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)



class food_type(models.Model):
    Name = models.CharField(max_length = 20)
    kCal = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'),null=True, blank=True)
    mac = models.ForeignKey(device_info,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
       return self.Name
    def natural_key(self):
       return (self.Name) #外鍵顯示內容非PK
class Schedule(models.Model):
    Tag = models.ForeignKey(Tag_Info,on_delete=models.CASCADE)
    mac = models.ForeignKey(device_info,on_delete=models.CASCADE)
    schedule_time = models.TimeField(null=True, blank=True)
    food_amount = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'),null=True, blank=True)
 