from django.contrib import admin
from .models import TimeClock
# Register your models here.

class TimeClockAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'clock_in_time', 'clock_out_time', 'location', 'role')

admin.site.register(TimeClock, TimeClockAdmin)