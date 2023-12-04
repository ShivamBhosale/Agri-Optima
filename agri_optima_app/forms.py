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


class CropYieldForm(forms.Form):

    CROP_CHOICES = [
        (0, 'Maize'),
        (1, 'Potato'),
        (2, 'Soybean'),
        (3, 'Wheat'),
    ]

    item = forms.ChoiceField(
        choices=CROP_CHOICES,
        label="Crop Name",
        
        widget=forms.Select(attrs={'placeholder': 'Select crop'}),
        required=True,
    )

    
    
    
    average_temp = forms.FloatField(
        label="Average Temp",
        widget=forms.TextInput(attrs={'placeholder': 'Enter the average temperature'}),
        required=False,
    )

    pesticide_amount = forms.FloatField(
        label="Pesticide Amount",
        widget=forms.TextInput(attrs={'placeholder': 'Enter the pesticide amount'}),
        required=False,
    )

    average_rain = forms.FloatField(
        label="Average Rain",
        widget=forms.TextInput(attrs={'placeholder': 'Enter the average rainfall'}),
        required=False,
    )
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = None






