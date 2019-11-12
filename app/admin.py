from django.contrib import admin
from .models import env_info ,pet_info ,Schedule ,Tag_Info ,food_type ,device_info ,control

class env_infoAdmin(admin.ModelAdmin):  
    list_display = ('mac','temperature','humidity','updated_at','created_at')
class device_infoAdmin(admin.ModelAdmin):
    list_display = ('device_name','mac','updated_at','created_at')
    #後台要顯示的資料表格
class pet_infoAdmin(admin.ModelAdmin):
    list_display = ('Tag','food_eat','water_drink','updated_at')
    #後台要顯示的資料表格
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('Tag','mac','schedule_time','food_amount')
    #後台要顯示的資料表格
class Tag_InfoAdmin(admin.ModelAdmin):
    list_display = ('Tag','nickname','category' ,'weight','per','cat_statue','dog_statue','suggest_feed_amount_daily','suggest_water_drinking_daily','updated_at','created_at')
    #後台要顯示的資料表格
class food_typeAdmin(admin.ModelAdmin):
    list_display = ('Name','mac','kCal','created_at')
    #後台要顯示的資料表格
class controlAdmin(admin.ModelAdmin):
    list_display = ('x_angle','y_angle')
    #後台要顯示的資料表格  
admin.site.register(device_info,device_infoAdmin)
admin.site.register(env_info,env_infoAdmin)        #註冊 env_info 這個 model
admin.site.register(pet_info,pet_infoAdmin)        
admin.site.register(Schedule,ScheduleAdmin)       
admin.site.register(Tag_Info,Tag_InfoAdmin) 
admin.site.register(food_type,food_typeAdmin)   
admin.site.register(control,controlAdmin)  




