from rest_framework import serializers
from .models import Line

class LineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Line
        fields = '__all__'