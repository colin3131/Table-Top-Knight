from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .forms import SignUpForm, VoteForm
from database.models import Vote, Event, Game

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

def handler404(request):
    return render(request, 'invalid.html')

# TODO
# Other Data Needed: 
def log_in(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    elif request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

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

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# VOTING PAGE
@login_required
def vote(request, eventID):
    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid():
            Vote.objects.create(
                event=Event.objects.get(pk=eventID),
                game=form.cleaned_data['game1'],
                rank=1,
                profile=request.user.profile
            )
            Vote.objects.create(
                event=Event.objects.get(pk=eventID),
                game=form.cleaned_data['game2'],
                rank=2,
                profile=request.user.profile
            )
            Vote.objects.create(
                event=Event.objects.get(pk=eventID),
                game=form.cleaned_data['game3'],
                rank=3,
                profile=request.user.profile
            )
            return redirect('myevent', eventID=eventID)
        else:
            form = VoteForm(eventID)
        return render(request, 'vote.html', {'form':form})

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
    game = Game.objects.get(pk=gameID)
    if request.method == 'POST':
        added = request.user.profile.addGame(game)
        if added:
            return redirect('library')
    game_owned = game in request.user.profile.getLibrary()
    return render(request, 'game.html', {"game": game, "game_owned": game_owned})

# TODO
# Other Data Needed: 
@login_required
def myevent(request, eventID):
    this_event = Event.objects.get(pk=eventID)
    return render(request, 'event.html', {"event": this_event})

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
def friend(request, userID):
    return render(request, 'friend.html', User.objects.get(pk=userID))

@login_required
def addfriend(request, userID):
    request.user.profile.addFriend(User.objects.get(pk=userID).profile)
    return redirect('friends')

# TODO
# Other pages: ?