from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Line
from .serializers import LineSerializer
from . import services

# Create your views here.
class LineViewSet(viewsets.ModelViewSet):
    queryset = Line.objects.all()
    serializer_class = LineSerializer

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        try:
            line = services.activate_line(pk)
            return Response({'status': 'Line activated', 'line_id': line.id})
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def suspend(self, request, pk=None):
        try:
            line = services.suspend_line(pk)
            return Response({'status': 'Line suspended', 'line_id': line.id})
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        try:
            line = services.restore_line(pk)
            return Response({'status': 'Line restored', 'line_id': line.id})
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)