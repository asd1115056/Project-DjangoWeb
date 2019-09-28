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
    title = 'Home Page'
    year = datetime.now().year
    return render(request,'app/index.html',locals())

def pet(request):
    """Renders the home page."""
    #assert isinstance(request, HttpRequest)
    #apps=models.env_info.objects.values('name').distinct()
    #apps=models.env_info.objects.all()
    apps = models.Tag_Info.objects.all()
    title = 'Pet Page'
    year = datetime.now().year
    return render(request,'app/pet.html',locals())

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
    #data= serializers.serialize('json',c.Schedule_set.all())
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
    try:
        Tag = request.GET.get('Tag')
    except Tag.DoesNotExist:
        Tag = None
    finally:
        request.session['Tag'] = Tag
    return HttpResponse(Tag)


def Tag_Info(request):
    from django.core import serializers
    import datetime
    Tag = request.session['Tag']
    data = serializers.serialize('json',models.Tag_Info.objects.filter(Tag=Tag))
    return HttpResponse(data) 

def pet_filter_info(request):
    from django.core import serializers
    from datetime import datetime, timedelta, time
    from django.utils import timezone
    Tag = request.session['Tag']
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    today_start = timezone.make_aware(datetime.combine(today, time()))
    today_end = timezone.make_aware(datetime.combine(tomorrow, time())) #轉換時區
    #date_filter = datetime.datetime.now(tz=timezone.utc)
                                                                           #-datetime.timedelta(days=10)#現在時間UTC+8轉成UTC+0
    data = serializers.serialize('json',models.Tag_Info.objects.get(Tag=Tag).pet_info_set.filter(updated_at__lte=today_end,updated_at__gte=today_start).order_by('updated_at'))
    return HttpResponse(data) 

def pet_filter_Schedule(request):
    from django.core import serializers
    Tag = request.session['Tag']
    data = serializers.serialize('json',models.Tag_Info.objects.get(Tag=Tag).Schedule_set.all().order_by('updated_at'))
    return HttpResponse(data) 

def list_Schedule(request):
    from django.core import serializers
    Tag = request.session['Tag']
    temp = models.Tag_Info.objects.filter(Tag=Tag)
    pk = list(temp.values_list('pk',flat=True)) #實際輸出['1','2',…] 用python List轉換成[1,2,...]
    data = serializers.serialize('json',models.Schedule.objects.filter(Tag=pk[0]).order_by('schedule_time'))
    return HttpResponse(data)
def all_list_Schedule(request):
    from django.core import serializers
    data = serializers.serialize('json',models.Schedule.objects.all().order_by('schedule_time','Tag'),use_natural_foreign_keys=True, use_natural_primary_keys=True)
    return HttpResponse(data) 

@csrf_exempt
def search_foodName(request):
    from django.core import serializers
    if request.method == 'POST':
        Data_POST = request.POST
        Data_POST = json.dumps(Data_POST)
        Data_POST = json.loads(Data_POST)
        Object = Data_POST.get('object')
        Value = Data_POST.get('value')
        if Object == "pk" :
            data = models.food_type.objects.filter(pk=Value)
        data = serializers.serialize('json',data)
        return HttpResponse(data)
def list_foodType(request):
    from django.core import serializers
    data = serializers.serialize('json',models.food_type.objects.all())
    return HttpResponse(data)

@csrf_exempt
def json_upload(request):
    #Tag = request.session['Tag']
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
def post_form(request):
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
        if Data_POST.get('Category') != "0":
            info.category = int(Data_POST.get('Category'))
            if Data_POST.get('Category') == "1":
                if Data_POST.get('Status') != "0":
                    info.cat_statue = float(Data_POST.get('Status'))
                    info.dog_statue = None
            if Data_POST.get('Category') == "2":
                    if Data_POST.get('Status') != "0":
                        info.dog_statue = float(Data_POST.get('Status'))
                        info.cat_statue = None
        if Data_POST.get('User_feed_amount_setting_daily') != "":
            info.user_feed_amount_setting_daily = int(Data_POST.get('User_feed_amount_setting_daily'))     
        if Data_POST.get('User_water_drinking_setting_daily') != "":
            info.user_water_drinking_setting_daily = int(Data_POST.get('User_water_drinking_setting_daily'))        
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
                if (per_temp[0] != 0 or per_temp[0] != None) and (cat_statue_temp[0] != 0 or cat_statue_temp[0] != None):
                    temp_daily = per_temp[0] * cat_statue_temp[0]
            elif category_temp[0] == 2:
                temp = weight_temp[0] * 60
                if (per_temp[0] != 0 or per_temp[0] != None) and (dog_statue_temp[0] != 0 or dog_statue_temp[0] != None):
                     temp_daily = per_temp[0] * dog_statue_temp[0]

        info1 = models.Tag_Info.objects.get(Tag=Tag)
        info1.suggest_water_drinking_daily = temp
        info1.suggest_feed_amount_daily = temp_daily
        info1.save()

        #info.suggest_feed_amount_daily =
        
        text = " Update Successfully"
        return JsonResponse({"status": 200, "msg": text  })
@csrf_exempt
def del_data(request):
    Tag = request.session['Tag']
    if request.method == 'POST':
        Data_POST = request.POST
        Data_POST = json.dumps(Data_POST)
        Data_POST = json.loads(Data_POST)
        if Data_POST.get('Delete') == "confrim":
            models.Tag_Info.objects.get(Tag=Tag).delete()
            return JsonResponse({"status": 200, "msg": "deleted!"  })
@csrf_exempt
def add_Schedule(request):
    Tag = request.session['Tag']
    temp = models.Tag_Info.objects.filter(Tag=Tag)
    pk = list(temp.values_list('pk',flat=True)) #實際輸出['1','2',…] 用python List轉換成[1,2,...]
    if request.method == 'POST':
        Data_POST1 = request.POST.getlist('time[]')
        Data_POST2 = request.POST.getlist('amount[]')
        Data_POST3 = request.POST.getlist('select[]')
        if len(Data_POST1) == len(Data_POST2) and len(Data_POST2) == len(Data_POST3):
            for i in range(len(Data_POST2)):
                food_type_pk = list(models.food_type.objects.filter(Name=Data_POST3[i]).values_list('pk',flat=True)) #實際輸出['1','2',…] 用python List轉換成[1,2,...]
                if Data_POST1[i] != "" and Data_POST2[i] != "" and Data_POST3[i] != "":
                    temp = models.Schedule.objects.filter(Tag_id=pk[0],schedule_time=datetime.strptime(Data_POST1[i], '%H:%M').time())
                    if temp.exists():
                        info = models.Schedule.objects.get(Tag_id=pk[0],schedule_time=datetime.strptime(Data_POST1[i], '%H:%M').time())               
                        info.food_Name_id = food_type_pk[0]
                        info.food_amount = Data_POST2[i]
                        info.save()
                    else:
                        info = models.Schedule.objects.create(Tag_id=pk[0],food_Name_id=food_type_pk[0])
                        info.schedule_time = datetime.strptime(Data_POST1[i],'%H:%M').time()
                        info.food_amount = Data_POST2[i]
                        info.save()
            text = " Update Successfully"
            return JsonResponse({"status": 200, "msg": text  })
    else:
        return JsonResponse({"status": 400, "msg": "It is GET" })
@csrf_exempt
def add_foodType(request):
    if request.method == 'POST':
        Data_POST1 = request.POST.getlist('Name[]')
        Data_POST2 = request.POST.getlist('kCal[]')
        if len(Data_POST1) == len(Data_POST2):
            for i in range(len(Data_POST2)):
                if Data_POST1[i] != "" and Data_POST2[i] != "":
                    temp = models.food_type.objects.filter(Name=Data_POST1[i])
                    if temp.exists():
                        None
                    else:
                        Name = models.food_type.objects.create(Name=Data_POST1[i])
                        Name.save()
                    temp.update(kCal=Data_POST2[i])
        text = " Update Successfully"
        return JsonResponse({"status": 200, "msg": text  })
    else:
        return JsonResponse({"status": 400, "msg": "It is GET" })
@csrf_exempt
def del_Schedule(request):
    Tag = request.session['Tag']
    temp = models.Tag_Info.objects.filter(Tag=Tag)
    pk = list(temp.values_list('pk',flat=True)) #實際輸出['1','2',…] 用python List轉換成[1,2,...]
    if request.method == 'POST':
        Data_POST = request.POST.getlist('checkbax1[]')
        if Data_POST != "":
            for i in range(len(Data_POST)):
                models.Schedule.objects.get(Tag_id=pk[0],schedule_time=Data_POST[i]).delete()
            return JsonResponse({"status": 200, "msg": "deleted!"  })
@csrf_exempt
def del_foodType(request):
    if request.method == 'POST':
        Data_POST = request.POST.getlist('checkbax2[]')
        if Data_POST != "":
            for i in range(len(Data_POST)):
                models.food_type.objects.get(Name=Data_POST[i]).delete()
            return JsonResponse({"status": 200, "msg": "deleted!"  })