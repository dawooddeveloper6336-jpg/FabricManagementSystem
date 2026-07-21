from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import User
from .forms import (
    LoginForm, ForgotPasswordForm, UserAddForm, UserEditForm,
    UserProfileForm, CustomPasswordChangeForm
)

# ---------- MIXIN FOR MODULE PERMISSIONS ----------
class ModulePermissionMixin(PermissionRequiredMixin):
    """Check if user has the required module permission."""
    permission_required = None

    def handle_no_permission(self):
        return render(self.request, 'accounts/permission_denied.html')

# ---------- Helper ----------
def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

# ---------- Authentication Views ----------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')
    if request.method == 'POST':
        form = LoginForm(data=request.POST)   # ✅ FIXED: no duplicate 'data'
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if remember_me:
                    request.session.set_expiry(1209600)
                else:
                    request.session.set_expiry(0)
                return redirect('dashboard:dashboard')
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            try:
                form.save(username)
                messages.success(request, "Password reset successfully. Please login with new password.")
                return redirect('accounts:login')
            except Exception as e:
                messages.error(request, str(e))
    else:
        form = ForgotPasswordForm()
    return render(request, 'accounts/forgot_password.html', {'form': form})


# ---------- User Management (Admin Only) ----------
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return is_admin(self.request.user)
    def handle_no_permission(self):
        return render(self.request, 'accounts/permission_denied.html')


class UserListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 15

    def get_queryset(self):
        queryset = User.objects.all().order_by('-created_at')
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(username__icontains=search) |
                Q(role__icontains=search) |
                Q(status__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context


class UserCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = User
    form_class = UserAddForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')

    def form_valid(self, form):
        messages.success(self.request, "User created successfully.")
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')

    def form_valid(self, form):
        messages.success(self.request, "User updated successfully.")
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('accounts:user_list')

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        if user == request.user:
            messages.error(request, "You cannot delete your own account.")
            return redirect('accounts:user_list')
        user.delete()
        messages.success(request, "User deleted successfully.")
        return redirect(self.success_url)


@login_required
@user_passes_test(is_admin, login_url='dashboard:dashboard')
def toggle_user_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user == request.user:
        messages.error(request, "You cannot change your own status.")
        return redirect('accounts:user_list')
    user.status = 'inactive' if user.status == 'active' else 'active'
    user.save()
    status_text = 'activated' if user.status == 'active' else 'deactivated'
    messages.success(request, f"User {status_text} successfully.")
    return redirect('accounts:user_list')


@login_required
@user_passes_test(is_admin, login_url='dashboard:dashboard')
def reset_password_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password reset successfully.")
            return redirect('accounts:user_list')
    else:
        form = CustomPasswordChangeForm(user)
    return render(request, 'accounts/change_password.html', {'form': form, 'target_user': user})


# ---------- Profile Views ----------
@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'accounts/user_profile.html', {'form': form, 'user': user})


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Password changed successfully.")
            return redirect('accounts:profile')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})