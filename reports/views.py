from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.http import HttpResponse
import csv

from purchase.models import PurchaseOrder, PurchaseReceiving
from inventory.models import GreigeStock, TransitStock, FinishedStock, Dispatch, ProcessingReceiving, ProcessingReceivingGrade
from sales.models import SalesInvoice
from masters.models import Fabric, Manufacturer
from .forms import (
    PurchaseReportFilterForm, ReceivingReportFilterForm, DispatchReportFilterForm,
    ProcessingReportFilterForm, StockReportFilterForm, SalesReportFilterForm
)


@login_required
def purchase_report(request):
    # Permission check
    if not request.user.has_perm('accounts.can_view_reports'):
        return render(request, 'accounts/permission_denied.html')

    form = PurchaseReportFilterForm(request.GET or None)
    data = []
    if form.is_valid():
        queryset = PurchaseOrder.objects.select_related('manufacturer', 'buying_house', 'agent', 'fabric')
        if form.cleaned_data.get('date_from'):
            queryset = queryset.filter(po_date__gte=form.cleaned_data['date_from'])
        if form.cleaned_data.get('date_to'):
            queryset = queryset.filter(po_date__lte=form.cleaned_data['date_to'])
        if form.cleaned_data.get('manufacturer'):
            queryset = queryset.filter(manufacturer_id=form.cleaned_data['manufacturer'])
        if form.cleaned_data.get('po_number'):
            queryset = queryset.filter(po_number__icontains=form.cleaned_data['po_number'])
        data = queryset
    context = {'form': form, 'data': data, 'report_type': 'Purchase'}
    return render(request, 'reports/purchase_reports.html', context)


@login_required
def receiving_report(request):
    if not request.user.has_perm('accounts.can_view_reports'):
        return render(request, 'accounts/permission_denied.html')

    form = ReceivingReportFilterForm(request.GET or None)
    data = []
    if form.is_valid():
        queryset = PurchaseReceiving.objects.select_related('purchase_order', 'purchase_order__manufacturer')
        if form.cleaned_data.get('date_from'):
            queryset = queryset.filter(receive_date__gte=form.cleaned_data['date_from'])
        if form.cleaned_data.get('date_to'):
            queryset = queryset.filter(receive_date__lte=form.cleaned_data['date_to'])
        if form.cleaned_data.get('po_number'):
            queryset = queryset.filter(purchase_order__po_number__icontains=form.cleaned_data['po_number'])
        data = queryset
    context = {'form': form, 'data': data, 'report_type': 'Receiving'}
    return render(request, 'reports/receiving_reports.html', context)


@login_required
def dispatch_report(request):
    if not request.user.has_perm('accounts.can_view_reports'):
        return render(request, 'accounts/permission_denied.html')

    form = DispatchReportFilterForm(request.GET or None)
    data = []
    if form.is_valid():
        queryset = Dispatch.objects.select_related('fabric', 'manufacturer')
        if form.cleaned_data.get('date_from'):
            queryset = queryset.filter(dispatch_date__gte=form.cleaned_data['date_from'])
        if form.cleaned_data.get('date_to'):
            queryset = queryset.filter(dispatch_date__lte=form.cleaned_data['date_to'])
        if form.cleaned_data.get('fabric'):
            queryset = queryset.filter(fabric_id=form.cleaned_data['fabric'])
        if form.cleaned_data.get('manufacturer'):
            queryset = queryset.filter(manufacturer_id=form.cleaned_data['manufacturer'])
        data = queryset
    context = {'form': form, 'data': data, 'report_type': 'Dispatch'}
    return render(request, 'reports/dispatch_reports.html', context)


@login_required
def processing_report(request):
    if not request.user.has_perm('accounts.can_view_reports'):
        return render(request, 'accounts/permission_denied.html')

    form = ProcessingReportFilterForm(request.GET or None)
    data = []
    report_type = 'Loss'
    if form.is_valid():
        report_type = form.cleaned_data.get('report_type', 'loss')
        queryset = ProcessingReceivingGrade.objects.select_related('receiving', 'receiving__dispatch')
        if form.cleaned_data.get('date_from'):
            queryset = queryset.filter(receiving__receiving_date__gte=form.cleaned_data['date_from'])
        if form.cleaned_data.get('date_to'):
            queryset = queryset.filter(receiving__receiving_date__lte=form.cleaned_data['date_to'])
        if report_type == 'loss':
            queryset = queryset.filter(loss__gt=0)
        elif report_type == 'gain':
            queryset = queryset.filter(gain__gt=0)
        data = queryset
    context = {'form': form, 'data': data, 'report_type': report_type.capitalize()}
    return render(request, 'reports/processing_reports.html', context)


@login_required
def stock_report(request):
    if not request.user.has_perm('accounts.can_view_reports'):
        return render(request, 'accounts/permission_denied.html')

    form = StockReportFilterForm(request.GET or None)
    data = []
    stock_type = 'greige'
    if form.is_valid():
        stock_type = form.cleaned_data.get('stock_type', 'greige')
        queryset = None
        if stock_type == 'greige':
            queryset = GreigeStock.objects.select_related('fabric', 'manufacturer')
        elif stock_type == 'transit':
            queryset = TransitStock.objects.select_related('fabric', 'manufacturer')
        elif stock_type == 'finished':
            queryset = FinishedStock.objects.select_related('fabric', 'manufacturer')
        if form.cleaned_data.get('fabric'):
            queryset = queryset.filter(fabric_id=form.cleaned_data['fabric'])
        if form.cleaned_data.get('color') and stock_type == 'finished':
            queryset = queryset.filter(color__icontains=form.cleaned_data['color'])
        data = queryset
    context = {'form': form, 'data': data, 'stock_type': stock_type, 'report_type': 'Stock'}
    return render(request, 'reports/stock_reports.html', context)


@login_required
def sales_report(request):
    if not request.user.has_perm('accounts.can_view_reports'):
        return render(request, 'accounts/permission_denied.html')

    form = SalesReportFilterForm(request.GET or None)
    data = []
    if form.is_valid():
        queryset = SalesInvoice.objects.select_related('created_by')
        if form.cleaned_data.get('date_from'):
            queryset = queryset.filter(invoice_date__gte=form.cleaned_data['date_from'])
        if form.cleaned_data.get('date_to'):
            queryset = queryset.filter(invoice_date__lte=form.cleaned_data['date_to'])
        if form.cleaned_data.get('customer'):
            queryset = queryset.filter(customer_name__icontains=form.cleaned_data['customer'])
        if form.cleaned_data.get('invoice'):
            queryset = queryset.filter(invoice_number__icontains=form.cleaned_data['invoice'])
        data = queryset
    context = {'form': form, 'data': data, 'report_type': 'Sales'}
    return render(request, 'reports/sales_reports.html', context)