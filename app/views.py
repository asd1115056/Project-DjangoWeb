from datetime import datetime, timedelta
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
    apps = models.device_info.objects.all()
    year = datetime.now().year
    return render(request,'app/index.html',locals())

def pet(request):
    """Renders the home page."""
    #assert isinstance(request, HttpRequest)
    #apps=models.env_info.objects.values('location_id').distinct()
    #apps=models.env_info.objects.all()
    apps = models.Tag_Info.objects.all()
    title = 'Pet Page'
    year = datetime.now().year
    return render(request,'app/pet.html',locals())

def env_all(request):
    #apps = models.device_info.objects.values('mac').distinct()
    apps = models.device_info.objects.all()
    title = 'Env Page'
    year = datetime.now().year
    return render(request,'app/env.html',locals())

def temperature(request):
    #apps = models.device_info.objects.values('mac').distinct()
    apps = models.device_info.objects.all()
    title = 'Env Page'
    year = datetime.now().year
    return render(request,'app/temperature.html',locals())

def humidity(request):
    apps = models.env_info.objects.values('location_code').distinct() 
    title = 'Env Page'
    year = datetime.now().year
    return render(request,'app/humidity.html',locals())

def json_test(request):
    from django.core import serializers
    #data=models.env_info.objects.values('location_id').distinct()
    #data=models.env_info.objects.filter(name__contains='home').values()
    #c=models.Tag_Info.objects.get(Tag='GG45FC')
    #data= serializers.serialize('json',c.Schedule_set.all())
    #test =
    #serializers.serialize('json',models.Tag_Info.objects.filter(Tag='GG45FC').values_list('id')).
    test = models.Tag_Info.objects.filter(Tag='GG45FC').values_list('pk',flat=True)
    return HttpResponse(test)

def env_get(request):
    location_id = request.GET.get('location_id')
    request.session['location_id'] = location_id
    return HttpResponse(location_id)

def env_filter(request):
    from django.core import serializers
    location_id = request.session['location_id']
    data = serializers.serialize('json',models.env_info.objects.filter(location_id__contains=location_id).order_by('updated_at'))
    return HttpResponse(data) 

def env_get_id(request):
    try:
        mac = request.GET.get('mac')
    except mac.DoesNotExist:
        mac = None
    finally:
        request.session['mac'] = mac
    return HttpResponse(mac)

def Device_Info(request):
    from django.core import serializers
    import datetime
    mac = request.session['mac']
    data = serializers.serialize('json',models.device_info.objects.filter(mac=mac))
    return HttpResponse(data) 

def All_device(request):
    from django.core import serializers
    import datetime
    data = serializers.serialize('json',models.device_info.objects.all())
    return HttpResponse(data) 

def env_filter_latest(request):
    from django.core import serializers
    from django.db.models.base import ObjectDoesNotExist
    mac = request.session['mac']
    try:
        data = serializers.serialize('json',[models.device_info.objects.get(mac=mac).env_info_set.filter(updated_at__isnull=False).latest('updated_at')])
    except ObjectDoesNotExist:
        data = "[]"
    return HttpResponse(data) 
def env_filter_earliest(request):
    from django.core import serializers
    from django.db.models.base import ObjectDoesNotExist
    mac = request.session['mac']
    try:
        data = serializers.serialize('json',[models.device_info.objects.get(mac=mac).env_info_set.filter(updated_at__isnull=False).earliest('updated_at')])
    except ObjectDoesNotExist:
        data = "[]"
    return HttpResponse(data) 

@csrf_exempt
def env_filter_chart_search(request):
     if request.method == 'POST':
        try:
            Data_POST = request.POST
            Data_POST = json.dumps(Data_POST)
            Data_POST = json.loads(Data_POST)
        except Data_POST.DoesNotExist:
            Data_POST = None
        finally:
            if Data_POST.get('type') == "offset":
                request.session['type'] = Data_POST.get('type')
                request.session['offset'] = Data_POST.get('offset')
            else:
                request.session['type'] = Data_POST.get('type')
                request.session['begintime'] = Data_POST.get('date1')
                request.session['endtime'] = Data_POST.get('date2')
        return HttpResponse(1)
    
def env_filter_chart(request):
    from django.core import serializers
    from datetime import datetime, timedelta, time
    from django.utils import timezone
    mac = request.session['mac']
    type = request.session['type']
    if type == 'offset':
        offset = request.session['offset']
        current = datetime.now()
        past = current - timedelta(hours=int(offset))
        current = timezone.make_aware(current,timezone.get_current_timezone())
        past = timezone.make_aware(past,timezone.get_current_timezone()) #轉換時區
        data = serializers.serialize('json',models.device_info.objects.get(mac=mac).env_info_set.filter(updated_at__lte=current,updated_at__gte=past).order_by('updated_at'))
        #print(offset)
        return HttpResponse(data)
    else:
        begintime = request.session['begintime']
        endtime = request.session['endtime']
        data = serializers.serialize('json',models.device_info.objects.get(mac=mac).env_info_set.filter(updated_at__lte=endtime,updated_at__gte=begintime).order_by('updated_at'))
        return HttpResponse(data) 
@csrf_exempt
def del_device_data(request):
    mac = request.session['mac']
    if request.method == 'POST':
        Data_POST = request.POST
        Data_POST = json.dumps(Data_POST)
        Data_POST = json.loads(Data_POST)
        if Data_POST.get('Delete') == "confrim":
            models.device_info.objects.get(mac=mac).delete()
            return JsonResponse({"status": 200, "msg": "deleted!"  })

@csrf_exempt
def post_device_form(request):
    mac = request.session['mac']
    if request.method == 'POST':
        Data_POST = request.POST
        Data_POST = json.dumps(Data_POST)
        Data_POST = json.loads(Data_POST)
        info = models.device_info.objects.get(mac=mac)
        info.device_name = Data_POST.get('Locationname')
        info.save()
        text = " Update Successfully"
        return JsonResponse({"status": 200, "msg": text  })

def pet_get_id(request):
    try:
        Tag = request.GET.get('Tag')
    except Tag.DoesNotExist:
        Tag = None
    finally:
        request.session['Tag'] = Tag
    return HttpResponse(Tag)

def Tag_list(request):
    from django.core import serializers
    data = serializers.serialize('json',models.Tag_Info.objects.all())
    return HttpResponse(data) 


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
    data = serializers.serialize('json',models.Tag_Info.objects.get(Tag=Tag).pet_info_set.filter(updated_at__lte=today_end,updated_at__gte=today_start).order_by('updated_at'))
    return HttpResponse(data) 

def pet_filter_latest(request):
    from django.core import serializers
    from django.db.models.base import ObjectDoesNotExist
    Tag = request.session['Tag']
    try:
        data = serializers.serialize('json',[models.Tag_Info.objects.get(Tag=Tag).pet_info_set.filter(updated_at__isnull=False).latest('updated_at')])
    except ObjectDoesNotExist:
        data = "[]"
    return HttpResponse(data) 
def pet_filter_earliest(request):
    from django.core import serializers
    from django.db.models.base import ObjectDoesNotExist
    Tag = request.session['Tag']
    try:
        data = serializers.serialize('json',[models.Tag_Info.objects.get(Tag=Tag).pet_info_set.filter(updated_at__isnull=False).earliest('updated_at')])
    except ObjectDoesNotExist:
        data = "[]"
    return HttpResponse(data) 
@csrf_exempt
def pet_filter_chart_search(request):
     if request.method == 'POST':
        try:
            Data_POST = request.POST
            Data_POST = json.dumps(Data_POST)
            Data_POST = json.loads(Data_POST)
        except Data_POST.DoesNotExist:
            Data_POST = None
        finally:
            if Data_POST.get('type') == "offset":
                request.session['type1'] = Data_POST.get('type')
                request.session['offset1'] = Data_POST.get('offset')
            else:
                request.session['type1'] = Data_POST.get('type')
                request.session['begintime1'] = Data_POST.get('date1')
                request.session['endtime1'] = Data_POST.get('date2')
        return HttpResponse(1)
    
def pet_filter_chart(request):
    from django.core import serializers
    from datetime import datetime, timedelta, time
    from django.utils import timezone
    Tag = request.session['Tag']
    type = request.session['type1']
    if type == 'offset':
        offset = request.session['offset1']
        current = datetime.now()
        past = current - timedelta(hours=int(offset))
        current = timezone.make_aware(current,timezone.get_current_timezone())
        past = timezone.make_aware(past,timezone.get_current_timezone()) #轉換時區
        data = serializers.serialize('json',models.Tag_Info.objects.get(Tag=Tag).pet_info_set.filter(updated_at__lte=current,updated_at__gte=past).order_by('updated_at'))
        #print(data)
        return HttpResponse(data)
    else:
        begintime = request.session['begintime1']
        endtime = request.session['endtime1']
        data = serializers.serialize('json',models.Tag_Info.objects.get(Tag=Tag).pet_info_set.filter(updated_at__lte=endtime,updated_at__gte=begintime).order_by('updated_at'))
        #print(data)
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
            data = serializers.serialize('json',models.food_type.objects.filter(pk=Value))
            return HttpResponse(data)
        if Object == "mac" :
            data = serializers.serialize('json',models.food_type.objects.filter(mac=Value))
            return HttpResponse(data)

def list_foodType(request):
    from django.core import serializers
    data = serializers.serialize('json',models.food_type.objects.all())
    return HttpResponse(data)


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
        Data_POST4 = request.POST.getlist('select1[]')
        if len(Data_POST1) == len(Data_POST2) and len(Data_POST2) == len(Data_POST3) and len(Data_POST1) == len(Data_POST4):
            for i in range(len(Data_POST4)):
                 if Data_POST4[i] == "":
                     return HttpResponse("BindDevice(Name/MAC) is required")
            for i in range(len(Data_POST2)):
                food_type_pk = list(models.food_type.objects.filter(Name=Data_POST3[i]).values_list('pk',flat=True)) #實際輸出['1','2',…] 用python List轉換成[1,2,...]
                mac_pk = list(models.device_info.objects.filter(mac=Data_POST4[i]).values_list('pk',flat=True)) #實際輸出['1','2',…] 用python List轉換成[1,2,...]
                if Data_POST1[i] != "" and Data_POST2[i] != "" and Data_POST3[i] != "":
                    temp = models.Schedule.objects.filter(Tag_id=pk[0],mac_id=mac_pk[0],schedule_time=datetime.strptime(Data_POST1[i], '%H:%M').time())
                    if temp.exists():
                        info = models.Schedule.objects.get(Tag_id=pk[0],mac_id=mac_pk[0],schedule_time=datetime.strptime(Data_POST1[i], '%H:%M'))               
                        info.food_Name_id = food_type_pk[0]
                        info.food_amount = Data_POST2[i]
                        info.save()
                    else:
                        info = models.Schedule.objects.create(Tag_id=pk[0],food_Name_id=food_type_pk[0],mac_id=mac_pk[0])
                        info.schedule_time = datetime.strptime(Data_POST1[i],'%H:%M').time()
                        info.food_amount = Data_POST2[i]
                        info.save()
                else:
                    return HttpResponse("Time,Amount and FoodType is required")
            return HttpResponse()



@csrf_exempt
def add_foodType(request):
    if request.method == 'POST':
        Data_POST1 = request.POST.getlist('Name[]')
        Data_POST2 = request.POST.getlist('kCal[]')
        Data_POST3 = request.POST.getlist('select1[]')

        if len(Data_POST1) == len(Data_POST2) == len(Data_POST3):
            for i in range(len(Data_POST3)):
                if  Data_POST3[i] == "":
                    return HttpResponse("DeviceName is required") 
            for i in range(len(Data_POST2)):
                if Data_POST1[i] != "" and Data_POST2[i] != "":
                    pk = list(models.device_info.objects.filter(mac=Data_POST3[i]).values_list('pk',flat=True)) #實際輸出['1','2',…] 用python List轉換成[1,2,...]
                    temp = models.food_type.objects.filter(Name=Data_POST1[i])
                    if temp.exists():
                        None
                    else:
                        Name = models.food_type.objects.create(Name=Data_POST1[i],mac_id=pk[0])
                        Name.save()     
                    temp.update(kCal=Data_POST2[i])
                    return HttpResponse() 
                else:
                    return HttpResponse("Name and kCal(per 100g) is required") 
            

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

@csrf_exempt
def pet_pannel(request):
    from django.core import serializers
    from datetime import datetime, timedelta, time
    from django.utils import timezone
    if request.method == 'POST':
        Data_POST = request.POST
        Data_POST = json.dumps(Data_POST)
        Data_POST = json.loads(Data_POST)
        TAG = Data_POST.get('TAG')
        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        today_start = timezone.make_aware(datetime.combine(today, time()))
        today_end = timezone.make_aware(datetime.combine(tomorrow, time())) #轉換時區
        data = serializers.serialize('json',models.Tag_Info.objects.get(Tag=TAG).pet_info_set.filter(updated_at__lte=today_end,updated_at__gte=today_start).order_by('updated_at'))
        return HttpResponse(data) 

@csrf_exempt
def pet_filter_latest1(request):
    from django.core import serializers
    from django.db.models.base import ObjectDoesNotExist
    if request.method == 'POST':
        Data_POST = request.POST
        Data_POST = json.dumps(Data_POST)
        Data_POST = json.loads(Data_POST)
        TAG = Data_POST.get('TAG')
        try:
            data = serializers.serialize('json',[models.Tag_Info.objects.get(Tag=TAG).pet_info_set.filter(updated_at__isnull=False).latest('updated_at')])
        except ObjectDoesNotExist:
            data = "[]"
        return HttpResponse(data) 
@csrf_exempt
def device_filter_latest1(request):
    from django.core import serializers
    from django.db.models.base import ObjectDoesNotExist
    if request.method == 'POST':
        Data_POST = request.POST
        Data_POST = json.dumps(Data_POST)
        Data_POST = json.loads(Data_POST)
        mac = Data_POST.get('mac')
        try:
            data = serializers.serialize('json',[models.device_info.objects.get(mac=mac).env_info_set.filter(updated_at__isnull=False).latest('updated_at')])
        except ObjectDoesNotExist:
            data = "[]"
        return HttpResponse(data) 
@csrf_exempt
def device_serach(request):
    from django.core import serializers
    from django.db.models.base import ObjectDoesNotExist
    if request.method == 'POST':
        Data_POST = request.POST
        Data_POST = json.dumps(Data_POST)
        Data_POST = json.loads(Data_POST)
        mac = Data_POST.get('mac')
        try:
            data = serializers.serialize('json',[models.device_info.objects.get(pk=mac)])
        except ObjectDoesNotExist:
            data = "[]"
        return HttpResponse(data) 

@csrf_exempt
def data_upload(request):
    if request.method == 'POST': 
        Data_POST = json.loads(request.body.decode("utf-8"))
        DATA = Data_POST.get('DATA')
        MAC = "%s:%s:%s:%s:%s:%s" % (DATA[1:3], DATA[3:5], DATA[5:7], DATA[7:9], DATA[9:11], DATA[11:13])
        Mac = list(models.device_info.objects.filter(mac=MAC).values_list('pk',flat=True)) #實際輸出['1','2',…] 用python List轉換成[1,2,...]
        #print(MAC)
        mac = models.device_info.objects.filter(mac=MAC)
        if mac.exists():
            text1 = "Mac Existing"
            #return JsonResponse({"status": 200, "msg": "Tag Existing" })
        else:
            mac = models.device_info.objects.create(mac=MAC)
            mac.save()
            text1 = "Create New Mac"
        if DATA[0] == "P":
            Tag = models.Tag_Info.objects.filter(Tag=DATA[22:30])
            if Tag.exists():
                text2 = "Tag Existing"
                #return JsonResponse({"status": 200, "msg": "Tag Existing" })
            else:
                TAG = models.Tag_Info.objects.create(Tag=DATA[22:30])
                TAG.save()
                text2 = "Create New Tag"
            pk = list(Tag.values_list('pk',flat=True)) #實際輸出['1','2',…] 用python List轉換成[1,2,...]
            info = models.pet_info.objects.create(Tag_id=pk[0],mac_id=Mac[0])
            info.food_eat = float('%s.%s' % (DATA[30:33], DATA[33:35]))
            info.water_drink = float('%s.%s' % (DATA[35:38], DATA[38:41]))
            datetime_temp = str(datetime(2000, 1, 1, 12, 0) + timedelta(seconds=int(DATA[13:22])) - timedelta(days=1)) + " +0800"
            info.updated_at = datetime.strptime(datetime_temp,"%Y-%m-%d %H:%M:%S %z")
            info.save()
            return JsonResponse({"status": 200, "msg": text2 + " and " + "Successful Save!"})
        if DATA[0] == "E":
            info = models.env_info.objects.create(mac_id=Mac[0])
            info.temperature = float('%s.%s' % (DATA[22:25], DATA[25:27]))
            info.humidity = float('%s.%s' % (DATA[27:30], DATA[30:32]))
            datetime_temp = str(datetime(2000, 1, 1, 12, 0) + timedelta(seconds=int(DATA[13:22])) - timedelta(days=1)) + " +0800"
            info.updated_at = datetime.strptime(datetime_temp,"%Y-%m-%d %H:%M:%S %z")
            info.save()
            return JsonResponse({"status": 200, "msg": text1 + " and " + "Successful Save!"})
        return JsonResponse({"status": 200, "msg": text1 })
    else:
        return JsonResponse({"status": 400, "msg": "It is GET" })

def schedule_list(request):
    from django.core import serializers
    temp = []
    data = serializers.serialize('json',models.Schedule.objects.all().order_by('mac','schedule_time','Tag'),use_natural_foreign_keys=True, use_natural_primary_keys=True)
    data = json.loads(data)
    for di in data:
        del di['fields']['food_Name'] #移除food_Name
        temp.append(di['fields'])
    return HttpResponse(json.dumps(temp)) 

def device_list(request):
    from django.core import serializers
    data = list(models.device_info.objects.values('mac').distinct())
    temp = []
    for di in data:
        temp.append(di['mac'])
    #data = serializers.serialize('json',temp)
    return HttpResponse(json.dumps(temp)) 