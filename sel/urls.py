from django.urls import path
from . import views


urlpatterns = [
    path('sendemail/', views.send_email, name='sendmail'),
    path('success/', views.success, name='success')
]