from django.db import models
# Create your models here.
from django.db import models


class Cabin(models.Model):
    CABIN_CHOICES = [
        ('Saro', 'Cabin Saro'),
        ('Duwa', 'Cabin Duwa'),
        ('Gabos','Cabin Gabos'),
    ]
    
    TIME_SLOT_CHOICES = [
        ('sunrise', 'Sunrise (9am-6pm)'),
        ('sunset', 'Sunset (8pm-7am)'),
        ('moon', 'Fullstay Moon (8pm-6pm)'),
        ('star', 'Fullstay Star (9am-7am)'),
    ]
    
    name = models.CharField(max_length=50, choices=CABIN_CHOICES)
    description = models.TextField()
    amenity = models.JSONField(default=list, blank=True)  # Example: list of strings,
    image = models.ImageField(upload_to='cabins/', height_field=None, width_field=None, max_length=None)
    capacity = models.IntegerField()  # Base capacity
    max_capacity = models.IntegerField(null=True)  # Maximum capacity
    is_available = models.BooleanField(default=True)

    # Price configuration based on time slots
    prices_weekday = models.JSONField()  # A JSON field to store the weekday prices (Mon-Thurs)
    prices_weekend = models.JSONField()  # A JSON field to store the weekend/holiday prices (Fri-Sun)

    image = models.ImageField(upload_to='cabins/', null=True, blank=True)

    def __str__(self):
        return f'{self.name} ({self.capacity} people)'

    
    def get_price(self, time_slot, is_weekend_or_holiday, num_people):
        """
        Retrieve price based on time slot, day type (weekday/weekend), and the number of people.
        """
        prices = self.prices_weekend if is_weekend_or_holiday else self.prices_weekday

        # Retrieve the base price for the given time slot
        base_price = prices.get(time_slot, 0)
        
        if base_price == 0:
            raise ValueError(f"Invalid time slot: {time_slot} or no price configured for this time slot.")
        
        # Calculate additional charges for excess people
        additional_charge = 0
        base_capacity = self.capacity  # Base capacity
        max_capacity = self.max_capacity  # Maximum allowed capacity

        if num_people > base_capacity:
            excess_people = num_people - base_capacity
            if num_people <= max_capacity:
                additional_charge = self._calculate_additional_charge(excess_people, time_slot)
            else:
                raise ValueError(f"The number of people exceeds the maximum capacity of {max_capacity}.")
        
        # Total price includes the base price and additional charge for excess people
        total_price = base_price + additional_charge
        return total_price

    def _calculate_additional_charge(self, excess_people, time_slot):
        """
        Calculate the additional charge for the number of excess people based on the time slot.
        """
        if time_slot in ['sunrise', 'sunset']:
            return 250 * excess_people
        elif time_slot in ['moon', 'star']:
            return 450 * excess_people
        return 0

