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
    apps=models.Rfid.objects.values('R_id').distinct() 
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
    c=models.Rfid.objects.get(R_id='GG45FC')
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
    R_ID=request.GET.get('R_ID')
    request.session['R_ID'] = R_ID
    return HttpResponse(R_ID)


def pet_get_form(request):
    return HttpResponse(1)

def pet_filter_info(request):
    from django.core import serializers
    import datetime
    R_ID = request.session['R_ID']
    date_filter = datetime.datetime.now(tz=timezone.utc) - datetime.timedelta(days=10) #現在時間UTC+8 轉成 UTC+0
    data= serializers.serialize('json',models.Rfid.objects.get(R_id=R_ID,updated_at__gte=date_filter).pet_info_set.all().order_by('updated_at'))
    return HttpResponse(data) 

def pet_filter_user_setting(request):
    from django.core import serializers
    R_ID = request.session['R_ID']
    data= serializers.serialize('json',models.Rfid.objects.get(R_id=R_ID).user_setting_set.all().order_by('updated_at'))
    return HttpResponse(data) 