from django.shortcuts import render, redirect
from . import model
from cd import models
from .forms import PreorderForm, OrderForm, TimeForm
from django.utils import timezone
from django.db.models import Sum
from django.db import connection
from itertools import chain

# Create your views here.
def preordercd(request):
    if request.session.get('is_admin'):
        if request.method == "GET":
            request.session['id'] = request.GET.get('id')
            cd = models.cd.objects.get(id = request.session.get('id'))
            preform = PreorderForm()
            return render(request, "preordercd.html", locals())
        if request.method == "POST":
            preform = PreorderForm(request.POST)
            id_ = request.session.get('id')
            cd = models.cd.objects.get(id = id_)
            if preform.is_valid():
                amount = preform.cleaned_data['amount']
                model.orderlist.objects.create(status="未付款", mark=True, cd=True, amount=amount, tar=id_, cost=cd.cost, name=cd.name, produce_area=cd.produce_area)
                return redirect('/orderlist')  # 自动跳转到订单列表
            message = "请检查填写的内容！"
            return render(request, "preordercd.html", {'cd':cd})  # 自动跳转到唱片编辑页面
    return redirect('/')

def preordervinyl(request):
    if request.session.get('is_admin'):
        if request.method == "GET":
            request.session['id'] = request.GET.get('id')
            vinyl = models.vinyl.objects.get(id = request.session.get('id'))
            preform = PreorderForm()
            return render(request, "preordervinyl.html", locals())
        if request.method == "POST":
            preform = PreorderForm(request.POST)
            id_ = request.session.get('id')
            vinyl = models.vinyl.objects.get(id = id_)
            if preform.is_valid():
                amount = preform.cleaned_data['amount']
                model.orderlist.objects.create(status="未付款", mark=True, cd=False, amount=amount, tar=id_, cost=vinyl.cost, name=vinyl.name, produce_area=vinyl.produce_area)
                return redirect('/orderlist')  # 自动跳转到订单列表
            message = "请检查填写的内容！"
            return render(request, "preordervinyl.html", {'vinyl':vinyl})  # 自动跳转到唱片编辑页面
    return redirect('/')

def buycd(request):
    if request.session.get('is_login') and request.session.get('is_admin')==False:
        if request.method == "GET":
            request.session['id'] = request.GET.get('id')
            cd = models.cd.objects.get(id = request.session.get('id'))
            buyform = PreorderForm()
            return render(request, "buycd.html", locals())
        if request.method == "POST":
            buyform = PreorderForm(request.POST)
            id_ = request.session.get('id')
            cd = models.cd.objects.get(id = id_)
            if buyform.is_valid():
                amount = buyform.cleaned_data['amount']
                if amount>cd.remain:
                    message = "库存不足！"
                    return render(request, "buycd.html", locals())  # 自动跳转到唱片编辑页面
                if amount<=0:
                    message = "购买数量必须大于0！"
                    return render(request, "buycd.html", locals())  # 自动跳转到唱片编辑页面
                total = amount*cd.cost
                model.userorder.objects.create(cd=True, amount=amount, tar=id_, cost=cd.cost, total=total, username=request.session.get('user_name'))
                remain = cd.remain
                models.cd.objects.filter(id=id_).update(remain=remain-amount)
                return redirect('/userorder')  # 自动跳转到订单列表
            message = "请检查填写的内容！"
            return render(request, "buycd.html", {'cd':cd})  # 自动跳转到唱片编辑页面
    return redirect('/')

def buyvinyl(request):
    if request.session.get('is_login') and request.session.get('is_admin')==False:
        if request.method == "GET":
            request.session['id'] = request.GET.get('id')
            vinyl = models.vinyl.objects.get(id = request.session.get('id'))
            buyform = PreorderForm()
            return render(request, "buyvinyl.html", locals())
        if request.method == "POST":
            buyform = PreorderForm(request.POST)
            id_ = request.session.get('id')
            vinyl = models.vinyl.objects.get(id = id_)
            if buyform.is_valid():
                amount = buyform.cleaned_data['amount']
                if amount>vinyl.remain:
                    message = "库存不足！"
                    return render(request, "buyvinyl.html", locals())  # 自动跳转到唱片编辑页面
                if amount<=0:
                    message = "购买数量必须大于0！"
                    return render(request, "buyvinyl.html", locals())  # 自动跳转到唱片编辑页面
                total = amount*vinyl.cost
                model.userorder.objects.create(cd=False, amount=amount, tar=id_, cost=vinyl.cost, total=total, username=request.session.get('user_name'))
                remain = vinyl.remain
                models.vinyl.objects.filter(id=id_).update(remain=remain-amount)
                return redirect('/userorder')  # 自动跳转到订单列表
            message = "请检查填写的内容！"
            return render(request, "buyvinyl.html", {'vinyl':vinyl})  # 自动跳转到唱片编辑页面
    return redirect('/')

def orderlist(request):
    if request.session.get('is_admin')==False: # 店长才允许使用此功能
        return redirect("/")
    form = OrderForm()
    orderlist = model.orderlist.objects.all()
    ol = model.orderlist.objects.filter(status='已付款')
    money = 0.0
    for o in ol:
        money = money + o.cost * o.amount
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():  # 获取数据
            if form.cleaned_data['status']:
                orderlist = orderlist.filter(status=form.cleaned_data['status'])
            if form.cleaned_data['name']:
                orderlist = orderlist.filter(name=form.cleaned_data['name'])
            orderlist = orderlist.filter(cd=form.cleaned_data['cd'])
            ol = orderlist.filter(status='已付款')
            money = 0.0
            for o in ol:
                money = money + o.cost * o.amount
    return render(request, "orderlist.html", locals())

def pay(request):
    if request.session.get('is_admin')==False:
        return redirect("/")
    id = request.GET.get('id')
    model.orderlist.objects.filter(id=id).update(status="已付款")
    model.orderlist.objects.filter(id=id).update(mark=False)
    model.orderlist.objects.filter(id=id).update(time=timezone.now())
    temp = model.orderlist.objects.get(id=id)
    if temp.cd:
        cd = models.cd.objects.get(id=temp.tar)
        models.cd.objects.filter(id=temp.tar).update(remain=cd.remain+temp.amount)
    else:
        vinyl = models.vinyl.objects.get(id=temp.tar)
        models.vinyl.objects.filter(id=temp.tar).update(remain=vinyl.remain+temp.amount)
    return redirect("/orderlist")

def cancel(request):
    if request.session.get('is_admin')==False:
        return redirect("/")
    id = request.GET.get('id')
    model.orderlist.objects.filter(id=id).update(status="已取消")
    model.orderlist.objects.filter(id=id).update(mark=False)
    model.orderlist.objects.filter(id=id).update(time=timezone.now())
    return redirect("/orderlist")

def userorder(request):
    if request.session.get('is_login'):
        if request.session.get('is_admin'):
            orderlist = model.userorder.objects.all()
            timeform = TimeForm(initial={'start':'2021-06-08', 'end':'2021-'})
            income = orderlist.aggregate(Sum('total'))['total__sum']
            if request.method=='POST':
                timeform = TimeForm(request.POST)
                if timeform.is_valid():
                    start = timeform.cleaned_data['start']
                    end = timeform.cleaned_data['end']
                    orderlist = orderlist.filter(time__date__gte=start)
                    orderlist = orderlist.filter(time__date__lte=end)
                    income = orderlist.aggregate(Sum('total'))['total__sum']
        else:
            orderlist = model.userorder.objects.filter(username=request.session.get('user_name'))
            timeform = TimeForm(initial={'start':'2021-06-08', 'end':'2021-'})
            money = orderlist.aggregate(Sum('total'))['total__sum']
            if request.method=='POST':
                timeform = TimeForm(request.POST)
                if timeform.is_valid():
                    start = timeform.cleaned_data['start']
                    end = timeform.cleaned_data['end']
                    orderlist = orderlist.filter(time__date__gte=start)
                    orderlist = orderlist.filter(time__date__lte=end)
                    money = orderlist.aggregate(Sum('total'))['total__sum']
        return render(request, "userorder.html", locals())
    return redirect('/')

def top10(request):
    if request.session.get('is_login'):
        cursor=connection.cursor()
        cursor.execute("select sum(amount), name, artist, cd, produce_area, tar from cd_cd join list_userorder on cd_cd.id=tar where cd=True group by name, cd, artist, produce_area, tar")
        r1 = cursor.fetchall()
        cursor=connection.cursor()
        cursor.execute("select sum(amount), name, artist, cd, produce_area, tar from cd_vinyl join list_userorder on cd_vinyl.id=tar where cd=False group by name, cd, artist, produce_area, tar")
        r2 = cursor.fetchall()
        ranklist = chain(r1, r2)
        ranklist = sorted(ranklist, reverse=True)
        ranklist = ranklist[0:10]
        return render(request, "top10.html", {'ranklist':ranklist})
    return redirect('/')
