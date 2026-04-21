from rest_framework.routers import DefaultRouter
from .views import LineViewSet

router = DefaultRouter()
router.register(r'lines', LineViewSet)

urlpatterns = router.urls