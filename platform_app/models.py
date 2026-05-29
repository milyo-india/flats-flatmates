from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# ─── Choices ────────────────────────────────────────────────────────────────────

DIET_CHOICES = [('veg', 'Pure Veg'), ('nonveg', 'Non-Veg'), ('vegan', 'Vegan')]
SCHEDULE_CHOICES = [('early_bird', 'Early Bird'), ('night_owl', 'Night Owl')]
PETS_CHOICES = [('has_pets', 'Has Pets'), ('no_pets', 'No Pets'), ('pet_friendly', 'Pet Friendly')]
SMOKING_CHOICES = [('non_smoker', 'Non-Smoker'), ('smoker', 'Smoker'), ('occasional', 'Occasional')]
GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('nonbinary', 'Non-binary'),
    ('prefer_not', 'Prefer not to say'),
]
ACTION_CHOICES = [('LIKE', 'Like'), ('PASS', 'Pass')]


# ─── Models ─────────────────────────────────────────────────────────────────────

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    bio = models.TextField(max_length=300, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True)
    is_verified = models.BooleanField(default=True)
    diet = models.CharField(max_length=20, choices=DIET_CHOICES, blank=True)
    schedule = models.CharField(max_length=20, choices=SCHEDULE_CHOICES, blank=True)
    pets = models.CharField(max_length=20, choices=PETS_CHOICES, blank=True)
    smoking = models.CharField(max_length=20, choices=SMOKING_CHOICES, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    @property
    def profile_picture_url(self):
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            try:
                return self.profile_picture.url
            except ValueError:
                pass
        return f'https://i.pravatar.cc/300?u={self.user.username}'


class Listing(models.Model):
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=200)
    description = models.TextField()
    rent = models.PositiveIntegerField()
    security_deposit = models.PositiveIntegerField()
    available_from = models.DateField()
    room_image = models.ImageField(upload_to='listings/', blank=True, null=True)
    image_url = models.URLField(blank=True, help_text='Fallback image URL for seeded data')
    latitude = models.FloatField()
    longitude = models.FloatField()
    locality = models.CharField(max_length=100)
    city = models.CharField(max_length=50, default='Bangalore')
    pref_diet = models.CharField(max_length=20, choices=DIET_CHOICES, blank=True)
    pref_schedule = models.CharField(max_length=20, choices=SCHEDULE_CHOICES, blank=True)
    pref_pets = models.CharField(max_length=20, choices=PETS_CHOICES, blank=True)
    pref_smoking = models.CharField(max_length=20, choices=SMOKING_CHOICES, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - ₹{self.rent}/mo"

    @property
    def display_image_url(self):
        if self.room_image and hasattr(self.room_image, 'url'):
            try:
                return self.room_image.url
            except ValueError:
                pass
        if self.image_url:
            return self.image_url
        return 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop'


class SwipeAction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='swipes')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='swipes')
    action = models.CharField(max_length=4, choices=ACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'listing']

    def __str__(self):
        return f"{self.user.username} → {self.action} → {self.listing.title}"


class Match(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='matches')
    searcher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_searcher')
    STATUS_CHOICES = [('PENDING', 'Pending'), ('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected')]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['listing', 'searcher']

    def __str__(self):
        return f"Match: {self.searcher.username} ↔ {self.listing.title}"


# ─── Signals ────────────────────────────────────────────────────────────────────

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
