from django import forms
from django.utils import timezone

class DateRangeForm(forms.Form):
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        if date_from and date_to and date_to < date_from:
            raise forms.ValidationError("End date cannot be before start date.")
        return cleaned_data


class PurchaseReportFilterForm(DateRangeForm):
    manufacturer = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    po_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PO Number'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from masters.models import Manufacturer
        manufacturers = Manufacturer.objects.all()
        self.fields['manufacturer'].choices = [('', 'All')] + [(m.id, m.manufacturer_name) for m in manufacturers]


class ReceivingReportFilterForm(DateRangeForm):
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All'), ('pending', 'Pending'), ('completed', 'Completed'), ('partial', 'Partial')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    po_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PO Number'})
    )


class DispatchReportFilterForm(DateRangeForm):
    fabric = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    manufacturer = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from masters.models import Fabric, Manufacturer
        fabrics = Fabric.objects.all()
        manufacturers = Manufacturer.objects.all()
        self.fields['fabric'].choices = [('', 'All')] + [(f.id, f.fabric_code) for f in fabrics]
        self.fields['manufacturer'].choices = [('', 'All')] + [(m.id, m.manufacturer_name) for m in manufacturers]


class ProcessingReportFilterForm(DateRangeForm):
    report_type = forms.ChoiceField(
        required=False,
        choices=[('loss', 'Loss Report'), ('gain', 'Gain Report'), ('color', 'Color Wise'), ('grade', 'Grade Wise')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class StockReportFilterForm(forms.Form):
    stock_type = forms.ChoiceField(
        required=False,
        choices=[('greige', 'Greige Stock'), ('transit', 'Transit Stock'), ('finished', 'Finished Stock')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    grade_type = forms.ChoiceField(
        required=False,
        choices=[('', 'All Grades'), ('A', 'Grade A'), ('B', 'Grade B'), ('C', 'CP')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    fabric = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    color = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Color'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from masters.models import Fabric
        fabrics = Fabric.objects.all()
        self.fields['fabric'].choices = [('', 'All')] + [(f.id, f.fabric_code) for f in fabrics]


class SalesReportFilterForm(DateRangeForm):
    customer = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Customer Name'})
    )
    invoice = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Invoice Number'})
    )