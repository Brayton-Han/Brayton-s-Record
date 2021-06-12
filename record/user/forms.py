from django import forms 
from captcha.fields import CaptchaField

class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128)
    password = forms.CharField(label="密码", max_length=256)
    #captcha = CaptchaField(label='验证码')

class RegisterForm(forms.Form):
    gender = (
        (None, "不选"),
        ('male', "男"),
        ('female', "女"),
        ('others', "其他"),
    )
    username = forms.CharField(label="*用户名", max_length=128)
    password1 = forms.CharField(label="*密码", max_length=256)
    password2 = forms.CharField(label="*再次输入密码", max_length=256)
    name = forms.CharField(label="*姓名", max_length=128)
    sex = forms.ChoiceField(label="性别", choices=gender, required=False)
    birthday = forms.DateField(label="出生日期", help_text="格式：year-month-day", required=False)
    email = forms.EmailField(label="邮箱地址", max_length=128, required=False)
    tel = forms.CharField(label="*电话号码", max_length=15)
    captcha = CaptchaField(label='验证码')

class EditForm(forms.Form):
    gender = (
        (None, "不选"),
        ('male', "男"),
        ('female', "女"),
        ('others', "其他"),
    )
    username = forms.CharField(label="*用户名", max_length=128)
    name = forms.CharField(label="*姓名", max_length=128)
    sex = forms.ChoiceField(label="性别", choices=gender, required=False)
    birthday = forms.DateField(label="出生日期", help_text="格式：year-month-day", required=False)
    email = forms.EmailField(label="邮箱地址", max_length=128, required=False)
    tel = forms.CharField(label="*电话号码", max_length=15)

class EditForm2(forms.Form):
    password = forms.CharField(label="旧密码", max_length=256)
    password1 = forms.CharField(label="新密码", max_length=256)
    password2 = forms.CharField(label="再次输入密码", max_length=256)

class QueryuserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, required=False)
    name = forms.CharField(label="姓名", max_length=128, required=False)
    email = forms.EmailField(label="邮箱地址", max_length=128, required=False)
    tel = forms.CharField(label="电话号码", max_length=15, required=False)