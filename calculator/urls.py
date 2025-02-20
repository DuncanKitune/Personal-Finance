from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main_menu, name='main_menu'),
    path('accounts/', include('django.contrib.auth.urls')),  # Include auth-related views
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
    path('calculate-exponential', views.exponential_growth, name='exponential_growth'),
    path('retirement-planner', views.retirement_planner, name='retirement_planner'),
    path('terms_conditions', views.terms_conditions, name='terms_conditions'),
    path('loan-armotization', views.loan_amortization_schedule, name='loan_amortization_schedule'),
    path('calculate-import-cost', views.calculate_import_cost, name='calculate_import_cost'),
    path('tax-calculator', views.tax_calculator, name='tax_calculator'),
    
    path('herd_simulator_view',views.herd_simulator_view, name='herd_simulator_view'),
    path('simulation_results_view', views.simulation_results_view, name='simulation_results_view'),
    path('simulation_results/<int:simulation_id>/', views.simulation_results_view, name='simulation_results_view'),
    
    path('goat_simulator_view', views.goat_simulator_view, name='goat_simulator_view'),
    path('goat_simulation_results_view/', views.goat_simulation_results_view, name='goat_simulation_results'),
    path('goat_simulation_results/<int:simulation_id>/', views.goat_simulation_results_view, name='goat_simulation_results'),
    
    path('chicken_simulator_view', views.chicken_simulator_view, name='chicken_simulator_view'),
    path('chicken_simulation_results_view', views.chicken_simulation_results_view, name='chicken_simulation_results'),
    path('chicken_simulation_results/<int:simulation_id>/', views.chicken_simulation_results_view, name='chicken_simulation_results'),
    
    # path('', views.simulation_view, name='simulation'), #only create method now to access to each link types

    path('results/<int:simulation_id>/', views.simulation_results_view, name = "simulation_results"),# also route as all simulation ids come into same route handler for common handling

    path('simulation_results_view', views.simulation_results_view, name='simulation_results_view'),

    path('subscribe/', views.subscribe, name='subscribe'),
    path('premium-contnet/', views.premium_content, name='premium_content'),

    path('checkout/<int:plan_id>/', views.create_checkout_session, name='checkout'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-cancel/', views.payment_cancel, name='payment_cancel'),

    path('login/', views.login_required, name='login'),

    path('notify_expiring_subscriptions/', views.notify_expiring_subscriptions, name='notify_expiring_subscriptions'),

    path('alert_view/', views.alert_view, name='alert_view'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
