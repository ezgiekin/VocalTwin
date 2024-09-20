# base/forms.py
from django import forms
from .models import VoiceRecording,CustomUser,CustomUserManager
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import PasswordInput,TextInput
from django.contrib.auth import password_validation

class VoiceRecordingForm(forms.ModelForm):
    name = forms.TextInput()
    gender = forms.TextInput()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password-input'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_type')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.user_type = self.cleaned_data['user_type']
        
        if user.user_type == 'admin':
            user.is_staff = True
            user.is_superuser = True
        
        if commit:
            user.save()
        return user
    

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

class VoiceRecordingEdit(forms.ModelForm):
    class Meta:
        model = VoiceRecording
        fields = ['name', 'gender'] 

class CloneText(forms.Form):
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
        ('de', 'German'),
        ('it', 'Italian'),
        ('pt', 'Portuguese'),
        ('pl', 'Polish'),
        ('tr', 'Turkish'),
        ('ru', 'Russian'),
        ('nl', 'Dutch'),
        ('cs', 'Czech'),
        ('ar', 'Arabic'),
        ('zh-cn', 'Chinese'),
        ('ja', 'Japanese'),
        ('hu', 'Hungarian'),
        ('ko', 'Korean'),
        ('hi', 'Hindi'),
    ]
    
    text = forms.CharField(widget=forms.Textarea,required=False)
    text_language = forms.ChoiceField(choices=LANGUAGE_CHOICES,required=False)