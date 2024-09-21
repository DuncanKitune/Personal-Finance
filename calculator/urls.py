from django.urls import path
from . import views

urlpatterns = [
    path('', views.calculate_future_value, name='calculate_future_value'),
]
