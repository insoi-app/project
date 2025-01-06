# cabin/urls.py
from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CabinViewSet
from django.conf.urls.static import static
from django.urls import path

# Create a router and register the CabinViewSet with it
router = DefaultRouter()
router.register(r'cabins', CabinViewSet)
  # Register the CabinViewSet
# Define URL patterns
urlpatterns = [
    path('api/', include(router.urls)),  # Prefixed with 'api/' for API endpoints
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)