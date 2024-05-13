from django.contrib import admin
from .models import Goods
# Register your models here.

class GoodsAdmin(admin.ModelAdmin):
    list_display = ('name','price','c_date')
admin.site.register(Goods,GoodsAdmin)