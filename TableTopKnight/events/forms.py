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
    friendName = forms.CharField(validators=[validate_user])
    
def validate_user(username):
    if not User.objects.filter(username=username).exists():
        raise ValidationError(
            _("User %(username)s does not exist."),
           params={"username": username},
        )
