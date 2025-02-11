from idlelib.rpc import request_queue

from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList, PasswordResetForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth.hashers import make_password
@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request, username = request.POST['username'], password = request.POST['password']
        )
        if user is None:
            template_data['error'] = 'The username or password you entered is invalid.'
            return render(request, 'accounts/login.html', {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')

def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html', {'template_data': template_data})

def password_reset(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            security_answer = form.cleaned_data["security_answer"].strip().lower()
            new_password = form.cleaned_data["new_password"]
            confirm_password = form.cleaned_data["confirm_password"]

            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return render(request, "accounts/reset_password.html", {"form": form})

            try:
                user = User.objects.get(username=username, email=email)
                user_profile = UserProfile.objects.get(user=user)

                if user_profile.security_question.lower() == security_answer:
                    user.set_password(new_password)
                    user.save()

                    messages.success(request, "Your password has been reset. You can now log in.")
                    return redirect("accounts.login")
                else:
                    messages.error(request, "Incorrect answer to the security question.")

            except (User.DoesNotExist, UserProfile.DoesNotExist):
                messages.error(request, "User not found. Please check your details.")

    else:
        form = PasswordResetForm()

    return render(request, "accounts/reset_password.html", {"form": form})