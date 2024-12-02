# apps/jobs/forms.py
from django import forms
from .models import Quotation

class QuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = [ 'description', 'budget']

    # Si el campo price no se está enviando, asegúrate de que esté completado por defecto o validado
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None or price == 0:  # Si el precio es nulo o 0, asignar un valor predeterminado
            return 0  # Valor predeterminado
        return price

class CounterOfferForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = ['counter_offer', 'time_estimate']

class EditQuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = [ 'description', 'budget']

    # Si el campo price no se está enviando, asegúrate de que esté completado por defecto o validado
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None or price == 0:  # Si el precio es nulo o 0, asignar un valor predeterminado
            return 0  # Valor predeterminado
        return price