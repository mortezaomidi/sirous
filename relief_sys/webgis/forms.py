from django import forms
from django.forms import ModelForm
from .models import Need
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='This field is optional' )
    last_name = forms.CharField(max_length=30, required=False, help_text='This field is optional' )
    national_cod = forms.CharField(max_length=10, required=True, help_text='Required field')
    age = forms.IntegerField(max_value=120, min_value=10, help_text='This field is optional')
    sex_cioices = (
    (0, 'Woman'),
    (1,'Men'),
    )

    sex = forms.ChoiceField(widget=forms.Select,
                                             choices=sex_cioices)
    email = forms.EmailField(required=True, help_text='Required. Inform a valid email address.')
    affiliation_choices = (
        (1, 'Partnership'),
        (2, 'Red Crescent'),
        (3, 'Emergency Medicine'),
        (4, 'Municipality'),
        (5, 'Healthcare'),
        (6, 'Police'),
        (7, 'Military'),
    )

    affiliation = forms.ChoiceField(widget=forms.Select,
                                             choices=affiliation_choices)


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'national_cod', 'sex', 'age', 'email', 'affiliation', 'password1', 'password2')


class NeedForm(ModelForm):
    """docstring for NeedForm ."""
    class Meta:
        model = Need
        fields = '__all__'
        #exclude = ['location']
