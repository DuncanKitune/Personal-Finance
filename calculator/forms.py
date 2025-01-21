from django import forms
from .models import Simulation
from .models import HerdSimulation
from .models import ChickenSimulation
from .models import GoatSimulation

class SimulationForm(forms.ModelForm):
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