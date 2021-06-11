"""record URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf.urls import url
from django.conf.urls.static import static
from record import settings
from django.urls import path
from user import views
from cd import views1
from list import views2
from django.urls import include
 
urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('login/', views.login),
    path('self/', views.self),
    path('editself/', views.editself),
    path('editpassword/', views.editpassword),
    path('register/', views.register),
    path('logout/', views.logout),
    path('queryuser/', views.queryuser),
    path('querycd/', views1.querycd),
    path('queryvinyl/', views1.queryvinyl),
    path('editcd/', views1.editcd),
    path('editvinyl/', views1.editvinyl),
    path('detailcd/', views1.detailcd),
    path('detailvinyl/', views1.detailvinyl),
    path('preordercd/', views2.preordercd),
    path('preordervinyl/', views2.preordervinyl),
    path('buycd/', views2.buycd),
    path('buyvinyl/', views2.buyvinyl),
    path('orderlist/', views2.orderlist),
    path('pay/', views2.pay),
    path('cancel/', views2.cancel),
    path('userorder/', views2.userorder),
    path('detailuser/', views.detailuser),
    path('top10/', views2.top10),
    url(r'^captcha', include('captcha.urls')),
]

#设置静态文件路径
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)