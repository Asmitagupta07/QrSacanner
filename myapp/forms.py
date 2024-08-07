from django import forms
from .models import UserRegistration

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = UserRegistration
        fields = '__all__'
        widgets = {
            'bill_date': forms.DateInput(attrs={'type': 'date'}),
            'supply_order_date': forms.DateInput(attrs={'type': 'date'}),
        }
