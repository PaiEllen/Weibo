"""sina URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from Web.Controllers import api
from Web.Controllers import Account
from Web.Controllers import Home
from Web.Controllers import so
from Web.Controllers import my

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^test_new/', api.count),
    url(r'^get_new/', api.new),
    url(r'^create_wb/', Home.create_wb),
    url(r"^login/", Account.login),
    url(r"^index/", Home.index),
    url(r"^home/", Home.home),
    url(r"^upload_img/", Home.upload_img),
    url(r"^check_code/", Account.CHECK_CODE),
    url(r"^load_wb/", Home.load_wb),
    url(r"^upload_head/", Home.upload_head),
    url(r"^sou/wb/", so.wb),
    # url(r"^sou/user/", so.user),
    url(r"^my/", my.my),
    url(r"^guan/", my.guan),
]
