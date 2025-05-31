from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    """Represents a company or organization."""
    name = models.CharField(max_length=255)
    website = models.URLField(blank=True)
    industry = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    """Represents an individual contact within a company."""
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='customers')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_customers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Lead(models.Model):
    """Represents a sales lead associated with a customer."""
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('lost', 'Lost'),
        ('converted', 'Converted'),
    ]

    source = models.CharField(max_length=100, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='leads')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    estimated_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_leads')

    def __str__(self):
        return f"Lead for {self.customer} [{self.status}]"


class Interaction(models.Model):
    """Logs an interaction or communication with a customer."""
    TYPE_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone Call'),
        ('meeting', 'Meeting'),
        ('other', 'Other'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='interactions')
    interaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    summary = models.TextField()
    date = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='interactions')

    def __str__(self):
        customer_name = str(self.customer) if self.customer else "Unknown"
        return f"{self.interaction_type.title()} with {customer_name} on {self.date.strftime('%Y-%m-%d')}"


class CustomerNote(models.Model):
    """Internal notes made by staff about a customer."""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='notes')
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='customer_notes')

    def __str__(self):
        customer_name = str(self.customer) if self.customer else "Unknown"
        return f"Note for {customer_name} ({self.created_at.strftime('%Y-%m-%d')})"


class Task(models.Model):
    """A task or reminder associated with a customer."""
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('done', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tasks')
    due_date = models.DateField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.priority})"


class Tag(models.Model):
    """Tag for categorizing customers."""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class CustomerTag(models.Model):
    """Linking table for customers and tags (many-to-many relationship)."""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tagged_customers')

    class Meta:
        unique_together = ('customer', 'tag')

    def __str__(self):
        return f"{self.customer} - {self.tag.name}"