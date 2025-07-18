from django.contrib.auth.forms import UserCreationForm , AuthenticationForm 
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import redirect, render
from django.contrib import auth, messages




class RegistrationForm(UserCreationForm):

    username = forms.CharField(
        max_length=50, 
        required=True, 
        label='Username', 
        help_text='50 characters or fewer. Letters, digits and @/./+/-/_ only.',
        widget=forms.TextInput(attrs={
            'placeholder': 'username',
            'class': 'form-control'
        })

    )

    
    email = forms.EmailField(
        required=True,
        label='Email Address',
        help_text='Enter a valid email address.',
        widget=forms.EmailInput(attrs={
            'placeholder': 'example@example.com',
            'class': 'form-control'  
        })
    )

    password1 = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password',
            'class': 'form-control'
        })
    )

    password2 = forms.CharField(
    label='Confirm Password',
    required=True,
    widget=forms.PasswordInput(attrs={
        'placeholder': 'Re-enter password',
        'class': 'form-control'
    })
)



    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=50,
        required=True,
        label='Username',
        help_text='Enter your username.',
        widget=forms.TextInput(attrs={
            'placeholder': 'username',
            'class': 'form-control',
           
        })
    )
    
    password = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password',
            'class': 'form-control',
            
        })
    )

    class Meta:
            model = User
            fields = ('username', 'password')