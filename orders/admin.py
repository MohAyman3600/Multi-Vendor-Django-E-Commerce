"""Admin site model."""
from django.contrib import admin

from .models import Order, OrderProduct, BillingDetails


class OrderProductInline(admin.StackedInline):
    model = OrderProduct


class BillingDetailsInline(admin.StackedInline):
    model = BillingDetails


class OrderAdmin(admin.ModelAdmin):
    inlines = [BillingDetailsInline, OrderProductInline, ]
    list_display = ('status', 'total_price', 'tracking_code', 'get_email')

    def get_email(self, obj):
        return obj.billing_details.email
    get_email.short_description = 'customer'
    get_email.admin_order_field = 'billingdetails__email'

    class Meta:
        model = Order
        fields = ('customer', 'tracking_code',
                  'billing_details', 'status', 'created')


admin.site.register(Order, OrderAdmin)
