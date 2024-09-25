from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
import random
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
import math
from io import BytesIO
from django.core.files.storage import FileSystemStorage
from weasyprint import HTML # Import necessary libraries for PDF generation
# from weasyprint import WeasyTemplateResponseMixin, WeasyTemplateResponse

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
            principal = (target_amount / ((1 + rate_per_period) ** total_periods))/total_periods

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
            "Your net worth is zero. Consider evaluating your assets and liabilities to find areas for improvement.",
            "Your net worth is zero. Focus on building your savings to create a buffer for unexpected expenses.",
            "Your net worth is zero. Assess your financial habits and seek ways to increase your income.",
            "Consider creating a budget to track your income and expenses and identify areas to save.",
            "Explore ways to increase your income, like taking on a side hustle or negotiating a raise.",
            "Develop a plan to pay down debt, focusing on high-interest debts first.",
            "Consult a financial advisor to develop a personalized wealth management plan eg DKC Consulting Africa @ +254 720 984 457."
        ]
        negative_net_worth_responses = [
            "Your net worth is negative. If not careful, you might be relegated to bankruptcy. Review your expenses and liabilities.",
            "Your net worth is negative. Create a strict budget to manage your finances effectively.",
            "Consult a financial advisor to develop a personalized wealth management plan eg DKC Consulting Africa  +254 720 984 457.",
            "Your net worth is negative. Consider debt counseling and explore options for financial recovery.",
            "Create a strict budget and prioritize essential expenses. Consider reducing discretionary spending.",
            "Seek professional help from a credit counselor to develop a debt repayment strategy.",
            "Explore options for consolidating debt to simplify management and potentially reduce interest rates."
        ]
        positive_net_worth_responses = [
            "Diversify your investments to minimize risk and maximize long-term growth.",
            "Consider contributing to a retirement savings account to secure your future.",
            "Consult a financial advisor to develop a personalized wealth management plan eg  DKC Consulting Africa Tel: +254 720 984 457.",
            "Your net worth is positive. Consider investing your surplus to grow your wealth.",
            "Your net worth is positive. Build a financial safety net by saving a portion of your income.",
            "Your net worth is positive. Diversify your investments to minimize risks and enhance growth.",
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




expense_categories = {
    'Rent': 'Needs',
    'Groceries': 'Needs',
    'Utilities': 'Needs',
    'Transport': 'Needs',
    'Insurance': 'Needs',
    'Dining out': 'Wants',
    'Clothing': 'Wants',
    'Travel': 'Luxury',
    'Gym membership': 'Wants',
    'Entertainment': 'Wants',
    'Savings': 'Savings & Investments',
    'Investments': 'Savings & Investments',
    # More expenses can be added here
}

# Predefined recommendations
recommendations = {
    'Needs': ["Consider downsizing some of your fixed costs like utilities or rent.",
              "Review your grocery shopping habits to reduce unnecessary expenses."],
    'Wants': ["Try to limit dining out to a certain number of times per week.",
              "Avoid impulse buying and stick to a planned budget for discretionary spending."],
    'Luxury': ["Luxury expenses should be avoided unless savings goals are met.",
               "Redirect luxury spending into savings or investments to grow wealth."],
    'Savings & Investments': ["Continue to save and invest in low-risk assets for a secure future.",
                              "Consider diversifying your investments to reduce risk."]
}

# Function to calculate total for each category
def calculate_totals(expenses):
    totals = {
        'Needs': 0,
        'Wants': 0,
        'Luxury': 0,
        'Savings & Investments': 0,
        'Other': 0
    }

    for expense in expenses:
        description = expense['description']
        amount = expense['amount']
        category = expense_categories.get(description, 'Other')  # If not in predefined, assign to 'Other'
        totals[category] += amount

    return totals

# Function to provide recommendations based on the budget
def generate_recommendations(totals, income):
    insights = []
    total_expenses = sum(totals.values())
    rent_percentage = (totals.get('Needs', 0) / income) * 100 if income else 0

    # Check for exceeding limits
    if totals['Needs'] > income * 0.40:
        insights.append(f"Your needs exceed the recommended 40% threshold. {recommendations['Needs'][0]}")
    if totals['Wants'] > income * 0.10:
        insights.append(f"Your wants exceed the recommended 10% threshold. {recommendations['Wants'][0]}")
    if totals['Luxury'] > 0:
        insights.append(f"Luxury expenses should be minimized. {recommendations['Luxury'][0]}")
    if rent_percentage > 25:
        insights.append("Your rent is more than 25% of your income. You may be living above your means.")
    if totals['Savings & Investments'] < income * 0.50:
        insights.append(f"Your savings & investments are less than the recommended 50%. {recommendations['Savings & Investments'][0]}")

    # Additional insight if income exceeds expenditure or vice versa
    if income > total_expenses:
        insights.append("You have a surplus, which is great! Consider investing the excess.")
    elif income < total_expenses:
        insights.append("You are spending more than your income. Consider taking short-term measures or reducing discretionary spending.")

    return insights

# View for handling the budget input and calculation
def personal_budget(request):
    if request.method == 'POST':
        # Get list of incomes and their amounts
        incomes = request.POST.getlist('income[]', [])
        income_amounts = request.POST.getlist('income_amount[]', [])

        # Calculate total income
        total_income = sum([float(amount) for amount in income_amounts if amount])

        # Get list of expenses and their amounts
        expenses = []
        expense_descriptions = request.POST.getlist('expense[]', [])
        expense_amounts = request.POST.getlist('expense_amount[]', [])
        
        for i in range(len(expense_descriptions)):
            description = expense_descriptions[i]
            amount = float(expense_amounts[i]) if expense_amounts[i] else 0
            expenses.append({'description': description, 'amount': amount})
            
        # Calculate totals for each category
        totals = calculate_totals(expenses)  # This should return a dict with category totals
        
        total_expenses = sum([expense['amount'] for expense in expenses])

        # Ensure the Savings & Investment category exists
        if 'Savings & Investment' not in totals:
            totals['Savings & Investment'] = 0

        # Calculate surplus or deficit
        surplus_or_deficit_amount = total_income - total_expenses
        
        # If there is a surplus, classify it as Savings & Investment
        if surplus_or_deficit_amount > 0:
            totals['Savings & Investment'] += surplus_or_deficit_amount

        # Recalculate percentages after adding surplus
        percentages = {
            'Needs': (totals.get('Needs', 0) / total_income) * 100 if total_income > 0 else 0,
            'Wants': (totals.get('Wants', 0) / total_income) * 100 if total_income > 0 else 0,
            'Luxury': (totals.get('Luxury', 0) / total_income) * 100 if total_income > 0 else 0,
            'Savings & Investment': (totals.get('Savings & Investment', 0) / total_income) * 100 if total_income > 0 else 0,
            'Other': (totals.get('Other', 0) / total_income) * 100 if total_income > 0 else 0,
        }

        # Generate recommendations based on percentages
        recommendations = generate_recommendations(totals, total_income)  # Define this function

        # Determine whether it's a surplus or deficit
        surplus_or_deficit_label = f"{surplus_or_deficit_amount:.2f} {'+' if surplus_or_deficit_amount >= 0 else '-'}"

        return render(request, 'calculator/budget_summary.html', {
            'total_income': total_income,
            'expenses': expenses,
            'total_expenses': total_expenses,
            'percentages': percentages,  # Pass the recalculated percentages
            'recommendations': recommendations,
            'surplus_or_deficit': surplus_or_deficit_label
        })

    return render(request, 'calculator/personal_budget.html')


# Views.py logic for risk calculations
def risk_calculations(request):
    context = {}
    if request.method == 'POST':
        # Retrieve form data
        formula = request.POST.get('formula')
        returns = list(map(float, request.POST.get('returns').split(',')))  # Convert to list of floats
        expected_return = float(request.POST.get('expected_return'))
        risk_free_rate = float(request.POST.get('risk_free_rate', 0))
        market_return = float(request.POST.get('market_return', 0))
        variance_market = float(request.POST.get('variance_market', 0))
        probability_loss = float(request.POST.get('probability_loss', 0))
        loss_amount = float(request.POST.get('loss_amount', 0))
        discount_rate = float(request.POST.get('discount_rate', 0))

        # Perform the selected calculation
        if formula == 'Standard Deviation':
            mean = sum(returns) / len(returns)
            variance = sum((x - mean) ** 2 for x in returns) / len(returns)
            result = math.sqrt(variance)
            context['result'] = {'Formula': 'Standard Deviation', 'Result': result}

        elif formula == 'Value at Risk (VaR)':
            z_score = 1.65  # for 95% confidence level
            std_dev = math.sqrt(sum((x - expected_return) ** 2 for x in returns) / len(returns))
            result = expected_return - z_score * std_dev
            context['result'] = {'Formula': 'Value at Risk (VaR)', 'Result': result}

        elif formula == 'Beta':
            covariance = sum((x - expected_return) * (market_return - expected_return) for x in returns) / len(returns)
            result = covariance / variance_market
            context['result'] = {'Formula': 'Beta', 'Result': result}

        elif formula == 'Sharpe Ratio':
            std_dev = math.sqrt(sum((x - expected_return) ** 2 for x in returns) / len(returns))
            result = (expected_return - risk_free_rate) / std_dev
            context['result'] = {'Formula': 'Sharpe Ratio', 'Result': result}

        elif formula == 'Risk-Return Ratio':
            result = sum(returns) / expected_return
            context['result'] = {'Formula': 'Risk-Return Ratio', 'Result': result}

        elif formula == 'Expected Loss':
            result = probability_loss * loss_amount
            context['result'] = {'Formula': 'Expected Loss', 'Result': result}

        elif formula == 'Discounted Cash Flow (DCF)':
            periods = list(range(1, len(returns) + 1))
            result = sum([c / (1 + discount_rate) ** t for c, t in zip(returns, periods)])
            context['result'] = {'Formula': 'Discounted Cash Flow (DCF)', 'Result': result}

        elif formula == 'Coefficient of Variation (CV)':
            mean = sum(returns) / len(returns)
            std_dev = math.sqrt(sum((x - mean) ** 2 for x in returns) / len(returns))
            result = std_dev / mean
            context['result'] = {'Formula': 'Coefficient of Variation (CV)', 'Result': result}

    return render(request, 'calculator/risk_calculation.html', context)

# View for generating the PDF
def generate_pdf(request):
    # Assume context is populated with the data you want to display
    context = {'results': request.session.get('result', {})}
    html = render_to_string('calculator/risk_calculations_pdf.html', context)
    pdf_file = BytesIO()
    HTML(string=html).write_pdf(pdf_file)

    response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="risk_results.pdf"'
    return response


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
