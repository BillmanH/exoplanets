from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import NumberInput, CheckboxInput

# https://docs.djangoproject.com/en/3.1/ref/forms/widgets/#built-in-widgets

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )



class HomeSystemForm(forms.Form):
    planet_name = forms.CharField(label='Planet Name', max_length=100)
    num_planets = forms.IntegerField(max_value=10,min_value=1,initial=6,label='Number of planets',widget=NumberInput,help_text='(not planet-like objects)')
    num_moons = forms.IntegerField(max_value=10,min_value=1,initial=24,label='Number of moons',widget=NumberInput,help_text='(randomly distributed to planets)')
    home_has_moons = forms.BooleanField(initial=True,help_text='ensure that your planet has at least one moon')
    sep = forms.CharField(label='sep')


