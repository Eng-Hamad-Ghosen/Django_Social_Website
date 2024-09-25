from django.shortcuts import render
from .forms import LoginForm, UserEditForm, ProfileEditForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.hashers import make_password
from.forms import UserRegistrationForm
from . models import Profile
from django.contrib.auth.decorators import login_required


# Create your views here.


def user_login(request):
    if request.method=='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            print('000')
            if user:
                print('111')
                if user.is_active:
                    print('222')
                    login(request,user)
                else:
                    print('Not active')
            else:
                print('invalid Login')
                    
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form':form})
        
    
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.name = new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required(login_url='user_login')
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})