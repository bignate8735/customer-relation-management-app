from django.contrib import admin
from .models import *

# Register your models here.
# admin.py
from django.contrib import admin
from .models import (
    Customer, Company, Lead, Interaction,
    CustomerNote, Task, Tag, CustomerTag
)

admin.site.register(Customer)
admin.site.register(Company)
admin.site.register(Lead)
admin.site.register(Interaction)
admin.site.register(CustomerNote)
admin.site.register(Task)
admin.site.register(Tag)
admin.site.register(CustomerTag)

