from django.contrib import admin

# Register your models here.
from .models import Hotel, Booking, Profile,Rating

admin.site.register(Hotel)
admin.site.register(Booking)
admin.site.register(Profile)
admin.site.register(Rating)