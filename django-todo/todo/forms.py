from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import Item

class CustomSignupForm(UserCreationForm):
    username = forms.CharField(label=_('Имя пользователя'), widget=forms.widgets.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label=_('Пароль'), strip=False, widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label=_('Подтвержение пароля'), strip=False, widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'}))

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(label=_('Имя пользователя'), widget=forms.widgets.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label=_('Пароль'), strip=False, widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'}))

class ItemForm(forms.ModelForm):
    text = forms.CharField(widget=forms.widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите предмет'}))
    class Meta:
        model = Item
        fields = 'text',