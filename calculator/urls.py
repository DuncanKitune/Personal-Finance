from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_menu, name='main_menu'),
    path('calculate-future-value/', views.calculate_future_value, name='calculate_future_value'),
    path('calculate-principle/', views.calculate_principle, name='calculate_principle'),
    path('calculate-net-worth/', views.net_worth_calculator, name='net_worth_calculator'),
    path('calculate-net-worth/', views.net_worth_calculator, name='download_pdf'),
    path('calculate-budget/', views.personal_budget, name='personal_budget'),
    path('calculate-business-risk/', views.risk_calculations, name='risk_calculations'),
    path('pdf/', views.generate_pdf, name='generate_pdf'),
    path('compound-interest', views.compound_interest, name='compound_interest'),
    path('calculate-material', views.calculate_materials, name='calculate_materials'),
    path('calculate-feasilility', views.feasibility_study,name='feasibility_study'),
]
