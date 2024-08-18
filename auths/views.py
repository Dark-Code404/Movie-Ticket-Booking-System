from datetime import datetime
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from auths.models import UserProfile
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def register(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        email = request.POST.get('email')
        password = request.POST.get('passw')
        confirm_password = request.POST.get('passwo')
        mobile = request.POST.get('mobile')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('register')

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            UserProfile.objects.create(user=user, mobile=mobile, gender=gender, dob=dob)
            messages.success(request, "Registration successful")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('register')

    return render(request, 'register.html')

def Login(request):
    if request.method == 'POST':
        identifier = request.POST.get('email')
        userpass = request.POST.get('passw')

        myuser = authenticate(username=identifier, password=userpass)

        if myuser is None:
            try:
                user_with_email = User.objects.get(email=identifier)
                myuser = authenticate(username=user_with_email.username, password=userpass)
            except User.DoesNotExist:
                myuser = None

        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Login Success")
            request.session['username'] = myuser.username
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'login.html')

@login_required(login_url='/auth/login/')
def user_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    context = {
        'user_profile': user_profile,
    }
    return render(request, 'user_profile.html', context)

@login_required(login_url='/auth/login/')
def edit_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        dob = request.POST.get('dob')
        mobile = request.POST.get('mobile')
        gender = request.POST.get('gender')

        # Check if the new username already exists
        if User.objects.filter(username=username).exclude(id=request.user.id).exists():
            messages.error(request, "Username already exists. Please choose a different one.")
            return redirect('edit_profile')

        # Update User model fields
        user = request.user
        user.username = username
        user.email = email
        user.save()

        # Update UserProfile model fields
        user_profile.first_name = first_name
        user_profile.last_name = last_name
        user_profile.dob = dob
        user_profile.mobile = mobile
        user_profile.gender = gender

        # Handle profile image upload
        if 'profile_image' in request.FILES:
            user_profile.profile_image = request.FILES['profile_image']

        user_profile.save()

        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('user_profile') 

    context = {
        'user_profile': user_profile,
    }
    return render(request, 'edit_profile.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)

    context = {
        'form': form,
    }
    return render(request, 'change_password.html', context)

def Logout(request):
    logout(request)
    return redirect(reverse('login'))
