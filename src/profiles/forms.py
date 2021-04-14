from .models import User, Profile
from django import forms
from django.forms import ValidationError
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import validate_email
from django.utils.translation import gettext as _


class UserForm(UserCreationForm):
    birth_date = forms.DateField(label=_('Birth date:'),
                                widget=forms.SelectDateWidget(years=range(1940, timezone.now().year - 18)))

    username = forms.CharField(label=_('User Name:'), max_length=15, min_length=2,
                               help_text=_('Enter an username between 15 and 3 characters.'),
                              widget=forms.TextInput())

    password1 = forms.CharField(label=_('Password:'),
                                min_length=3,
                                help_text='', widget=forms.PasswordInput())

    password2 = forms.CharField(label=_('Confirm password:'),
                               help_text='', widget=forms.PasswordInput())

    email = forms.EmailField(label='Email:', max_length=254,
                             widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'bio', 'location', 'birth_date', 'avatar')
        labels = {'bio': _('Biography'), }
        help_texts = {'bio': _('Write about yourself.'), }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except exceptions.ValidationError as e:
            raise ValidationError('The email is not valid')
        if User.objects.filter(email__exact=email):
            raise ValidationError('This email has been taken')
        else:
            return email


    def _translate_errors(self, fields):
        d = {
            "__all__": {
                'old': 'new'
            },
            "password": {
                'old': 'new'
            }
        }
        for error_field in fields:
            try:
                errors = self.errors[error_field]
                error_translate = d[error_field]
                errors_ = [error_translate.get(error, error) for error in errors]
                self.errors[error_field] = errors_
            except Exception as e:
                print(e)

    def _post_clean(self):
        try:
            super(UserForm, self)._post_clean()
            self._translate_errors(['__all__'])
        except Exception as e:
            raise e

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'location', 'birth_date','avatar')