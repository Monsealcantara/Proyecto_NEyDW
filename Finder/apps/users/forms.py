from django import forms
from .models import Worker,Client

class ProfileFormWorker(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['profession', 'bio']
class ProfileFormClient(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['location']
