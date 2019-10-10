from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views


urlpatterns = [path('', views.home, name='home'),
    path('env/temperature', views.temperature, name='env_temperature'),
    path('env/humidity', views.humidity, name='env_humidity'),
    path('env/all', views.env_all, name='env_all'),
    path('json', views.json_test, name='json'),
    path('ajax/env_filter', views.env_filter, name='env_filter'),
    path('ajax/tag_Info', views.Tag_Info, name='Tag_Info'),
    path('ajax/device_Info', views.Device_Info, name='Device_Info'),
    path('ajax/pet_pannel', views.pet_pannel, name='pet_pannel'),
    path('ajax/Tag_list', views.Tag_list, name='Tag_list'),
    path('ajax/device_list', views.device_list, name='device_list'),
    path('ajax/pet_filter_info', views.pet_filter_info, name='pet_filter_info'),
    path('ajax/pet_filter_Schedule', views.pet_filter_Schedule, name='pet_filter_Schedule'),
    path('ajax/pet_filter_chart_search', views.pet_filter_chart_search, name='pet_filter_chart_search'),
    path('ajax/pet_filter_chart', views.pet_filter_chart,name='pet_filter_chart'),
    path('ajax/pet_filter_latest', views.pet_filter_latest, name='pet_filter_latest'),
    path('ajax/pet_filter_latest1', views.pet_filter_latest1, name='pet_filter_latest1'),
    path('ajax/device_filter_latest1', views.device_filter_latest1, name='device_filter_latest1'),
    path('ajax/pet_filter_earliest', views.pet_filter_earliest, name='pet_filter_earliest'),
    path('ajax/env_get_id', views.env_get_id, name='env_get_id'),
    path('ajax/env_filter_latest', views.env_filter_latest, name='env_filter_latest'),
    path('ajax/env_filter_earliest', views.env_filter_earliest, name='env_filter_earliest'),
    path('ajax/env_filter_chart_search', views.env_filter_chart_search, name='env_filter_chart_search'),
    path('ajax/env_filter_chart', views.env_filter_chart,name='env_filter_chart'),
    path('ajax/pet_get_id', views.pet_get_id, name='pet_get_id'),
    path('api/data_upload', views.data_upload, name='data_upload'),
    path('ajax/post_form', views.post_form, name='post_form'),
    path('ajax/post_device_form', views.post_device_form, name='post_device_form'),
    path('ajax/del_data', views.del_data, name='del_data'),
    path('ajax/del_device_data', views.del_device_data, name='del_device_data'),
    path('ajax/add_Schedule', views.add_Schedule, name='add_Schedule'),
    path('ajax/del_Schedule', views.del_Schedule, name='del_Schedule'),
    path('ajax/list_Schedule', views.list_Schedule, name='list_Schedule'),
    path('ajax/search_foodName', views.search_foodName, name='search_foodName'),
    path('ajax/list_foodType', views.list_foodType, name='list_foodType'),
    path('ajax/add_foodType', views.add_foodType, name='add_foodType'),
    path('ajax/del_foodType', views.del_foodType, name='del_foodType'),
    path('ajax/all_list_Schedule', views.all_list_Schedule, name='all_list_Schedule'),
    path('ajax/device_serach', views.device_serach, name='device_serach'),
    path('pet', views.pet, name='pet'),
    path('login/',
         LoginView.as_view(template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls,name='admin')
    ,]
