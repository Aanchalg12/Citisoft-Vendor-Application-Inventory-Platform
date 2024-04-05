# from myCitisoft.models import CustomUser
from .models import CustomUser
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from .profile import Profile
from django.contrib.auth import authenticate

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignupForm(UserCreationForm):
    address = forms.CharField(label='Address', widget=forms.TextInput(attrs={'placeholder': 'Enter your address'}))
    phone_number = forms.CharField(label='Phone Number', widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'address']

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isnumeric() or len(phone_number) != 10:
            raise forms.ValidationError("Please enter a valid 10-digit phone number")
        return phone_number

    def clean_address(self):
        address = self.cleaned_data.get('address')
        if len(address) < 5:
             raise forms.ValidationError("Address must be at least 5 characters long")
        elif not any(char.isalpha() for char in address):
            raise forms.ValidationError("Address must contain at least one alphabetic character")
        elif not any(char.isdigit() for char in address):
            raise forms.ValidationError("Address must contain at least one numeric character")
        return address


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        # Check if username and password are provided
        if not username:
            self.add_error('username', 'Username is required')
        if not password:
            self.add_error('password', 'Password is required')

        # If both fields are provided, attempt to authenticate user
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Invalid username or password')
        return cleaned_data


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'address', 'profile_photo']

        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = True

class AddUserForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'address', 'role', 'profile_photo',]


























    # class SignupForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email', 'password1', 'password2']
#         username = forms.CharField(max_length=150) 
#         email = forms.EmailField()
#         password1 = forms.CharField(widget=forms.PasswordInput)
#         password2 = forms.CharField(widget=forms.PasswordInput)

        # def clean_username(self):
        #     username = self.cleaned_data['username']
        #     if CustomUser.objects.filter(username=username).exists():
        #         raise ValidationError(_('Username already exists. Please choose a different one.'))
        #     return username

        # def clean_email(self):
        #     email = self.cleaned_data['email']
        #     if CustomUser.objects.filter(email=email).exists():
        #         raise ValidationError(_('Email already exists. Please use a different one.'))
        #     return email

        # def clean_password1(self):
        #     password1 = self.cleaned_data.get('password1')
        #     validate_password(password1)
        #     return password1

        # def clean(self):
        #     cleaned_data = super().clean()
        #     password1 = cleaned_data.get('password1')
        #     password2 = cleaned_data.get('password2')
        #     if password1 and password2 and password1 != password2:
        #         raise ValidationError(_("The two password fields didn't match."))

        # def save(self, commit=True):
        #     user = super().save(commit=False)
        #     user.email = self.cleaned_data['email']
        #     if commit:
        #         user.save()
        #     return user 