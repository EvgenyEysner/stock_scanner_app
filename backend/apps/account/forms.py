from django.contrib.auth import forms

from apps.account.models import User


class UserCreateForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = ("email", "password")


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User
        field_classes = {}
