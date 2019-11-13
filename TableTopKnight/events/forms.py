from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from database.models import Vote

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class VoteForm(forms.Form):
    def __init__(self, game_choices, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        self.fields['game1'].choices = game_choices
        self.fields['game2'].choices = game_choices
        self.fields['game3'].choices = game_choices

    game1 = forms.ChoiceField(choices=(), required=True)
    rank1 = forms.TypedChoiceField(
            choices=[(x, x) for x in range (1, 3)],
            coerce=int,
            help_text='Rank: '
        )

    game2 = forms.ChoiceField(choices=(), required=True)
    rank2 = forms.TypedChoiceField(
            choices=[(x, x) for x in range (1, 3)],
            coerce=int,
            help_text='Rank: '
        )

    game3 = forms.ChoiceField(choices=(), required=True)
    rank3 = forms.TypedChoiceField(
            choices=[(x, x) for x in range (1, 3)],
            coerce=int,
            help_text='Rank: '
        )
