from django.contrib import admin
from .models import Cabin, CabinImage

class CabinImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'cabin', 'image', 'description')
    search_fields = ('cabin__name', 'description')

class CabinAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'is_available', 'get_weekday_prices', 'get_weekend_prices')
    search_fields = ('name', 'description')
    list_filter = ('is_available', 'name')
 # Allows you to add one extra CabinImage by default

    
    # Custom method to display the weekday prices in the admin
    def get_weekday_prices(self, obj):
        # Display a summary of the prices, e.g., a string or range
        weekday_prices = obj.prices_weekday
        return ', '.join([f"{key}: {value}" for key, value in weekday_prices.items()]) if weekday_prices else "No prices configured"
    get_weekday_prices.short_description = 'Weekday Prices'
    
    # Custom method to display the weekend prices in the admin
    def get_weekend_prices(self, obj):
        # Display a summary of the prices, e.g., a string or range
        weekend_prices = obj.prices_weekend
        return ', '.join([f"{key}: {value}" for key, value in weekend_prices.items()]) if weekend_prices else "No prices configured"
    get_weekend_prices.short_description = 'Weekend Prices'
# Register the model with the custom admin interface
admin.site.register(Cabin, CabinAdmin)
admin.site.register(CabinImage, CabinImageAdmin)


