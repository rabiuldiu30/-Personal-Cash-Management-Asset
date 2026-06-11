from django.contrib import admin

from .models import AddCash, Expense


@admin.register(AddCash)
class AddCashAdmin(admin.ModelAdmin):
    list_display = ('source', 'user', 'amount', 'datetime')
    list_filter = ('datetime', 'source')
    search_fields = ('source', 'description', 'user__username', 'user__email')


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'user', 'amount', 'datetime')
    list_filter = ('datetime',)
    search_fields = ('description', 'user__username', 'user__email')
