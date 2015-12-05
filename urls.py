"""StoreProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^$', include('storeApp.urls', namespace = "storeApp")), 
    url(r'^index/', include('storeApp.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', 'storeApp.views.loginPage'),
    url(r'^logout/', 'storeApp.views.logoutPage'),
    url(r'^register/', 'storeApp.views.registerPage'),
    url(r'^home/', 'storeApp.views.homePage', name="home"),
    url(r'^account/', 'storeApp.views.accountPage'),
    url(r'^products/', 'storeApp.views.productPage', name ="products"),
    url(r'^contact/', 'storeApp.views.contactPage', name = "contact"),
    url(r'^updateAccount/', 'storeApp.views.updateAccountPage'),
    url(r'^deleteAccount/', 'storeApp.views.deleteAccountPage'),
    url(r'^loadProducts/', 'storeApp.views.loadProducts')
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()