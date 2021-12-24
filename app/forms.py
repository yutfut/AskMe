from django import forms
from django.forms import ModelForm, TextInput, PasswordInput, DateTimeInput, Textarea, FileInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from app.models import *


class LoginForm(forms.Form):
    username = forms.CharField(required=True,
                               widget=forms.TextInput,
                               label='Login')
    password = forms.CharField(required=True,
                               widget=forms.PasswordInput,
                               label='Password')


class SignupForm(forms.ModelForm):
    password2 = forms.CharField(required=True,
                                widget=PasswordInput(attrs={
                                   'class': 'form-control',
                                }),
                                label='Password check')
    ava = forms.FileField(required=False,
                          label='Avatar')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control',
            }),
            'email': TextInput(attrs={
                'class': 'form-control',
            }),
            'password': PasswordInput(attrs={
                'class': 'form-control',
            }),
        }

        labels = {
            'username': 'Login',
        }

    def clean(self):
        if not 'password' in self.cleaned_data or not 'password2' in self.cleaned_data:
            raise forms.ValidationError('Password is too short (minimum 1 characters)')
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            self.add_error('password', 'Passwords do not match!')
            self.add_error('password2', 'Passwords do not match!')
            raise forms.ValidationError('Passwords do not match!')

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            self.add_error(None, 'This username is already in use')
            raise forms.ValidationError('This username is already in use')
        return self.cleaned_data['username']

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            self.add_error(None, 'This email is already in use')
            raise forms.ValidationError('This email is already in use')
        return self.cleaned_data['email']

    def save(self, **kwargs):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = User.objects.create_user(username, email, password)

        profile = Profile.objects.create(user_id=user)
        if self.cleaned_data['ava'] is not None:
            profile.avatar = self.cleaned_data['ava']
            profile.save()

        return user


class SettingsForm(forms.ModelForm):
    password2 = forms.CharField(required=True,
                                widget=PasswordInput(attrs={
                                    'class': 'form-control',
                                }),
                                label='Password check')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control',
            }),
            'email': TextInput(attrs={
                'class': 'form-control',
            }),
            'password': PasswordInput(attrs={
                'class': 'form-control',
            }),
        }

        labels = {
            'username': 'Login',
        }

    def __init__(self, user=None, **kwargs):
        self.user = user
        super(SettingsForm, self).__init__(**kwargs)

    def clean(self):
        if not 'password' in self.cleaned_data or not 'password2' in self.cleaned_data:
            raise forms.ValidationError('Password is too short (minimum 1 characters)')
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            self.add_error('password', 'Passwords do not match!')
            self.add_error('password2', 'Passwords do not match!')
            raise forms.ValidationError('Passwords do not match!')

    def clean_username(self):
        if self.user_id.username != self.cleaned_data['username']:
            if User.objects.filter(username=self.cleaned_data['username']).exists():
                self.add_error(None, 'This username is already in use')
                raise forms.ValidationError('This username is already in use')
        return self.cleaned_data['username']

    def clean_email(self):
        if self.user.email != self.cleaned_data['email']:
            if User.objects.filter(email=self.cleaned_data['email']).exists():
                self.add_error(None, 'This email is already in use')
                raise forms.ValidationError('This email is already in use')
        return self.cleaned_data['email']

    def save(self, **kwargs):
        self.user.username = self.cleaned_data['username']
        self.user.email = self.cleaned_data['email']

        self.user.set_password(self.cleaned_data['password'])

        self.user.save()

        return self.user


class ImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']

        labels = {
            'avatar': 'Upload avatar',
        }


class AskForm(forms.ModelForm):
    tags = forms.CharField(required=False,
                           widget=forms.TextInput(attrs={
                               'class': 'form-control',
                           }),
                           label='Tags')

    class Meta:
        model = Question
        fields = ['title', 'text']

        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
            }),
            'text': Textarea(attrs={
                'class': 'form-control',
                'rows': '7',
            }),
        }

        labels = {
            'title': 'Title',
            'text': 'Text',
        }

    def __init__(self, author=None, **kwargs):
        self._author = author
        super(AskForm, self).__init__(**kwargs)

    def clean_tags(self):
        self.tags = self.cleaned_data['tags'].split()
        if len(self.tags) > 3:
            self.add_error(None, 'use no more than 3 tags!')
            raise forms.ValidationError('use no more than 3 tags!')
        return self.tags

    def save(self, **kwargs):
        post = Question()
        post.profile_id = self._author
        post.title = self.cleaned_data['title']
        post.text = self.cleaned_data['text']
        post.save()

        for tag in self.tags:
            if not Tag.objects.filter(tag=tag).exists():
                Tag.objects.create(tag=tag)
        post.tags.set(Tag.objects.create_question(self.tags))

        return post