from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PlanViewSet, InvoiceViewSet, invoice_list_view, plan_list_view

router = DefaultRouter()
router.register(r'plans', PlanViewSet)
router.register(r'invoices', InvoiceViewSet)

urlpatterns = [
    path('invoices/', invoice_list_view, name='invoice-list'),
    path('plans/', plan_list_view, name='plan-list'),
]
urlpatterns += router.urls