from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import SoilImage, PlantImage


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']  

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        # Add the necessary classes and placeholders to the form fields
        self.fields['username'].widget.attrs.update({
            'class': 'input-field',
            'placeholder': 'Username'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'input-field',
            'placeholder': 'Email'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'input-field',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'input-field',
            'placeholder': 'Confirm Password'
        })
        self.fields['first_name'].widget.attrs.update({
            'class': 'input-field',
            'placeholder': 'First Name'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'input-field',
            'placeholder': 'Last Name'
        })


class SoilImageUploadForm(forms.ModelForm):
    class Meta:
        model = SoilImage
        fields = ['image']

class PlantImageUploadForm(forms.ModelForm):
    class Meta:
        model = PlantImage
        fields = ['image']







