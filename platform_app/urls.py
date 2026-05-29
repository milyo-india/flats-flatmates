from django.urls import path

from . import views

app_name = 'platform'

urlpatterns = [
    path('', views.discovery_feed, name='discovery'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/setup/', views.profile_setup, name='profile_setup'),
    path('swipe/<int:listing_id>/', views.swipe_action, name='swipe'),
    path('interests/', views.interests_feed, name='interests'),
    path('interest/<int:match_id>/', views.interest_action, name='interest_action'),
    path('listing/create/', views.create_listing, name='create_listing'),
    path('my-listings/', views.my_listings, name='my_listings'),
    path('listing/<int:listing_id>/edit/', views.edit_listing, name='edit_listing'),
    path('matches/', views.matches_dashboard, name='matches'),
]
