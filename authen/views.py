from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from base.models import CartModel,OrderModel
from .models import ProfilePic
# Create your views here.
def login_(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        uname = request.POST['uname']
        pasw = request.POST['pasw']
        user = authenticate(username = uname,password = pasw)
        if user:
            login(request,user)
            messages.success(request,'login Sucessfully.......!')
            return redirect('home')
        else:
            messages.error(request,'Username or password is incorrect...!')
            return redirect('login_')
    return render(request, 'login_.html')

def register(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        uname = request.POST['uname']
        pasw = request.POST['pasw']
        confirm_pasw = request.POST['confirm_pasw']

        # Check username
        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username already exists.....!")
            return redirect('register')

        # Check password length
        if len(pasw) < 8:
            messages.error(request, "Password must be at least 8 characters long.....!")
            return redirect('register')

        # Check password confirmation
        if pasw != confirm_pasw:
            messages.error(request, "Passwords do not match.....!")
            return redirect('register')

        # Create user
        User.objects.create_user(
            first_name=fname,
            last_name=lname,
            email=email,
            username=uname,
            password=pasw,
        )

        messages.success(request, "New User Registered Successfully.....!")
        return redirect('login_')

    return render(request, 'register.html')


@login_required
def profile(request):
    cart_count = CartModel.objects.filter(host=request.user).count()
    profile = ProfilePic.objects.filter(host=request.user).first()

    return render(
        request,
        "profile.html",
        {
            'cart_count': cart_count,
            'profile': profile
        }
    )

@login_required
def logout_(request):

    logout(request)

    return redirect('login_')

@login_required
def update_profile(request):

    if request.method == 'POST':

        request.user.username = request.POST['uname']
        request.user.first_name = request.POST['fname']
        request.user.last_name = request.POST['lname']
        request.user.email = request.POST['email']

        request.user.save()

        pimage = request.FILES.get('pimage')

        if pimage:
            profile, created = ProfilePic.objects.get_or_create(
                host=request.user
            )

            profile.pimage = pimage
            profile.save()

        messages.success(request, "Profile updated successfully!")

        return redirect('profile')

    return render(request, 'update_profile.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        if 'old_pasw' in request.POST:
            print(request.POST)
            old_pasw = request.POST['old_pasw']
            user = authenticate (username = request.user.username,password = old_pasw)
            if user: 
                return render(request,'change_password.html',{'new':True})
            else:
                messages.error(request,'Enter old password is wrong')
                return redirect('change_password')
        else:
            if 'new_pasw' in request.POST:
                print(request.POST)
                new_pasw = request.POST['new_pasw']
                user = User.objects.get(username = request.user.username)
                user.set_password(new_pasw)
                user.save()
                messages.success(request,'Password Updated Sucessfully.....!')
                return redirect('login_')
    return render(request,'change_password.html')

@login_required
def my_orders(request):
    orders = OrderModel.objects.filter(host=request.user)
    return render(request, 'my_orders.html', {'orders': orders})


def forgot_password(request):

    if request.method == 'POST':

        # Step 1: Check username
        if 'uname' in request.POST and 'reset_password' not in request.POST:

            uname = request.POST['uname']

            try:
                user = User.objects.get(username=uname)
                return render(request, 'reset_password.html', {'user': user})

            except User.DoesNotExist:
                messages.error(request, 'Username does not exist.....!')
                return redirect('forgot_password')

        # Step 2: Reset password
        if 'reset_password' in request.POST:

            uname = request.POST['uname']
            new_pasw = request.POST['new_pasw']
            confirm_pasw = request.POST['confirm_pasw']

            if new_pasw != confirm_pasw:
                messages.error(request, 'Passwords do not match.....!')
                user = User.objects.get(username=uname)
                return render(request, 'reset_password.html', {'user': user})

            if len(new_pasw) < 8:
                messages.error(
                    request,
                    'Password must be at least 8 characters long.....!'
                )
                user = User.objects.get(username=uname)
                return render(request, 'reset_password.html', {'user': user})

            user = User.objects.get(username=uname)
            user.set_password(new_pasw)
            user.save()

            messages.success(request, 'Password reset successfully.....!')
            return redirect('login_')

    return render(request, 'forgot_password.html')