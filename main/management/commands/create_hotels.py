from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import Hotel, Profile  # Change 'hotel' to your app name
from faker import Faker
import random
from django.core.files.base import ContentFile
import requests
import os


class Command(BaseCommand):
    help = 'Creates hotel owners and hotels for the database'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Step 1: Create 20 Hotel Owner users
        def create_hotel_owners():
            owners = []
            user_name = ["Sunil", "Anjikya", "Manohar", "Arav", "Virat", "Atul", "Sanket", "Rohan", "Ajit", "Rohit", "Pandurang", "Rounak", "Asim", "Virendar", "Rakesh", "Anup", "pradip", "Pavan", "sai", "Dilip", "Mohit", "Ranjan", "Akash", "Ravindar", "Akshay", "Amar", "Rajat", "Hardik"]
            for username in user_name:  # Create 20 hotel owners
                random_number = random.randint(100, 999) 
                email = f"{username.lower()}{random_number}@gmail.com"
                password = 'Password@123'  # You can change this if you want
                user = User.objects.create_user(username=username, email=email, password=password)
                Profile.objects.create(user=user, role='hotel_owner')
                owners.append(user)

            return owners

        # Step 2: Create 100 Hotels and associate them with the created hotel owners
        def create_hotels(owners):
            hotel_names = ["Hotel Sunshine", "The Royal Inn", "Oceanview Resort", "Mountain Retreat", "City Central Hotel", "Tawade Hotel", "Rambagh Palace", "ITC Hotel", "Chandra Bhavan", "Swarna Bhavan", "Root", "Rolex"]  # Add more as needed
            locations = ["Mumbai", "Delhi", "Bengaluru", "Chennai", "Kolkata", "Rajasthan", "Kolhapur", "Chandigad", "Nagpur", "Nashik", "Solapur", "Ch.Sambhajinagar", "Gurgaon", "Amritsar", "Guwahati", "Ahmedabad", "Surat", "Lucknow", "Pune", "Hyderabad"]
            amenities = ["Free WiFi", "Pool", "Gym", "Restaurant", "Spa", "Parking", "Cab System"]
            image_folder = r"D:\mini project\Hello\images"

            image_files = os.listdir(image_folder)
        

            for _ in range(200):  # Create 200 hotels
                hotel_name = random.choice(hotel_names) 
                location = random.choice(locations)
                price_per_night = random.uniform(500, 10000)
                amenities_str = ", ".join(random.sample(amenities, 3))  # Randomly choose 3 amenities
                number_of_rooms = random.randint(10, 100)
                owner = random.choice(owners)  
                
                if image_files:
                    image_file_name = random.choice(image_files)
                    image_path = os.path.join(image_folder, image_file_name)

                with open(image_path, 'rb') as image_file:
                    image = ContentFile(image_file.read(), name=image_file_name)
# Randomly assign a hotel owner
                # Only save hotel if image exis
                hotel = Hotel(
                    name=hotel_name,
                    location=location,
                    price_per_night=price_per_night,
                    amenities=amenities_str,
                    image=image,  # Save the image if it's fetched
                    number_of_rooms=number_of_rooms,
                    owner=owner,
                )
                hotel.save()
            else:
                print(f"No image fetched for hotel: {hotel_name}")

        # Run the script
        owners = create_hotel_owners()
        create_hotels(owners)

        self.stdout.write(self.style.SUCCESS('Hotel owners and hotels created successfully!'))
