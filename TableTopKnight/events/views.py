from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, VoteForm
from .models import Vote, Event, Game

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
def log_in(request):
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

# VOTING PAGE
def vote(request, eventID):
    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid():
            Vote.objects.create(
                event=Event.objects.get(pk=eventID),
                game=form.cleaned_data['game1'],
                rank=form.cleaned_data['rank1']
            )
            Vote.objects.create(
                event=Event.objects.get(pk=eventID),
                game=form.cleaned_data['game2'],
                rank=form.cleaned_data['rank2']
            )
            Vote.objects.create(
                event=Event.objects.get(pk=eventID),
                game=form.cleaned_data['game3'],
                rank=form.cleaned_data['rank3']
            )
            return redirect('myevent', eventID=eventID)
        else:
            game_choices = [(game, game.gameName) for game in Event.objects.get(pk=eventID).getFilteredGames()]
            form = VoteForm(game_choices=game_choices)
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