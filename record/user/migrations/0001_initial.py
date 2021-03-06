# Generated by Django 3.2.3 on 2021-06-01 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=256)),
                ('name', models.CharField(max_length=128)),
                ('sex', models.CharField(choices=[('male', '男'), ('female', '女'), ('others', '其他')], max_length=32)),
                ('birthday', models.DateField()),
                ('email', models.EmailField(max_length=128)),
                ('tel', models.CharField(max_length=15)),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'ordering': ['username'],
            },
        ),
    ]
