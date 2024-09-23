from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse

# def calculate_future_value(request):
#     return HttpResponse("The view is working!")

def main_menu(request):
    return render(request, 'calculator/main_menu.html')

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

def calculate_principle(request):
    if request.method == 'POST':
        try:
            # Retrieve values from POST request
            annual_rate = float(request.POST.get('annual_rate', 0)) / 100  # Convert percentage to decimal
            years = int(request.POST.get('years', 0))
            target_amount = float(request.POST.get('target_amount', 0))
            compounds_per_year = int(request.POST.get('compounds_per_year', 1))

            # Calculate the principal using the derived formula
            rate_per_period = annual_rate / compounds_per_year
            total_periods = years * compounds_per_year
            principal = target_amount / ((1 + rate_per_period) ** total_periods)

            # Formatting the principal to two decimal places
            formatted_principal = f"{principal:.2f}"

            # Render a response to HTML
            return render(request, 'calculator/principle_calculator.html', {
                'principal': formatted_principal
            })
        except (ValueError, ZeroDivisionError) as e:
            return HttpResponse(f"Error: {str(e)}")

    return render(request, 'calculator/principle_calculator.html')



def net_worth_calculator(request):
    if request.method == 'POST':
        # Get asset and liability data from the request
        asset_names = request.POST.getlist('asset_name')
        asset_values = request.POST.getlist('asset_value')
        liability_names = request.POST.getlist('liability_name')
        liability_values = request.POST.getlist('liability_value')

        # Calculate total assets and liabilities
        total_assets = sum(float(value) for value in asset_values if value)
        total_liabilities = sum(float(value) for value in liability_values if value)

        # Calculate net worth
        net_worth = total_assets - total_liabilities

        # Zip asset names and values, liability names and values
        zipped_assets = zip(asset_names, asset_values)
        zipped_liabilities = zip(liability_names, liability_values)

        return render(request, 'calculator/net_worth_calculator.html', {
            'zipped_assets': zipped_assets,
            'zipped_liabilities': zipped_liabilities,
            'total_assets': total_assets,
            'total_liabilities': total_liabilities,
            'net_worth': net_worth,
        })

    return render(request, 'calculator/net_worth_calculator.html')

# def net_worth_calculator(request):
#     if request.method == 'POST':
#         # Get asset and liability data from the request
#         asset_names = request.POST.getlist('asset_name')
#         asset_values = request.POST.getlist('asset_value')
#         liability_names = request.POST.getlist('liability_name')
#         liability_values = request.POST.getlist('liability_value')

#         # Calculate total assets and liabilities
#         total_assets = sum(float(value) for value in asset_values if value)
#         total_liabilities = sum(float(value) for value in liability_values if value)

#         # Calculate net worth
#         net_worth = total_assets - total_liabilities

#         # Pass the data back to the template
#         return render(request, 'calculator/net_worth_calculator.html', {
#             'asset_names': asset_names,
#             'asset_values': asset_values,
#             'liability_names': liability_names,
#             'liability_values': liability_values,
#             'total_assets': total_assets,
#             'total_liabilities': total_liabilities,
#             'net_worth': net_worth,
#         })

#     return render(request, 'calculator/net_worth_calculator.html')


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
