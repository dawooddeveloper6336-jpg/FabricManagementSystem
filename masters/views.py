from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from accounts.views import ModulePermissionMixin
from .models import Manufacturer, BuyingHouse, Agent, Fabric
from .forms import ManufacturerForm, BuyingHouseForm, AgentForm, FabricForm

# ---------- Manufacturer ----------
class ManufacturerListView(LoginRequiredMixin, ModulePermissionMixin, ListView):
    permission_required = 'accounts.can_view_masters'
    model = Manufacturer
    template_name = 'masters/manufacturer_list.html'
    context_object_name = 'manufacturers'
    paginate_by = 10

    def get_queryset(self):
        queryset = Manufacturer.objects.all()
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(manufacturer_name__icontains=search) |
                Q(contact_person__icontains=search) |
                Q(phone__icontains=search) |
                Q(status__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context

class ManufacturerCreateView(LoginRequiredMixin, ModulePermissionMixin, CreateView):
    permission_required = 'accounts.can_view_masters'
    model = Manufacturer
    form_class = ManufacturerForm
    template_name = 'masters/manufacturer_form.html'
    success_url = reverse_lazy('masters:manufacturer_list')

    def form_valid(self, form):
        messages.success(self.request, "Manufacturer added successfully.")
        return super().form_valid(form)

class ManufacturerUpdateView(LoginRequiredMixin, ModulePermissionMixin, UpdateView):
    permission_required = 'accounts.can_view_masters'
    model = Manufacturer
    form_class = ManufacturerForm
    template_name = 'masters/manufacturer_form.html'
    success_url = reverse_lazy('masters:manufacturer_list')

    def form_valid(self, form):
        messages.success(self.request, "Manufacturer updated successfully.")
        return super().form_valid(form)

class ManufacturerDeleteView(LoginRequiredMixin, ModulePermissionMixin, DeleteView):
    permission_required = 'accounts.can_view_masters'
    model = Manufacturer
    success_url = reverse_lazy('masters:manufacturer_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Manufacturer deleted successfully.")
        return super().delete(request, *args, **kwargs)

# ---------- Buying House ----------
class BuyingHouseListView(LoginRequiredMixin, ModulePermissionMixin, ListView):
    permission_required = 'accounts.can_view_masters'
    model = BuyingHouse
    template_name = 'masters/buying_house_list.html'
    context_object_name = 'buying_houses'
    paginate_by = 10

    def get_queryset(self):
        queryset = BuyingHouse.objects.all()
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(buying_house_name__icontains=search) |
                Q(phone__icontains=search) |
                Q(email__icontains=search) |
                Q(status__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context

class BuyingHouseCreateView(LoginRequiredMixin, ModulePermissionMixin, CreateView):
    permission_required = 'accounts.can_view_masters'
    model = BuyingHouse
    form_class = BuyingHouseForm
    template_name = 'masters/buying_house_form.html'
    success_url = reverse_lazy('masters:buying_house_list')

    def form_valid(self, form):
        messages.success(self.request, "Buying House added successfully.")
        return super().form_valid(form)

class BuyingHouseUpdateView(LoginRequiredMixin, ModulePermissionMixin, UpdateView):
    permission_required = 'accounts.can_view_masters'
    model = BuyingHouse
    form_class = BuyingHouseForm
    template_name = 'masters/buying_house_form.html'
    success_url = reverse_lazy('masters:buying_house_list')

    def form_valid(self, form):
        messages.success(self.request, "Buying House updated successfully.")
        return super().form_valid(form)

class BuyingHouseDeleteView(LoginRequiredMixin, ModulePermissionMixin, DeleteView):
    permission_required = 'accounts.can_view_masters'
    model = BuyingHouse
    success_url = reverse_lazy('masters:buying_house_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Buying House deleted successfully.")
        return super().delete(request, *args, **kwargs)

# ---------- Agent ----------
class AgentListView(LoginRequiredMixin, ModulePermissionMixin, ListView):
    permission_required = 'accounts.can_view_masters'
    model = Agent
    template_name = 'masters/agent_list.html'
    context_object_name = 'agents'
    paginate_by = 10

    def get_queryset(self):
        queryset = Agent.objects.all()
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(agent_name__icontains=search) |
                Q(phone__icontains=search) |
                Q(email__icontains=search) |
                Q(status__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context

class AgentCreateView(LoginRequiredMixin, ModulePermissionMixin, CreateView):
    permission_required = 'accounts.can_view_masters'
    model = Agent
    form_class = AgentForm
    template_name = 'masters/agent_form.html'
    success_url = reverse_lazy('masters:agent_list')

    def form_valid(self, form):
        messages.success(self.request, "Agent added successfully.")
        return super().form_valid(form)

class AgentUpdateView(LoginRequiredMixin, ModulePermissionMixin, UpdateView):
    permission_required = 'accounts.can_view_masters'
    model = Agent
    form_class = AgentForm
    template_name = 'masters/agent_form.html'
    success_url = reverse_lazy('masters:agent_list')

    def form_valid(self, form):
        messages.success(self.request, "Agent updated successfully.")
        return super().form_valid(form)

class AgentDeleteView(LoginRequiredMixin, ModulePermissionMixin, DeleteView):
    permission_required = 'accounts.can_view_masters'
    model = Agent
    success_url = reverse_lazy('masters:agent_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Agent deleted successfully.")
        return super().delete(request, *args, **kwargs)

# ---------- Fabric ----------
class FabricListView(LoginRequiredMixin, ModulePermissionMixin, ListView):
    permission_required = 'accounts.can_view_masters'
    model = Fabric
    template_name = 'masters/fabric_list.html'
    context_object_name = 'fabrics'
    paginate_by = 10

    def get_queryset(self):
        queryset = Fabric.objects.all()
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(fabric_code__icontains=search) |
                Q(fabric_blend__icontains=search) |
                Q(fabric_quality__icontains=search) |
                Q(weave__icontains=search) |
                Q(status__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context

class FabricCreateView(LoginRequiredMixin, ModulePermissionMixin, CreateView):
    permission_required = 'accounts.can_view_masters'
    model = Fabric
    form_class = FabricForm
    template_name = 'masters/fabric_form.html'
    success_url = reverse_lazy('masters:fabric_list')

    def form_valid(self, form):
        messages.success(self.request, "Fabric added successfully.")
        return super().form_valid(form)

class FabricUpdateView(LoginRequiredMixin, ModulePermissionMixin, UpdateView):
    permission_required = 'accounts.can_view_masters'
    model = Fabric
    form_class = FabricForm
    template_name = 'masters/fabric_form.html'
    success_url = reverse_lazy('masters:fabric_list')

    def form_valid(self, form):
        messages.success(self.request, "Fabric updated successfully.")
        return super().form_valid(form)

class FabricDeleteView(LoginRequiredMixin, ModulePermissionMixin, DeleteView):
    permission_required = 'accounts.can_view_masters'
    model = Fabric
    success_url = reverse_lazy('masters:fabric_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Fabric deleted successfully.")
        return super().delete(request, *args, **kwargs)