from django import forms
from django.core.exceptions import ValidationError
from .models import Dispatch, DispatchSpecification, GreigeStock
from .models import ProcessingReceiving, ProcessingReceivingGrade, Dispatch

class DispatchForm(forms.ModelForm):
    # We'll handle specifications via a separate inline formset, but we can add a field for dynamic specs.
    # We'll use a formset for specifications in the view, so this form only handles the dispatch fields.

    class Meta:
        model = Dispatch
        fields = [
            'dispatch_date', 'fabric', 'manufacturer', 'dispatch_quantity',
            'color', 'shade', 'width', 'finish', 'instructions', 'status'
        ]
        widgets = {
            'dispatch_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fabric': forms.Select(attrs={'class': 'form-select'}),
            'manufacturer': forms.Select(attrs={'class': 'form-select'}),
            'dispatch_quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Color'}),
            'shade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shade'}),
            'width': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Width'}),
            'finish': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Finish'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Instructions'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit fabric choices to those with positive available stock? We'll validate in clean.
        pass

    def clean(self):
        cleaned_data = super().clean()
        fabric = cleaned_data.get('fabric')
        manufacturer = cleaned_data.get('manufacturer')
        qty = cleaned_data.get('dispatch_quantity')

        if fabric and manufacturer and qty:
            # Get GreigeStock for this fabric+manufacturer
            try:
                stock = GreigeStock.objects.get(fabric=fabric, manufacturer=manufacturer)
                available = stock.available_stock
            except GreigeStock.DoesNotExist:
                raise ValidationError("No stock available for this fabric and manufacturer combination.")

            if qty > available:
                raise ValidationError(f"Dispatch quantity cannot exceed available stock ({available}).")

        return cleaned_data


# Formset for specifications (dynamic rows)
DispatchSpecificationFormSet = forms.inlineformset_factory(
    Dispatch,
    DispatchSpecification,
    fields=('spec_name', 'spec_value'),
    extra=1,
    can_delete=True,
    widgets={
        'spec_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Specification Name'}),
        'spec_value': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Specification Value'}),
    }
)
# ---------- Processing Receiving Forms ----------
from django.forms import inlineformset_factory
from .models import ProcessingReceiving, ProcessingReceivingGrade

class ProcessingReceivingForm(forms.ModelForm):
    class Meta:
        model = ProcessingReceiving
        fields = ['dispatch', 'receiving_date']
        widgets = {
            'dispatch': forms.Select(attrs={'class': 'form-select', 'id': 'id_dispatch'}),
            'receiving_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show dispatches that are 'in_transit'
        self.fields['dispatch'].queryset = Dispatch.objects.filter(status='in_transit')

# Grade formset – each row is a color with dispatch quantity (read-only) and grade inputs
class ProcessingReceivingGradeForm(forms.ModelForm):
    class Meta:
        model = ProcessingReceivingGrade
        fields = ['color', 'dispatch_quantity', 'grade_a', 'grade_b', 'cp']
        widgets = {
            'color': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'dispatch_quantity': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            'grade_a': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'grade_b': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'cp': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        grade_a = cleaned_data.get('grade_a', 0)
        grade_b = cleaned_data.get('grade_b', 0)
        cp = cleaned_data.get('cp', 0)
        dispatch_qty = cleaned_data.get('dispatch_quantity', 0)
        received = grade_a + grade_b + cp
        if received > dispatch_qty:
            raise forms.ValidationError("Received quantity cannot exceed dispatched quantity.")
        return cleaned_data

ProcessingReceivingGradeFormSet = inlineformset_factory(
    ProcessingReceiving,
    ProcessingReceivingGrade,
    form=ProcessingReceivingGradeForm,
    extra=0,
    can_delete=False,
)