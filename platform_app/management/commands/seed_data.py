import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from platform_app.models import Listing, UserProfile


class Command(BaseCommand):
    help = 'Seed the database with demo users and listings for Flats & Flatmates'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Clearing existing demo data...'))

        # Clear existing demo users (cascades to profiles, listings, swipes, matches)
        User.objects.filter(username__startswith='demo_').delete()
        User.objects.filter(username='testuser').delete()

        # ─── Demo Users ─────────────────────────────────────────────────────

        users_data = [
            {
                'username': 'demo_priya',
                'first_name': 'Priya',
                'last_name': 'Sharma',
                'profile': {
                    'age': 26,
                    'bio': 'Product designer who loves minimalist spaces and chai. Weekend potter. Looking for a peaceful flatmate who respects boundaries.',
                    'gender': 'female',
                    'diet': 'veg',
                    'schedule': 'early_bird',
                    'pets': 'no_pets',
                    'smoking': 'non_smoker',
                    'phone_number': '9876543210',
                },
            },
            {
                'username': 'demo_arjun',
                'first_name': 'Arjun',
                'last_name': 'Mehta',
                'profile': {
                    'age': 28,
                    'bio': 'Software engineer at a fintech startup. Guitar player, coffee snob, and terrible cook. Clean freak though!',
                    'gender': 'male',
                    'diet': 'nonveg',
                    'schedule': 'night_owl',
                    'pets': 'pet_friendly',
                    'smoking': 'non_smoker',
                    'phone_number': '9876543211',
                },
            },
            {
                'username': 'demo_sneha',
                'first_name': 'Sneha',
                'last_name': 'Iyer',
                'profile': {
                    'age': 24,
                    'bio': 'Freelance content writer. Dog mom to a golden retriever named Mango. Need a pet-loving flatmate!',
                    'gender': 'female',
                    'diet': 'nonveg',
                    'schedule': 'night_owl',
                    'pets': 'has_pets',
                    'smoking': 'non_smoker',
                    'phone_number': '9876543212',
                },
            },
            {
                'username': 'demo_rohan',
                'first_name': 'Rohan',
                'last_name': 'Desai',
                'profile': {
                    'age': 30,
                    'bio': 'CA by day, stand-up comedian by night. I promise my jokes are better than my cooking.',
                    'gender': 'male',
                    'diet': 'veg',
                    'schedule': 'night_owl',
                    'pets': 'no_pets',
                    'smoking': 'occasional',
                    'phone_number': '9876543213',
                },
            },
            {
                'username': 'demo_ananya',
                'first_name': 'Ananya',
                'last_name': 'Kapoor',
                'profile': {
                    'age': 27,
                    'bio': 'Yoga instructor and plant mom. My room smells like lavender and looks like a jungle. Looking for someone chill.',
                    'gender': 'female',
                    'diet': 'vegan',
                    'schedule': 'early_bird',
                    'pets': 'pet_friendly',
                    'smoking': 'non_smoker',
                    'phone_number': '9876543214',
                },
            },
            {
                'username': 'demo_vikram',
                'first_name': 'Vikram',
                'last_name': 'Singh',
                'profile': {
                    'age': 29,
                    'bio': 'Data scientist who works from home. Board game enthusiast. Looking for flatmates who are up for game nights!',
                    'gender': 'male',
                    'diet': 'nonveg',
                    'schedule': 'night_owl',
                    'pets': 'no_pets',
                    'smoking': 'non_smoker',
                    'phone_number': '9876543215',
                },
            },
            {
                'username': 'demo_meera',
                'first_name': 'Meera',
                'last_name': 'Reddy',
                'profile': {
                    'age': 25,
                    'bio': 'Medical resident surviving on coffee and optimism. Neat, quiet, and rarely home. The perfect flatmate, honestly.',
                    'gender': 'female',
                    'diet': 'veg',
                    'schedule': 'early_bird',
                    'pets': 'no_pets',
                    'smoking': 'non_smoker',
                    'phone_number': '9876543216',
                },
            },
            {
                'username': 'demo_karan',
                'first_name': 'Karan',
                'last_name': 'Patel',
                'profile': {
                    'age': 31,
                    'bio': 'Architect with an obsession for well-designed spaces. I will judge your furniture choices. Fair warning.',
                    'gender': 'male',
                    'diet': 'nonveg',
                    'schedule': 'early_bird',
                    'pets': 'pet_friendly',
                    'smoking': 'non_smoker',
                    'phone_number': '9876543217',
                },
            },
        ]

        created_users = {}
        for data in users_data:
            user = User.objects.create_user(
                username=data['username'],
                password='testpass123',
                first_name=data['first_name'],
                last_name=data['last_name'],
            )
            # Update the auto-created profile
            profile = user.profile
            for key, value in data['profile'].items():
                setattr(profile, key, value)
            profile.save()

            created_users[data['username']] = user
            self.stdout.write(f"  ✓ Created user: {data['first_name']} {data['last_name']} ({data['username']})")

        # ─── Listings ────────────────────────────────────────────────────────

        available_from = datetime.date.today() + datetime.timedelta(days=30)

        listings_data = [
            {
                'user': 'demo_priya',
                'title': 'Sunny 2BHK in Indiranagar',
                'description': 'Spacious room in a well-maintained 2BHK. Balcony, modular kitchen, 24/7 water supply. 5 mins walk from 100ft road.',
                'rent': 22000,
                'security_deposit': 44000,
                'locality': 'Indiranagar',
                'lat': 12.9784,
                'lon': 77.6408,
                'pref_diet': 'veg',
                'pref_schedule': 'early_bird',
                'pref_pets': 'no_pets',
                'pref_smoking': 'non_smoker',
                'image_url': 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop',
            },
            {
                'user': 'demo_arjun',
                'title': 'Modern Flat near Koramangala Sony World',
                'description': 'Fully furnished room with AC in a gated society. Gym, pool, and clubhouse access. Startups hub walkable.',
                'rent': 28000,
                'security_deposit': 56000,
                'locality': 'Koramangala',
                'lat': 12.9352,
                'lon': 77.6245,
                'pref_diet': 'nonveg',
                'pref_schedule': 'night_owl',
                'pref_pets': 'pet_friendly',
                'pref_smoking': 'non_smoker',
                'image_url': 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&h=600&fit=crop',
            },
            {
                'user': 'demo_sneha',
                'title': 'Pet-Friendly 3BHK in HSR Layout',
                'description': 'Large room with attached bathroom in a pet-friendly building. Near Agara lake. Building has a garden for dog walks.',
                'rent': 18000,
                'security_deposit': 36000,
                'locality': 'HSR Layout',
                'lat': 12.9121,
                'lon': 77.6446,
                'pref_diet': 'nonveg',
                'pref_schedule': 'night_owl',
                'pref_pets': 'has_pets',
                'pref_smoking': 'non_smoker',
                'image_url': 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop',
            },
            {
                'user': 'demo_rohan',
                'title': 'Cozy Room in Jayanagar',
                'description': 'Compact but well-designed room in a heritage building. Rooftop access with city views. Walking distance to Metro.',
                'rent': 15000,
                'security_deposit': 30000,
                'locality': 'Jayanagar',
                'lat': 12.9299,
                'lon': 77.5824,
                'pref_diet': 'veg',
                'pref_schedule': 'night_owl',
                'pref_pets': 'no_pets',
                'pref_smoking': 'occasional',
                'image_url': 'https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=800&h=600&fit=crop',
            },
            {
                'user': 'demo_ananya',
                'title': 'Zen Loft in Whitefield',
                'description': 'Beautifully done-up room with lots of natural light and plants. Terrace access. Perfect for someone working in ITPL.',
                'rent': 25000,
                'security_deposit': 50000,
                'locality': 'Whitefield',
                'lat': 12.9698,
                'lon': 77.7499,
                'pref_diet': 'vegan',
                'pref_schedule': 'early_bird',
                'pref_pets': 'pet_friendly',
                'pref_smoking': 'non_smoker',
                'image_url': 'https://images.unsplash.com/photo-1536376072261-38c75010e6c9?w=800&h=600&fit=crop',
            },
            {
                'user': 'demo_vikram',
                'title': 'Tech Hub Room in Mahadevpura',
                'description': 'Room in a modern high-rise with coworking space in the building. High-speed internet included. Near Phoenix Mall.',
                'rent': 30000,
                'security_deposit': 60000,
                'locality': 'Mahadevpura',
                'lat': 12.9880,
                'lon': 77.6895,
                'pref_diet': 'nonveg',
                'pref_schedule': 'night_owl',
                'pref_pets': 'no_pets',
                'pref_smoking': 'non_smoker',
                'image_url': 'https://images.unsplash.com/photo-1554995207-c18c203602cb?w=800&h=600&fit=crop',
            },
            {
                'user': 'demo_meera',
                'title': 'Quiet Studio near JP Nagar',
                'description': 'Independent studio-style room with kitchenette. Very quiet building, perfect for odd-hour schedules.',
                'rent': 16000,
                'security_deposit': 32000,
                'locality': 'JP Nagar',
                'lat': 12.9063,
                'lon': 77.5857,
                'pref_diet': 'veg',
                'pref_schedule': 'early_bird',
                'pref_pets': 'no_pets',
                'pref_smoking': 'non_smoker',
                'image_url': 'https://images.unsplash.com/photo-1585412727339-54e4bae3bbf9?w=800&h=600&fit=crop',
            },
            {
                'user': 'demo_karan',
                'title': 'Designer Flat in MG Road',
                'description': 'Architect-designed space with custom furniture. Floor-to-ceiling windows, city view. Building has infinity pool.',
                'rent': 35000,
                'security_deposit': 70000,
                'locality': 'MG Road',
                'lat': 12.9733,
                'lon': 77.6083,
                'pref_diet': 'nonveg',
                'pref_schedule': 'early_bird',
                'pref_pets': 'pet_friendly',
                'pref_smoking': 'non_smoker',
                'image_url': 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&h=600&fit=crop',
            },
        ]

        for data in listings_data:
            Listing.objects.create(
                posted_by=created_users[data['user']],
                title=data['title'],
                description=data['description'],
                rent=data['rent'],
                security_deposit=data['security_deposit'],
                available_from=available_from,
                locality=data['locality'],
                latitude=data['lat'],
                longitude=data['lon'],
                pref_diet=data['pref_diet'],
                pref_schedule=data['pref_schedule'],
                pref_pets=data['pref_pets'],
                pref_smoking=data['pref_smoking'],
                image_url=data['image_url'],
            )
            self.stdout.write(f"  ✓ Created listing: {data['title']} (₹{data['rent']}/mo)")

        # ─── Test User ──────────────────────────────────────────────────────

        test_user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='Test',
            last_name='User',
        )
        profile = test_user.profile
        profile.age = 27
        profile.diet = 'nonveg'
        profile.schedule = 'night_owl'
        profile.pets = 'pet_friendly'
        profile.smoking = 'non_smoker'
        profile.phone_number = '9999999999'
        profile.bio = 'A test user for exploring the platform.'
        profile.save()
        self.stdout.write(f"  ✓ Created test user: testuser (password: testpass123)")

        # ─── Summary ────────────────────────────────────────────────────────

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('═' * 50))
        self.stdout.write(self.style.SUCCESS('Seed data created successfully!'))
        self.stdout.write(self.style.SUCCESS('═' * 50))
        self.stdout.write(f"  Users created: {len(users_data) + 1}")
        self.stdout.write(f"  Listings created: {len(listings_data)}")
        self.stdout.write(f"  Test login: testuser / testpass123")
        self.stdout.write(self.style.SUCCESS('═' * 50))
