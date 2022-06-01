from django import forms
from .models import *
from phonenumber_field.formfields import PhoneNumberField


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ContactForm(forms.Form):
    name = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = PhoneNumberField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', "rows": 5}))


class EmailForDistributionForm(forms.ModelForm):
    class Meta:
        model = EmailForDistribution
        fields = ['email']
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter Email Address"}),
        }

