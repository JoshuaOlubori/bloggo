from http.client import HTTPResponse
import re
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm,  UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import Profile

# Create your views here.

def user_login(request):
    if request.method == 'POST': # check if the request method is POST
        form = LoginForm(request.POST) # instantiate form, loaded with the request's POST data
        if form.is_valid(): # check if form is valid
            cd = form.cleaned_data # pass the clean data of form into variable cd
            user = authenticate(request, username=cd['username'], password=cd['password']) # check if the user is in the records by taking the user's username and password and returning the User object into the user variable
            if user is not None: # if user is present in records
                if user.is_active: # if user is flagged as active
                    login(request, user) # login the user; sets the user into the current session
                    return HTTPResponse('Authenticated successfully!') # display success message to the user
                else: # if user is flagged as inactive
                    return HttpResponse('Your account has been disabled. Contact admin for info')
            else: # if user is not present in records i.e new user
                return HttpResponse('Invalid login') # display message that user cannot login
    else: # if form is not valid
        form = LoginForm() # instantiate new login form
    return render(request, 'accounts/login.html', {'form': form}) # return login form


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
 # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
 # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
 # Save the User object
            new_user.save()
            return render(request,'accounts/register_done.html',{'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
 'accounts/register.html',
 {'user_form': user_form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # create a new user obj but don't save it yet
            new_user=user_form.save(commit=False)
            # set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            #save user obj
            new_user.save()
            # create user profile
            Profile.objects.create(user=new_user)
            return render(request, 'accounts/register_done.html', {'new_user': new_user})

    else:
        user_form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'user_form': user_form})