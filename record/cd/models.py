from django.db import models

# Create your models here.
class cd(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    barcode = models.CharField(max_length=13, null=False)
    name = models.CharField(max_length=128, null=False)
    artist = models.CharField(max_length=128, null=True, blank=True)
    cover = models.ImageField(upload_to='img', null=False)
    number = models.IntegerField(null=True, blank=True)
    genre = models.CharField(max_length=128, null=True, blank=True)
    produce_area = models.CharField(max_length=128, null=False)
    price = models.FloatField(null=False, )
    cost = models.FloatField(null=False)
    seal_off = models.BooleanField(null=False)
    explicit = models.BooleanField(null=False)
    remain = models.IntegerField(null=False)
    
    def __str__(self):   #人性化显示对象信息
        return self.name

    class Meta:
        ordering = ['name']   #默认按照专辑名排序
        verbose_name = '专辑名' 
        verbose_name_plural = '专辑名'
        unique_together = (('barcode', 'produce_area', 'cost'))
        

class vinyl(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    barcode = models.CharField(max_length=13, null=False)
    name = models.CharField(max_length=128, null=False)
    artist = models.CharField(max_length=128, null=True, blank=True)
    cover = models.ImageField(upload_to='img', null=False)
    number = models.IntegerField(null=True, blank=True)
    genre = models.CharField(max_length=128, null=True, blank=True)
    produce_area = models.CharField(max_length=128, null=False)
    price = models.FloatField(null=False)
    cost = models.FloatField(null=False)
    second_hand = models.BooleanField(null=False)
    remain = models.IntegerField(null=False)
    
    def __str__(self):   #人性化显示对象信息
        return self.name

    class Meta:
        ordering = ['name']   #默认按照专辑名排序
        verbose_name = '专辑名' 
        verbose_name_plural = '专辑名'
        unique_together = (('barcode', 'produce_area', 'cost'))