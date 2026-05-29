from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Listing, UserProfile

# ─── Shared CSS classes ─────────────────────────────────────────────────────────

INPUT_CSS = (
    'w-full px-4 py-3 rounded-xl border border-gray-200 bg-white '
    'focus:ring-2 focus:ring-indigo-500 focus:border-transparent '
    'transition-all duration-200 text-gray-800 placeholder-gray-400'
)

SELECT_CSS = (
    'w-full px-4 py-3 rounded-xl border border-gray-200 bg-white '
    'focus:ring-2 focus:ring-indigo-500 focus:border-transparent '
    'transition-all duration-200 text-gray-800'
)

TEXTAREA_CSS = (
    'w-full px-4 py-3 rounded-xl border border-gray-200 bg-white '
    'focus:ring-2 focus:ring-indigo-500 focus:border-transparent '
    'transition-all duration-200 text-gray-800 resize-none h-24'
)

FILE_CSS = (
    'w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 '
    'file:rounded-xl file:border-0 file:text-sm file:font-medium '
    'file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'
)


# ─── Forms ──────────────────────────────────────────────────────────────────────

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = INPUT_CSS
            field.widget.attrs['placeholder'] = field.label or field_name.replace('_', ' ').title()


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['username', 'password']:
            self.fields[field_name].widget.attrs['class'] = INPUT_CSS
            self.fields[field_name].widget.attrs['placeholder'] = self.fields[field_name].label


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'profile_picture', 'age', 'bio', 'gender',
            'diet', 'schedule', 'pets', 'smoking', 'phone_number',
        ]
        help_texts = {
            'phone_number': 'WhatsApp number suggested',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        select_fields = {'gender', 'diet', 'schedule', 'pets', 'smoking'}
        for field_name, field in self.fields.items():
            if field_name == 'profile_picture':
                field.widget.attrs['class'] = FILE_CSS
            elif field_name == 'bio':
                field.widget = forms.Textarea(attrs={
                    'class': TEXTAREA_CSS,
                    'placeholder': 'Tell potential flatmates about yourself...',
                })
            elif field_name in select_fields:
                field.widget.attrs['class'] = SELECT_CSS
            else:
                field.widget.attrs['class'] = INPUT_CSS
                field.widget.attrs['placeholder'] = field.label or field_name.replace('_', ' ').title()


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            'title', 'description', 'rent', 'security_deposit',
            'available_from', 'room_image', 'image_url',
            'latitude', 'longitude', 'locality', 'city',
            'pref_diet', 'pref_schedule', 'pref_pets', 'pref_smoking',
        ]
        help_texts = {
            'latitude': 'e.g., 19.076',
            'longitude': 'e.g., 72.8777',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        select_fields = {'pref_diet', 'pref_schedule', 'pref_pets', 'pref_smoking', 'city'}

        self.fields['available_from'].widget = forms.DateInput(attrs={
            'type': 'date',
            'class': INPUT_CSS,
        })

        for field_name, field in self.fields.items():
            if field_name == 'available_from':
                continue  # already set above
            elif field_name == 'room_image':
                field.widget.attrs['class'] = FILE_CSS
            elif field_name == 'description':
                field.widget = forms.Textarea(attrs={
                    'class': TEXTAREA_CSS,
                    'placeholder': 'Describe the room and flat...',
                })
            elif field_name in select_fields:
                field.widget.attrs['class'] = SELECT_CSS
            else:
                field.widget.attrs['class'] = INPUT_CSS
                placeholder = field.label or field_name.replace('_', ' ').title()
                field.widget.attrs['placeholder'] = placeholder
