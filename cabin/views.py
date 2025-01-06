from urllib import request
from rest_framework import viewsets, permissions
from .models import Cabin, CabinImage
from rest_framework import serializers
from .serializers import CabinSerializer, CabinImageSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class CabinImageViewSet(viewsets.ModelViewSet):
    queryset = CabinImage.objects.all()
    serializer_class = CabinImageSerializer
    permission_classes = [permissions.AllowAny] 

class CabinViewSet(viewsets.ModelViewSet):
    queryset = Cabin.objects.all()
    serializer_class = CabinSerializer
    permission_classes = [permissions.AllowAny]  # Restricting to authenticated users (change as needed)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ['name', 'is_available', 'capacity']  # Add filtering by fields like name, availability, and capacity
    search_fields = ['name', 'description']  # Enable search for name and description
    ordering_fields = ['name', 'capacity', 'is_available']  # Enable ordering by name, capacity, or availability
    ordering = ['name']  # Default ordering (you can modify as needed)

    def perform_create(self, serializer):
        """
        Override the `perform_create` method to add custom logic before saving the instance.
        For example, you could check cabin availability before creation.
        """
        # Add your custom logic here, e.g., ensuring availability
        if not serializer.validated_data['is_available']:
            raise serializers.ValidationError("The cabin is not available for reservation.")

        serializer.save()

    @action(detail=False, methods=['get'])
    def available_cabins(self, request):
        """
        Custom action to list only available cabins.
        """
        available_cabins = Cabin.objects.filter(is_available=True)
        serializer = self.get_serializer(available_cabins, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def calculate_price(self, request, pk=None):
        """
        Custom action to calculate price for a cabin based on input parameters.
        """
        cabin = self.get_object()
        
        # Parameters from request
        time_slot = request.query_params.get('time_slot')
        num_people = int(request.query_params.get('num_people', 0))
        
        # Check for valid input
        if not time_slot:
            return Response({'error': 'time_slot is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if num_people <= 0:
            return Response({'error': 'num_people must be greater than 0'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Assuming `get_price` accepts time_slot and num_people
            price = cabin.get_price(time_slot, False, num_people)  # You might want to implement holiday check here
            return Response({'price': price})
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
