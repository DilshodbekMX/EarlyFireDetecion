from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import LoginForm, UserRegistrationForm


# Create your views here.
def loginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('director:index')
                else:
                    return render(request, 'authentication/login.html', {'error_message': 'Disabled account', 'form': form})
            else:
                return render(request, 'authentication/login.html', {'error_message': 'Invalid login', 'form': form})
    else:
        form = LoginForm()
    return render(request, 'authentication/login.html', {'form': form})


def registerView(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password( form.cleaned_data['password'])
            new_user.save()

            return render(request, 'authentication/register_done.html', {'new_user': new_user})
    else:
        form = UserRegistrationForm()
    return render(request, 'authentication/register.html', {'form': form})

@login_required
def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('inspector:index'))
