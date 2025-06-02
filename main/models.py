from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Extend user roles
class Profile(models.Model):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('hotel_owner', 'Hotel Owner'),
        ('superuser', 'Superuser')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    role = models.CharField(max_length=20, default='superuser')
   

    def __str__(self):
        return f"{self.user.username} ({self.role})"

# models.py

class Hotel(models.Model):
    hotel_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    amenities = models.TextField()
    number_of_rooms = models.PositiveIntegerField(default=0)  # ✅ New field
    image = models.ImageField(upload_to='hotel_images/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name



class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    no_of_rooms=models.IntegerField(default=0)
    amount=models.FloatField(default=0.00)
    check_in = models.DateField()
    check_out = models.DateField()
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.hotel.hotel_id}"


class Rating(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='ratings')
    stars = models.PositiveSmallIntegerField(default=5)  # Range from 1 to 5
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('customer', 'hotel')  # Prevent multiple ratings from same customer

    def __str__(self):
        return f'{self.customer.username} rated {self.hotel.name} - {self.stars} stars'