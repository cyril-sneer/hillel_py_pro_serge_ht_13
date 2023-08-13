from django.contrib import admin
from .models import Quotes, Pointer

# Register your models here.


class QuotesAdmin(admin.ModelAdmin):
    list_display = ['text', 'author']
    list_filter = ['author']


class PointerAdmin(admin.ModelAdmin):
    list_display = ['page', 'quote_num']


admin.site.register(Quotes, QuotesAdmin)
admin.site.register(Pointer, PointerAdmin)