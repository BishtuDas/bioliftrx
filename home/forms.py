from django import forms
from .models import Contact



class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'number', 'message']  # Include the fields you want in the form
