from django import forms
from django.core.exceptions import ValidationError
from .models import PurchaseOrder, PurchaseReceiving


class PurchaseOrderForm(forms.ModelForm):
    revision_reason = forms.CharField(
        label='Revision Reason',
        widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Reason for this revision'}),
        required=False
    )

    class Meta:
        model = PurchaseOrder
        fields = [
            'po_date', 'manufacturer', 'buying_house', 'agent', 'agent_commission',
            'fabric', 'order_quantity', 'tolerance_percentage', 'delivery_date',
            'remarks', 'status'
        ]
        widgets = {
            'po_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'manufacturer': forms.Select(attrs={'class': 'form-select'}),
            'buying_house': forms.Select(attrs={'class': 'form-select'}),
            'agent': forms.Select(attrs={'class': 'form-select'}),
            'agent_commission': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'fabric': forms.Select(attrs={'class': 'form-select'}),
            'order_quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tolerance_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'delivery_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['agent'].required = False
        if self.instance and self.instance.pk:
            self.fields['revision_reason'].required = True
        else:
            self.fields['revision_reason'].required = False
        if not self.instance.pk:
            self.initial['status'] = 'draft'

    def clean(self):
        cleaned_data = super().clean()
        po_date = cleaned_data.get('po_date')
        delivery_date = cleaned_data.get('delivery_date')
        if po_date and delivery_date and delivery_date < po_date:
            raise ValidationError("Delivery date cannot be before PO date.")
        return cleaned_data

    def clean_order_quantity(self):
        qty = self.cleaned_data.get('order_quantity')
        if qty is not None and qty <= 0:
            raise ValidationError("Order quantity must be greater than 0.")
        return qty

    def clean_tolerance_percentage(self):
        tol = self.cleaned_data.get('tolerance_percentage')
        if tol is not None and tol < 0:
            raise ValidationError("Tolerance cannot be negative.")
        return tol

    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.pk:
            instance.revision_number += 1
            instance.revision_reason = self.cleaned_data.get('revision_reason', '')
        else:
            instance.revision_reason = ''
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class PurchaseReceivingForm(forms.ModelForm):
    class Meta:
        model = PurchaseReceiving
        fields = [
            'purchase_order', 'receive_date', 'challan_number', 'invoice_number',
            'received_quantity', 'remarks'
        ]
        widgets = {
            'purchase_order': forms.Select(attrs={'class': 'form-select', 'id': 'id_purchase_order'}),
            'receive_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'challan_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Challan Number'}),
            'invoice_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Invoice Number'}),
            'received_quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Remarks'}),
        }

    def clean_received_quantity(self):
        qty = self.cleaned_data.get('received_quantity')
        if qty is not None and qty <= 0:
            raise ValidationError("Receive quantity must be greater than 0.")
        return qty

    def clean(self):
        cleaned_data = super().clean()
        po = cleaned_data.get('purchase_order')
        qty = cleaned_data.get('received_quantity')
        if po and qty:
            total_received = PurchaseReceiving.get_total_received(po)
            if self.instance and self.instance.pk:
                total_received -= self.instance.received_quantity
            remaining = po.order_quantity - total_received
            if qty > remaining:
                raise ValidationError(
                    f"Received quantity cannot exceed remaining quantity ({remaining})."
                )
        return cleaned_data