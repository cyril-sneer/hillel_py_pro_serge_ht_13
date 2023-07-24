from django.urls import path
from . import views


urlpatterns = [
    path('sendemail/', views.index, name='sendmail'),
    path('success/', views.success, name='success')
]