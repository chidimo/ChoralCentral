
"""http://morozov.ca/django-pdf-msword-excel-templates.html"""

from django.db import models 

class Customer(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    def __str__(self):
        return self.name
    
# forms.py

from django import forms
from invoices.models import Customer

class InvoiceForm(forms.Form):
    FORMAT_CHOICES = ( ('pdf', 'PDF'), ('docx', 'MS Word'), ('html', 'HTML'), )
    number = forms.CharField(label='Invoice #')
    customer = forms.ModelChoiceField(queryset=Customer.objects.all())
    subject = forms.CharField()
    amount = forms.DecimalField()
    format = forms.ChoiceField(choices=FORMAT_CHOICES)
    
# views.py
from django.shortcuts import render
from templated_docs import fill_template
from templated_docs.http import FileResponse
from invoices.forms import InvoiceForm

def invoice_view(request):
    form = InvoiceForm(request.POST or None)
    if form.is_valid():
        doctype = form.cleaned_data['format']
        filename = fill_template( 'invoices/invoice.odt', form.cleaned_data, output_format=doctype)
        visible_filename = 'invoice.{}'.format(doctype)
        return FileResponse(filename, visible_filename)
    else:
        return render(request, 'invoices/form.html', {'form': form})
    