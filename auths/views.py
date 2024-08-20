
from  django. contrib import  messages as msg
from  django. shortcuts import get_object_or_404, redirect, render
from  django.contrib.auth.models import  User
from  django.contrib.auth import login, logout,authenticate
from  django.contrib.auth.decorators import login_required
from  MT_main.models import Bookings
from  auths. models import UserProfile
from django.contrib.auth.forms import PasswordChangeForm
from  django.contrib.auth import update_session_auth_hash
from django. urls import reverse

def register(request):
    if request.method =='POST' :
        username =request.POST.get('uname')
        email =request.POST.get('email')
        passw =request.POST.get('passw')
        repassw =request.POST.get('passwo')
        mobile =request.POST.get('mobile')
        gender =request.POST.get('gender')
        dob =request.POST.get('dob')

        if passw != repassw:
            msg.error(request, "Password not matched")
            return redirect('register')

        if User.objects.filter (username=username).exists() :
            msg.error(request, "Username already exists")
            return redirect('register')

        if User.objects.filter (email=email).exists() :
            msg.error(request, "Email already exists")
            return redirect('register')

        try:
            user=User.objects.create_user(username=username , email=email , password=passw)
            UserProfile.objects.create(user=user,mobile=mobile , gender=gender, dob=dob)
            msg.success(request, "Registration successful")
            return redirect('login')
        except Exception as e :
            msg.error(request, f"An error occurred: {str(e)}")
            return redirect('register')

    return render(request, 'register.html')

def Login(request):
    if request.method == 'POST' :
        email = request. POST. get('email')
        passw = request. POST. get('passw')

        account_login = authenticate(username=email, password=passw)

        if account_login is None:
            try:
                user_with_email = User.objects.get(email=email)
                account_login = authenticate(username=user_with_email.username, password=passw)
            except User.DoesNotExist:
                account_login = None

   
   
   
        if account_login is not None:
            login(request, account_login)
            msg.success(request, "Login Success")
            request.session['username'] = account_login.username
            return redirect("home")
        else:
            msg.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'login.html')

@login_required(login_url='/auth/login/')
def user_profile(request) :
    counts=Bookings.objects.filter(user=request.user).count()
    profile=get_object_or_404(UserProfile, user=request.user)
    context = {
        'user_profile': profile,
        'total_booking_count': counts,
    }
    return render( request, 'user_profile.html', context )

@login_required(login_url='/auth/login/')
def edit_profile(request) :
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method=="POST":
        fname=request.POST.get('first_name')
        lname=request.POST.get('last_name')
        username=request.POST.get('username')
        email=request.POST.get('email')
        dob=request.POST.get('dob')
        mobile_no=request.POST.get('mobile')
        gender=request.POST.get('gender')

      
        if User.objects.filter(username=username).exclude(id=request.user.id).exists():
            msg.error(request, "Username already exists")
            return redirect('edit_profile')

       
        user = request.user
        user.username = username
        user.email = email
        user.save()

        user_profile.first_name = fname
        user_profile.last_name = lname
        user_profile.dob = dob
        user_profile.mobile = mobile_no
        user_profile.gender = gender

         
        if 'profile_image' in request.FILES:
            user_profile.profile_image = request.FILES['profile_image']

        user_profile.save()

        msg.success(request, 'Profile updated successfully')
        return redirect('user_profile')


    context = {
        'user_profile': user_profile,
    }
    return render(request, 'edit_profile.html', context)

@login_required
def change_password(request):
    if request.method== 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            msg.success(request, 'Your password was successfully updated!')
            return redirect('user_profile')
        else:
            msg.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)

    context = {
        'form': form,
    }
    return render(request, 'change_password.html', context)

def Logout(request):
    logout(request)
    return redirect(reverse('login'))
