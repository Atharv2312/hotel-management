from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import Hotel, Rating, Profile
import random

class Command(BaseCommand):
    help = 'Create fake reviews for hotels'

    
    def handle(self, *args, **kwargs):
        fake_reviews = [
        "The room was clean and spacious.",
        "Excellent location near major attractions.",
        "Staff were extremely friendly and helpful.",
        "The bed was super comfortable.",
        "Loved the rooftop pool and lounge area.",
        "Amazing breakfast buffet with lots of variety.",
        "Very peaceful and quiet environment.",
        "The bathroom was spotless and luxurious.",
        "Fast and reliable WiFi connection.",
        "Gym facilities were top-notch.",
        "The view from my balcony was breathtaking.",
        "Convenient free parking on site.",
        "Smooth and fast check-in process.",
        "Loved the decor and design of the hotel.",
        "Great value for money!",
        "Highly recommend their in-house restaurant.",
        "The air conditioning worked perfectly.",
        "Shuttle service to the airport was very convenient.",
        "Walking distance to popular shopping areas.",
        "The concierge gave great local recommendations.",
        "The spa services were excellent.",
        "Very family-friendly atmosphere.",
        "Romantic setting, perfect for couples.",
        "Pet-friendly and accommodating to our dog.",
        "The minibar was well-stocked.",
        "Room service was fast and delicious.",
        "Beautiful garden and outdoor seating area.",
        "Laundry service was very quick.",
        "The room had an amazing city view.",
        "Very comfortable working desk for business trips.",
        "Lots of TV channels and entertainment options.",
        "Loved the complimentary toiletries.",
        "Very secure with keycard access everywhere.",
        "The beach was just a short walk away.",
        "Amazing hospitality from the front desk staff.",
        "The coffee machine in the room was a nice touch.",
        "Huge variety in room service menu.",
        "The lobby was very elegant and clean.",
        "Perfect for a weekend getaway.",
        "Elevators were super fast and efficient.",
        "They upgraded us to a suite for free!",
        "Nice touch with complimentary welcome drinks.",
        "Great soundproofing – no outside noise at all.",
        "Comfortable pillows and soft linens.",
        "Impressive eco-friendly initiatives.",
        "Tasty and affordable breakfast options.",
        "Plenty of power outlets in the room.",
        "The lighting in the room was cozy and adjustable.",
        "Excellent housekeeping service every day.",
        "Felt very safe staying here alone.",
        "Easy access to public transportation.",
        "24-hour reception service was very helpful.",
        "Luxurious rain shower in the bathroom.",
        "Loved the modern room interiors.",
        "The pool bar served amazing cocktails.",
        "Extremely clean lobby and public areas.",
        "The welcome snacks were delicious!",
        "Check-out was fast and hassle-free.",
        "Big, spacious wardrobe and storage space.",
        "Perfectly located near all the major attractions.",
        "The breakfast had healthy options too!",
        "Great spot for digital nomads.",
        "Excellent conference room facilities.",
        "Loved the outdoor terrace seating.",
        "Bike rentals available at the hotel.",
        "The room smelled fresh and clean.",
        "Personalized service made our stay special.",
        "Kids' play area was clean and well-equipped.",
        "The fireplace in the lobby was cozy.",
        "Very flexible with early check-in requests.",
        "The restaurant had vegetarian and vegan options.",
        "Super close to metro and bus stations.",
        "Amazing room service pizza!",
        "Valet parking was quick and easy.",
        "Great ambiance in the common areas.",
        "Rooms had blackout curtains for good sleep.",
        "Loved the hot tub and sauna facilities.",
        "Nice little touches like bathrobes and slippers.",
        "Beautifully maintained property.",
        "Friendly staff who spoke multiple languages.",
        "The hotel bar had live music events.",
        "Convenient location for business travelers.",
        "Highly recommend for family vacations.",
        "Wide selection of teas and coffee in the room.",
        "Flexible cancellation policy helped us a lot.",
        "The room heater was very effective during winter.",
        "Lots of USB ports for charging devices.",
        "Loved the rain shower and bathtub combo.",
        "Very clean swimming pool.",
        "The property was beautifully landscaped.",
        "Complimentary bottled water every day.",
        "Breakfast hours were very flexible.",
        "Nice little library corner in the lobby.",
        "Loved the evening turndown service.",
        "Incredible mountain views from the room.",
        "Spacious balcony with comfy seating.",
        "They provided free umbrellas on rainy days.",
        "Really good blackout blinds for deep sleep.",
        "The mattress was very orthopedic and supportive.",
        "Nice smell in the lobby and hallways.",
        "Everything was exactly like the photos online.",
        "The room key worked smoothly every time.",
        "Hotel manager personally checked on us."
    ]

        customers = User.objects.filter(profile__role='customer')  # Only customers
        hotels = Hotel.objects.all()

        for hotel in hotels:
            num_reviews = random.randint(3, 8)  # Each hotel gets 3 to 8 reviews

            reviewers = random.sample(list(customers), min(num_reviews, customers.count()))

            for reviewer in reviewers:
                stars = random.randint(1, 5)
                review_text = random.choice(fake_reviews)

                # Prevent duplicate reviews
                if not Rating.objects.filter(customer=reviewer, hotel=hotel).exists():
                    Rating.objects.create(
                        customer=reviewer,
                        hotel=hotel,
                        stars=stars,
                        review=review_text,
                    )


        self.stdout.write(self.style.SUCCESS('Successfully created fake reviews for hotels!'))
