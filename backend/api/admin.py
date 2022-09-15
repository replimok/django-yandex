from django.contrib import admin

from .models import SystemItem

admin.site.register(SystemItem, admin.ModelAdmin)