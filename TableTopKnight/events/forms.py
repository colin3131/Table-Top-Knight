from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from database.models import Vote, Event
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class VoteForm(forms.Form):
    def __init__(self, eventID, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        self.fields['game1'].queryset = Event.objects.get(pk=eventID).getFilteredGames()
        self.fields['game2'].queryset = Event.objects.get(pk=eventID).getFilteredGames()
        self.fields['game3'].queryset = Event.objects.get(pk=eventID).getFilteredGames()

    game1 = forms.ModelChoiceField(
        queryset=None, 
        required=True,
        label="Rank 1 Game",
        to_field_name="gameName"
        )

    game2 = forms.ModelChoiceField(
        queryset=None, 
        required=True,
        label="Rank 2 Game",
        to_field_name="gameName"
        )

    game3 = forms.ModelChoiceField(
        queryset=None, 
        required=True,
        label="Rank 3 Game",
        to_field_name="gameName"
        )

class EventForm(ModelForm):
    def __init__(self, userID, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['pendingPlayers'].queryset = User.objects.get(pk=userID).profile.getFriends()
    class Meta:
        model = Event
        fields = ('eventDateTime', 'location', 'pendingPlayers')
        exclude = ['host', 'attendees', 'eventGames', 'event_state']
        labels = {
            'eventDateTime': _("Event's Date & Time"),
            'location': _("Event's Location"),
            'pendingPlayers': _("Add Friends")
        }
        help_texts = {
            'eventDateTime': _("MM/DD/YYYY HH:MI")
        }

class FriendForm(forms.Form):
    friendName = forms.CharField()
    
    def clean_friendName(self):
        username = self.cleaned_data['friendName']
        if not User.objects.filter(username=username).exists():
            raise ValidationError(
                _("User %(username)s does not exist."),
                params={"username": username},
            )
        thisuser = User.objects.get(pk=self.userid)
        thatuser = User.objects.get(username=username)
        if(thatuser.profile in thisuser.profile.getFriends()):
            raise ValidationError(
                _("User %(username)s is already your friend."),
                params={"username": username},
            )
        if(thatuser.id == thisuser.id):
            raise ValidationError(
                _("You can't add yourself."),
                params={"username": username},
            )
        return username

    def __init__(self, *args, **kwargs):
        self.userid = kwargs.pop('userid', None)
        super(FriendForm, self).__init__(*args, **kwargs)

class PendingPlayerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.userid = kwargs.pop('userid', None)
        self.eventid = kwargs.pop('eventid', None)
        super(PendingPlayerForm, self).__init__(*args, **kwargs)

    playerName = forms.CharField()

    def clean_playerName(self):
        username = self.cleaned_data['playerName']
        if not User.objects.filter(username=username).exists():
            raise ValidationError(
                _("User %(username)s does not exist."),
                params={"username": username},
            )
        thisuser = User.objects.get(pk=self.userid)
        thatuser = User.objects.get(username=username)
        event = Event.objects.get(pk=self.eventid)
        if(not thatuser.profile in thisuser.profile.getFriends()):
            raise ValidationError(
                _("User %(username)s is not your friend."),
                params={"username": username},
            )
        if(thatuser.profile in event.getPendingPlayers()):
            raise ValidationError(
                _("User %(username)s is already pending."),
                params={"username": username},
            )
        if(thatuser.profile in event.getAttendingPlayers()):
            raise ValidationError(
                _("User %(username)s is already attending."),
                params={"username": username},
            )
        return username
        
    

