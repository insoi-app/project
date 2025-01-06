from django.contrib import admin
from .models import Cabin, Reservation
from django.contrib.auth import get_user_model

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('customer', 'cabin', 'start_date', 'end_date', 'time_slot', 'total_price', 'created_at')
    search_fields = ('customer__username', 'cabin__name')
    list_filter = ('start_date', 'end_date', 'time_slot', 'cabin__name')

    # Make total_price read-only in admin form
    readonly_fields = ('total_price',)

    def save_model(self, request, obj, form, change):
        """
        Override the save_model to calculate total_price when the reservation is saved or updated.
        """
        # Ensure num_people is valid
        if not obj.num_people or obj.num_people <= 0:
            raise ValueError("The number of people must be provided and greater than 0.")
        
        # Calculate if the start_date is on a weekend or holiday
        is_weekend_or_holiday = obj.is_weekend_or_holiday(obj.start_date)
        
        # Get the price per night for the selected time slot
        price_per_night = obj.cabin.get_price(obj.time_slot, is_weekend_or_holiday, obj.num_people)
        
        # Ensure duration is valid
        duration = (obj.end_date - obj.start_date).days
        if duration <= 0:
            raise ValueError("End date must be after start date.")

        # Calculate the total price
        obj.total_price = price_per_night * duration

        # Save the model instance
        super().save_model(request, obj, form, change)


# Register the models with the admin site

admin.site.register(Reservation, ReservationAdmin)
