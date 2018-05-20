"""Forms"""

from django import forms
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django_addanother.widgets import AddAnotherWidgetWrapper
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import SiteUser, Role, SiteUserGroup, GroupMembership, GroupJoinRequest, Follow

CustomUser = get_user_model()

class UserCreationForm(forms.ModelForm):
    """Custom UCF. Takes the standard
    variables of 'email', 'password1', 'password2'
    For creating instances of 'CustomUser'."""
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))

    class Meta:
        model = CustomUser
        fields = ('email', )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField

    class Meta:
        model = CustomUser
        fields = ["email", "password", "is_active", "is_admin"]

    def clean_password(self):
        return self.initial["password"]

class SiteUserMixin(forms.ModelForm):
    class Meta:
        model = SiteUser
        fields = ("screen_name", )
        widgets = {
            "screen_name" : forms.TextInput(attrs={'class':'form-control', "placeholder" : "Display name"}),
        }

# class SiteUserRegistrationForm(SiteUserMixin):
class SiteUserRegistrationForm(forms.Form):

    agreement = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput())

    screen_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control', "placeholder" : "Screen name"}))

    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control', "placeholder" : "Email address"}))

    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', "placeholder" : "Enter password"}))

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', "placeholder" : "Verify password"}))

    def clean(self):
        data = self.cleaned_data
        email = data.get("email", None).strip()
        password1 = data.get('password1', None).strip()
        password2 = data.get('password2', None).strip()
        screen_name = data.get("screen_name", None).strip()

        User = get_user_model()
        if User.objects.filter(email=email).exists():
            self.add_error('email', 'Email already registered.')

        if password1 and password2 and password1 != password2:
            self.add_error('password1', "Passwords do not match")

        if SiteUser.objects.filter(screen_name=screen_name).exists():
            self.add_error('screen_name', 'Display name already taken.')


    # def clean_email(self):
    #     User = get_user_model()
    #     email = self.cleaned_data["email"]
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError("Email already exists")
    #     return email

    # def clean_password2(self):
    #     password1 = self.cleaned_data.get('password1')
    #     password2 = self.cleaned_data.get('password2')
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError("Passwords do not match")
    #     return password2

    # def clean_screen_name(self):
    #     screen_name = self.cleaned_data["screen_name"]
    #     if SiteUser.objects.filter(screen_name=screen_name).exists():
    #         raise forms.ValidationError("Display name already taken.")
    #     return screen_name

class SiteUserEditForm(forms.ModelForm):
    class Meta:
        model = SiteUser
        fields = ["first_name", "last_name", "location", "avatar", "roles"]

        widgets = {
            "first_name" : forms.TextInput(attrs={'class' : 'form-control', "placeholder" : "First name"}),
            "last_name" : forms.TextInput(attrs={'class' : 'form-control', "placeholder" : "Last name"}),
            "location" : forms.TextInput(attrs={'class' : 'form-control', "placeholder" : "Location"}),
            "roles" : AddAnotherWidgetWrapper(
                forms.SelectMultiple(attrs={'class' : 'form-control'}),
                reverse_lazy('siteuser:role_create')),}

class NewRoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ("role", )

        widgets = {
            "role" : forms.TextInput(
                attrs={'class' : 'form-control', "placeholder" : "Role"})
        }

    def clean_role(self):
        role = self.cleaned_data.get("role", None).upper()
        if Role.objects.filter(role=role):
            raise forms.ValidationError(_("{} already exists".format(role)))
        return role

class RoleEditForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ("role", )

        widgets = {
            "role" : forms.TextInput(
                attrs={'class' : 'form-control', "placeholder" : "Role"})
        }

class NewSiteUserGroupForm(forms.ModelForm):
    class Meta:
        model = SiteUserGroup
        fields = ('name','group_social',  'about_group', )

        widgets = {
            "name" : forms.TextInput(
                attrs={'class' : 'form-control', "placeholder" : "Group name"}),
            "about_group" : forms.Textarea(
                attrs={'class' : 'form-control', "placeholder" : "About group"}),
            "group_social" : forms.TextInput(
                attrs={'class' : 'form-control', "placeholder" : "Group social media address (optional)"}),
        }
