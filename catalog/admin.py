from django.contrib import admin

# Register your models here.

from .models import FlightsheetDetails, FlightsheetHeader

class FlightsheetDetailsAdmin(admin.ModelAdmin):
    list_display = ('flight_key', 'glider', 'pilot1', 'duration_time')

class FlightsheetHeaderAdmin(admin.ModelAdmin):
    pass

admin.site.register(FlightsheetDetails, FlightsheetDetailsAdmin)
admin.site.register(FlightsheetHeader, FlightsheetHeaderAdmin)
