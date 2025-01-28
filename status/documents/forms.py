from django import forms
from .models import Document
from django.core.exceptions import ValidationError


class Send_notes(forms.ModelForm):
    class Meta :
        model = Document
        fields = ['notes']



class Death_register(forms.Form):
    national_dead = forms.CharField(max_length=15)

    def clean_national_num(self):
        data = self.cleaned_data['national_partner']
        if not data.startswith('0') or len(data)!=11 :
            raise ValidationError('error')
        return str(data)



