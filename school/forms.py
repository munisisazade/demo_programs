from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.contrib.auth import authenticate
from school.models import Studend,Payment,PandaBranch
from school.options.tools import VALID_IMAGE_FILETYPES
from PIL import Image


User = get_user_model()


class MyUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(MyUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class MyUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=_("Password"),
                                         help_text=_("Raw passwords are not stored, so there is no way to see "
                                                     "this user's password, but you can change the password "
                                                     "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MyUserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]



"""
    ################################################################################################
    User login school system -----------------------------------------------------------------------
    ################################################################################################
"""


class BaseAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=254, label="İstifadəçi adı")
    password = forms.CharField(label="Parol", widget=forms.PasswordInput())


    def __init__(self, *args, **kwargs):
        super(BaseAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={
             'class': 'form-control form-project', 'id': 'user_email','autofocus':None})
        self.fields['password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control form-project', 'id': 'user_password'})

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Təəsüflər olsunki email və ya şifrə yanlışdır")
        return user

"""
    This is Teachers add form views
"""
class TeachersForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','birthday','unvani','phone','study','position','subjects','username','email','password')


class ManagersForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','birthday','unvani','phone','study','position','subjects','username','email','password')


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('profile_picture',)
        widget = forms.TextInput(attrs={'readonly': 'readonly'})


class StudentAddForm(forms.ModelForm):
    class Meta:
        model = Studend
        fields = ('full_name','unvani','phone','plan','gender','money','qalan_ders','groups')

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('prize',)

class BranchAddForm(forms.ModelForm):
    class Meta:
        model = PandaBranch
        fields = ('name',)

class ChangePictureForm(forms.Form):

    profile_image = forms.FileField()
    # Add some custom validation to image field
    def clean_photo(self):
        photo = self.cleaned_data.get(['profile_image'])
        if photo:
            format = Image.open(photo.file).format
            photo.file.seek(0)
            if format in VALID_IMAGE_FILETYPES:
                return photo
        raise forms.ValidationError('Yalnız jpg, png və tiff formatında şəkillər qəbul olunur')