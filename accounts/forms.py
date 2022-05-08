from django import forms
from django.db import transaction
from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from accounts.helpers import getUsernameFromEmail
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'mobile_number', 'address')
    

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        # user.username = getUsernameFromEmail(self.cleaned_data['email'])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'mobile_number', 'address']


class PublicCustomUserChangeForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'mobile_number', 'address']
