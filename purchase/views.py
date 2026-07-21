from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from accounts.views import ModulePermissionMixin
from .models import PurchaseOrder, PurchaseReceiving
from .forms import PurchaseOrderForm, PurchaseReceivingForm
from masters.models import Fabric


# ========== PURCHASE ORDER VIEWS ==========
class PurchaseOrderListView(LoginRequiredMixin, ModulePermissionMixin, ListView):
    permission_required = 'accounts.can_view_purchase'
    model = PurchaseOrder
    template_name = 'purchase/purchase_order_list.html'
    context_object_name = 'purchase_orders'
    paginate_by = 10

    def get_queryset(self):
        queryset = PurchaseOrder.objects.select_related(
            'manufacturer', 'buying_house', 'agent', 'fabric', 'created_by'
        )
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(po_number__icontains=search) |
                Q(manufacturer__manufacturer_name__icontains=search) |
                Q(buying_house__buying_house_name__icontains=search) |
                Q(agent__agent_name__icontains=search) |
                Q(status__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context

class PurchaseOrderCreateView(LoginRequiredMixin, ModulePermissionMixin, CreateView):
    permission_required = 'accounts.can_view_purchase'
    model = PurchaseOrder
    form_class = PurchaseOrderForm
    template_name = 'purchase/purchase_order_form.html'
    success_url = reverse_lazy('purchase:po_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Purchase Order created successfully.")
        return super().form_valid(form)

class PurchaseOrderUpdateView(LoginRequiredMixin, ModulePermissionMixin, UpdateView):
    permission_required = 'accounts.can_view_purchase'
    model = PurchaseOrder
    form_class = PurchaseOrderForm
    template_name = 'purchase/purchase_order_form.html'
    success_url = reverse_lazy('purchase:po_list')

    def form_valid(self, form):
        messages.success(self.request, "Purchase Order updated successfully.")
        return super().form_valid(form)

class PurchaseOrderDeleteView(LoginRequiredMixin, ModulePermissionMixin, DeleteView):
    permission_required = 'accounts.can_view_purchase'
    model = PurchaseOrder
    success_url = reverse_lazy('purchase:po_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Purchase Order deleted successfully.")
        return super().delete(request, *args, **kwargs)

class PurchaseOrderPrintView(LoginRequiredMixin, ModulePermissionMixin, DetailView):
    permission_required = 'accounts.can_view_purchase'
    model = PurchaseOrder
    template_name = 'purchase/purchase_order_print.html'
    context_object_name = 'po'


# ========== PURCHASE RECEIVING VIEWS ==========
class PurchaseReceivingListView(LoginRequiredMixin, ModulePermissionMixin, ListView):
    permission_required = 'accounts.can_view_purchase'
    model = PurchaseReceiving
    template_name = 'purchase/purchase_receiving_list.html'
    context_object_name = 'receivings'
    paginate_by = 10

    def get_queryset(self):
        queryset = PurchaseReceiving.objects.select_related(
            'purchase_order', 'purchase_order__manufacturer', 'purchase_order__fabric', 'created_by'
        )
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(receiving_number__icontains=search) |
                Q(purchase_order__po_number__icontains=search) |
                Q(purchase_order__manufacturer__manufacturer_name__icontains=search) |
                Q(purchase_order__fabric__fabric_code__icontains=search) |
                Q(receive_date__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context

class PurchaseReceivingCreateView(LoginRequiredMixin, ModulePermissionMixin, CreateView):
    permission_required = 'accounts.can_view_purchase'
    model = PurchaseReceiving
    form_class = PurchaseReceivingForm
    template_name = 'purchase/purchase_receiving_form.html'
    success_url = reverse_lazy('purchase:receiving_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Receiving saved successfully.")
        return super().form_valid(form)

class PurchaseReceivingUpdateView(LoginRequiredMixin, ModulePermissionMixin, UpdateView):
    permission_required = 'accounts.can_view_purchase'
    model = PurchaseReceiving
    form_class = PurchaseReceivingForm
    template_name = 'purchase/purchase_receiving_form.html'
    success_url = reverse_lazy('purchase:receiving_list')

    def form_valid(self, form):
        messages.success(self.request, "Receiving updated successfully.")
        return super().form_valid(form)

class PurchaseReceivingDeleteView(LoginRequiredMixin, ModulePermissionMixin, DeleteView):
    permission_required = 'accounts.can_view_purchase'
    model = PurchaseReceiving
    success_url = reverse_lazy('purchase:receiving_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Receiving deleted successfully.")
        return super().delete(request, *args, **kwargs)

class PurchaseReceivingPrintView(LoginRequiredMixin, ModulePermissionMixin, DetailView):
    permission_required = 'accounts.can_view_purchase'
    model = PurchaseReceiving
    template_name = 'purchase/purchase_receiving_print.html'
    context_object_name = 'receiving'


# ========== AJAX VIEWS ==========
def get_fabric_details(request):
    fabric_id = request.GET.get('fabric_id')
    if fabric_id:
        try:
            fabric = Fabric.objects.get(pk=fabric_id)
            data = {
                'fabric_blend': fabric.fabric_blend,
                'fabric_quality': fabric.fabric_quality,
                'warp': fabric.warp,
                'weft': fabric.weft,
                'ends': fabric.ends,
                'picks': fabric.picks,
                'weave': fabric.weave,
                'greige_width_on_loom': str(fabric.greige_width_on_loom) if fabric.greige_width_on_loom else '',
                'greige_width_off_loom': str(fabric.greige_width_off_loom) if fabric.greige_width_off_loom else '',
                'selvedge_type': fabric.selvedge_type or '',
                'unit': fabric.get_unit_display(),
            }
            return JsonResponse(data)
        except Fabric.DoesNotExist:
            return JsonResponse({})
    return JsonResponse({})

def get_po_details(request):
    po_id = request.GET.get('po_id')
    if po_id:
        try:
            po = PurchaseOrder.objects.select_related('manufacturer', 'buying_house', 'agent', 'fabric').get(pk=po_id)
            total_received = PurchaseReceiving.get_total_received(po)
            remaining = po.order_quantity - total_received
            data = {
                'po_number': po.po_number,
                'po_date': po.po_date.strftime('%Y-%m-%d'),
                'manufacturer': po.manufacturer.manufacturer_name,
                'buying_house': po.buying_house.buying_house_name,
                'agent': po.agent.agent_name if po.agent else '-',
                'fabric_code': po.fabric.fabric_code,
                'fabric_blend': po.fabric.fabric_blend,
                'fabric_quality': po.fabric.fabric_quality,
                'warp': po.fabric.warp,
                'weft': po.fabric.weft,
                'ends': po.fabric.ends,
                'picks': po.fabric.picks,
                'weave': po.fabric.weave,
                'unit': po.fabric.get_unit_display(),
                'order_quantity': float(po.order_quantity),
                'total_received': float(total_received),
                'remaining': float(remaining),
            }
            return JsonResponse(data)
        except PurchaseOrder.DoesNotExist:
            return JsonResponse({})
    return JsonResponse({})