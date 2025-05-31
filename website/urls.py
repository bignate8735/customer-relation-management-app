from django.urls import path
from .views import (
    home,
    login_user,
    logout_user,
    register_user,
    customer_list,
    customer_create,
    customer_edit,
    DashboardView,
)

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),

    # Dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # Customers
    path('customers/', customer_list, name='customer_list'),
    path('customers/new/', customer_create, name='customer_create'),
    path('customers/edit/<int:pk>/', customer_edit, name='customer_edit'),

    # Placeholder for future sections:
    # path('leads/', lead_list, name='lead_list'),
    # path('tasks/', task_list, name='task_list'),
    # path('interactions/', interaction_list, name='interaction_list'),
]