from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db import transaction
from django.db.models import Q, Sum
from django.http import JsonResponse
from accounts.views import ModulePermissionMixin

from .models import (
    GreigeStock, Dispatch, DispatchSpecification, TransitStock,
    ProcessingReceiving, ProcessingReceivingGrade, FinishedStock
)
from .forms import (
    DispatchForm, DispatchSpecificationFormSet,
    ProcessingReceivingForm, ProcessingReceivingGradeFormSet
)


# ========== Greige Stock ==========
class GreigeStockListView(LoginRequiredMixin, ListView):
    permission_required = 'accounts.can_view_inventory'
    model = GreigeStock
    template_name = 'inventory/greige_stock.html'
    context_object_name = 'stocks'
    paginate_by = 15

    def get_queryset(self):
        self.update_stock()
        queryset = GreigeStock.objects.select_related('fabric', 'manufacturer')
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(fabric__fabric_code__icontains=search) |
                Q(fabric__fabric_blend__icontains=search) |
                Q(manufacturer__manufacturer_name__icontains=search)
            )
        return queryset

    def update_stock(self):
        from purchase.models import PurchaseReceiving
        received_qs = PurchaseReceiving.objects.values(
            'purchase_order__fabric',
            'purchase_order__manufacturer'
        ).annotate(total_received=Sum('received_quantity'))

        for item in received_qs:
            fabric_id = item['purchase_order__fabric']
            manufacturer_id = item['purchase_order__manufacturer']
            total = item['total_received'] or 0

            stock, created = GreigeStock.objects.get_or_create(
                fabric_id=fabric_id,
                manufacturer_id=manufacturer_id,
                defaults={'current_stock': total}
            )
            if not created:
                stock.current_stock = total
                stock.save()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context


# ========== Dispatch for Dyeing ==========
class DispatchListView(LoginRequiredMixin, ListView):
    permission_required = 'accounts.can_view_inventory'
    model = Dispatch
    template_name = 'inventory/dispatch_list.html'
    context_object_name = 'dispatches'
    paginate_by = 10

    def get_queryset(self):
        queryset = Dispatch.objects.select_related('fabric', 'manufacturer')
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(dispatch_number__icontains=search) |
                Q(fabric__fabric_code__icontains=search) |
                Q(manufacturer__manufacturer_name__icontains=search) |
                Q(dispatch_date__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context


class DispatchCreateView(LoginRequiredMixin, CreateView):
    permission_required = 'accounts.can_view_inventory'
    model = Dispatch
    form_class = DispatchForm
    template_name = 'inventory/dispatch_form.html'
    success_url = reverse_lazy('inventory:dispatch_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['spec_formset'] = DispatchSpecificationFormSet(self.request.POST)
        else:
            data['spec_formset'] = DispatchSpecificationFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        spec_formset = context['spec_formset']
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.created_by = self.request.user
            self.object.save()

            spec_formset.instance = self.object
            if spec_formset.is_valid():
                spec_formset.save()
            else:
                return self.form_invalid(form)

            greige = GreigeStock.objects.get(
                fabric=self.object.fabric,
                manufacturer=self.object.manufacturer
            )
            greige.current_stock -= self.object.dispatch_quantity
            greige.save()

            transit, created = TransitStock.objects.get_or_create(
                fabric=self.object.fabric,
                manufacturer=self.object.manufacturer,
                defaults={'quantity': 0}
            )
            transit.quantity += self.object.dispatch_quantity
            transit.save()

            messages.success(self.request, "Dispatch created successfully.")
            return redirect(self.success_url)


class DispatchUpdateView(LoginRequiredMixin, UpdateView):
    permission_required = 'accounts.can_view_inventory'
    model = Dispatch
    form_class = DispatchForm
    template_name = 'inventory/dispatch_form.html'
    success_url = reverse_lazy('inventory:dispatch_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['spec_formset'] = DispatchSpecificationFormSet(self.request.POST, instance=self.object)
        else:
            data['spec_formset'] = DispatchSpecificationFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        spec_formset = context['spec_formset']
        with transaction.atomic():
            original = Dispatch.objects.get(pk=self.object.pk)
            self.object = form.save()

            spec_formset.instance = self.object
            if spec_formset.is_valid():
                spec_formset.save()
            else:
                return self.form_invalid(form)

            qty_diff = self.object.dispatch_quantity - original.dispatch_quantity
            if qty_diff != 0:
                greige = GreigeStock.objects.get(
                    fabric=self.object.fabric,
                    manufacturer=self.object.manufacturer
                )
                greige.current_stock -= qty_diff
                greige.save()

                transit = TransitStock.objects.get(
                    fabric=self.object.fabric,
                    manufacturer=self.object.manufacturer
                )
                transit.quantity += qty_diff
                transit.save()

            messages.success(self.request, "Dispatch updated successfully.")
            return redirect(self.success_url)


class DispatchDeleteView(LoginRequiredMixin, DeleteView):
    permission_required = 'accounts.can_view_inventory'
    model = Dispatch
    success_url = reverse_lazy('inventory:dispatch_list')

    def delete(self, request, *args, **kwargs):
        dispatch = self.get_object()
        with transaction.atomic():
            greige = GreigeStock.objects.get(
                fabric=dispatch.fabric,
                manufacturer=dispatch.manufacturer
            )
            greige.current_stock += dispatch.dispatch_quantity
            greige.save()

            transit = TransitStock.objects.get(
                fabric=dispatch.fabric,
                manufacturer=dispatch.manufacturer
            )
            transit.quantity -= dispatch.dispatch_quantity
            transit.save()

            dispatch.delete()
        messages.success(self.request, "Dispatch deleted successfully.")
        return redirect(self.success_url)


class DispatchPrintView(LoginRequiredMixin, DetailView):
    permission_required = 'accounts.can_view_inventory'
    model = Dispatch
    template_name = 'inventory/dispatch_print.html'
    context_object_name = 'dispatch'


# ========== Processing In Transit ==========
class ProcessingTransitListView(LoginRequiredMixin, ListView):
    permission_required = 'accounts.can_view_inventory'
    model = Dispatch
    template_name = 'inventory/processing_transit.html'
    context_object_name = 'dispatches'
    paginate_by = 10

    def get_queryset(self):
        queryset = Dispatch.objects.filter(status='in_transit').select_related('fabric', 'manufacturer')
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(dispatch_number__icontains=search) |
                Q(fabric__fabric_code__icontains=search) |
                Q(manufacturer__manufacturer_name__icontains=search) |
                Q(dispatch_date__icontains=search) |
                Q(status__icontains=search)
            )
        status_filter = self.request.GET.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['selected_status'] = self.request.GET.get('status', '')
        return context


# ========== Processing Receiving ==========
class ProcessingReceivingListView(LoginRequiredMixin, ListView):
    permission_required = 'accounts.can_view_inventory'
    model = ProcessingReceiving
    template_name = 'inventory/processing_receiving_list.html'
    context_object_name = 'receivings'
    paginate_by = 10

    def get_queryset(self):
        queryset = ProcessingReceiving.objects.select_related('dispatch', 'dispatch__fabric', 'dispatch__manufacturer')
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(receiving_number__icontains=search) |
                Q(dispatch__dispatch_number__icontains=search) |
                Q(dispatch__fabric__fabric_code__icontains=search) |
                Q(dispatch__manufacturer__manufacturer_name__icontains=search) |
                Q(receiving_date__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context


class ProcessingReceivingCreateView(LoginRequiredMixin, CreateView):
    permission_required = 'accounts.can_view_inventory'
    model = ProcessingReceiving
    form_class = ProcessingReceivingForm
    template_name = 'inventory/processing_receiving_form.html'
    success_url = reverse_lazy('inventory:processing_receiving_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['grade_formset'] = ProcessingReceivingGradeFormSet(self.request.POST)
        else:
            data['grade_formset'] = ProcessingReceivingGradeFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        grade_formset = context['grade_formset']
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.created_by = self.request.user
            self.object.save()

            grade_formset.instance = self.object
            if grade_formset.is_valid():
                grade_formset.save()
            else:
                return self.form_invalid(form)

            # Compute totals
            total_received = 0
            total_loss = 0
            total_gain = 0
            for grade in self.object.grades.all():
                total_received += grade.received_qty
                total_loss += grade.loss
                total_gain += grade.gain
            self.object.total_received = total_received
            self.object.total_loss = total_loss
            self.object.total_gain = total_gain
            self.object.save()

            # Update Transit Stock
            transit = TransitStock.objects.get(
                fabric=self.object.dispatch.fabric,
                manufacturer=self.object.dispatch.manufacturer
            )
            transit.quantity -= self.object.dispatch.dispatch_quantity
            transit.save()

            # ========== UPDATED Finished Stock logic ==========
            for grade in self.object.grades.all():
                finished, created = FinishedStock.objects.get_or_create(
                    fabric=self.object.dispatch.fabric,
                    manufacturer=self.object.dispatch.manufacturer,
                    color=grade.color,
                    defaults={'grade_a': 0, 'grade_b': 0, 'cp': 0}
                )
                finished.grade_a += grade.grade_a
                finished.grade_b += grade.grade_b
                finished.cp += grade.cp
                finished.save()
            # ==================================================

            # Update Dispatch status
            dispatch = self.object.dispatch
            dispatch.status = 'returned'
            dispatch.save()

            messages.success(self.request, "Processing Receiving created successfully.")
            return redirect(self.success_url)


class ProcessingReceivingUpdateView(LoginRequiredMixin, UpdateView):
    permission_required = 'accounts.can_view_inventory'
    model = ProcessingReceiving
    form_class = ProcessingReceivingForm
    template_name = 'inventory/processing_receiving_form.html'
    success_url = reverse_lazy('inventory:processing_receiving_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['grade_formset'] = ProcessingReceivingGradeFormSet(self.request.POST, instance=self.object)
        else:
            data['grade_formset'] = ProcessingReceivingGradeFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        grade_formset = context['grade_formset']
        with transaction.atomic():
            # Revert old stock
            old = ProcessingReceiving.objects.get(pk=self.object.pk)
            # Revert transit
            transit = TransitStock.objects.get(
                fabric=old.dispatch.fabric,
                manufacturer=old.dispatch.manufacturer
            )
            transit.quantity += old.dispatch.dispatch_quantity
            transit.save()

            # Revert finished stock (per color)
            for grade in old.grades.all():
                finished = FinishedStock.objects.get(
                    fabric=old.dispatch.fabric,
                    manufacturer=old.dispatch.manufacturer,
                    color=grade.color
                )
                finished.grade_a -= grade.grade_a
                finished.grade_b -= grade.grade_b
                finished.cp -= grade.cp
                finished.save()

            # Apply new receiving
            self.object = form.save()
            grade_formset.instance = self.object
            if grade_formset.is_valid():
                grade_formset.save()
            else:
                return self.form_invalid(form)

            # Recompute totals
            total_received = 0
            total_loss = 0
            total_gain = 0
            for grade in self.object.grades.all():
                total_received += grade.received_qty
                total_loss += grade.loss
                total_gain += grade.gain
            self.object.total_received = total_received
            self.object.total_loss = total_loss
            self.object.total_gain = total_gain
            self.object.save()

            # Update Transit Stock (decrease)
            transit = TransitStock.objects.get(
                fabric=self.object.dispatch.fabric,
                manufacturer=self.object.dispatch.manufacturer
            )
            transit.quantity -= self.object.dispatch.dispatch_quantity
            transit.save()

            # Update Finished Stock (per color)
            for grade in self.object.grades.all():
                finished, created = FinishedStock.objects.get_or_create(
                    fabric=self.object.dispatch.fabric,
                    manufacturer=self.object.dispatch.manufacturer,
                    color=grade.color,
                    defaults={'grade_a': 0, 'grade_b': 0, 'cp': 0}
                )
                finished.grade_a += grade.grade_a
                finished.grade_b += grade.grade_b
                finished.cp += grade.cp
                finished.save()

            # Update Dispatch status
            dispatch = self.object.dispatch
            dispatch.status = 'returned'
            dispatch.save()

            messages.success(self.request, "Processing Receiving updated successfully.")
            return redirect(self.success_url)


class ProcessingReceivingDeleteView(LoginRequiredMixin, DeleteView):
    permission_required = 'accounts.can_view_inventory'
    model = ProcessingReceiving
    success_url = reverse_lazy('inventory:processing_receiving_list')

    def delete(self, request, *args, **kwargs):
        receiving = self.get_object()
        with transaction.atomic():
            # Revert transit
            transit = TransitStock.objects.get(
                fabric=receiving.dispatch.fabric,
                manufacturer=receiving.dispatch.manufacturer
            )
            transit.quantity += receiving.dispatch.dispatch_quantity
            transit.save()

            # Revert finished stock
            for grade in receiving.grades.all():
                finished = FinishedStock.objects.get(
                    fabric=receiving.dispatch.fabric,
                    manufacturer=receiving.dispatch.manufacturer,
                    color=grade.color
                )
                finished.grade_a -= grade.grade_a
                finished.grade_b -= grade.grade_b
                finished.cp -= grade.cp
                finished.save()

            # Revert dispatch status
            dispatch = receiving.dispatch
            dispatch.status = 'in_transit'
            dispatch.save()

            receiving.delete()
        messages.success(self.request, "Processing Receiving deleted successfully.")
        return redirect(self.success_url)


class ProcessingReceivingPrintView(LoginRequiredMixin, DetailView):
    permission_required = 'accounts.can_view_inventory'
    model = ProcessingReceiving
    template_name = 'inventory/processing_receiving_print.html'
    context_object_name = 'receiving'


# ========== AJAX for Dispatch Colors ==========
def get_dispatch_colors(request):
    dispatch_id = request.GET.get('dispatch_id')
    if not dispatch_id:
        return JsonResponse({})
    try:
        dispatch = Dispatch.objects.get(pk=dispatch_id)
        data = {
            'dispatch_number': dispatch.dispatch_number,
            'dispatch_date': dispatch.dispatch_date.strftime('%Y-%m-%d'),
            'manufacturer': dispatch.manufacturer.manufacturer_name,
            'fabric': dispatch.fabric.fabric_code,
            'fabric_blend': dispatch.fabric.fabric_blend,
            'dispatch_quantity': float(dispatch.dispatch_quantity),
            'color': dispatch.color or '',
        }
        return JsonResponse(data)
    except Dispatch.DoesNotExist:
        return JsonResponse({})


# ========== Finished Stock View (NEW) ==========
class FinishedStockListView(LoginRequiredMixin, ListView):
    permission_required = 'accounts.can_view_inventory'
    model = FinishedStock
    template_name = 'inventory/finished_stock.html'
    context_object_name = 'stocks'
    paginate_by = 15

    def get_queryset(self):
        queryset = FinishedStock.objects.select_related('fabric', 'manufacturer')
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(fabric__fabric_code__icontains=search) |
                Q(fabric__fabric_blend__icontains=search) |
                Q(manufacturer__manufacturer_name__icontains=search) |
                Q(color__icontains=search)
            )
        fabric_filter = self.request.GET.get('fabric')
        if fabric_filter:
            queryset = queryset.filter(fabric__id=fabric_filter)
        manufacturer_filter = self.request.GET.get('manufacturer')
        if manufacturer_filter:
            queryset = queryset.filter(manufacturer__id=manufacturer_filter)
        color_filter = self.request.GET.get('color')
        if color_filter:
            queryset = queryset.filter(color__icontains=color_filter)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['fabric_filter'] = self.request.GET.get('fabric', '')
        context['manufacturer_filter'] = self.request.GET.get('manufacturer', '')
        context['color_filter'] = self.request.GET.get('color', '')
        from masters.models import Fabric, Manufacturer
        context['fabrics'] = Fabric.objects.all().order_by('fabric_code')
        context['manufacturers'] = Manufacturer.objects.all().order_by('manufacturer_name')
        return context