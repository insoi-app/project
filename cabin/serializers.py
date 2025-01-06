from rest_framework import serializers
from .models import Cabin

class CabinSerializer(serializers.ModelSerializer):
    # You can serialize the images as well (if needed)
    image = serializers.ImageField()
    # Additional fields to represent the pricing logic can be added here if necessary
    prices_weekday = serializers.JSONField()
    prices_weekend = serializers.JSONField()

    class Meta:
        model = Cabin
        fields = ['id', 'name', 'description', 'capacity', 'is_available', 'prices_weekday', 'prices_weekend', 'image', 'amenity' ]

    def to_representation(self, instance):
        """
        You can add custom logic to modify the response representation of the Cabin serializer here.
        For instance, if you need to add the calculated price, it can be done here.
        """
        representation = super().to_representation(instance)
        
        # Example: Add a computed field for the price for a given time slot (assuming a default time slot)
        representation['price_for_sunrise'] = instance.get_price('sunrise', False, 1)  # Example, 1 person, weekday

        # Similarly, you can compute and add other information like weekend price, max_capacity, etc.

        return representation


