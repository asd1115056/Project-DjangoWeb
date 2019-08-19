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
import json
import math


@login_required(login_url='/login/')
def home(request):
    """Renders the home page."""
    #assert isinstance(request, HttpRequest)
    #apps=models.env_info.objects.values('name').distinct()
    #apps=models.env_info.objects.all()
    apps = models.Tag_Info.objects.all()
    title = 'Home Page'
    year = datetime.now().year
    return render(request,'app/index.html',locals())

def temperature(request):
    apps = models.env_info.objects.values('name').distinct() 
    title = 'Env Page'
    year = datetime.now().year
    return render(request,'app/temperature.html',locals())

def humidity(request):
    apps = models.env_info.objects.values('name').distinct() 
    title = 'Env Page'
    year = datetime.now().year
    return render(request,'app/humidity.html',locals())

def json_test(request):
    from django.core import serializers
    #data=models.env_info.objects.values('name').distinct()
    #data=models.env_info.objects.filter(name__contains='home').values()
    #c=models.Tag_Info.objects.get(Tag='GG45FC')
    #data= serializers.serialize('json',c.user_setting_set.all())
    #test =
    #serializers.serialize('json',models.Tag_Info.objects.filter(Tag='GG45FC').values_list('id')).
    test = models.Tag_Info.objects.filter(Tag='GG45FC').values_list('pk',flat=True)
    return HttpResponse(test)

def env_get(request):
    loction_name = request.GET.get('loction_name')
    request.session['loction_name'] = loction_name
    return HttpResponse(loction_name)

def env_filter(request):
    from django.core import serializers
    loction_name = request.session['loction_name']
    data = serializers.serialize('json',models.env_info.objects.filter(name__contains=loction_name).order_by('updated_at'))
    return HttpResponse(data) 

def pet_get_id(request):
    Tag = request.GET.get('Tag')
    request.session['Tag'] = Tag
    return HttpResponse(Tag)


def pet_get_form(request):
    return HttpResponse(1)

def Tag_Info(request):
    from django.core import serializers
    import datetime
    Tag = request.session['Tag']
    data = serializers.serialize('json',models.Tag_Info.objects.filter(Tag=Tag))
    return HttpResponse(data) 

def pet_filter_info(request):
    from django.core import serializers
    from datetime import datetime, timedelta, time
    Tag = request.session['Tag']
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())
    #date_filter = datetime.datetime.now(tz=timezone.utc) -
    #datetime.timedelta(days=10) #現在時間UTC+8 轉成 UTC+0
    data = serializers.serialize('json',models.Tag_Info.objects.get(Tag=Tag).pet_info_set.filter(updated_at__lte=today_end,updated_at__gte=today_start).order_by('updated_at'))
    return HttpResponse(data) 

def pet_filter_user_setting(request):
    from django.core import serializers
    Tag = request.session['Tag']
    data = serializers.serialize('json',models.Tag_Info.objects.get(Tag=Tag).user_setting_set.all().order_by('updated_at'))
    return HttpResponse(data) 


@csrf_exempt
def json_upload(request):
    if request.method == 'POST':
        Data_POST = json.loads(request.body.decode("utf-8"))
        Tag = Data_POST.get('Tag')
        temp = models.Tag_Info.objects.filter(Tag=Tag)
        if temp.exists():
            text1 = "Tag Existing"
            #return JsonResponse({"status": 200, "msg": "Tag Existing" })
        else:
            TAG = models.Tag_Info.objects.create(Tag=Tag)
            TAG.save()
            text1 = "Create New Tag"
            #return JsonResponse({"status": 200, "msg": "Create New Tag" })
        pk = list(temp.values_list('pk',flat=True)) #實際輸出['1','2',…] 用python List轉換成[1,2,...]
        info = models.pet_info.objects.create(Tag_id=pk[0])
        info.water_drink = Data_POST.get('water_drink')
        info.food_eat = Data_POST.get('food_eat')
        info.save()
        text2 = " and Save Successfully"
        return JsonResponse({"status": 200, "msg": text1 + text2  })
    else:
        return JsonResponse({"status": 400, "msg": "It is GET" })


@csrf_exempt
def json_test(request):
    Tag = request.session['Tag']
    if request.method == 'POST':
        Data_POST = request.POST
        Data_POST = json.dumps(Data_POST)
        Data_POST = json.loads(Data_POST)
        info = models.Tag_Info.objects.get(Tag=Tag)
        if Data_POST.get('Nickname') != "":
            info.nickname = Data_POST.get('Nickname')
        if Data_POST.get('Weight') != "":
            info.weight = float(Data_POST.get('Weight'))
            info.per = 70 * round(math.pow(float(Data_POST.get('Weight')),0.75),2)
        if Data_POST.get('Category') != "":
            info.category = int(Data_POST.get('Category'))
            if Data_POST.get('Category') == "1":
                info.cat_statue = float(Data_POST.get('Status'))
                info.dog_statue = None
            if Data_POST.get('Category') == "2":
                info.dog_statue = float(Data_POST.get('Status'))
                info.cat_statue = None
        info.save()
        
        weight_temp = list(models.Tag_Info.objects.filter(Tag=Tag).values_list('weight',flat=True))
        category_temp = list(models.Tag_Info.objects.filter(Tag=Tag).values_list('category',flat=True))
        per_temp = list(models.Tag_Info.objects.filter(Tag=Tag).values_list('per',flat=True))
        cat_statue_temp = list(models.Tag_Info.objects.filter(Tag=Tag).values_list('cat_statue',flat=True))
        dog_statue_temp = list(models.Tag_Info.objects.filter(Tag=Tag).values_list('dog_statue',flat=True))

        temp = None
        temp_daily = None
        if weight_temp[0] != 0 and category_temp[0] != 0:
            if category_temp[0] == 1:
                temp = weight_temp[0] * 50
                if per_temp[0] != 0 and cat_statue_temp[0] != 0:
                    temp_daily = per_temp[0] * cat_statue_temp[0]
            elif category_temp[0] == 2:
                temp = weight_temp[0] * 60
                if per_temp[0] != 0 and cat_statue_temp[0] != 0:
                     temp_daily = per_temp[0] * dog_statue_temp[0]

        info1 = models.Tag_Info.objects.get(Tag=Tag)
        info1.suggest_water_drinking_daily = temp
        info1.suggest_feed_amount_daily = temp_daily
        info1.save()


        #info.suggest_feed_amount_daily =
        
        text = " Update Successfully"

        return JsonResponse({"status": 200, "msg": text  })
