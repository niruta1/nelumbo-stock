from django.shortcuts import render, redirect, HttpResponse
from inventory.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from inventory.models import CustomUser
from .forms import RegistrationForm


def base(request):
    return render(request, 'base.html')


def LOGIN(request):
    return render(request, 'login.html')


def do_login(request):
    if request.method == "POST":
        user = EmailBackEnd.authenticate(request,
                                         username=request.POST.get('email'),
                                         password=request.POST.get('password'))
        if user != None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('hod_home')
            elif user_type == '2':
                return redirect('staff_home')
            elif user_type == '3':
                return HttpResponse('This is DCEC Panel')
            else:
                messages.error(request, 'Email and password are invalid!')
                return redirect('login')
        else:
            messages.error(request, 'Email and password are invalid!')
            return redirect('login')
    return render(request, 'login.html')  # Render the initial login page



def do_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/')
def profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    context = {
        "user": user,
    }
    return render(request, 'profile.html', context)


@login_required(login_url='/')
def profile_update(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        # email = request.POST.get('email')
        # username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)

            customuser.first_name = first_name
            customuser.last_name = last_name

            if password != None and password != "":
                customuser.set_password(password)

            if profile_pic != None and profile_pic != "":
                customuser.profile_pic = profile_pic
            customuser.save()
            messages.success(request, 'Your Profile Is Updated Successfully!')
            return redirect('Profile')
        except:
            messages.error(request, 'Failed To Update Your Profile!')
    return render(request, 'profile.html')



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Check if the email or username is already registered
            if CustomUser.objects.filter(email=form.cleaned_data['email']).exists():
                form.add_error('email', 'This email is already registered.')
            elif CustomUser.objects.filter(username=form.cleaned_data['username']).exists():
                form.add_error('username', 'This username is already taken.')
            else:
                # Create the user account
                new_user = CustomUser.objects.create_user(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                    email=form.cleaned_data['email'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name']
                )
                new_user.profile_pic = form.cleaned_data['profile_pic']
                new_user.save()
                
                # Log in the user
                user = authenticate(
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password']
                )
                if user is not None:
                    login(request, user)
                    return redirect('home')  # Redirect to the dashboard page
                    
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})