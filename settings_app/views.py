import os
import json
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.conf import settings
from django.http import FileResponse
from django.core.management import call_command
from .models import CompanyInfo, InvoiceSettings, AppearanceSettings
from .forms import CompanyInfoForm, InvoiceSettingsForm, AppearanceSettingsForm

@staff_member_required
def settings_view(request):
    company, _ = CompanyInfo.objects.get_or_create(pk=1)
    invoice, _ = InvoiceSettings.objects.get_or_create(pk=1)
    appearance, _ = AppearanceSettings.objects.get_or_create(pk=1)

    if request.method == 'POST':
        company_form = CompanyInfoForm(request.POST, request.FILES, instance=company)
        invoice_form = InvoiceSettingsForm(request.POST, instance=invoice)
        appearance_form = AppearanceSettingsForm(request.POST, instance=appearance)

        if company_form.is_valid() and invoice_form.is_valid() and appearance_form.is_valid():
            company_form.save()
            invoice_form.save()
            appearance_form.save()
            messages.success(request, "Settings updated successfully.")
            return redirect('settings:settings')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        company_form = CompanyInfoForm(instance=company)
        invoice_form = InvoiceSettingsForm(instance=invoice)
        appearance_form = AppearanceSettingsForm(instance=appearance)

    import django
    import sys
    system_info = {
        'software_version': '1.0.0',
        'django_version': django.get_version(),
        'python_version': sys.version.split()[0],
        'database_type': 'MySQL',
        'database_name': settings.DATABASES['default']['NAME'],
        'server_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }

    context = {
        'company_form': company_form,
        'invoice_form': invoice_form,
        'appearance_form': appearance_form,
        'system_info': system_info,
        'company': company,
    }
    return render(request, 'settings/settings.html', context)


@staff_member_required
def backup_database(request):
    if request.method == 'POST':
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"backup_{timestamp}.json"
        filepath = os.path.join(backup_dir, filename)

        try:
            with open(filepath, 'w') as f:
                call_command('dumpdata', exclude=['contenttypes', 'auth.permission', 'sessions'], stdout=f)
            messages.success(request, f"Backup created successfully: {filename}")
        except Exception as e:
            messages.error(request, f"Backup failed: {str(e)}")
        return redirect('settings:settings')
    return redirect('settings:settings')


@staff_member_required
def download_backup(request, filename):
    backup_dir = os.path.join(settings.BASE_DIR, 'backups')
    filepath = os.path.join(backup_dir, filename)
    if os.path.exists(filepath):
        return FileResponse(open(filepath, 'rb'), as_attachment=True, filename=filename)
    else:
        messages.error(request, "Backup file not found.")
        return redirect('settings:settings')


@staff_member_required
def backup_history(request):
    backup_dir = os.path.join(settings.BASE_DIR, 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    files = []
    for f in os.listdir(backup_dir):
        if f.endswith('.json'):
            filepath = os.path.join(backup_dir, f)
            size = os.path.getsize(filepath)
            modified = datetime.fromtimestamp(os.path.getmtime(filepath))
            files.append({'name': f, 'size': size, 'modified': modified})
    files.sort(key=lambda x: x['modified'], reverse=True)
    context = {'backup_files': files}
    return render(request, 'settings/backup_history.html', context)


@staff_member_required
def restore_database(request):
    if request.method == 'POST' and request.FILES.get('backup_file'):
        uploaded = request.FILES['backup_file']
        if not uploaded.name.endswith('.json'):
            messages.error(request, "Only JSON backup files are allowed.")
            return redirect('settings:restore')

        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        temp_path = os.path.join(backup_dir, 'temp_restore.json')
        with open(temp_path, 'wb+') as dest:
            for chunk in uploaded.chunks():
                dest.write(chunk)

        try:
            call_command('flush', interactive=False, verbosity=0)
            call_command('loaddata', temp_path, verbosity=0)
            messages.success(request, "Database restored successfully.")
        except Exception as e:
            messages.error(request, f"Restore failed: {str(e)}")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        return redirect('settings:settings')

    return render(request, 'settings/restore.html')


@staff_member_required
def delete_backup(request, filename):
    if request.method == 'POST':
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        filepath = os.path.join(backup_dir, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            messages.success(request, f"Backup {filename} deleted.")
        else:
            messages.error(request, "File not found.")
    return redirect('settings:backup_history')