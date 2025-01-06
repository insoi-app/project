
from rest_framework import viewsets, permissions
from .models import Reservation
from .serializers import ReservationSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from datetime import datetime

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['post'])
    def calculate_price(self, request, pk=None):
        """
        Custom action to calculate price for a reservation based on input parameters.
        """
        reservation = self.get_object()

        # Retrieve and validate the required parameters from the request
        start_date_str = request.data.get('start_date')
        num_people = request.data.get('num_people')
        time_slot = request.data.get('time_slot')

        # Check if any of the required parameters are missing
        if not start_date_str or not num_people or not time_slot:
            return Response({'error': 'start_date, num_people, and time_slot are required'}, status=400)

        # Validate that num_people is an integer
        try:
            num_people = int(num_people)
        except ValueError:
            return Response({'error': 'num_people must be an integer'}, status=400)

        # Convert the start_date to a date object
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid start_date format. Please use YYYY-MM-DD.'}, status=400)

        # Get the cabin related to the reservation
        cabin = reservation.cabin

        # Check if the cabin can accommodate the number of people
        if num_people > cabin.capacity:
            return Response({'error': f'{cabin.name} can only accommodate up to {cabin.capacity} people.'}, status=400)

        # Calculate if the start_date is on a weekend or holiday
        is_weekend_or_holiday = reservation.is_weekend_or_holiday(start_date)

        # Corrected: Pass num_people as the third argument to get_price
        try:
            price_per_night = cabin.get_price(time_slot, is_weekend_or_holiday, num_people)
        except ValueError as e:
            return Response({'error': str(e)}, status=400)

        # Calculate the total price based on the duration of the stay
        # Check if the end_date is passed, otherwise use reservation's end_date
        if 'end_date' in request.data:
            try:
                end_date = datetime.strptime(request.data.get('end_date'), '%Y-%m-%d').date()
            except ValueError:
                return Response({'error': 'Invalid end_date format. Please use YYYY-MM-DD.'}, status=400)
        else:
            end_date = reservation.end_date

        # Ensure duration is valid
        duration = (end_date - start_date).days
        if duration <= 0:
            return Response({'error': 'End date must be after the start date.'}, status=400)

        total_price = price_per_night * duration

        # Return the calculated total price
        return Response({'total_price': total_price})
