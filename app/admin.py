from django.contrib import admin
from .models import env_info



class env_infoAdmin(admin.ModelAdmin):
    list_display = ('name','temperature','humidity','updated_at')
    #後台要顯示的資料表格
    #list_filter = ['updated_at']


admin.site.register(env_info,env_infoAdmin)        #註冊 env_info 這個 model
