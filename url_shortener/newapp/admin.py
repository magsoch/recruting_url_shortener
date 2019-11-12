from django.contrib import admin
from .models import Url

@admin.register(Url)
class Admin(admin.ModelAdmin):
    list_display = ( 'url', 'short_code', 'date')