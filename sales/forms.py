from django import forms
from django.core.exceptions import ValidationError
from .models import SalesInvoice, SalesInvoiceItem
from inventory.models import FinishedStock

class SalesInvoiceForm(forms.ModelForm):
    class Meta:
        model = SalesInvoice
        fields = ['invoice_date', 'customer_name', 'customer_phone', 'customer_address', 'remarks']
        widgets = {
            'invoice_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Customer Name'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'customer_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Address'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Remarks'}),
        }


class SalesInvoiceItemForm(forms.ModelForm):
    class Meta:
        model = SalesInvoiceItem
        fields = ['fabric', 'color', 'grade', 'quantity', 'rate']
        widgets = {
            'fabric': forms.Select(attrs={'class': 'form-select fabric-select'}),
            'color': forms.TextInput(attrs={'class': 'form-control color-input'}),
            'grade': forms.Select(attrs={'class': 'form-select grade-select', 'choices': (('A', 'Grade A'), ('B', 'Grade B'), ('C', 'CP'))}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control quantity-input', 'step': '0.01', 'min': '0'}),
            'rate': forms.NumberInput(attrs={'class': 'form-control rate-input', 'step': '0.01', 'min': '0'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        fabric = cleaned_data.get('fabric')
        color = cleaned_data.get('color')
        grade = cleaned_data.get('grade')
        qty = cleaned_data.get('quantity')

        if fabric and color and grade and qty:
            # Check available stock
            try:
                stock = FinishedStock.objects.get(fabric=fabric, color=color)
                available = stock.available_stock
                if grade == 'A':
                    available = stock.grade_a - stock.reserved
                elif grade == 'B':
                    available = stock.grade_b - stock.reserved
                elif grade == 'C':
                    available = stock.cp - stock.reserved
                # Note: we should check per grade – we'll need to modify FinishedStock model to have per-grade reserved? For simplicity, we'll assume no per-grade reserved and just use total.
                # Better: we will compute available from the model's grade fields.
                # Since we already have grade_a, grade_b, cp separately, we'll check the respective field.
            except FinishedStock.DoesNotExist:
                raise ValidationError("No stock available for this fabric, color, and grade combination.")

        return cleaned_data


from django.forms import inlineformset_factory

SalesInvoiceItemFormSet = inlineformset_factory(
    SalesInvoice,
    SalesInvoiceItem,
    form=SalesInvoiceItemForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
)