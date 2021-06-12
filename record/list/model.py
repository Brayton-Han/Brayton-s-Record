from django.db import models

# Create your models here.
class orderlist(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    time = models.DateTimeField(auto_now_add=True, null=False)
    status = models.CharField(null=False, max_length=5)
    mark = models.BooleanField(null=False)
    cd = models.BooleanField(null=False)
    amount = models.IntegerField(null=False)
    cost = models.FloatField(null=False)
    tar = models.IntegerField(null=False)
    name = models.CharField(null=False, max_length=128)
    produce_area = models.CharField(null=False, max_length=128)

    class Meta:
        ordering = ['time']   #默认按照创建时间排序
        verbose_name = '订单' 

class userorder(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    time = models.DateTimeField(auto_now_add=True, null=False)
    cd = models.BooleanField(null=False)
    amount = models.IntegerField(null=False)
    cost = models.FloatField(null=False)
    total = models.FloatField(null=False)
    tar = models.IntegerField(null=False)
    username = models.CharField(max_length=128, null=False)

    class Meta:
        ordering = ['time']   #默认按照创建时间排序
        verbose_name = '订单' 