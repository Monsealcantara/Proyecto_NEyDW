from django import forms
from django.contrib.auth.models import User
from .models import Worker, Client, Service, Keyword

# Formulario para editar el perfil de usuario (sin permitir cambiar el 'role')
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']  # Los campos editables del usuario
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}),
        }

# Formulario para editar el perfil de un trabajador
class ProfileFormWorker(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['profession','bio', 'gallery']

# Formulario para editar el perfil de un cliente
class ProfileFormClient(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['location']

class ServiceForm(forms.ModelForm):
    keywords = forms.ModelMultipleChoiceField(
        queryset=Keyword.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Palabras clave'
    )
    
    new_keywords = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Palabra clave nueva'}),
        label='Nueva palabra clave (opcional)'
    )
    
    class Meta:
        model = Service
        fields = ['name', 'description', 'keywords']