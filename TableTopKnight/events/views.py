from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .forms import SignUpForm, VoteForm, EventForm, FriendForm, PendingPlayerForm
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

def handler404(request, exception):
    return render(request, 'invalid.html')

# TODO
# Other Data Needed:
def log_in(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    elif request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
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
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# All user data is included by default
# Need to create forms for: Creating an event, voting (possibly), and adding to library (possibly)

@login_required
def newevent(request):
    if request.method == 'POST':
        form = EventForm(data=request.POST, userID=request.user.id)
        if form.is_valid():
            event = form.save(commit=False)
            event.host = request.user.profile
            event.event_state='PV'
            event.save()
            form.save_m2m()
            event.sendInvites()
            return redirect('myevent', event.id)
    else:
        form = EventForm(userID=request.user.id)
    return render(request, 'createevent.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def addfriend(request):
    if request.method == 'POST':
        form = FriendForm(data=request.POST, userid=request.user.id)
        if form.is_valid():
            usr = form.cleaned_data.get('friendName')
            newfriend = User.objects.get(username=usr).profile
            request.user.profile.sendFriendRequest(newfriend)
            return redirect('friends')
    else:
        form = FriendForm(userid=request.user.id)
    return render(request, 'addfriend.html', {"form": form})

@login_required
def addpendingplayer(request, eventID):
    if request.method == 'POST':
        form = PendingPlayerForm(data=request.POST, userid=request.user.id, eventid=eventID)
        if form.is_valid():
            usr = form.cleaned_data.get('playerName')
            newpending = User.objects.get(username=usr).profile
            cur_event = Event.objects.get(pk=eventID)
            cur_event.addPending(newpending)
            cur_event.save()
            cur_event.sendInvite(newpending.user.pk)
            return redirect('myevent', eventID)
    else:
        form = PendingPlayerForm(userid=request.user.id, eventid=eventID)
    return render(request, 'addpending.html', {"form": form})


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
    return render(request, 'dashboard.html', {
        "events_hosting": request.user.profile.getEventsHosting(),
        "events_attending": request.user.profile.getEventsAttending(),
        "library": request.user.profile.getLibrary(),
        "notifications": request.user.profile.getNotifications(),
    })

# TODO
# Other Data Needed:
@login_required
def library(request):
    return render(request, 'library.html', {"library": request.user.profile.getLibrary()})

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
    return render(request, 'events.html', {
        "events_hosting": request.user.profile.getEventsHosting(),
        "events_attending": request.user.profile.getEventsAttending(),
    })

# TODO
# Other Data Needed:
@login_required
def friends(request):
    return render(request, 'myfriends.html', {"friends": request.user.profile.getFriends()})

# TODO
# Other Data Needed:
@login_required
def friend(request, userID):
    return render(request, 'friend.html', {"friend": User.objects.get(pk=userID)})

@login_required
def eventrequest(request, eventID):
    return render(request, "eventrequest.html", {"event": Event.objects.get(pk=eventID)})

@login_required
def joinevent(request, eventID):
    cur_event = Event.objects.get(pk=eventID)
    cur_event.addAttendee(request.user.profile)
    cur_event.removePending(request.user.profile)
    request.user.profile.removeNotification(
        request.user.profile.getNotifications().get(link="/events/"+str(eventID)+"/request")
    )
    return redirect('myevent', eventID)

@login_required
def rejectevent(request, eventID):
    cur_event = Event.objects.get(pk=eventID)
    cur_event.removePending(request.user.profile)
    request.user.profile.removeNotification(
        request.user.profile.getNotifications().get(link="/events/"+str(eventID)+"/request")
    )
    return redirect('myevents')

@login_required
def leaveevent(request, eventID):
    cur_event = Event.objects.get(pk=eventID)
    cur_event.removeAttendee(request.user.profile)
    return redirect('myevents')

@login_required # called via /games/<id>/add
def addgame(request, gameID):
    request.user.profile.addGame(Game.objects.get(pk=gameID))
    return redirect('library')

@login_required # called via /games/<id>/remove
def removegame(request, gameID):
    request.user.profile.removeGame(Game.objects.get(pk=gameID))
    return redirect('game', gameID)

@login_required
def acceptfriend(request, userID):
    request.user.profile.addFriend(User.objects.get(pk=userID).profile)
    request.user.profile.removeNotification(
        request.user.profile.getNotifications().get(link="/friends/"+str(userID)+"/request")
    )
    return redirect('friends')

@login_required
def rejectfriend(request, userID):
    request.user.profile.removeNotification(
        request.user.profile.getNotifications().get(link="/friends/"+str(userID)+"/request")
    )
    return redirect('friends')

@login_required
def removefriend(request, userID):
    request.user.profile.removeFriend(User.objects.get(pk=userID).profile)
    return redirect('friends')

@login_required
def friendrequest(request, userID):
    return render(request, "friendrequest.html", {"friend": User.objects.get(pk=userID)})

@login_required
def removeevent(request, eventID):
    Event.objects.remove_event(eventID)
    return redirect('myevents')

@login_required
def allgames(request):
    return render(request, 'games.html', {"games": Game.objects.getAllGames()})

# TODO
# Other pages: ?
