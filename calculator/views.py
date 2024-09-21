from django.shortcuts import render

# Create your views here.
# from django.http import HttpResponse

# def calculate_future_value(request):
#     return HttpResponse("The view is working!")


from django.shortcuts import render
from django.http import JsonResponse

def calculate_future_value(request):
    if request.method == 'POST':
        # Get data from the request (assuming values are posted in a form)
        principal = float(request.POST.get('principal', 0))
        annual_rate = float(request.POST.get('annual_rate', 0)) / 100  # Convert percentage to decimal
        years = int(request.POST.get('years', 0))
        compounds_per_year = int(request.POST.get('compounds_per_year', 0))  # Number of compounding periods per year

        # Compound interest calculation formula
        rate_per_period = annual_rate / compounds_per_year
        total_periods = years * compounds_per_year
        
        # Calculate future value based on the formula
        future_value = principal * ((1 + rate_per_period) ** total_periods - 1) / rate_per_period

        # Decide on the response type based on request header or any other condition
        if 'application/json' in request.META.get('HTTP_ACCEPT'):
            # If client accepts JSON, return a JSON response
            return JsonResponse({
                'future_value': round(future_value, 2),
            })
        else:
            # Otherwise return HTML
            return render(request, 'calculator/index.html', {'future_value': future_value})

    # Show the form initially
    return render(request, 'calculator/index.html')

# from django.http import JsonResponse
# import math
# View to handle compound interest calculation
# def calculate_future_value(request):
#     if request.method == 'POST':
#         # Get data from the request (assuming values are posted in a form)
#         principal = float(request.POST.get('principal', 0))
#         annual_rate = float(request.POST.get('annual_rate', 0)) / 100  # Convert percentage to decimal
#         years = int(request.POST.get('years', 0))
#         n = int(request.POST.get('compounds_per_year', 0))  # Number of compounding periods per year

#         # Compound interest calculation formula
#         rate_per_period = annual_rate / n
#         total_periods = years * n
        
#         # Calculate future value based on the formula
#         future_value = principal * (((1 + rate_per_period) ** total_periods - 1) / rate_per_period)

#         # Return the result as a JSON response
#         return JsonResponse({
#             'future_value': round(future_value, 2),
#         })

#     return render(request, 'calculator/index.html')  # Show the form initially
