from rest_framework import serializers
from .models import Reservation
from cabin.serializers import CabinSerializer
from cabin.models import Cabin
from django.contrib.auth import get_user_model
from decimal import Decimal

class CabinSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cabin
        fields = ['id', 'name']  # Only include the id and name fields

# Custom User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email']

# Reservation Serializer
class ReservationSerializer(serializers.ModelSerializer):
    cabin = CabinSimpleSerializer()
    customer = UserSerializer()
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'cabin', 'customer', 'start_date', 'end_date', 'time_slot', 'num_people', 'total_price', 'created_at']

    def validate(self, data):
        cabin = data.get('cabin')
        num_people = data.get('num_people')

        # Ensure num_people is provided and within the cabin capacity
        if num_people is None:
            raise serializers.ValidationError("The number of people must be provided.")
        
        if cabin.capacity < num_people:
            raise serializers.ValidationError(f"The cabin {cabin.name} cannot accommodate {num_people} people. Max capacity: {cabin.capacity}.")
        
        # Ensure valid time slot is provided
        time_slot = data.get('time_slot')
        if time_slot not in dict(Cabin.TIME_SLOT_CHOICES):
            raise serializers.ValidationError(f"Invalid time slot: {time_slot}. Please choose from available time slots.")

        return data

    def create(self, validated_data):
        cabin_data = validated_data.pop('cabin')
        customer_data = validated_data.pop('customer')

        cabin = Cabin.objects.get(id=cabin_data['id'])
        customer = get_user_model().objects.get(id=customer_data['id'])

        start_date = validated_data.get('start_date')
        time_slot = validated_data.get('time_slot')  # Get the time_slot from validated data
        num_people = validated_data.get('num_people')  # Get the number of people from validated data

        # Validate number of people against cabin capacity
        if cabin.capacity < num_people:
            raise serializers.ValidationError(f"The cabin {cabin.name} cannot accommodate {num_people} people. Max capacity: {cabin.capacity}.")

        is_weekend_or_holiday = self.is_weekend_or_holiday(start_date)
    
        # Get the price per night based on the cabin's pricing method
        price_per_night = Decimal(cabin.get_price(time_slot, is_weekend_or_holiday, num_people))

        # Calculate the duration in days
        duration = (validated_data['end_date'] - validated_data['start_date']).days
        if duration <= 0:
            raise serializers.ValidationError("End date must be after start date.")

        total_price = price_per_night * duration

        reservation = Reservation.objects.create(cabin=cabin, customer=customer, total_price=total_price, **validated_data)
        return reservation
    
    def update(self, instance, validated_data):
        cabin_data = validated_data.pop('cabin', None)
        customer_data = validated_data.pop('customer', None)

        if cabin_data:
            instance.cabin = Cabin.objects.get(id=cabin_data['id'])
        if customer_data:
            instance.customer = get_user_model().objects.get(id=customer_data['id'])

        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.time_slot = validated_data.get('time_slot', instance.time_slot)
        instance.num_people = validated_data.get('num_people', instance.num_people)

        # Validate number of people against cabin capacity when updating reservation
        if instance.cabin.capacity < instance.num_people:
            raise serializers.ValidationError(f"The cabin {instance.cabin.name} cannot accommodate {instance.num_people} people. Max capacity: {instance.cabin.capacity}.")

        # Only recalculate price if relevant fields have changed
        is_weekend_or_holiday = self.is_weekend_or_holiday(instance.start_date)
        price_per_night = Decimal(instance.cabin.get_price(instance.time_slot, is_weekend_or_holiday, instance.num_people))
        
        # Calculate the duration in days
        duration = (instance.end_date - instance.start_date).days
        instance.total_price = price_per_night * duration

        instance.save()
        return instance

    def is_weekend_or_holiday(self, date):
        """
        Returns True if the date is a Friday, Saturday, Sunday, or a holiday.
        """
        return date.weekday() >= 4  # Friday-Sunday
