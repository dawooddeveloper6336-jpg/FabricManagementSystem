from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db import transaction
from django.db.models import Q
from .models import SalesInvoice, SalesInvoiceItem
from .forms import SalesInvoiceForm, SalesInvoiceItemFormSet
from inventory.models import FinishedStock
from accounts.views import ModulePermissionMixin

class SalesInvoiceListView(LoginRequiredMixin, ListView):
    permission_required = 'accounts.can_view_sales'
    model = SalesInvoice
    template_name = 'sales/sales_invoice_list.html'
    context_object_name = 'invoices'
    paginate_by = 10

    def get_queryset(self):
        queryset = SalesInvoice.objects.select_related('created_by')
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(invoice_number__icontains=search) |
                Q(customer_name__icontains=search) |
                Q(invoice_date__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context


class SalesInvoiceCreateView(LoginRequiredMixin, CreateView):
    permission_required = 'accounts.can_view_sales'
    model = SalesInvoice
    form_class = SalesInvoiceForm
    template_name = 'sales/sales_invoice_form.html'
    success_url = reverse_lazy('sales:invoice_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['item_formset'] = SalesInvoiceItemFormSet(self.request.POST)
        else:
            data['item_formset'] = SalesInvoiceItemFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        item_formset = context['item_formset']
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.created_by = self.request.user
            self.object.save()

            item_formset.instance = self.object
            if item_formset.is_valid():
                item_formset.save()
            else:
                return self.form_invalid(form)

            # Recalculate total amount
            total = sum(item.amount for item in self.object.items.all())
            self.object.total_amount = total
            self.object.save()

            # Reduce Finished Stock
            for item in self.object.items.all():
                # Get the finished stock for this fabric+color
                try:
                    stock = FinishedStock.objects.get(fabric=item.fabric, color=item.color)
                    # Reduce the specific grade
                    if item.grade == 'A':
                        stock.grade_a -= item.quantity
                    elif item.grade == 'B':
                        stock.grade_b -= item.quantity
                    elif item.grade == 'C':
                        stock.cp -= item.quantity
                    stock.save()
                except FinishedStock.DoesNotExist:
                    # Should not happen because we validated availability in form
                    pass

            messages.success(self.request, "Sales Invoice created successfully.")
            return redirect(self.success_url)


class SalesInvoiceUpdateView(LoginRequiredMixin, UpdateView):
    permission_required = 'accounts.can_view_sales'
    model = SalesInvoice
    form_class = SalesInvoiceForm
    template_name = 'sales/sales_invoice_form.html'
    success_url = reverse_lazy('sales:invoice_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['item_formset'] = SalesInvoiceItemFormSet(self.request.POST, instance=self.object)
        else:
            data['item_formset'] = SalesInvoiceItemFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        item_formset = context['item_formset']
        with transaction.atomic():
            # Revert old stock
            old_invoice = SalesInvoice.objects.get(pk=self.object.pk)
            for old_item in old_invoice.items.all():
                try:
                    stock = FinishedStock.objects.get(fabric=old_item.fabric, color=old_item.color)
                    if old_item.grade == 'A':
                        stock.grade_a += old_item.quantity
                    elif old_item.grade == 'B':
                        stock.grade_b += old_item.quantity
                    elif old_item.grade == 'C':
                        stock.cp += old_item.quantity
                    stock.save()
                except FinishedStock.DoesNotExist:
                    pass

            self.object = form.save()
            item_formset.instance = self.object
            if item_formset.is_valid():
                item_formset.save()
            else:
                return self.form_invalid(form)

            # Apply new stock reductions
            for item in self.object.items.all():
                try:
                    stock = FinishedStock.objects.get(fabric=item.fabric, color=item.color)
                    if item.grade == 'A':
                        stock.grade_a -= item.quantity
                    elif item.grade == 'B':
                        stock.grade_b -= item.quantity
                    elif item.grade == 'C':
                        stock.cp -= item.quantity
                    stock.save()
                except FinishedStock.DoesNotExist:
                    pass

            total = sum(item.amount for item in self.object.items.all())
            self.object.total_amount = total
            self.object.save()

            messages.success(self.request, "Sales Invoice updated successfully.")
            return redirect(self.success_url)


class SalesInvoiceDeleteView(LoginRequiredMixin, DeleteView):
    permission_required = 'accounts.can_view_sales'
    model = SalesInvoice
    success_url = reverse_lazy('sales:invoice_list')

    def delete(self, request, *args, **kwargs):
        invoice = self.get_object()
        with transaction.atomic():
            # Revert stock
            for item in invoice.items.all():
                try:
                    stock = FinishedStock.objects.get(fabric=item.fabric, color=item.color)
                    if item.grade == 'A':
                        stock.grade_a += item.quantity
                    elif item.grade == 'B':
                        stock.grade_b += item.quantity
                    elif item.grade == 'C':
                        stock.cp += item.quantity
                    stock.save()
                except FinishedStock.DoesNotExist:
                    pass
            invoice.delete()
        messages.success(self.request, "Sales Invoice deleted successfully.")
        return redirect(self.success_url)


class SalesInvoicePrintView(LoginRequiredMixin, DetailView):
    permission_required = 'accounts.can_view_sales'
    model = SalesInvoice
    template_name = 'sales/sales_invoice_print.html'
    context_object_name = 'invoice'