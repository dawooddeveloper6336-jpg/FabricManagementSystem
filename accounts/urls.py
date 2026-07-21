from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),

    # User Management (Admin only)
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/add/', views.UserCreateView.as_view(), name='user_add'),
    path('users/edit/<int:pk>/', views.UserUpdateView.as_view(), name='user_edit'),
    path('users/delete/<int:pk>/', views.UserDeleteView.as_view(), name='user_delete'),
    path('users/toggle-status/<int:user_id>/', views.toggle_user_status, name='toggle_status'),
    path('users/reset-password/<int:user_id>/', views.reset_password_view, name='reset_password'),

    # Profile
    path('profile/', views.profile_view, name='profile'),
    path('change-password/', views.change_password_view, name='change_password'),
]