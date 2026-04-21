from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, account_list_view

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)

urlpatterns = [
    path('accounts/', account_list_view, name='account_list'),
]

urlpatterns += router.urls