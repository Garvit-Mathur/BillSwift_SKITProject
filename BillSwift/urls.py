"""
URL configuration for BillSwift project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from re import template
from django.contrib import admin
from django.urls import path

from auth_app import views
from django.conf import settings
from django.conf.urls.static import static
from auth_app.views import view_bill_image

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('login/',views.login_handle),
    path('signup/',views.Create_Account),
    path('logout/',views.logouthandle),
    path('about/',views.about),
    path('contact/',views.contact),
    path('index_login/',views.index_login),
    path('view_image/',views.view_image,name="view_image"),
    path('view_bill_image/',views.view_bill_image,name="view_bill_image"),
    path('approve_bill/<int:bill_id>/', views.approve_bill, name='approve_bill'),
    path('reject_bill/<int:bill_id>/', views.reject_bill, name='reject_bill'),
    path('display_bills/', views.display_bills, name='display_bills'),
    path('view_bill_image/<int:bill_id>/', views.view_bill_image, name='view_bill_image'),
    path('index_login/delete_bill',views.delete_bill,name="delete_bill"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
