from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'security_question')  # Show in admin list view
    fields = ('user', 'security_question')  # Ensure it's visible in the detail view

admin.site.register(UserProfile, UserProfileAdmin)
