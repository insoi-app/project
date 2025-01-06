from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReservationViewSet

router = DefaultRouter()
# Register the viewsets
router.register(r'reservations', ReservationViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  # Prefixed with 'api/' for API endpoints
]
