from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer, Company, Lead, Interaction, CustomerNote, Task


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ['created_by']  # assuming this is set automatically in the view
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter customer address'}),
        }


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ['created_by']  # assuming you want to associate this with the logged-in user


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        exclude = ['created_by']  # optionally exclude or include fields depending on use case
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter lead notes'}),
        }


class InteractionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        exclude = ['created_by']  # again assuming this is handled in the view
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe the interaction'}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class CustomerNoteForm(forms.ModelForm):
    class Meta:
        model = CustomerNote
        exclude = ['created_by']
        widgets = {
            'note': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Add a note about the customer'}),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['created_by']  # assuming tasks are user-specific
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Task description'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }