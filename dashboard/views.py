# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from django.db.models import Sum, Count, Q
# from django.utils import timezone
# from datetime import datetime, timedelta
# from purchase.models import PurchaseOrder, PurchaseReceiving
# from inventory.models import GreigeStock, Dispatch, TransitStock
# from masters.models import Fabric

# @login_required(login_url='accounts:login')
# def dashboard_view(request):
#     today = timezone.now().date()
#     first_day_of_month = today.replace(day=1)

#     # ---------- Summary Cards ----------
#     # Today's Purchase Receiving (sum of received_quantity for today)
#     today_receiving = PurchaseReceiving.objects.filter(
#         receive_date=today
#     ).aggregate(total=Sum('received_quantity'))['total'] or 0

#     # Today's Purchase (we treat Today's Purchase as Today's Receiving)
#     today_purchase = today_receiving

#     # Greige Stock (sum of current_stock across all fabrics)
#     greige_stock = GreigeStock.objects.aggregate(total=Sum('current_stock'))['total'] or 0

#     # Processing Stock (we can use TransitStock as "processing" for now)
#     processing_stock = TransitStock.objects.aggregate(total=Sum('quantity'))['total'] or 0

#     # Finished Stock (not implemented yet; we'll keep dummy or 0)
#     finished_stock = 0  # To be implemented later

#     # Pending Purchase Orders (status = 'pending' or 'draft')
#     pending_po = PurchaseOrder.objects.filter(
#         Q(status='pending') | Q(status='draft')
#     ).count()

#     # Pending Dispatch (status = 'pending')
#     pending_dispatch = Dispatch.objects.filter(status='pending').count()

#     # Today's Sales (if you have Sales model, otherwise dummy)
#     # For now, we'll compute from Dispatch? Or keep dummy.
#     today_sales = 0  # To be implemented later

#     # ---------- Monthly Purchase Chart (last 6 months) ----------
#     month_labels = []
#     purchase_data = []
#     today = timezone.now().date()
#     for i in range(6, -1, -1):  # last 7 months including current
#         month_date = today.replace(day=1) - timedelta(days=30*i)
#         # Adjust to start of month
#         month_start = month_date.replace(day=1)
#         # End of month
#         if month_start.month == 12:
#             month_end = month_start.replace(year=month_start.year+1, month=1, day=1) - timedelta(days=1)
#         else:
#             month_end = month_start.replace(month=month_start.month+1, day=1) - timedelta(days=1)
#         month_total = PurchaseReceiving.objects.filter(
#             receive_date__gte=month_start,
#             receive_date__lte=month_end
#         ).aggregate(total=Sum('received_quantity'))['total'] or 0
#         month_labels.append(month_start.strftime('%b'))
#         purchase_data.append(float(month_total))

#     # ---------- Monthly Sales Chart (if no Sales model, use Dispatch quantity as proxy) ----------
#     # We'll use Dispatch quantity for now (or you can adjust later)
#     sales_data = []
#     for i in range(6, -1, -1):
#         month_date = today.replace(day=1) - timedelta(days=30*i)
#         month_start = month_date.replace(day=1)
#         if month_start.month == 12:
#             month_end = month_start.replace(year=month_start.year+1, month=1, day=1) - timedelta(days=1)
#         else:
#             month_end = month_start.replace(month=month_start.month+1, day=1) - timedelta(days=1)
#         month_total = Dispatch.objects.filter(
#             dispatch_date__gte=month_start,
#             dispatch_date__lte=month_end
#         ).aggregate(total=Sum('dispatch_quantity'))['total'] or 0
#         sales_data.append(float(month_total))

#     # ---------- Stock Overview Chart ----------
#     # Get current stock values for Greige, Processing (Transit), Finished (0 for now)
#     greige_total = GreigeStock.objects.aggregate(total=Sum('current_stock'))['total'] or 0
#     transit_total = TransitStock.objects.aggregate(total=Sum('quantity'))['total'] or 0
#     finished_total = 0  # to be implemented
#     stock_labels = ['Greige', 'Processing', 'Finished']
#     stock_values = [float(greige_total), float(transit_total), float(finished_total)]

#     # ---------- Recent Activity Tables (latest records) ----------
#     latest_purchases = PurchaseReceiving.objects.select_related(
#         'purchase_order', 'purchase_order__manufacturer'
#     ).order_by('-receive_date')[:5]
#     latest_receivings = PurchaseReceiving.objects.select_related(
#         'purchase_order', 'purchase_order__manufacturer'
#     ).order_by('-receive_date')[:5]
#     latest_dispatch = Dispatch.objects.select_related(
#         'fabric', 'manufacturer'
#     ).order_by('-dispatch_date')[:5]
#     latest_sales = []  # to be implemented

#     # Format for template
#     latest_purchases_list = []
#     for rec in latest_purchases:
#         latest_purchases_list.append({
#             'po_no': rec.purchase_order.po_number,
#             'supplier': rec.purchase_order.manufacturer.manufacturer_name,
#             'date': rec.receive_date.strftime('%Y-%m-%d'),
#             'amount': float(rec.received_quantity),
#         })

#     latest_receivings_list = []
#     for rec in latest_receivings:
#         latest_receivings_list.append({
#             'grn_no': rec.receiving_number,
#             'supplier': rec.purchase_order.manufacturer.manufacturer_name,
#             'date': rec.receive_date.strftime('%Y-%m-%d'),
#             'qty': float(rec.received_quantity),
#         })

#     latest_dispatch_list = []
#     for d in latest_dispatch:
#         latest_dispatch_list.append({
#             'dispatch_no': d.dispatch_number,
#             'customer': d.manufacturer.manufacturer_name,  # or maybe customer? we use manufacturer
#             'date': d.dispatch_date.strftime('%Y-%m-%d'),
#             'qty': float(d.dispatch_quantity),
#         })

#     latest_sales_list = []  # to be implemented

#     context = {
#         # Cards
#         'today_purchase': today_purchase,
#         'today_receiving': today_receiving,
#         'greige_stock': greige_stock,
#         'processing_stock': processing_stock,
#         'finished_stock': finished_stock,
#         'pending_purchase_orders': pending_po,
#         'pending_dispatch': pending_dispatch,
#         'today_sales': today_sales,

#         # Charts
#         'month_labels': month_labels,
#         'purchase_data': purchase_data,
#         'sales_data': sales_data,
#         'stock_labels': stock_labels,
#         'stock_values': stock_values,

#         # Tables
#         'latest_purchases': latest_purchases_list,
#         'latest_receiving': latest_receivings_list,
#         'latest_dispatch': latest_dispatch_list,
#         'latest_sales': latest_sales_list,
#     }
#     return render(request, 'dashboard/dashboard.html', context)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='accounts:login')
def dashboard_view(request):
    # Simplified version to avoid data errors
    context = {
        # Empty context – dashboard will show without data
        'today_purchase': 0,
        'today_receiving': 0,
        'greige_stock': 0,
        'processing_stock': 0,
        'finished_stock': 0,
        'pending_purchase_orders': 0,
        'pending_dispatch': 0,
        'today_sales': 0,
        'month_labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
        'purchase_data': [0, 0, 0, 0, 0, 0, 0],
        'sales_data': [0, 0, 0, 0, 0, 0, 0],
        'stock_labels': ['Greige', 'Processing', 'Finished'],
        'stock_values': [0, 0, 0],
        'latest_purchases': [],
        'latest_receiving': [],
        'latest_dispatch': [],
        'latest_sales': [],
    }
    return render(request, 'dashboard/dashboard.html', context)