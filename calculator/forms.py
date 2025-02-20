from django import forms
from .models import Simulation
from .models import HerdSimulation
from .models import ChickenSimulation
from .models import GoatSimulation
from .models import SubscriptionPlan

class SubscriptionForm(forms.Form):
    plan = forms.ModelChoiceField(queryset=SubscriptionPlan.objects.all(), required=True)


class HerdSimulationForm(forms.ModelForm):
    class Meta:
        model = Simulation
        fields = ['simulation_type', 'initial_count', 'simulation_months', 'average_per_cycle']

    def clean_initial_count(self):
        initial_count = self.cleaned_data.get('initial_count')
        if initial_count <= 0:
            raise forms.ValidationError("Initial count must be greater than zero.")
        return initial_count

    def clean_simulation_months(self):
        simulation_months = self.cleaned_data.get('simulation_months')
        if not (1 <= simulation_months <= 120):
            raise forms.ValidationError("Simulation months must be between 1 and 120.")
        return simulation_months

    def clean_average_per_cycle(self):
        average_per_cycle = self.cleaned_data.get('average_per_cycle')
        if average_per_cycle < 1:
            raise forms.ValidationError("Average per cycle must be at least 1.")
        return average_per_cycle

    def clean_simulation_type(self):
        simulation_type = self.cleaned_data.get('simulation_type')
        allowed_types = ['herd', 'chicken', 'goat']
        if simulation_type not in allowed_types:
            raise forms.ValidationError("Invalid simulation type selected.")
        return simulation_type


class GoatSimulationForm(forms.ModelForm):
    class Meta:
        model = GoatSimulation
        fields = ['initial_goats','simulation_months', 'average_kids_per_birth']

class ChickenSimulationForm(forms.ModelForm):
    class Meta:
        model = ChickenSimulation
        fields = ['initial_chickens', 'simulation_months','average_eggs_per_laying']

class SimulationForm(forms.ModelForm):
    class Meta:
        model = HerdSimulation
        fields = ['initial_mothers', 'simulation_months']

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