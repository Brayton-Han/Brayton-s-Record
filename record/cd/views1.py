from django.shortcuts import render, redirect
from . import models 
from .forms import QuerycdForm, QueryvinylForm, EditcdForm, EditvinylForm

# Create your views here.

def querycd(request):
    if request.session.get('is_login')==False: # 未登录时不允许使用此功能
        return redirect("/")
    query_form = QuerycdForm(initial={"explicit":True})
    cd_list = models.cd.objects.all()
    if request.method == "POST":
        query_form = QuerycdForm(request.POST)
        if query_form.is_valid():  # 获取数据
            if query_form.cleaned_data['name']:
                cd_list = cd_list.filter(name=query_form.cleaned_data['name'])
            if query_form.cleaned_data['artist']:
                cd_list = cd_list.filter(artist=query_form.cleaned_data['artist'])
            cd_list = cd_list.filter(explicit=query_form.cleaned_data['explicit'])
            cd_list = cd_list.filter(seal_off=query_form.cleaned_data['seal_off'])
    return render(request, "querycd.html", locals())

def queryvinyl(request):
    if request.session.get('is_login')==False: # 未登录时不允许使用此功能
        return redirect("/")
    query_form = QueryvinylForm(locals())
    vinyl_list = models.vinyl.objects.all()
    if request.method == "POST":
        query_form = QueryvinylForm(request.POST)
        if query_form.is_valid():  # 获取数据
            if query_form.cleaned_data['name']:
                vinyl_list = vinyl_list.filter(name=query_form.cleaned_data['name'])
            if query_form.cleaned_data['artist']:
                vinyl_list = vinyl_list.filter(artist=query_form.cleaned_data['artist'])
            vinyl_list = vinyl_list.filter(second_hand=query_form.cleaned_data['second_hand'])
    return render(request, "queryvinyl.html", locals())

def detailcd(request):
    if request.session.get('is_login'):
        if request.GET.get('id'):
            cd = models.cd.objects.get(id = request.GET.get('id'))
            return render(request, "detailcd.html", locals())
        cd = models.cd.objects.get(id = request.session.get('id'))
        return render(request, "detailcd.html", locals())
    return redirect('/')

def detailvinyl(request):
    if request.session.get('is_login'):
        if request.GET.get('id'):
            vinyl = models.vinyl.objects.get(id = request.GET.get('id'))
            return render(request, "detailvinyl.html", locals())
        vinyl = models.vinyl.objects.get(id = request.session.get('id'))
        return render(request, "detailvinyl.html", locals())
    return redirect('/')

def editcd(request):
    if request.session.get('is_admin'):
        if request.method == "GET":
            request.session['id'] = request.GET.get('id')
            cd = models.cd.objects.get(id = request.session.get('id'))
            edit_form = EditcdForm(initial={"barcode":cd.barcode, "name":cd.name, 
            "artist":cd.artist, "number":cd.number, "genre":cd.genre,
            "produce_area":cd.produce_area, "price":cd.price, "cost":cd.cost,
            "seal_off":cd.seal_off, "explicit":cd.explicit, "remain":cd.remain})
            return render(request, "editcd.html", locals())
        if request.method == "POST":
            edit_form = EditcdForm(request.POST)
            id_ = request.session.get('id')
            cd = models.cd.objects.get(id = id_)
            if edit_form.is_valid():
                barcode = edit_form.cleaned_data['barcode']
                name = edit_form.cleaned_data['name']
                if edit_form.cleaned_data['artist']:
                    artist = edit_form.cleaned_data['artist']
                else:
                    artist = None
                if edit_form.cleaned_data['number']:
                    number = edit_form.cleaned_data['number']
                else:
                    number = None
                if edit_form.cleaned_data['genre']:
                    genre = edit_form.cleaned_data['genre']
                else:
                    genre = None
                produce_area = edit_form.cleaned_data['produce_area']
                price = edit_form.cleaned_data['price']
                cost = edit_form.cleaned_data['cost']
                if edit_form.cleaned_data['seal_off']:
                    seal_off = edit_form.cleaned_data['seal_off']
                else:
                    seal_off = False
                if edit_form.cleaned_data['explicit']:
                    explicit = edit_form.cleaned_data['explicit']
                else:
                    explicit = False

                if barcode != cd.barcode:
                    check = models.cd.objects.filter(barcode=barcode, produce_area=produce_area, cost=cost)
                    if check: 
                        message = "唱片已经存在，请重新填写条形码！"
                        return render(request, 'editcd.html', locals())
                    models.cd.objects.filter(id=id_).update(barcode=barcode)
                if name != cd.name:
                    models.cd.objects.filter(id=id_).update(name=name)
                if artist != cd.artist:
                    models.cd.objects.filter(id=id_).update(artist=artist)
                if number != cd.number:
                    models.cd.objects.filter(id=id_).update(number=number)
                if genre != cd.genre:
                    models.cd.objects.filter(id=id_).update(genre=genre)
                if produce_area != cd.produce_area:
                    check = models.cd.objects.filter(barcode=barcode, produce_area=produce_area, cost=cost)
                    if check: 
                        message = "唱片已经存在，请重新填写生产地！"
                        return render(request, 'editcd.html', locals())
                    models.cd.objects.filter(id=id_).update(produce_area=produce_area)
                if price != cd.price:
                    models.cd.objects.filter(id=id_).update(price=price)
                if cost != cd.cost:
                    check = models.cd.objects.filter(barcode=barcode, produce_area=produce_area, cost=cost)
                    if check: 
                        message = "唱片已经存在，请重新填写进货价！"
                        return render(request, 'editcd.html', locals())
                    models.cd.objects.filter(id=id_).update(cost=cost)
                if seal_off != cd.seal_off:
                    models.cd.objects.filter(id=id_).update(seal_off=seal_off)
                if explicit != cd.explicit:
                    models.cd.objects.filter(id=id_).update(explicit=explicit)

                message = "已成功修改唱片信息"
                return redirect('/detailcd')  # 自动跳转到唱片详细页面
            message = "请检查填写的内容！"
            return render(request, "editcd.html", {'cd':cd})  # 自动跳转到唱片编辑页面
    return redirect('/')

def editvinyl(request):
    if request.session.get('is_admin'):
        if request.method == "GET":
            request.session['id'] = request.GET.get('id')
            vinyl = models.vinyl.objects.get(id = request.session.get('id'))
            edit_form = EditvinylForm(initial={"barcode":vinyl.barcode, "name":vinyl.name, 
            "artist":vinyl.artist, "number":vinyl.number, "genre":vinyl.genre,
            "produce_area":vinyl.produce_area, "price":vinyl.price, "cost":vinyl.cost,
            "second_hand":vinyl.second_hand, "remain":vinyl.remain})
            return render(request, "editvinyl.html", locals())
        if request.method == "POST":
            edit_form = EditvinylForm(request.POST)
            id_ = request.session.get('id')
            vinyl = models.vinyl.objects.get(id = id_)
            if edit_form.is_valid():
                barcode = edit_form.cleaned_data['barcode']
                name = edit_form.cleaned_data['name']
                if edit_form.cleaned_data['artist']:
                    artist = edit_form.cleaned_data['artist']
                else:
                    artist = None
                if edit_form.cleaned_data['number']:
                    number = edit_form.cleaned_data['number']
                else:
                    number = None
                if edit_form.cleaned_data['genre']:
                    genre = edit_form.cleaned_data['genre']
                else:
                    genre = None
                produce_area = edit_form.cleaned_data['produce_area']
                price = edit_form.cleaned_data['price']
                cost = edit_form.cleaned_data['cost']
                if edit_form.cleaned_data['second_hand']:
                    second_hand = edit_form.cleaned_data['second_hand']
                else:
                    second_hand = False
               
                if barcode != vinyl.barcode:
                    check = models.vinyl.objects.filter(barcode=barcode, produce_area=produce_area, cost=cost)
                    if check: 
                        message = "唱片已经存在，请重新填写条形码！"
                        return render(request, 'editvinyl.html', locals())
                    models.vinyl.objects.filter(id=id_).update(barcode=barcode)
                if name != vinyl.name:
                    models.vinyl.objects.filter(id=id_).update(name=name)
                if artist != vinyl.artist:
                    models.vinyl.objects.filter(id=id_).update(artist=artist)
                if number != vinyl.number:
                    models.vinyl.objects.filter(id=id_).update(number=number)
                if genre != vinyl.genre:
                    models.vinyl.objects.filter(id=id_).update(genre=genre)
                if produce_area != vinyl.produce_area:
                    check = models.vinyl.objects.filter(barcode=barcode, produce_area=produce_area, cost=cost)
                    if check: 
                        message = "唱片已经存在，请重新填写生产地！"
                        return render(request, 'editvinyl.html', locals())
                    models.vinyl.objects.filter(id=id_).update(produce_area=produce_area)
                if price != vinyl.price:
                    models.vinyl.objects.filter(id=id_).update(price=price)
                if cost != vinyl.cost:
                    check = models.vinyl.objects.filter(barcode=barcode, produce_area=produce_area, cost=cost)
                    if check: 
                        message = "唱片已经存在，请重新填写进货价！"
                        return render(request, 'editvinyl.html', locals())
                    models.vinyl.objects.filter(id=id_).update(cost=cost)
                if second_hand != vinyl.second_hand:
                    models.vinyl.objects.filter(id=id_).update(second_hand=second_hand)

                message = "已成功修改唱片信息"
                return redirect('/detailvinyl')  # 自动跳转到唱片详细页面
            message = "请检查填写的内容！"
            return render(request, "editvinyl.html", {'vinyl':vinyl})  # 自动跳转到唱片编辑页面
    return redirect('/')
