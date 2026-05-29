import math

from django.contrib import auth
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ListingForm, LoginForm, SignUpForm, UserProfileForm
from .models import Listing, Match, SwipeAction


# ─── Helpers ────────────────────────────────────────────────────────────────────

def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance between two points on Earth (in km)."""
    R = 6371  # Earth's radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _get_filtered_listings(user):
    """Return active listings not posted by the user and not already swiped."""
    swiped_ids = SwipeAction.objects.filter(user=user).values_list('listing_id', flat=True)
    return Listing.objects.filter(is_active=True).exclude(
        posted_by=user
    ).exclude(
        id__in=swiped_ids
    )


def _sort_listings(listings, sort_param, user_profile):
    """Sort a queryset of listings according to the given sort parameter."""
    if sort_param == 'rent_asc':
        return listings.order_by('rent')
    elif sort_param == 'distance':
        # Distance from Bangalore center
        city_lat, city_lon = 12.9716, 77.5946
        listings_list = list(listings)
        listings_list.sort(key=lambda l: haversine(city_lat, city_lon, l.latitude, l.longitude))
        return listings_list
    else:
        # Default: relevance — match lifestyle preferences
        listings_list = list(listings)

        def relevance_score(listing):
            score = 0
            if user_profile.diet and listing.pref_diet and user_profile.diet == listing.pref_diet:
                score += 1
            if user_profile.schedule and listing.pref_schedule and user_profile.schedule == listing.pref_schedule:
                score += 1
            if user_profile.pets and listing.pref_pets and user_profile.pets == listing.pref_pets:
                score += 1
            if user_profile.smoking and listing.pref_smoking and user_profile.smoking == listing.pref_smoking:
                score += 1
            return score

        listings_list.sort(key=lambda l: (-relevance_score(l), l.rent))
        return listings_list


# ─── Auth Views ─────────────────────────────────────────────────────────────────

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/profile/setup/')
    else:
        form = SignUpForm()
    return render(request, 'auth/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('/login/')


# ─── Profile ────────────────────────────────────────────────────────────────────

@login_required
def profile_setup(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'profile_setup.html', {'form': form})


# ─── Discovery ──────────────────────────────────────────────────────────────────

@login_required
def discovery_feed(request):
    user_profile = request.user.profile
    current_sort = request.GET.get('sort', 'relevance')
    listings = _get_filtered_listings(request.user)
    sorted_listings = _sort_listings(listings, current_sort, user_profile)

    current_listing = sorted_listings[0] if sorted_listings else None

    return render(request, 'discovery.html', {
        'current_listing': current_listing,
        'current_sort': current_sort,
    })


# ─── Swipe ──────────────────────────────────────────────────────────────────────

@login_required
def swipe_action(request, listing_id):
    if request.method != 'POST':
        return redirect('/')

    listing = get_object_or_404(Listing, id=listing_id)
    action_value = request.POST.get('action', 'PASS')
    current_sort = request.POST.get('current_sort', 'relevance')

    swipe, created = SwipeAction.objects.get_or_create(
        user=request.user,
        listing=listing,
        defaults={'action': action_value},
    )
    if not created:
        swipe.action = action_value
        swipe.save()

    # Get next listing from remaining pool
    user_profile = request.user.profile
    remaining = _get_filtered_listings(request.user)
    sorted_remaining = _sort_listings(remaining, current_sort, user_profile)
    next_listing = sorted_remaining[0] if sorted_remaining else None

    if action_value == 'LIKE':
        Match.objects.get_or_create(
            listing=listing, 
            searcher=request.user,
            defaults={'status': 'PENDING'}
        )
        # Fall through to return next listing silently (no instant match modal)

    if next_listing:
        return render(request, 'components/house_card.html', {
            'listing': next_listing,
            'current_sort': current_sort,
        })
    else:
        return render(request, 'components/empty_state.html')


# ─── Listings ───────────────────────────────────────────────────────────────────

@login_required
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.posted_by = request.user
            listing.save()
            return redirect('platform:my_listings')
    else:
        form = ListingForm()
    return render(request, 'create_listing.html', {'form': form})

@login_required
def my_listings(request):
    listings = Listing.objects.filter(posted_by=request.user).order_by('-created_at')
    return render(request, 'my_listings.html', {'listings': listings})

@login_required
def edit_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id, posted_by=request.user)
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('platform:my_listings')
    else:
        form = ListingForm(instance=listing)
    return render(request, 'create_listing.html', {'form': form, 'is_edit': True})


# ─── Matches ────────────────────────────────────────────────────────────────────

@login_required
def matches_dashboard(request):
    matches = Match.objects.filter(
        Q(listing__posted_by=request.user) | Q(searcher=request.user),
        status='ACCEPTED',
    ).select_related('listing', 'searcher', 'searcher__profile', 'listing__posted_by', 'listing__posted_by__profile').distinct()
    return render(request, 'matches.html', {'matches': matches})


# ─── Interests (Lister side) ────────────────────────────────────────────────────

@login_required
def interests_feed(request):
    """Lister views people who liked their listings"""
    # Get all pending matches for listings posted by this user
    pending_matches = Match.objects.filter(
        listing__posted_by=request.user,
        status='PENDING'
    ).select_related('searcher', 'searcher__profile', 'listing').order_by('-created_at')
    
    current_match = pending_matches.first()
    
    return render(request, 'interests.html', {
        'current_match': current_match,
    })

@login_required
def interest_action(request, match_id):
    """Lister accepts or rejects an interest"""
    if request.method != 'POST':
        return redirect('/')
        
    match = get_object_or_404(Match, id=match_id, listing__posted_by=request.user)
    action_value = request.POST.get('action', 'PASS')
    
    if action_value == 'LIKE':
        match.status = 'ACCEPTED'
        match.save()
        
        searcher_profile = match.searcher.profile
        lister_profile = request.user.profile
        whatsapp_url = f'https://wa.me/91{searcher_profile.phone_number}'
        
        next_match = Match.objects.filter(
            listing__posted_by=request.user,
            status='PENDING'
        ).exclude(id=match_id).order_by('-created_at').first()
        
        return render(request, 'components/match_modal.html', {
            'listing': match.listing,
            'searcher_profile': searcher_profile,
            'lister_profile': lister_profile,
            'whatsapp_url': whatsapp_url,
            'next_match': next_match,
            'is_lister': True,
        })
    else:
        match.status = 'REJECTED'
        match.save()
        
        next_match = Match.objects.filter(
            listing__posted_by=request.user,
            status='PENDING'
        ).exclude(id=match_id).order_by('-created_at').first()
        
        if next_match:
            return render(request, 'components/profile_card.html', {
                'match': next_match,
            })
        else:
            return render(request, 'components/empty_state.html')
