# recommend_hotels.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from .models import Hotel, Rating
from django.contrib.auth.models import User

def build_content_similarity():
    hotels = Hotel.objects.all()
    df = pd.DataFrame(list(hotels.values('hotel_id', 'name', 'location', 'amenities', 'price_per_night')))
    
    # Combine important fields
    df['combined_features'] = df['location'] + " " + df['amenities']
    
    # TF-IDF Vectorizer
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['combined_features'])
    
    # Cosine Similarity
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    return df, cosine_sim

def recommend_hotels_for_user(user):
    df, cosine_sim = build_content_similarity()
    hotels = Hotel.objects.all()
    
    # Fetch user's rated hotels
    user_ratings = Rating.objects.filter(customer=user).order_by('-stars')
    # Else, personalized recommendation
    hotel_indices = []
    for rating in user_ratings:
        hotel_index = df.index[df['hotel_id'] == rating.hotel.hotel_id].tolist()[0]
        hotel_indices.append(hotel_index)

    # Calculate scores
    similarity_scores = cosine_sim[hotel_indices]
    avg_scores = similarity_scores.mean(axis=0)
    
    # Get top hotels
    top_indices = avg_scores.argsort() # Top 20 hotels
    
    recommended_hotels = []
    for idx in top_indices:
        hotel_id = df.iloc[idx]['hotel_id']
        hotel = Hotel.objects.get(hotel_id=hotel_id)
        recommended_hotels.append(hotel)
    
    return recommended_hotels
