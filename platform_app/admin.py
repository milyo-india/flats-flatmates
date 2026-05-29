from django.contrib import admin

from .models import Listing, Match, SwipeAction, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_verified', 'diet', 'schedule']
    list_filter = ['is_verified', 'diet', 'schedule', 'gender']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'rent', 'posted_by', 'locality', 'is_active']
    list_filter = ['is_active', 'city', 'locality', 'pref_diet']
    search_fields = ['title', 'locality', 'posted_by__username']


@admin.register(SwipeAction)
class SwipeActionAdmin(admin.ModelAdmin):
    list_display = ['user', 'listing', 'action']
    list_filter = ['action']
    search_fields = ['user__username', 'listing__title']


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('listing', 'searcher', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('listing__title', 'searcher__username')
