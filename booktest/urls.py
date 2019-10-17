from django.conf.urls import url
from booktest.views import index,test
from django.urls import path

urlpatterns = [
    path('login/', index),
    path('test/',test),

]
