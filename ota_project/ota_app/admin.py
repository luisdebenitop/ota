from django.contrib import admin
from django.urls import reverse
from .models import User, Invoice
from django.utils.html import format_html


class InvoiceInline(admin.TabularInline):
    model = Invoice
    extra = 0
    exclude = ("invoice_number",)

    def has_delete_permission(self, request, obj=None):
        return False


class UserAdmin(admin.ModelAdmin):
    inlines = [InvoiceInline]
    list_display = (
        "name",
        "email",
        "company_name",
        "country",
        "invoice_currency",
        "total_invoiced",
        "invoices_link",
    )
    list_filter = ("invoice__is_paid", "invoice__invoiced_amount")
    search_fields = (
        "name",
        "email",
        "company_name",
        "country",
        "invoice__invoice_number",
    )

    def invoices_link(self, obj):
        url = (
            reverse("admin:ota_app_invoice_changelist") + f"?user__id__exact={obj.id}"
        )
        return format_html('<a href="{}">View invoices</a>', url)

    invoices_link.short_description = "Invoices"

    def total_invoiced(self, obj):
        invoices = Invoice.objects.filter(invoiced_user=obj)
        return sum([i.invoiced_amount for i in invoices])

    total_invoiced.short_description = "Total Invoiced"


class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "invoice_number",
        "invoiced_user",
        "invoiced_amount",
        "invoice_date",
        "is_paid",
    )
    list_filter = ("is_paid", "invoiced_user__name")
    search_fields = ("invoice_number", "invoiced_user__name")
    exclude = ("invoice_number",)

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(User, UserAdmin)
admin.site.register(Invoice, InvoiceAdmin)
