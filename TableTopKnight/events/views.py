from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from events.forms import SignUpForm

# TODO
# Other Data Needed: 
def home(request):
    return render(request, 'home.html')

# TODO
# Other Data Needed: 
def ourteam(request):
    return render(request, 'ourteam.html')

# TODO
# Other Data Needed: 
def contactus(request):
    return render(request, 'contactus.html')

# TODO
# Other Data Needed: 
def login(request):
    return render(request, 'login.html')

# SIGN UP PAGE
# 
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

# All user data is included by default
# Need to create forms for: Creating an event, voting (possibly), and adding to library (possibly)

# TODO
# Other Data Needed: 
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

# TODO
# Other Data Needed: 
@login_required
def library(request):
    return render(request, 'library.html')

# TODO
# Other Data Needed: 
@login_required
def game(request, gameID=1):
    return render(request, 'game.html')

# TODO
# Other Data Needed: 
@login_required
def myevent(request, eventID):
    return render(request, 'event.html')

# TODO
# Other Data Needed: 
@login_required
def myevents(request):
    return render(request, 'myevents.html')

# TODO
# Other Data Needed: 
@login_required
def friends(request):
    return render(request, 'myfriends.html')

# TODO
# Other Data Needed: 
@login_required
def friend(request):
    return render(request, 'friend.html')

# TODO
# Other pages: ?