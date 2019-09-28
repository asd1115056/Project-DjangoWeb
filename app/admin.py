from django.contrib import admin
from .models import env_info ,pet_info ,Schedule ,Tag_Info ,food_type



class env_infoAdmin(admin.ModelAdmin):
    list_display = ('name','temperature','humidity','updated_at')
    #後台要顯示的資料表格
class pet_infoAdmin(admin.ModelAdmin):
    list_display = ('Tag','food_eat','water_drink','active_time','updated_at')
    #後台要顯示的資料表格
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('Tag','schedule_time','food_Name','food_amount')
    #後台要顯示的資料表格
class Tag_InfoAdmin(admin.ModelAdmin):
    list_display = ('Tag','nickname','category' ,'weight','per','cat_statue','dog_statue','suggest_feed_amount_daily','suggest_water_drinking_daily','updated_at','created_at')
    #後台要顯示的資料表格
class food_typeAdmin(admin.ModelAdmin):
    list_display = ('Name','kCal','created_at')
    #後台要顯示的資料表格
admin.site.register(env_info,env_infoAdmin)        #註冊 env_info 這個 model
admin.site.register(pet_info,pet_infoAdmin)        
admin.site.register(Schedule,ScheduleAdmin)       
admin.site.register(Tag_Info,Tag_InfoAdmin) 
admin.site.register(food_type,food_typeAdmin)   




