from django.conf.urls import *
from django.contrib import admin
from .import views
admin.autodiscover()

from . import views

urlpatterns = [
    url(r'^$', views.homePage, name='homePage'), 
    url(r'^$', views.contactPage, name ='contactPage'),
    url(r'^$', views.productPage, name = 'productPage'),

]
