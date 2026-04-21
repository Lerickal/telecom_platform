from rest_framework import serializers
from .models import Plan, Invoice

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    is_overdue = serializers.ReadOnlyField()
    
    class Meta:
        model = Invoice
        fields = '__all__'