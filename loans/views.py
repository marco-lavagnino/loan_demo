from django.shortcuts import render
from django.views.generic import FormView, CreateView, View

from django.http import HttpResponse


from loans.models import LoanRequest
from loans.forms import LoanRequestForm

from loans.constants import remote_api_url

import requests


def get_backend_response(unsanitized_mapping):
    """
    Wrapper for the Scoring Service, guarantees error handling in case
    of service failure.
    """
    response = requests.get(remote_api_url, params={
        'document_number': unsanitized_mapping['document_number'],
        'gender': unsanitized_mapping['gender'],
        'email': unsanitized_mapping['email'],
    })

    try:
        backend_response = response.json()
    except ValueError:
        # Raised in case the backend didn't return a JSON value
        backend_response = {
            'error': True,
            'approved': True,
        }

    return backend_response


class LoanView(View):
    def get(self, request):
        return render(
            request,
            'loans/loanrequest_form.html',
            {'form': LoanRequestForm()},
        )
    
    def post(self, request):
        form = LoanRequestForm(request.POST)

        if not form.is_valid():
            return render(request, 'loans/separate_form.html', {'form': form})

        backend_response = get_backend_response(request.POST)

        if not backend_response['error'] and backend_response['approved']:
            # If loan was approved, save into DB.
            form.save()

        return render(request, 'loans/separate_form.html', {
            'form': form,
            'backend_response': backend_response,
        })


from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy


class LoanRequestListView(ListView):
    model = LoanRequest
    paginate_by = 100

class LoanRequestUpdate(UpdateView):
    model = LoanRequest
    fields = [
        'document_number',
        'complete_name',
        'gender',
        'email',
        'amount',
    ]
    success_url = '/loans'
    template_name_suffix = '_update_form'

class LoanRequestDelete(DeleteView):
    model = LoanRequest
    success_url = '/loans'
