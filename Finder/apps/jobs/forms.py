# apps/jobs/forms.py
from django import forms
from .models import Job

class JobCreateForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'keywords']  # Los campos necesarios para crear un trabajo
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
