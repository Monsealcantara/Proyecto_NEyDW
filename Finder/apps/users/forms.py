from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import User, Worker, Client

class UserProfileForm (UserChangeForm):
    # Campos comunes para todos los usuarios
    # email = forms.EmailField(required=True, label='Correo electrónico')
    # username = forms.CharField(max_length=150, required=True, label='Nombre de usuario')

    class Meta:
        model = User
        fields = ['username', 'email']
        #fields = ['username', 'email', 'password']
class ProfileFormWorker(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['profession', 'bio']
class ProfileFormClient(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['location']
