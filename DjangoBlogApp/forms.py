from .models import Post, Profile

from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(ModelForm):
    class Meta():
        model = Post
        fields = '__all__'


class AccountForm(ModelForm):
    class Meta():
        model = Profile
        fields = '__all__'
        exclude = ['user']


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control form-control-lg', 'placeholder': 'Enter username...'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control form-control-lg', 'placeholder': 'Enter email...'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control form-control-lg', 'placeholder': 'Enter password...'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control form-control-lg', 'placeholder': 'Confirm password...'})