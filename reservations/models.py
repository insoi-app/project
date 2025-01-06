from django.db import models
from accounts.models import CustomUser
from cabin.models import Cabin
from django.core.exceptions import ValidationError

class Reservation(models.Model):
    cabin = models.ForeignKey(Cabin, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_date = models.DateField(null=True)
    end_date = models.DateField()
    time_slot = models.CharField(max_length=50, choices=Cabin.TIME_SLOT_CHOICES)
    num_people = models.IntegerField(null=True)  # Number of people in the reservation
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Override the save method to calculate total_price when the reservation is saved or updated.
        """
        if not self.num_people or self.num_people <= 0:
            raise ValidationError("The number of people must be provided and greater than 0.")
        
        # Check if the reservation is within the cabin's allowed capacity
        if self.num_people > self.cabin.max_capacity:
            raise ValidationError(f"Number of people exceeds the cabin's maximum capacity of {self.cabin.max_capacity}.")
        
        # Calculate if the start_date is on a weekend or holiday
        is_weekend_or_holiday = self.is_weekend_or_holiday(self.start_date)
        
        # Get the cabin's price for the selected time slot and number of people
        price_per_night = self.cabin.get_price(self.time_slot, is_weekend_or_holiday, self.num_people)
        
        # Ensure duration is valid (end_date must be after start_date)
        duration = (self.end_date - self.start_date).days
        if duration < 0:
            raise ValidationError("End date must be after the start date.")
        
        # If duration is 0, the reservation is for a single day
        if duration == 0:
            duration = 1  # Set duration to 1 day for the price calculation

        # Check if the cabin is already booked on the same date range
        if self.is_cabin_booked_on_date(self.cabin, self.start_date, self.end_date):
            raise ValidationError(f"Cabin '{self.cabin.name}' is already booked on the selected date(s).")
        
        # Check if 'Gabos' cabin is booked on the same day as 'Saro' or 'Duwa'
        if self.is_gabos_conflict(self.start_date, self.end_date):
            raise ValidationError("Cannot book 'Gabos' cabin on the same day as 'Saro' or 'Duwa'.")
        
        # Calculate the total price for the reservation
        self.total_price = price_per_night * duration
        
        # Save the reservation
        super().save(*args, **kwargs)

    def is_weekend_or_holiday(self, date):
        """
        Returns True if the date is a Friday, Saturday, Sunday, or a holiday.
        This is a basic check; you can expand it to include actual holiday checks.
        """
        return date.weekday() >= 4  # Friday (4), Saturday (5), Sunday (6)

    def is_cabin_booked_on_date(self, cabin, start_date, end_date):
        """
        Checks if the cabin is already booked on the same day or within the date range.
        This method is modified to allow for bookings that start on the same day an existing reservation ends.
        """
        return Reservation.objects.filter(
            cabin=cabin,
            start_date__lt=end_date,  # If any reservation starts before the new end date
            end_date__gt=start_date   # And ends after the new start date
        ).exists()

    def is_gabos_conflict(self, start_date, end_date):
        """
        Checks if the 'Gabos' cabin is booked on the same day as 'Saro' or 'Duwa'.
        """
        # If the cabin is "Gabos", we need to check for conflicts with "Saro" or "Duwa"
        if self.cabin.name == "Gabos":
            saro_cabin = Cabin.objects.filter(name="Saro").first()
            duwa_cabin = Cabin.objects.filter(name="Duwa").first()

            if saro_cabin and self.is_cabin_booked_on_date(saro_cabin, start_date, end_date):
                return True
            if duwa_cabin and self.is_cabin_booked_on_date(duwa_cabin, start_date, end_date):
                return True
        
        return False

    def __str__(self):
        return f'Reservation by {self.customer.username} for {self.cabin.name} from {self.start_date} to {self.end_date}'
