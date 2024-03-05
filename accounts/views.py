from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomRegistrationForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm
from django.urls import reverse
# from .forms import DashboardForm
# from .models import AudienceType, SocialService

def home_page(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def register(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}!')
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = CustomRegistrationForm()

    return render(request, 'register.html', {'form': form})

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'login.html'
    
    def get_success_url(self):
        return reverse('home') 

def logout_user(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('home')

# def dashboard(request):
#     if request.method == 'POST':
#         form = DashboardForm(request.POST)
#         if 'audience_submit' in request.POST:
#             if form.is_valid():
#                 selected_audience = form.cleaned_data['audience']
#                 user = request.user
#                 audience_type = AudienceType.objects.create(user=user, name=selected_audience)
#                 return render(request, 'dashboard.html', {'form': form, 'selected_audience': audience_type, 'social_platform_selected': False})
#         elif 'platform_submit' in request.POST:
#             if form.is_valid():
#                 selected_platform = form.cleaned_data['social_platform']
#                 user = request.user
#                 social_service = SocialService.objects.create(user=user, name=selected_platform)
#                 return redirect('create_order')
#     else:
#         form = DashboardForm()

#     return render(request, 'dashboard.html', {'form': form, 'selected_audience': None, 'social_platform_selected': False})






