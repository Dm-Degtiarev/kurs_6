from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, AuthenticationForm
from django import forms
from mailing.models import User


class FormStyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserRegistartionForm(FormStyleMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'avatar', 'phone_number', 'country')


class UserAuthenticationForm(FormStyleMixin, AuthenticationForm):
    class Meta:
        model = User
        fields = '__all__'