from django.shortcuts import render
from rest_framework import viewsets
from .models import Account
from .serializers import AccountSerializer

# Create your views here.
class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


def account_list_view(request):
    accounts = Account.objects.all()
    return render(request, 'accounts/account_list.html', {'accounts': accounts})

def account_details_view(request, pk):
    return render(request, 'accounts/account_details.html', {'account_id': pk})