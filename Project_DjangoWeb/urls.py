from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views


urlpatterns = [
    path('', views.home, name='home'),
    path('env/temperature', views.temperature, name='env_temperature'),
    path('env/humidity', views.humidity, name='env_humidity'),
    path('json', views.json_test, name='json'),
    path('ajax/env_filter', views.env_filter, name='env_filter'),
    path('ajax/pet_filter_info', views.pet_filter_info, name='pet_filter_info'),
    path('ajax/pet_filter_user_setting', views.pet_filter_user_setting, name='pet_filter_user_setting'),
    path('ajax/env_get', views.env_get, name='env_get'),
    path('ajax/pet_get_id', views.pet_get_id, name='pet_get_id'),
    path('ajax/pet_get_form', views.pet_get_form, name='pet_get_form'),
    path('json_upload', views.json_upload, name='json_upload'),
    path('json_test', views.json_test, name='json_test'),


    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
]