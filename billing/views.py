from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from .models import Plan, Invoice
from .serializers import InvoiceSerializer, PlanSerializer
from . import services

# Create your views here.
class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        try:
            invoice = services.mark_invoice_paid(pk)
            return Response({'status': 'Invoice paid', 'invoice_id': invoice.id})
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def run_arrears_check(self, request):
        count = services.check_arrears()
        return Response({'status': f'Arrears check complete. {count} account(s) flagged.'})

    @action(detail=False, methods=['post'])
    def generate_monthly_invoices(self, request):
        results = services.generate_invoices_for_all_accounts()
        return Response({'results': results})

    @action(detail=False, methods=['post'])
    def generate_for_account(self, request):
        account_id = request.data.get('account_id')
        if not account_id:
            return Response({'error': 'account_id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            invoice = services.generate_invoice(account_id)
            return Response({
                'status': 'Invoice generated',
                'invoice_id': invoice.id,
                'amount': str(invoice.amount),
                'due_date': str(invoice.due_date)
            })
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


def invoice_list_view(request):
    return render(request, 'billing/invoice_list.html')

def plan_list_view(request):
    return render(request, 'billing/plan_list.html')