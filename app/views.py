from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from app import models
import json

@login_required(login_url='/login/')
def home(request):
    """Renders the home page."""
    #assert isinstance(request, HttpRequest)
    apps=models.env_info.objects.values('name').distinct() 
    #apps=models.env_info.objects.all()

    title='Home Page'
    year=datetime.now().year

    return render(request,'app/index.html',locals())

def json(request):
    from django.core import serializers
    data=models.env_info.objects.values('name').distinct() 
    return HttpResponse(data)
 