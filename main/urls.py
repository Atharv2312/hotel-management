from django.urls import path,include
from . import views
include('main.urls')  # ✅ Correct way

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),  # Login Page
    path('signup/', views.signup_view, name='signup'),
    path('signup_customer/', views.signup_customer, name='signup_customer'),
    path('login_owner/', views.login_owner, name='login_owner'),
    path('signup_owner/', views.signup_owner, name='signup_owner'),
    path('login_customer/', views.login_customer, name='login_customer'),
    path('register_hotel/', views.register_hotel, name='register_hotel'),
    path('edit_hotels/<str:name>/', views.edit_hotels, name='edit_hotels'),
    path('edit_specific_hotel/<int:id>/', views.edit_specific_hotel, name='edit_specific_hotel'),
    path('logout/', views.logout, name='logout'),
    path('book_hotel/<int:id>/', views.book_hotel, name='book_hotel'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('cancel_booking/<int:id>/', views.cancel_booking, name='cancel_booking'),
    path('rate_hotel/<int:id>/', views.rate_hotel, name='rate_hotel'),
    path('recommendations/', views.recommend_hotels, name='recommendations'),

]
