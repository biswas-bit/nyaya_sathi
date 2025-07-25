from django.contrib import admin
from .models import FIRReport

@admin.register(FIRReport)
class FIRReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'contact', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'contact']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'contact', 'address')
        }),
        ('Report Details', {
            'fields': ('description', 'evidence_image')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
