from django import forms
from .models import *


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control'}),
        }
