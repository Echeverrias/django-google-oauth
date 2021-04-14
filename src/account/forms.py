
from django import forms
from django.forms import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.core.validators import validate_email
from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.files.images import get_image_dimensions

from profiles.models import User, Profile

INIT_YEAR = 1940


def clean_ImageField(form):
    avatar = form.cleaned_data['avatar']
    if not avatar:
        return avatar

    try:
        w, h = get_image_dimensions(avatar)

        # validate dimensions
        max_width = max_height = 500
        if w > max_width or h > max_height:
            raise forms.ValidationError(
                u'Please use an image that is '
                '%s x %s pixels or smaller.' % (max_width, max_height))

        # validate content type
        main, sub = avatar.content_type.split('/')
        if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
            raise ValidationError(u'Please use a JPEG, '
                                        'GIF or PNG image.')

        # validate file size
        if len(avatar) > (20 * 1024):
            raise ValidationError(
                u'Avatar file size may not exceed 20k.')

    except AttributeError:
        """
        Handles case when we are updating the user profile
        and do not supply a new avatar
        """
        pass

    return avatar



class UserRegisterForm(UserCreationForm):
    birth_date = forms.DateField(label=_('Birth date:'),
                                widget=forms.SelectDateWidget(years=range(INIT_YEAR, timezone.now().year - 18)))

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

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date.year == INIT_YEAR and birth_date.month == 1 and birth_date.day == 1:
           # raise ValidationError('Select your birth date') #%
            return birth_date
        else:
            return birth_date

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

    def clean_avatar(self):
        try:
            avatar = clean_ImageField(self)
            return avatar
        except ValidationError as e:
            raise e


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
            super(UserRegisterForm, self)._post_clean()
            self._translate_errors(['__all__'])
        except Exception as e:
            raise e

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'].required = False
        self.fields['birth_date'].initial = None


class UserUpdateForm(UserChangeForm):
    password = None

    birth_date = forms.DateField(label=_('Birth date:'),
                                 widget=forms.SelectDateWidget(years=range(1940, timezone.now().year - 18)))

    password1 = forms.CharField(label=_('New password:'),
                                min_length=3,
                                help_text='', widget=forms.PasswordInput())

    password2 = forms.CharField(label=_('Confirm password:'),
                                help_text='', widget=forms.PasswordInput())


    class Meta:
        model = User
        fields = ('password1', 'password2', 'first_name', 'last_name', 'bio', 'location', 'birth_date', 'avatar')

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        kwargs.update(initial={
             **initial,
        })
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        try:
            user = get_object_or_404(User, pk=self.initial.get('pk', None))
            self.initial.update({'password1': user.password, 'password2': user.password})
        except Exception as e:
            print(f'Error: {e}')

    def clean_avatar(self):
        try:
            avatar = clean_ImageField(self)
            return avatar
        except ValidationError as e:
            raise e

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if (password1 or password2) and not(password1 == password2):
            raise ValidationError('Password mismatch')
        return cleaned_data

    def save(self):
        password1 = self.cleaned_data["password1"]
        commit = False if password1 else True
        user = super(UserUpdateForm, self).save(commit=commit)
        if not commit:
            user.set_password(self.cleaned_data["password1"])
            user.save()
        return user


class UserLoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ('username', 'password')