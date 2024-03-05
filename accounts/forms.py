# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from .models import AudienceType, SocialService
from .models import CustomUser

class CustomRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        
class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

# class DashboardForm(forms.Form):
#     audience = forms.ChoiceField(choices=AudienceType.AUDIENCE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
#     social_platform = forms.ChoiceField(choices=SocialService.SOCIAL_SERVICE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))


