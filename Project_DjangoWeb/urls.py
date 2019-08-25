from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views


urlpatterns = [path('', views.home, name='home'),
    path('env/temperature', views.temperature, name='env_temperature'),
    path('env/humidity', views.humidity, name='env_humidity'),
    path('json', views.json_test, name='json'),
    path('ajax/env_filter', views.env_filter, name='env_filter'),
    path('ajax/tag_Info', views.Tag_Info, name='Tag_Info'),
    path('ajax/pet_filter_info', views.pet_filter_info, name='pet_filter_info'),
    path('ajax/pet_filter_Schedule', views.pet_filter_Schedule, name='pet_filter_Schedule'),
    path('ajax/env_get', views.env_get, name='env_get'),
    path('ajax/pet_get_id', views.pet_get_id, name='pet_get_id'),
    path('json_upload', views.json_upload, name='json_upload'),
    path('ajax/post_form', views.post_form, name='post_form'),
    path('ajax/del_data', views.del_data, name='del_data'),
    path('ajax/add_Schedule', views.add_Schedule, name='add_Schedule'),
    path('ajax/del_Schedule', views.del_Schedule, name='del_Schedule'),
    path('ajax/list_Schedule', views.list_Schedule, name='list_Schedule'),
    path('ajax/search_foodName', views.search_foodName, name='search_foodName'),
    path('ajax/list_foodType', views.list_foodType, name='list_foodType'),
    path('ajax/add_foodType', views.add_foodType, name='add_foodType'),
    path('ajax/del_foodType', views.del_foodType, name='del_foodType'),


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
    path('admin/', admin.site.urls),]
