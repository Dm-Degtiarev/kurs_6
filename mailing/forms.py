from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, AuthenticationForm, SetPasswordForm
from django import forms
from transliterate.utils import _
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

class UserPasswordResetForm(FormStyleMixin, PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=255,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = User

class UserResetConfirmForm(SetPasswordForm):
    class Meta:
        model = User