from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from django.contrib import messages
from django.template.loader import render_to_string
import math
from io import BytesIO
from django.core.files.storage import FileSystemStorage
from weasyprint import HTML # Import necessary libraries for PDF generation
from django import forms
from decimal import Decimal
# from weasyprint import WeasyTemplateResponseMixin, WeasyTemplateResponse

# def calculate_future_value(request):
#     return HttpResponse("The view is working!")
def compound_interest(request):
    if request.method == 'POST':
        # Get form values
        principal = float(request.POST.get('principal', 0))
        rate = float(request.POST.get('rate', 0)) / 100  # Convert percentage to decimal
        times_compounded = int(request.POST.get('times_compounded', 1))
        years = int(request.POST.get('years', 1))
        
        # Compound interest formula
        amount = principal * math.pow((1 + rate / times_compounded), times_compounded * years)
        interest = amount - principal  # Total interest earned
        
        # Round to two decimal places
        amount = round(amount, 2)
        interest = round(interest, 2)
        
        # Render both the form and result in the same template
        return render(request, 'calculator/compound_interest.html', {
            'principal': principal,
            'rate': rate * 100,  # Convert back to percentage
            'times_compounded': times_compounded,
            'years': years,
            'amount': amount,
            'interest': interest
        })

    return render(request, 'calculator/compound_interest.html')

def main_menu(request):
    return render(request, 'calculator/index.html')

def terms_conditions(request):
    return render(request, 'calculator/terms_conditions.html')

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
            return render(request, 'calculator/future_annuity.html', {'future_value': future_value})

    # Show the form initially
    return render(request, 'calculator/future_annuity.html')

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

    return render(request, 'calculator/budget_summary.html')


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


# Define the form
class MaterialCalculatorForm(forms.Form):
    width = forms.FloatField(label="Width of the House (ft)", required=True)
    length = forms.FloatField(label="Length of the House (ft)", required=True)
    height = forms.FloatField(label="Height of the House (ft)", required=True)
    doors = forms.IntegerField(label="Number of Doors", required=True)
    door_width = forms.FloatField(label="Width of Doors (ft)", required=True)
    door_height = forms.FloatField(label="Height of Doors (ft)", required=True)
    windows = forms.IntegerField(label="Number of Windows", required=True)
    window_width = forms.FloatField(label="Width of Windows (ft)", required=True)
    window_height = forms.FloatField(label="Height of Windows (ft)", required=True)
    cost_per_stone = forms.FloatField(label="Cost per Stone", required=False)
    cost_per_cement_bag = forms.FloatField(label="Cost per Cement Bag", required=False)
    cost_per_sand_unit = forms.FloatField(label="Cost per Sand Unit", required=False)
    cost_per_mason = forms.FloatField(label="Cost per Mason (per day)", required=False)
    cost_per_laborer = forms.FloatField(label="Cost per Laborer (per day)", required=False)
    formula_type = forms.ChoiceField(choices=[('stone_walling', 'Stone Walling')], label="Formula Type", required=True)

# Calculation function for materials
def calculate_materials(width, length, height, doors, door_width, door_height, windows, window_width, window_height):
    # Perimeter and area of walls
    perimeter = 2 * (width + length)
    total_wall_area = perimeter * height
    door_area = doors * door_width * door_height
    window_area = windows * window_width * window_height
    net_wall_area = total_wall_area - (door_area + window_area)
    
    # Stone walling calculations
    stone_volume = net_wall_area * 0.67  # Assuming 200mm (0.67 ft) wall thickness
    stone_per_cubic_ft = 0.562  # Approx volume of one stone in cubic feet
    stones_required = stone_volume / stone_per_cubic_ft
    
    # Mortar (cement and sand) calculation
    mortar_volume = stone_volume * 0.3  # 30% of stone volume
    cement_required = mortar_volume / 4  # 1 part cement, 3 parts sand
    sand_required = mortar_volume * 0.75  # 3 parts sand
    
    return {
        'net_wall_area': net_wall_area,
        'stones_required': stones_required,
        'cement_required': cement_required,
        'sand_required': sand_required
    }

# View for handling the form and calculations
def MaterialCalculatorView(request):
    form = MaterialCalculatorForm(request.POST or None)
    result = None
    
    # Handle form submission and validation
    if request.method == 'POST' and form.is_valid():
        # Extract form data
        width = form.cleaned_data['width']
        length = form.cleaned_data['length']
        height = form.cleaned_data['height']
        doors = form.cleaned_data['doors']
        door_width = form.cleaned_data['door_width']
        door_height = form.cleaned_data['door_height']
        windows = form.cleaned_data['windows']
        window_width = form.cleaned_data['window_width']
        window_height = form.cleaned_data['window_height']
        
        # Optional cost inputs
        cost_per_stone = form.cleaned_data.get('cost_per_stone', 0)
        cost_per_cement_bag = form.cleaned_data.get('cost_per_cement_bag', 0)
        cost_per_sand_unit = form.cleaned_data.get('cost_per_sand_unit', 0)
        cost_per_mason = form.cleaned_data.get('cost_per_mason', 0)
        cost_per_laborer = form.cleaned_data.get('cost_per_laborer', 0)
        
        # Perform calculations
        material_totals = calculate_materials(
            width, length, height, doors, door_width, door_height, windows, window_width, window_height
        )
        
        # Calculate costs if cost data is provided
        stone_cost = material_totals['stones_required'] * cost_per_stone if cost_per_stone else 0
        cement_cost = material_totals['cement_required'] * cost_per_cement_bag if cost_per_cement_bag else 0
        sand_cost = material_totals['sand_required'] * cost_per_sand_unit if cost_per_sand_unit else 0
        
        # Store the results in a dictionary to display in the template
        result = {
            'stone_cost': stone_cost,
            'cement_cost': cement_cost,
            'sand_cost': sand_cost,
            'total_cost': stone_cost + cement_cost + sand_cost,
            'material_totals': material_totals
        }
    
    return render(request, 'calculator/material_calculator.html', {'form': form, 'result': result})




# Define a formset for operating costs with default values
class OperatingCostForm(forms.Form):
    cost_name = forms.CharField(label="Cost Name", max_length=100)
    cost_value = forms.DecimalField(label="Cost Amount", max_digits=15, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super(OperatingCostForm, self).__init__(*args, **kwargs)
        # Default operating costs
        self.fields['cost_name'].initial = 'Operating Cost Name'
        self.fields['cost_value'].initial = 0.00


# Define the main form for each investment option
class FeasibilityForm(forms.Form):
    investment_name = forms.CharField(label="Investment Name", max_length=100)
    purchase_cost = forms.DecimalField(label="Purchase Cost", max_digits=15, decimal_places=2)
    direct_income = forms.DecimalField(label="Direct Income", max_digits=15, decimal_places=2)
    indirect_income = forms.DecimalField(label="Indirect Income (Savings)", max_digits=15, decimal_places=2)
    years = forms.IntegerField(label="Investment Period (Years)")
    discount_rate = forms.DecimalField(label="Discount Rate (%)", max_digits=5, decimal_places=2)

    FORMULA_CHOICES = [
        ('npv', 'Net Present Value (NPV)'),
        ('eac', 'Equivalent Annual Cost (EAC)')
    ]
    formula = forms.ChoiceField(choices=FORMULA_CHOICES, label="Choose Formula", widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super(FeasibilityForm, self).__init__(*args, **kwargs)
        # Set formula options to appear where needed
        self.fields['formula'].initial = 'npv'


# Function to calculate NPV
def calculate_npv(purchase_cost, cash_flows, discount_rate, years):
    npv = -purchase_cost
    for t in range(1, years + 1):
        npv += cash_flows / ((1 + discount_rate / 100) ** t)
    return npv


# Function to calculate EAC
def calculate_eac(npv, discount_rate, years):
    eac = npv / ((1 - (1 + discount_rate / 100) ** -years) / (discount_rate / 100))
    return eac


def feasibility_study(request):
    # Create a formset for multiple operating costs
    OperatingCostFormSet = forms.formset_factory(OperatingCostForm, extra=0)  # No additional forms needed
    InvestmentFormSet = forms.formset_factory(FeasibilityForm, extra=1)

    if request.method == 'POST':
        investment_formset = InvestmentFormSet(request.POST, prefix='investments')
        cost_formset = OperatingCostFormSet(request.POST, prefix='costs')

        if investment_formset.is_valid() and cost_formset.is_valid():
            results = []
            recommendations = []
            for form in investment_formset:
                investment_name = form.cleaned_data['investment_name']
                purchase_cost = form.cleaned_data['purchase_cost']
                direct_income = form.cleaned_data['direct_income']
                indirect_income = form.cleaned_data['indirect_income']
                years = form.cleaned_data['years']
                discount_rate = form.cleaned_data['discount_rate']
                formula = form.cleaned_data['formula']

                # Predefined operating costs
                total_operating_cost = sum([cost_form.cleaned_data['cost_value'] for cost_form in cost_formset])

                # Calculate net cash flow
                net_cash_flow = (direct_income + indirect_income) - total_operating_cost
                npv_buy = calculate_npv(purchase_cost, net_cash_flow, discount_rate, years)

                if formula == 'eac':
                    eac_buy = calculate_eac(npv_buy, discount_rate, years)
                    results.append({
                        'investment_name': investment_name,
                        'eac_buy': eac_buy,
                        'formula': 'EAC'
                    })
                else:
                    results.append({
                        'investment_name': investment_name,
                        'npv_buy': npv_buy,
                        'formula': 'NPV'
                    })

                # Add recommendations based on NPV or EAC result
                if npv_buy > 0:
                    recommendations.append(f"{investment_name} is a profitable investment based on NPV.")
                else:
                    recommendations.append(f"{investment_name} is not a profitable investment based on NPV.")
                
                if formula == 'eac' and eac_buy < 0:
                    recommendations.append(f"Consider alternative financing options for {investment_name} as the EAC is negative.")

            return render(request, 'calculator/feasibility_result.html', {
                'results': results,
                'recommendations': recommendations
            })

    else:
        investment_formset = InvestmentFormSet(prefix='investments')
        cost_formset = OperatingCostFormSet(prefix='costs', initial=[
            {'cost_name': 'Wear and Tear', 'cost_value': 1000.00},
            {'cost_name': 'Spare Parts', 'cost_value': 500.00},
            {'cost_name': 'Fuel/Electricity', 'cost_value': 2000.00},
            {'cost_name': 'Manpower Costs', 'cost_value': 3000.00},
            {'cost_name': 'Depreciation', 'cost_value': 1500.00}
        ])

    return render(request, 'calculator/feasibility_input.html', {
        'investment_formset': investment_formset,
        'cost_formset': cost_formset
    })


def exponential_growth(request):
    if request.method == 'POST':
        try:
            # Get the input values from the form
            investment_name = forms.CharField(label="Investment Name", max_length=100)
            initial_amount = float(request.POST.get('initial_amount'))
            growth_rate = float(request.POST.get('growth_rate'))
            time = float(request.POST.get('time'))

            # Calculate exponential growth
            result = initial_amount * math.exp(growth_rate * time)
            
            # Round the result to 2 decimal places for display
            result = round(result, 2)

            # Pass the result back to the template
            context = {
                'investment_name': investment_name,
                'initial_amount': initial_amount,
                'growth_rate': growth_rate,
                'time': time,
                'result': result,
                'error': None
            }
        except ValueError:
            context = {
                'error': 'Please enter valid numeric values.'
            }
    else:
        context = {}
    
    return render(request, 'calculator/exponential_growth.html', context)

def retirement_planner(request):
    if request.method == 'POST':
        try:
            # Get the input values from the form
            retirement_date = forms.CharField(label="Planned Date of Retirement", max_length=100)
            meals_shopping = float(request.POST.get('meals_shopping'))
            transport_fuel = float(request.POST.get('transport_fuel'))
            vehicle_maintenance_costs = float(request.POST.get('vehicle_maintenance_costs'))
            clothing_personal_grooming = float(request.POST.get('clothing_personal_grooming'))
            jewellerly_beauty = float(request.POST.get('jewellerly_beauty'))
            clubs_membership_fee = float(request.POST.get('clubs_membership_fee'))
            insurance = float(request.POST.get('insurance'))
            holidays_vacations = float(request.POST.get('holidays_vacations'))
            workers = float(request.POST.get('workers'))
            church_contributions = float(request.POST.get('church_contributions'))
            community_charity_contributions = float(request.POST.get('community_charity_contributions'))
            land_rates = float(request.POST.get('land_rates'))
            time = float(request.POST.get('time'))

            # Calculate exponential growth
            result = meals_shopping + transport_fuel + vehicle_maintenance_costs + clothing_personal_grooming + jewellerly_beauty + clubs_membership_fee + insurance + holidays_vacations + workers + church_contributions + community_charity_contributions + land_rates
            
            # Round the result to 2 decimal places for display
            result = round(result, 2)

            # Pass the result back to the template
            context = {
                'retirement_date': retirement_date,
                'meals_shopping': meals_shopping,
                'transport_fuel': transport_fuel,
                'vehicle_maintenance_costs': vehicle_maintenance_costs,
                'clothing_personal_grooming': clothing_personal_grooming,
                'jewellerly_beauty': jewellerly_beauty,
                'clubs_membership_fee': clubs_membership_fee,
                'insurance': insurance,
                'holidays_vacations': holidays_vacations,
                'workers': workers,
                'church_contributions': church_contributions,
                'community_charity_contributions': community_charity_contributions,
                'land_rates': land_rates,
                'time': time,
                'result': result,
                'error': None
            }
        except ValueError:
            context = {
                'error': 'Please enter valid numeric values.'
            }
    else:
        context = {}
    
    return render(request, 'calculator/retirement_planner.html', context)

   

def loan_amortization_schedule(request):
    schedule = None
    formula_type = None
    total_interest = 0  # Initialize total interest

    if request.method == 'POST':
        loan_amount = float(request.POST.get('loan_amount'))
        interest_rate = float(request.POST.get('interest_rate')) / 100
        loan_term = int(request.POST.get('loan_term'))
        formula_type = request.POST.get('formula_type')
        payments_per_year = 12

        # Determine monthly interest rate and number of payments
        monthly_interest_rate = interest_rate / payments_per_year
        num_payments = loan_term * payments_per_year

        schedule = []
        balance = loan_amount

        if formula_type == 'reducing_balance':
            for i in range(1, num_payments + 1):
                interest_payment = balance * monthly_interest_rate
                total_payment = loan_amount / num_payments + interest_payment
                closing_balance = balance - (loan_amount / num_payments)

                total_interest += interest_payment  # Add interest to total

                schedule.append({
                    'month': i,
                    'opening_balance': round(balance, 2),
                    'interest_payment': round(interest_payment, 2),
                    'total_payment': round(total_payment, 2),
                    'closing_balance': round(closing_balance, 2)
                })

                balance = closing_balance
        elif formula_type == 'straight_line':
            monthly_payment = loan_amount / num_payments
            for i in range(1, num_payments + 1):
                interest_payment = balance * monthly_interest_rate
                total_payment = monthly_payment + interest_payment
                closing_balance = balance - monthly_payment

                total_interest += interest_payment  # Add interest to total

                schedule.append({
                    'month': i,
                    'opening_balance': round(balance, 2),
                    'interest_payment': round(interest_payment, 2),
                    'total_payment': round(total_payment, 2),
                    'closing_balance': round(closing_balance, 2)
                })

                balance = closing_balance

    return render(request, 'calculator/loan_amortization_schedule.html', {
        'schedule': schedule,
        'formula_type': formula_type,
        'total_interest': round(total_interest, 2)  # Pass total interest to the template
    })

# View for generating PDF
def generate_pdf(request):
    loan_amount = float(request.POST.get('loan_amount'))
    interest_rate = float(request.POST.get('interest_rate')) / 100
    loan_term = int(request.POST.get('loan_term'))
    formula_type = request.POST.get('formula_type')
    payments_per_year = 12

    monthly_interest_rate = interest_rate / payments_per_year
    num_payments = loan_term * payments_per_year
    schedule = []
    balance = loan_amount

    if formula_type == 'reducing_balance':
        for i in range(1, num_payments + 1):
            interest_payment = balance * monthly_interest_rate
            total_payment = loan_amount / num_payments + interest_payment
            closing_balance = balance - (loan_amount / num_payments)
            schedule.append({
                'month': i,
                'opening_balance': round(balance, 2),
                'interest_payment': round(interest_payment, 2),
                'total_payment': round(total_payment, 2),
                'closing_balance': round(closing_balance, 2)
            })
            balance = closing_balance
    elif formula_type == 'straight_line':
        monthly_payment = loan_amount / num_payments
        for i in range(1, num_payments + 1):
            interest_payment = balance * monthly_interest_rate
            total_payment = monthly_payment + interest_payment
            closing_balance = balance - monthly_payment
            schedule.append({
                'month': i,
                'opening_balance': round(balance, 2),
                'interest_payment': round(interest_payment, 2),
                'total_payment': round(total_payment, 2),
                'closing_balance': round(closing_balance, 2)
            })
            balance = closing_balance

    # Create PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="amortization_schedule.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    p.drawString(100, 800, "Loan Amortization Schedule")
    p.drawString(100, 780, f"Loan Amount: {loan_amount}")
    p.drawString(100, 760, f"Interest Rate: {interest_rate * 100}%")
    p.drawString(100, 740, f"Loan Term: {loan_term} years")
    p.drawString(100, 720, f"Formula Type: {formula_type.capitalize()}")

    y = 700
    p.drawString(100, y, "Month")
    p.drawString(150, y, "Opening Balance")
    p.drawString(250, y, "Interest")
    p.drawString(350, y, "Total Payment")
    p.drawString(450, y, "Closing Balance")
    
    for row in schedule:
        y -= 20
        p.drawString(100, y, str(row['month']))
        p.drawString(150, y, str(row['opening_balance']))
        p.drawString(250, y, str(row['interest_payment']))
        p.drawString(350, y, str(row['total_payment']))
        p.drawString(450, y, str(row['closing_balance']))

    p.showPage()
    p.save()
    buffer.seek(0)

    return HttpResponse(buffer, content_type='application/pdf')

# Sample car data stored directly in the view
car_data = [
    {"make": "Toyota", "model": "Corolla", "year": 2015, "retail_price": 2000000},
    {"make": "Nissan", "model": "Altima", "year": 2016, "retail_price": 2500000},
    {"make": "BMW", "model": "320i", "year": 2018, "retail_price": 3500000},
    # Add more cars as needed
]

def calculate_import_cost(request):
    total_cost = None
    vehicle_info = None

    if request.method == 'POST':
        car_make = request.POST.get('car_make')
        car_model = request.POST.get('car_model')
        year_of_manufacture = int(request.POST.get('year_of_manufacture'))
        cif_value = float(request.POST.get('cif_value'))

        # Find the car's retail price (CRSP) from the hardcoded data
        car = next(
            (car for car in car_data 
             if car["make"].lower() == car_make.lower() and
                car["model"].lower() == car_model.lower() and
                car["year"] == year_of_manufacture),
            None
        )

        if car:
            crsp = car['retail_price']
            vehicle_info = f"{car_make} {car_model} ({year_of_manufacture})"

            # Depreciation (10% per year up to 60%)
            depreciation_rate = min((2024 - year_of_manufacture) * 0.1, 0.6)
            adjusted_crsp = crsp * (1 - depreciation_rate)

            # Calculate taxes
            import_duty = adjusted_crsp * 0.25
            excise_duty = (adjusted_crsp + import_duty) * 0.20
            vat = (adjusted_crsp + import_duty + excise_duty) * 0.16
            idf_fee = cif_value * 0.0225
            railways_levy = cif_value * 0.015

            # Total taxes
            total_taxes = import_duty + excise_duty + vat + idf_fee + railways_levy
            total_cost = cif_value + total_taxes

        else:
            vehicle_info = "Car details not found in the database."

    return render(request, 'calculator/import_cost_form.html', {
        'total_cost': total_cost,
        'vehicle_info': vehicle_info
    })

    # Form classes
class EmploymentForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100)
    employment_status = forms.ChoiceField(choices=[('resident', 'Resident'), ('non_resident', 'Non-Resident')])
    income_type = forms.ChoiceField(choices=[('gross', 'Gross Pay'), ('net', 'Net Pay')])
    income_amount = forms.DecimalField(label="Income Amount", decimal_places=2)
    additional_income = forms.DecimalField(label="Additional Sole Proprietorship Income", required=False, decimal_places=2)

class BusinessForm(forms.Form):
    income_bracket = forms.ChoiceField(choices=[('1m_20m', '1M - 20M'), ('above_20m', 'Above 20M')])

# Helper functions for tax calculations
def calculate_statutory_deductions(income, additional_income=0):
    # convert income and additional income to Decimal
    income = Decimal(income)
    additional_income = Decimal(additional_income)
    # Sample values for deductions, you should use real values as per current Kenyan tax regulations
    PAYE = Decimal(income + additional_income) *Decimal(0.3)  # Example 30% PAYE rate
    NHIF = Decimal(500.00)  # Fixed amount for NHIF, adjust per current rates
    NSSF = Decimal(200.00)  # Fixed amount for NSSF, adjust per current rates
    
    total_deductions = PAYE + NHIF + NSSF
    return {'PAYE': PAYE, 'NHIF': NHIF, 'NSSF': NSSF, 'total_deductions': total_deductions}

def calculate_business_tax(income_bracket):
    if income_bracket == '1m_20m':
        return {
            'tax': '15% of your income',
            'advice': 'You are in the 1M - 20M income bracket. Your tax rate is 15%.'
        }
    else:
        return {
            'tax': '30% of your income',
            'advice': 'You are in the Above 20M income bracket. Your tax rate is 30%.'
        }

# Views
def tax_calculator(request):
    if request.method == 'POST':
        if 'employment_status' in request.POST:
            form = EmploymentForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                income_type = form.cleaned_data['income_type']
                income = form.cleaned_data['income_amount']
                additional_income = form.cleaned_data.get('additional_income', 0)
                
                # Calculate statutory deductions
                deductions = calculate_statutory_deductions(income, additional_income)
                net_income = income - deductions['total_deductions']
                
                context = {
                    'name': name,
                    'income_type': income_type,
                    'income': income,
                    'additional_income': additional_income,
                    'deductions': deductions,
                    'net_income': net_income
                }
                return render(request, 'calculator/tax_payslip.html', context)
        
        elif 'income_bracket' in request.POST:
            form = BusinessForm(request.POST)
            if form.is_valid():
                income_bracket = form.cleaned_data['income_bracket']
                tax_info = calculate_business_tax(income_bracket)
                
                context = {
                    'tax_info': tax_info,
                }
                return render(request, 'calculator/business_tax_advice.html', context)

    else:
        employment_form = EmploymentForm()
        business_form = BusinessForm()

    return render(request, 'calculator/tax_calculator.html', {'employment_form': employment_form, 'business_form': business_form})

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
