from django import forms
from django.core import validators
from loans.constants import genders
from loans.models import LoanRequest

class LoanForm(forms.Form):
    dni = forms.CharField(validators=[validators.RegexValidator(r'^\d{8}$')])
    complete_name = forms.CharField(min_length=5)
    gender = forms.ChoiceField(choices=genders)
    email = forms.EmailField()
    amount = forms.IntegerField()

class LoanRequestForm(forms.ModelForm):
    class Meta:
        model = LoanRequest
        fields = [
            'document_number',
            'complete_name',
            'gender',
            'email',
            'amount',
        ]
