from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm,Form
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['password'].widget = forms.PasswordInput()


class Sign_up(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['password'].widget = forms.PasswordInput()

class Log_in(Form):
    username = forms.CharField(max_length =15)
    password =  forms.CharField (max_length =15)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['password'].widget = forms.PasswordInput()

class Reset_pass(Form):
    new_password = forms.CharField(max_length =15)
    confirm_password = forms.CharField(max_length =15)
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['new_password'].widget = forms.PasswordInput()
        self.fields['confirm_password'].widget = forms.PasswordInput()
        
class Check_id(Form):
    national_num = forms.CharField(max_length =15)

    def clean_national_num(self):
        data = self.cleaned_data['national_num']
        if not data.startswith('0') or len(data)!=11 :
            raise ValidationError('error')
        return str(data)
    
class Login_employee(Form):
    password = forms.CharField(max_length =15)
    confirm_password = forms.CharField(max_length =15)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['confirm_password'].widget = forms.PasswordInput()
