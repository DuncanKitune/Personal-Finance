from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
import random
from django.shortcuts import render, redirect
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
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

        # Prepare insights based on net worth
        zero_net_worth_responses = [
            "Your net worth is zero. Recommendation: Consider evaluating your assets and liabilities to find areas for improvement.",
            "Your net worth is zero. Recommendation: Focus on building your savings to create a buffer for unexpected expenses.",
            "Your net worth is zero. Recommendation: Assess your financial habits and seek ways to increase your income.",
            "Consider creating a budget to track your income and expenses and identify areas to save.",
            "Explore ways to increase your income, like taking on a side hustle or negotiating a raise.",
            "Develop a plan to pay down debt, focusing on high-interest debts first.",
            "Consult a financial advisor to develop a personalized wealth management plan eg DKC Consulting Africa @ +254 720 984 457."
        ]
        negative_net_worth_responses = [
            "Your net worth is negative. If not careful, you might be relegated to bankruptcy. Recommendation: Review your expenses and liabilities.",
            "Your net worth is negative. Recommendation: Create a strict budget to manage your finances effectively.",
            "Consult a financial advisor to develop a personalized wealth management plan eg DKC Consulting Africa @ +254 720 984 457.",
            "Your net worth is negative. Recommendation: Consider debt counseling and explore options for financial recovery.",
            "Create a strict budget and prioritize essential expenses. Consider reducing discretionary spending.",
            "Seek professional help from a credit counselor to develop a debt repayment strategy.",
            "Explore options for consolidating debt to simplify management and potentially reduce interest rates."
        ]
        positive_net_worth_responses = [
            "Diversify your investments to minimize risk and maximize long-term growth.",
            "Consider contributing to a retirement savings account to secure your future.",
            "Consult a financial advisor to develop a personalized wealth management plan eg DKC Consulting Africa @ +254 720 984 457.",
            "Your net worth is positive. Recommendation: Consider investing your surplus to grow your wealth.",
            "Your net worth is positive. Recommendation: Build a financial safety net by saving a portion of your income.",
            "Your net worth is positive. Recommendation: Diversify your investments to minimize risks and enhance growth.",
        ]

        # Randomly select a response
        if net_worth == 0:
            insight = random.choice(zero_net_worth_responses)
        elif net_worth < 0:
            insight = random.choice(negative_net_worth_responses)
        else:
            insight = random.choice(positive_net_worth_responses)

        # Render the results on the web page before downloading the PDF
        if 'download_pdf' in request.POST:
            # Create a PDF report
            buffer = io.BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            p.drawString(100, 750, f"Net Worth Calculation Summary")
            p.drawString(100, 730, f"Assets: {total_assets}")
            p.drawString(100, 710, f"Liabilities: {total_liabilities}")
            p.drawString(100, 690, f"Net Worth: {net_worth}")
            p.drawString(100, 670, insight)
            p.showPage()
            p.save()

            # Generate PDF response
            buffer.seek(0)
            return HttpResponse(buffer, content_type='application/pdf', headers={'Content-Disposition': 'attachment; filename="net_worth_summary.pdf"'})

        # If the user hasn't requested a PDF, render the HTML template
        return render(request, 'calculator/net_worth_calculator.html', {
            'zipped_assets': zipped_assets,
            'zipped_liabilities': zipped_liabilities,
            'total_assets': total_assets,
            'total_liabilities': total_liabilities,
            'net_worth': net_worth,
            'recommendation': insight
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
