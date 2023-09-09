from django.contrib import admin
from .models import Box

# Register your models here.

@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ('id','length', 'width', 'height', 'created_by', 'created_at', 'updated_at')








# Key: Authorization
# Value: Bearer 14c6c84f2bd6189a76fa5e1607bcdd2b933bdb15

# {"token":"dd5f1df39aa40c0beb53b4ffe8d252e9ff736d00"}