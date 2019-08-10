from django.contrib import admin
from .models import env_info ,pet_info ,user_setting ,Tag_Info



class env_infoAdmin(admin.ModelAdmin):
    list_display = ('name','temperature','humidity','updated_at')
    #後台要顯示的資料表格
class pet_infoAdmin(admin.ModelAdmin):
    list_display = ('Tag','food_eat','water_drink','updated_at')
    #後台要顯示的資料表格
class user_settingAdmin(admin.ModelAdmin):
    list_display = ('Tag','user_food_setting','user_water_setting','updated_at')
    #後台要顯示的資料表格
class Tag_InfoAdmin(admin.ModelAdmin):
    list_display = ('Tag','name')
    #後台要顯示的資料表格

admin.site.register(env_info,env_infoAdmin)        #註冊 env_info 這個 model
admin.site.register(pet_info,pet_infoAdmin)        
admin.site.register(user_setting,user_settingAdmin)       
admin.site.register(Tag_Info,Tag_InfoAdmin)   




