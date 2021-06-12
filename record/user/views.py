from django.shortcuts import render, redirect
from . import models 
from .forms import UserForm, RegisterForm, EditForm, EditForm2, QueryuserForm
import hashlib

# Create your views here.
def index(request):
    if request.session.get('is_login'):
        user = models.User.objects.get(username=request.session.get('user_name'))
    return render(request,'mainpage.html', locals())

def self(request):
    if request.session.get('is_login'):
        user = models.User.objects.get(username=request.session.get('user_name'))
        return render(request, "selfpage.html", locals())
    return redirect('/')

def detailuser(request):
    if request.session.get('is_admin'):
        user = models.User.objects.get(username=request.GET.get('username'))
        return render(request, "detailuser.html", locals())
    return redirect('/')

def editself(request):
    if not request.session.get('is_login', None): # 本来就未登录
        return redirect("/")
    user = models.User.objects.get(username=request.session.get('user_name'))
    edit_form = EditForm(initial={"username":user.username, "name":user.name, "sex":user.sex,
                             "birthday":user.birthday, "email":user.email, "tel":user.tel})
    if request.method == "POST":
        e_form = EditForm(request.POST)
        if e_form.is_valid():
            username = e_form.cleaned_data['username']
            name = e_form.cleaned_data['name']
            if e_form.cleaned_data['sex']:
                sex = e_form.cleaned_data['sex']
            else:
                sex = None
            if e_form.cleaned_data['birthday']:
                birthday = e_form.cleaned_data['birthday']
            else:
                birthday = None
            if e_form.cleaned_data['email']:
                email = e_form.cleaned_data['email']
            else:
                email = None
            tel = e_form.cleaned_data['tel']

            if username != user.username:
                check = models.User.objects.filter(username=username)
                if check: 
                    message = "用户名已经存在，请重新选择用户名！"
                    return render(request, 'editself.html', locals())
                models.User.objects.filter(username=user.username).update(username=username)
                request.session['user_name'] = username  #很重要
                message = "已成功修改用户名"
            
            if name != user.name:
                models.User.objects.filter(username=username).update(name=name)
            if sex != user.sex:
                models.User.objects.filter(username=username).update(sex=sex)
            if birthday != user.birthday:
                models.User.objects.filter(username=username).update(birthday=birthday)
            if email != user.email:
                models.User.objects.filter(username=username).update(email=email)
            if tel != user.tel:
                models.User.objects.filter(username=username).update(tel=tel)
            
            message = "已成功修改个人信息"
            return redirect('/self/')  # 自动跳转到个人主页
    return render(request, "editself.html", locals())

def editpassword(request):
    if not request.session.get('is_login', None): # 本来就未登录
        return redirect("/index/")
    user = models.User.objects.get(username=request.session.get('user_name'))
    edit_form = EditForm2()
    if request.method == "POST":
        e_form = EditForm2(request.POST)
        if e_form.is_valid():
            password = e_form.cleaned_data['password']
            password1 = e_form.cleaned_data['password1']
            password2 = e_form.cleaned_data['password2']

            md5 = hashlib.md5()
            md5.update(password.encode())
            password_md5 = md5.hexdigest()

            if password_md5 != user.password:
                message = "原密码输入错误！"
                return render(request, "editpassword.html", locals())

            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, "editpassword.html", locals())

            md5 = hashlib.md5()
            md5.update(password1.encode())
            password_md5 = md5.hexdigest()
            models.User.objects.filter(username=user.username).update(password=password_md5)
            message = "已成功修改密码"
            
            return redirect('/self/')  # 自动跳转到个人主页
    return render(request, "editpassword.html", locals())

def login(request):
    if request.session.get('is_login', None):  #不重复登录
        return redirect('/')
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            md5 = hashlib.md5()
            md5.update(password.encode())
            password_md5 = md5.hexdigest()
            try:
                user = models.User.objects.get(username=username)
                if user.password == password_md5: 
                    request.session['is_login'] = True
                    request.session['user_name'] = user.username
                    if user.username=="brayton":
                        request.session['is_admin'] = True
                    else:
                        request.session['is_admin'] = False
                    return redirect('/index/') 
                else:
                    message = "密码不正确！"
            except:
                message = "用户名不存在！"
        return render(request, './admin.html', locals())
    login_form = UserForm() 
    return render(request,'admin.html', locals())

def register(request):
    if request.session.get('is_login', None): # 登录状态不允许注册
        return redirect("/")
    register_form = RegisterForm()
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            name = register_form.cleaned_data['name']
            if register_form.cleaned_data['sex']:
                sex = register_form.cleaned_data['sex']
            else:
                sex = None
            if register_form.cleaned_data['birthday']:
                birthday = register_form.cleaned_data['birthday']
            else:
                birthday = None
            if register_form.cleaned_data['email']:
                email = register_form.cleaned_data['email']
            else:
                email = None
            tel = register_form.cleaned_data['tel']
            
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'registration.html', locals())
            else:
                check = models.User.objects.filter(username=username)
                if check: 
                    message = '用户名已经存在，请重新选择用户名！'
                    return render(request, 'registration.html', locals())
                
                md5 = hashlib.md5()
                md5.update(password1.encode())
                password_md5 = md5.hexdigest()

                models.User.objects.create(username=username, password = password_md5, 
                    name = name, sex = sex, birthday = birthday, email = email, tel = tel)
                return redirect('/login/')  # 自动跳转到登录页面
        else:
            message = "请检查填写的内容"
    return render(request, 'registration.html', locals())

def logout(request):
    if not request.session.get('is_login', None): # 本来就未登录
        return redirect("/")
    request.session.flush() #清除登入的数据
    return redirect("/")

def queryuser(request):
    if request.session.get('is_admin')==False: # 用户不允许使用此功能
        return redirect("/")
    query_form = QueryuserForm(locals())
    user_list = models.User.objects.all()
    if request.method == "POST":
        query_form = QueryuserForm(request.POST)
        if query_form.is_valid():  # 获取数据
            if query_form.cleaned_data['username']:
                user_list = user_list.filter(username=query_form.cleaned_data['username'])
            if query_form.cleaned_data['name']:
                user_list = user_list.filter(name=query_form.cleaned_data['name'])
            if query_form.cleaned_data['email']:
                user_list = user_list.filter(email=query_form.cleaned_data['email'])
            if query_form.cleaned_data['tel']:
                user_list = user_list.filter(tel=query_form.cleaned_data['tel'])
    return render(request, 'queryuser.html', locals())