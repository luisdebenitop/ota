from django.urls import path

from . import views

urlpatterns = [path("<int:user_id>", views.unpaid_invoices, name="unpaid_invoices")]
