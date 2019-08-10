from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from app import models
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone


@login_required(login_url='/login/')
def home(request):
    """Renders the home page."""
    #assert isinstance(request, HttpRequest)
    #apps=models.env_info.objects.values('name').distinct() 
    #apps=models.env_info.objects.all()
    apps=models.Tag_Info.objects.values('Tag').distinct() 
    title='Home Page'
    year=datetime.now().year
    return render(request,'app/index.html',locals())

def temperature(request):
    apps=models.env_info.objects.values('name').distinct() 
    title='Env Page'
    year=datetime.now().year
    return render(request,'app/temperature.html',locals())

def humidity(request):
    apps=models.env_info.objects.values('name').distinct() 
    title='Env Page'
    year=datetime.now().year
    return render(request,'app/humidity.html',locals())

def json(request):
    from django.core import serializers
    #data=models.env_info.objects.values('name').distinct() 
    #data=models.env_info.objects.filter(name__contains='home').values()
    c=models.Tag_Info.objects.get(Tag='GG45FC')
    data= serializers.serialize('json',c.user_setting_set.all())
    return HttpResponse(data)

def env_get(request):
    loction_name=request.GET.get('loction_name')
    request.session['loction_name'] = loction_name
    return HttpResponse(loction_name)

def env_filter(request):
    from django.core import serializers
    loction_name = request.session['loction_name']
    data= serializers.serialize('json',models.env_info.objects.filter(name__contains=loction_name).order_by('updated_at'))
    return HttpResponse(data) 

def pet_get_id(request):
    Tag=request.GET.get('Tag')
    request.session['Tag'] = Tag
    return HttpResponse(Tag)


def pet_get_form(request):
    return HttpResponse(1)

def pet_filter_info(request):
    from django.core import serializers
    import datetime
    Tag = request.session['Tag']
    date_filter = datetime.datetime.now(tz=timezone.utc) - datetime.timedelta(days=10) #現在時間UTC+8 轉成 UTC+0
    data= serializers.serialize('json',models.Tag_Info.objects.get(Tag=Tag,updated_at__gte=date_filter).pet_info_set.all().order_by('updated_at'))
    return HttpResponse(data) 

def pet_filter_user_setting(request):
    from django.core import serializers
    Tag = request.session['Tag']
    data= serializers.serialize('json',models.Tag_Info.objects.get(Tag=Tag).user_setting_set.all().order_by('updated_at'))
    return HttpResponse(data) 

def json_upload(request):
    info = models.pet_info.objects.create(Tag=1)  
    info.water_drink=request.GET['water_drink']                
    info.food_eat=request.GET['food_eat']
    info.save()                                         #後臺資料庫儲存環境數據。
    return HttpResponse(1) 