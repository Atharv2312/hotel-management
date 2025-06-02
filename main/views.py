from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect,get_object_or_404
from .forms import HotelForm  # You’ll create this form
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import HotelForm
from django.contrib.auth.decorators import login_required
from .models import Hotel,Booking,Profile,User,Rating
from django.contrib.auth import logout as django_logout  # Import the built-in logout function
from django.contrib import messages
from datetime import timedelta
from django.db.models import Q,Avg
from .recommend import recommend_hotels_for_user

@login_required  # Ensures that only authenticated users can register a hotel
def register_hotel(request):
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)
        if form.is_valid():
            hotel = form.save(commit=False)
            hotel.owner = request.user  
            hotel.save()
            return redirect('register_hotel')  # or wherever you want
    else:
        form = HotelForm()

    return render(request, 'register_hotel.html', {
        'form': form,
        'owner_name': request.user.get_full_name() or request.user.username  # ✅ Owner name
    })

def home(request):
    hotels = Hotel.objects.annotate(avg_rating=Avg('ratings__stars'))
    search_query = request.GET.get('search', '')
    if search_query:
        hotels = Hotel.objects.filter(
            Q(name__icontains=search_query) | Q(location__icontains=search_query)
        )
    else:
         hotels = Hotel.objects.all() 

    hotel_ratings = Rating.objects.values('hotel').annotate(avg_rating=Avg('stars'))
    hotel_ratings_dict = {item['hotel']: item['avg_rating'] for item in hotel_ratings}
    
    # Attach avg_rating manually
    for hotel in hotels:

        hotel.avg_rating = hotel_ratings_dict.get(hotel.hotel_id, None)
# only show verified hotels
    return render(request, 'home.html', {'hotels': hotels, 'search_query': search_query})



# Customer Signup
#def signup_customer(request):
#    if request.method == 'POST':
 #       form = UserCreationForm(request.POST)
  #      if form.is_valid():
  #          user = form.save()
   #         login(request, user)
    #        return redirect('home')  # Redirect to home page after successful signup
   # else:
   #     form = UserCreationForm()
   # return render(request, 'signup_customer.html', {'form': form})

# Customer Login
def login_customer(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Ensure the user has a Profile and set role to 'customer' if not already set
            profile= Profile.objects.get(user=user)
            if profile.role!='customer':
                 messages.error(request, "You are not registered as a customer.")
                 return render(request, 'login_customer.html', {'form': form})
            
            else :
                login(request, user) 
                return redirect('home')  # Redirect to home page after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'login_customer.html', {'form': form})


# Hotel Owner Signup
#def signup_owner(request):
  #  if request.method == 'POST':
  #      form = UserCreationForm(request.POST)
  #          user = form.save()
   #         login(request, user)
   #         return redirect('register_hotel')  # Redirect to hotel registration after successful signup
   # else:
    #    form = UserCreationForm()
   # return render(request, 'signup_owner.html', {'form': form})

# Hotel Owner Login
def login_owner(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
           

            # Ensure the user has a Profile and set role to 'hotel_owner'
            profile = Profile.objects.get(user=user)
            if(profile.role!='hotel_owner'):
                 messages.error(request, "You are not registered as a hotel owner.")
                 return render(request, 'login_owner.html', {'form': form})
            
            else :
                login(request, user)
                return redirect('register_hotel')  # Redirect to hotel registration after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'login_owner.html', {'form': form})



def login_view(request):
    return render(request, 'login.html')


def signup_view(request):
    return render(request, 'signup.html')



@login_required
def edit_hotels(request, name):
    owner_id=User.objects.get(username = name)

    hotels = Hotel.objects.filter(owner=owner_id)
    # Add form handling here if needed for editing
    return render(request, 'edit_hotels.html', {'hotels': hotels})


@login_required
def edit_specific_hotel(request, id):
    hotel = Hotel.objects.get(hotel_id = id) # Ensure only the owner can edit their hotel
    
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES, instance=hotel)
        if form.is_valid():
            form.save()
            return redirect('edit_hotels')  # Redirect back to edit hotels page after saving
    else:
        form = HotelForm(instance=hotel)

    return render(request, 'edit_hotel_form.html', {'form': form, 'hotel': hotel})


def logout(request):
     django_logout(request)
     return redirect('home')


from .forms import CustomerSignupForm, HotelOwnerSignupForm

def signup_customer(request):
    if request.method == 'POST':
        form = CustomerSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, role='customer')  # form.save() also creates the Profile inside the form
            login(request, user)  # Log the user in
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomerSignupForm()

    return render(request, 'signup_customer.html', {'form': form})

def signup_owner(request):
    if request.method == 'POST':
        form = HotelOwnerSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user,role='hotel_owner')
            login(request, user)
            return redirect('register_hotel')
    else:
        messages.error(request, "Please correct the errors below.")
        form = HotelOwnerSignupForm()
    return render(request, 'signup_owner.html', {'form': form})



from .forms import BookingForm

@login_required(login_url='login_customer')
def book_hotel(request , id):
    hotel =Hotel.objects.get (hotel_id = id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.hotel = hotel
            number_of_days = (booking.check_out - booking.check_in).days
            rooms_requested = booking.no_of_rooms

            if hotel.number_of_rooms >= rooms_requested and number_of_days >= 0:
                hotel.number_of_rooms -= rooms_requested
                hotel.save()  # Save the updated hotel rooms

                booking.amount = rooms_requested * float(hotel.price_per_night)  # total amount calculation
                booking.save()  # Save the booking
                return redirect('my_bookings')  # Or wherever you want
            else:
                messages.error(request, 'Please Enter valid Details')
                return render(request, 'book_hotel.html', {'form': form, 'hotel': hotel})
    else:
        form = BookingForm()
    return render(request, 'book_hotel.html', {'form': form, 'hotel': hotel})



@login_required(login_url='login_customer')
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'my_bookings.html', {'bookings': bookings})


@login_required
def cancel_booking(request, id):
    booking = Booking.objects.get(booking_id= id)
    if request.method == 'POST':
        booking.delete()
        return redirect('my_bookings')
    return redirect('home') 





@login_required
def rate_hotel(request, id):
    hotel = get_object_or_404(Hotel, hotel_id=id)

    if request.method == 'POST':
        stars = request.POST.get('stars')
        review = request.POST.get('review')

        new_review = Rating.objects.create(
            hotel=hotel,
            customer=request.user,  # This should reference the logged-in user
            stars=stars,
            review=review
        )

    return redirect('home')  # or wherever you're showing the hotel




#recommendations
def recommend_hotels(request):
    user = request.user
    recommended_hotels = Hotel.objects.all()  # Default to all hotels if no filters are applied

    if request.method == "GET":
        location = request.GET.get('location')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        # Check if min_price and max_price are provided and are valid digits
       
        # Personalized recommendation if the user is authenticated and has rated hotels
        if user.is_authenticated:
            user_ratings = Rating.objects.filter(customer=user)
            if user_ratings:
                recommended_hotels = recommend_hotels_for_user(user)  # Your custom recommendation function
                if min_price and max_price and min_price.isdigit() and max_price.isdigit():
                    min_price = float(min_price)
                    max_price = float(max_price)

            # Ensure max_price is greater than min_price
                    if min_price <= max_price:
                        recommended_hotels = [
                        hotel for hotel in recommended_hotels
                        if hotel.price_per_night >= min_price
                        ]            
                        recommended_hotels = [
                        hotel for hotel in recommended_hotels
                        if hotel.price_per_night <= max_price
                        ]
                    else:
                        messages.error(request, "Max Price needs to be greater than Min Price")


                # Filter by location again if the user has preferences
                if location and location != "All":
                    recommended_hotels = [hotel for hotel in recommended_hotels if hotel.location == location]

        # If no specific filter applied, randomize the selection
        if not recommended_hotels:
            recommended_hotels = Hotel.objects.order_by('?')[:20] 
            
    hotel_ratings = Rating.objects.values('hotel').annotate(avg_rating=Avg('stars'))
    rating_map = {item['hotel']: item['avg_rating'] for item in hotel_ratings}

    # ⭐ Attach avg_rating to each recommended hotel
    for hotel in recommended_hotels:
        hotel.avg_rating = rating_map.get(hotel.hotel_id, None)

    context = {
        'recommended_hotels': recommended_hotels
    }

    return render(request, 'recommendations.html', context)
