# Generated by Django 3.2.3 on 2021-06-09 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0005_orderlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='userorder',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('cd', models.BooleanField()),
                ('amount', models.IntegerField()),
                ('cost', models.FloatField()),
                ('tar', models.IntegerField()),
                ('username', models.CharField(max_length=128)),
            ],
            options={
                'verbose_name': '订单',
                'ordering': ['time'],
            },
        ),
    ]