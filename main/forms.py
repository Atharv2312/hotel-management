from django import forms
from django.contrib.auth.models import User
from .models import Hotel, Booking, Profile, Rating
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'location', 'price_per_night', 'amenities','number_of_rooms','image']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['no_of_rooms','check_in', 'check_out']
    

# Customer Signup Form (with additional fields)
class CustomerSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email','password1', 'password2')

             #Create associated profile
    



# Hotel Owner Signup Form (with additional fields)
class HotelOwnerSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email', 'password1', 'password2')



class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['stars' , 'review']
        widgets = {
            'stars': forms.RadioSelect(choices=[(i, f'{i} Star') for i in range(1, 6)]),
            'review': forms.Textarea(attrs={'rows': 3})
        }