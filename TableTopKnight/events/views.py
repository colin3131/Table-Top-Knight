from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from events.forms import SignUpForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def ourteam(request):
    return render(request, 'ourteam.html')

def contactus(request):
    return render(request, 'contactus.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# TODO
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

# TODO
@login_required
def library(request):
    return render(request, 'library.html')

# TODO
@login_required
def game(request, gameID=1):
    return render(request, 'game.html')

# TODO
@login_required
def myevent(request, eventID):
    return render(request, 'event.html')

# TODO
@login_required
def myevents(request):
    return render(request, 'myevents.html')

# TODO
@login_required
def friends(request):
    return render(request, 'myfriends.html')

# TODO
@login_required
def friend(request):
    return render(request, 'friend.html')
