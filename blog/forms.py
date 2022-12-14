# INF601 - Advanced Programming in Python
# Lindsey Jimenez
# Mini Project 4

from .models import Comment, Contact, User, Forum, Discussion, Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm


# Sets comment form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


# Sets contact form
class ContactForm(forms.Form):
    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'email', 'subject', 'message')


# Sets registration form, saves to db
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"


class CreateInForum(forms.ModelForm):
    class Meta:
        model = Forum
        fields = "__all__"


class CreateInDiscussion(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = "__all__"
