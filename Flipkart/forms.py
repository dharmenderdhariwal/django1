 
# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer
class SignupForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['email', 'phone', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email



 
 
  
