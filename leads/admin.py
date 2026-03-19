from django.contrib import admin

from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'source', 'status', 'budget', 'created_at')
    list_filter = ('status', 'source', 'created_at')
    search_fields = ('full_name', 'phone', 'email', 'company', 'comment')
    readonly_fields = ('created_at', 'updated_at')
