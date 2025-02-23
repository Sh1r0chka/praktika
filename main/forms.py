from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import CustomUser, Ticket, Categories
from datetime import date, datetime
from django.forms import ModelForm, TextInput, Textarea


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text='Обязательное поле.')
    username = forms.CharField(max_length=24, help_text='Обязательное поле.')

    class Meta:
        model = CustomUser
        fields = ('username', 'phone', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class NewTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'category', 'photo']




class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['creator', 'title', 'description', 'category', 'photo', 'status', 'created_at']
