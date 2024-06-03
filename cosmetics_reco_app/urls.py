from django.urls import path
from . import views

urlpatterns = [
    path('', views.skin_result, name='skin_result'),
]