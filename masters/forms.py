from django import forms
from .models import Manufacturer, BuyingHouse, Agent, Fabric

# ... rest of the code (ManufacturerForm, BuyingHouseForm, AgentForm)

# ---------- Manufacturer Form ----------
class ManufacturerForm(forms.ModelForm):
    # ... (existing code, keep as is) ...
    class Meta:
        model = Manufacturer
        fields = ['manufacturer_name', 'contact_person', 'phone', 'email', 'address', 'status']
        widgets = {
            'manufacturer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter manufacturer name'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter contact person'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter address'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
    # ... validations ...


# ---------- Buying House Form ----------
class BuyingHouseForm(forms.ModelForm):
    class Meta:
        model = BuyingHouse
        fields = ['buying_house_name', 'address', 'phone', 'email', 'status']
        widgets = {
            'buying_house_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter buying house name'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_buying_house_name(self):
        name = self.cleaned_data.get('buying_house_name')
        if self.instance.pk:
            if BuyingHouse.objects.filter(buying_house_name=name).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Buying House with this name already exists.")
        else:
            if BuyingHouse.objects.filter(buying_house_name=name).exists():
                raise forms.ValidationError("Buying House with this name already exists.")
        return name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if self.instance.pk:
            if BuyingHouse.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Phone number already exists.")
        else:
            if BuyingHouse.objects.filter(phone=phone).exists():
                raise forms.ValidationError("Phone number already exists.")
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if self.instance.pk:
                if BuyingHouse.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                    raise forms.ValidationError("Email already exists.")
            else:
                if BuyingHouse.objects.filter(email=email).exists():
                    raise forms.ValidationError("Email already exists.")
        return email
# ---------- Agent Form ----------
class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ['agent_name', 'commission_percentage', 'phone', 'email', 'address', 'status']
        widgets = {
            'agent_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter agent name'}),
            'commission_percentage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter commission %', 'step': '0.01', 'min': '0', 'max': '100'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter address'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_agent_name(self):
        name = self.cleaned_data.get('agent_name')
        if self.instance.pk:
            if Agent.objects.filter(agent_name=name).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Agent with this name already exists.")
        else:
            if Agent.objects.filter(agent_name=name).exists():
                raise forms.ValidationError("Agent with this name already exists.")
        return name

    def clean_commission_percentage(self):
        value = self.cleaned_data.get('commission_percentage')
        if value is None:
            raise forms.ValidationError("Commission percentage is required.")
        if value < 0 or value > 100:
            raise forms.ValidationError("Commission percentage must be between 0 and 100.")
        return value

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if self.instance.pk:
            if Agent.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Phone number already exists.")
        else:
            if Agent.objects.filter(phone=phone).exists():
                raise forms.ValidationError("Phone number already exists.")
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if self.instance.pk:
                if Agent.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                    raise forms.ValidationError("Email already exists.")
            else:
                if Agent.objects.filter(email=email).exists():
                    raise forms.ValidationError("Email already exists.")
        return email
# ---------- Fabric Form ----------
class FabricForm(forms.ModelForm):
    class Meta:
        model = Fabric
        fields = [
            'fabric_blend', 'fabric_quality', 'warp', 'warp_blend',
            'weft', 'weft_blend', 'ends', 'picks', 'weave',
            'greige_width_on_loom', 'greige_width_off_loom', 'selvedge_type',
            'unit', 'status', 'remarks'
        ]
        widgets = {
            'fabric_blend': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter blend'}),
            'fabric_quality': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter quality'}),
            'warp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter warp count'}),
            'warp_blend': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter warp blend'}),
            'weft': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter weft count'}),
            'weft_blend': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter weft blend'}),
            'ends': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter ends'}),
            'picks': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter picks'}),
            'weave': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter weave type'}),
            'greige_width_on_loom': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Width on loom (inch)'}),
            'greige_width_off_loom': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Width off loom (inch)'}),
            'selvedge_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Selvedge type'}),
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Remarks (optional)'}),
        }

    def clean_fabric_blend(self):
        value = self.cleaned_data.get('fabric_blend')
        if not value:
            raise forms.ValidationError("Fabric Blend is required.")
        return value

    def clean_fabric_quality(self):
        value = self.cleaned_data.get('fabric_quality')
        if not value:
            raise forms.ValidationError("Fabric Quality is required.")
        return value

    def clean_warp(self):
        value = self.cleaned_data.get('warp')
        if not value:
            raise forms.ValidationError("Warp is required.")
        return value

    def clean_weft(self):
        value = self.cleaned_data.get('weft')
        if not value:
            raise forms.ValidationError("Weft is required.")
        return value

    def clean_ends(self):
        value = self.cleaned_data.get('ends')
        if value is None or value <= 0:
            raise forms.ValidationError("Ends must be a positive number.")
        return value

    def clean_picks(self):
        value = self.cleaned_data.get('picks')
        if value is None or value <= 0:
            raise forms.ValidationError("Picks must be a positive number.")
        return value

    def clean_greige_width_on_loom(self):
        value = self.cleaned_data.get('greige_width_on_loom')
        if value is not None and value < 0:
            raise forms.ValidationError("Width cannot be negative.")
        return value

    def clean_greige_width_off_loom(self):
        value = self.cleaned_data.get('greige_width_off_loom')
        if value is not None and value < 0:
            raise forms.ValidationError("Width cannot be negative.")
        return value