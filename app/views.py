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
    
 
    data= serializers.serialize('json',c.pet_info_set.all())
    return HttpResponse(data)

def ajax_get(request):
    loction_name=request.GET.get('loction_name')
    request.session['loction_name'] = loction_name
    return HttpResponse(loction_name)

def env_filter(request):
    from django.core import serializers
    loction_name = request.session['loction_name']
    data= serializers.serialize('json',models.env_info.objects.filter(name__contains=loction_name).order_by('updated_at'))
    return HttpResponse(data) 
