from django.db import models

# Create your models here.
class User(models.Model):
    '''用户表''' 
    gender = (
        ('', "不选"),
        ('male','男'),
        ('female','女'),
        ('others', '其他'),
    )
    username = models.CharField(max_length=128, primary_key=True, null=False)
    password = models.CharField(max_length=256, null=False)
    name = models.CharField(max_length=128, null=False)
    sex = models.CharField(max_length=32, choices=gender)
    birthday = models.DateField(null=True, blank=True)
    email = models.EmailField(max_length=128, null=True, blank=True)
    tel = models.CharField(max_length=15, null=False)
    def __str__(self):   #人性化显示对象信息
        return self.name
    class Meta:
        ordering = ['username']   #默认按照用户名排序
        verbose_name = '用户' 
        verbose_name_plural = '用户'