from django.contrib import admin
from dashapp.models import Customer, Project


@admin.register(Customer)
class Product(admin.ModelAdmin):
     pass

@admin.register(Project)
class Project(admin.ModelAdmin):
     pass
