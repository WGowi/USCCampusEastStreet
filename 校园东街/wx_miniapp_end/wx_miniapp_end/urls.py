"""wx_miniapp_end URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from DataInfo import views

# 配置路由
urlpatterns = [
    path('admin/', admin.site.urls),
    path('data/yzw', views.getYZWData),
    path('data/lost', views.getLostData),
    path('data/found', views.getFoundData),
    path('data/info', views.getInfoData),
    path('data/lostdetail', views.getLostDetailInfo),
    path('data/founddetail', views.getFoundDetailInfo),
    path('data/infodetail', views.getInfoDetailInfo),
    path('data/subject', views.getSubjectInfo),
    path('data/subject/detail', views.getYZWDetail),
    path('search/lost', views.searchLost),
    path('search/found', views.searchFound),
    path('search/info', views.searchInfo)
]
