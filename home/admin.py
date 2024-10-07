from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(Tags)
admin.site.register(Author)

admin.site.register(Blog)
admin.site.register(Solution)

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'number', 'message')  # Display these fields in the admin list view
    search_fields = ('name', 'email')  # Add a search bar for these fields
    list_filter = ('name',)  # Enable filtering by name

admin.site.register(Contact, ContactAdmin)