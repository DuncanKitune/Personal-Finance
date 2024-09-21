from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_menu, name='main_menu'),
    path('calculate-future-value/', views.calculate_future_value, name='calculate_future_value'),
    path('calculate-principle/', views.calculate_principle, name='calculate_principle'),
]
