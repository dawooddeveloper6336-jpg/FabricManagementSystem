from django import forms
from .models import CompanyInfo, InvoiceSettings, AppearanceSettings

class CompanyInfoForm(forms.ModelForm):
    class Meta:
        model = CompanyInfo
        fields = '__all__'
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'ntn': forms.TextInput(attrs={'class': 'form-control'}),
            'currency': forms.TextInput(attrs={'class': 'form-control'}),
            'default_unit': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_logo(self):
        logo = self.cleaned_data.get('logo')
        if logo:
            if logo.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Logo size must be under 2 MB.")
            if not logo.content_type.startswith('image/'):
                raise forms.ValidationError("Only image files are allowed.")
        return logo


class InvoiceSettingsForm(forms.ModelForm):
    class Meta:
        model = InvoiceSettings
        fields = '__all__'
        widgets = {
            'invoice_prefix': forms.TextInput(attrs={'class': 'form-control'}),
            'po_prefix': forms.TextInput(attrs={'class': 'form-control'}),
            'dispatch_prefix': forms.TextInput(attrs={'class': 'form-control'}),
            'sales_prefix': forms.TextInput(attrs={'class': 'form-control'}),
            'invoice_footer': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'terms_conditions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class AppearanceSettingsForm(forms.ModelForm):
    class Meta:
        model = AppearanceSettings
        fields = '__all__'
        widgets = {
            'theme': forms.Select(attrs={'class': 'form-select'}),
            'primary_color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'sidebar_style': forms.TextInput(attrs={'class': 'form-control'}),
        }