from django import forms 
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User


class Create_Account_Form(UserCreationForm):

    class Meta:

        model = User
        fields = ['username','email']


class login_form(AuthenticationForm):
    username = forms.CharField(
        label='username', widget=forms.TextInput(attrs={'placeholder': 'Username','class':'form-control'}))
    
    password = forms.CharField(
        label='password', widget=forms.PasswordInput(attrs={'placeholder': 'Enter Your Password','class':'form-control'}))

    