from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Invoice
from django.views.decorators.cache import cache_page


@cache_page(60, key_prefix="unpaid_invoices")
@require_http_methods(["GET"])
def unpaid_invoices(request, user_id):
    unpaid_invoices = Invoice.objects.filter(invoiced_user=user_id, is_paid=False)
    data = [
        {
            "invoice_number": invoice.invoice_number,
            "invoiced_amount": invoice.invoiced_amount,
            "invoice_date": invoice.invoice_date,
        }
        for invoice in unpaid_invoices
    ]
    return JsonResponse(data, safe=False)
