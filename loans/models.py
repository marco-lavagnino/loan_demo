from django.db import models
from loans.constants import genders
from django.core import validators


DNIValidator = validators.RegexValidator(r'^\d{8}$', 'DNI inválido.')

class LoanRequest(models.Model):
    document_number = models.CharField(
        validators=[DNIValidator],
        max_length=8,
    )
    complete_name = models.CharField(max_length=100)
    gender = models.CharField(choices=genders, max_length=1)
    email = models.EmailField()
    amount = models.IntegerField()
