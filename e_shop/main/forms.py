from django import forms
from main.models import *
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))



class RegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))


class OrderForm(forms.ModelForm):
    payment_type = forms.CharField(widget=forms.RadioSelect(choices=Order.PAYMENT))
    desc = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':'3'}))

    class Meta:
        model = Order
        exclude = ['cart','order_status']