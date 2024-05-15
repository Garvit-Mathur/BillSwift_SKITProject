from django.contrib import admin
from .models import *

# Register your models here.

# admin.site.register(Billswift)

@admin.register(Billswift)
class AdminBillswift(admin.ModelAdmin):
    list_display = ['id','user','file','date_time']
admin.site.register(BillData)