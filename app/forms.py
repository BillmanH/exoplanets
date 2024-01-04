from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import NumberInput

from .functions.maths import uuid

# https://docs.djangoproject.com/en/3.1/ref/forms/widgets/#built-in-widgets



class HomeSystemForm(forms.Form):
    planet_name = forms.CharField(label="Planet Name", max_length=100)
    num_planets = forms.IntegerField(
        max_value=10,
        min_value=1,
        initial=6,
        label="Number of planets",
        widget=NumberInput,
        help_text="(not planet-like objects)",
    )
    num_moons = forms.IntegerField(
        max_value=50,
        min_value=0,
        initial=24,
        label="Number of moons",
        widget=NumberInput,
        help_text="(randomly distributed to planets)",
    )
    home_has_moons = forms.BooleanField(
        initial=True, help_text="ensure that your planet has at least one moon"
    )
    starting_pop = forms.IntegerField(
        max_value=20,
        min_value=1,
        initial=7,
        label="Homeworld Population",
        widget=NumberInput,
        help_text="(population is in millions of people)",
    )
    conformity = forms.FloatField(
        max_value=1,
        min_value=0,
        initial=0.3,
        label="Population Conformity",
        widget=NumberInput,
        help_text='( % How much your people consider themselves "one people")',
    )
    literacy = forms.FloatField(
        max_value=1,
        min_value=0,
        initial=0.7,
        label="Homeworld Literacy",
        widget=NumberInput,
        help_text="( % affects the tech advancement)",
    )
    aggression = forms.FloatField(
        max_value=1,
        min_value=0,
        initial=0.5,
        label="Population Aggression",
        widget=NumberInput,
        help_text='( % agressive to "others")',
    )
    constitution = forms.FloatField(
        max_value=1,
        min_value=0,
        initial=0.5,
        label="Population Constitution",
        widget=NumberInput,
        help_text="( %  ability to persivere)",
    )
    def formToNode(self,post):
        fields = list(self.fields.keys())
        postDict = dict(post)
        node = {i:postDict[i][0] for i in postDict.keys() if i in fields}
        node['label'] = "form"
        node['name'] = "form"
        node['objid'] = uuid(n=13)
        return node