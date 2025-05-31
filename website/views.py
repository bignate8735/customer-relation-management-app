from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Company, Customer, Lead, Task, Interaction
from .forms import CustomUserCreationForm, CustomerForm

# Dashboard view using class-based approach
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'website/dashboard.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)

        context['my_customers'] = Customer.objects.filter(assigned_to=user)
        context['my_leads'] = Lead.objects.filter(customer__assigned_to=user)
        context['my_tasks'] = Task.objects.filter(assigned_to=user)
        context['my_interactions'] = Interaction.objects.filter(created_by=user)

        # Summary counts
        context['customer_count'] = context['my_customers'].count()
        context['lead_count'] = context['my_leads'].count()
        context['task_count'] = context['my_tasks'].count()
        context['interaction_count'] = context['my_interactions'].count()

        return context

# Redundant @login_required removed
@login_required
def home(request):
    customers = Customer.objects.filter(assigned_to=request.user).order_by('-created_at')[:5]
    leads = Lead.objects.filter(created_by=request.user).order_by('-created_at')[:5]
    interactions = Interaction.objects.filter(created_by=request.user).order_by('-date')[:5]
    
    context = {
        'customers': customers,
        'leads': leads,
        'interactions': interactions,
    }
    return render(request, 'website/dashboard.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'website/register.html', {'form': form})

@login_required
def customer_list(request):
    customers = Customer.objects.filter(assigned_to=request.user)
    return render(request, 'website/dashboard.html', {'customers': customers})

@login_required
def customer_create(request):
    form = CustomerForm(request.POST or None)
    if form.is_valid():
        customer = form.save(commit=False)
        customer.assigned_to = request.user
        customer.save()
        return redirect('customer_list')
    return render(request, 'website/dashboard.html', {'form': form})

@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    form = CustomerForm(request.POST or None, instance=customer)
    if form.is_valid():
        form.save()
        return redirect('customer_list')
    return render(request, 'website/dashboard.html', {'form': form})


