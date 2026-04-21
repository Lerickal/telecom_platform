from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import LineViewSet, line_list_view

router = DefaultRouter()
router.register(r'lines', LineViewSet)

urlpatterns = [
    path('lines/', line_list_view, name='line_list'),
]
urlpatterns += router.urls