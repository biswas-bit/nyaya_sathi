from django.contrib import admin
from .models import ChatHistory

class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'short_message', 'short_response', 'is_user_message', 'created_at')
    list_filter = ('is_user_message', 'created_at', 'user')
    search_fields = ('message', 'response', 'user__username')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 25
    
    fieldsets = (
        (None, {
            'fields': ('user', 'session_key', 'created_at')
        }),
        ('Message Details', {
            'fields': ('message', 'response', 'is_user_message'),
            'classes': ('wide',)
        }),
    )
    
    def short_message(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    short_message.short_description = 'Message'
    
    def short_response(self, obj):
        if obj.response:
            return obj.response[:50] + '...' if len(obj.response) > 50 else obj.response
        return '-'
    short_response.short_description = 'Response'

admin.site.register(ChatHistory, ChatHistoryAdmin)
