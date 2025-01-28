from django import forms
from django.forms import ModelForm,Form
from .models import Dead,TaskPerson
#from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class TaskPerson_in(ModelForm):
    class Meta :
        model = TaskPerson
        fields = ['first_name','last_name','national_num','dad_name','national_dad','mom_name','national_mom',
            'birth_place','birth_date','place_of_issue','number_of_issue','date_of_issue','religion','gender','status','image','date_of_event','place_of_event']
        widgets = {
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_of_issue': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_of_event': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'place_of_event': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(TaskPerson_in, self).__init__(*args, **kwargs)
        self.fields['date_of_event'].required = False
        self.fields['place_of_event'].required = False
    '''
    def clean_national_id(self, field_name):
        data = self.cleaned_data[field_name]
        if not data.startswith('0') or len(data) != 11:
            raise ValidationError('Invalid national ID format')
        return str(data)

    def clean_national_num(self):
        return self.clean_national_id('national_num')

    def clean_national_dad(self):
        return self.clean_national_id('national_dad')
    
    def clean_national_mom(self):
        return self.clean_national_id('national_mom')
    '''
    def clean_national_id(self, field_name, field_label):
        data = self.cleaned_data[field_name]
        if not data.startswith('0') or len(data) != 11:
            raise ValidationError(
                f'wrong {field_label}  ',
                code='invalid',
                params={'value': data},
            )
        return str(data)

    def clean_national_num(self):
        return self.clean_national_id('national_num', ' national id')

    def clean_national_dad(self):
        return self.clean_national_id('national_dad', ' national dad id')

    def clean_national_mom(self):
        return self.clean_national_id('national_mom', ' national mom id')


'''error_messages = {
        'national_num': {
            'invalid': 'رقم الهوية الوطنية غير صحيح',
        },
        'national_dad': {
            'invalid': 'رقم هوية الأب غير صحيح',
        },
        'national_mom': {
            'invalid': 'رقم هوية الأم غير صحيح',
        },
    }

    def clean_national_id(self, field_name):
        data = self.cleaned_data[field_name]
        if not data.startswith('0') or len(data) != 11:
            raise ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': data},
            )
        return str(data)'''

'''def clean_national_id(self, field_name, field_label):
        data = self.cleaned_data[field_name]
        if not data.startswith('0') or len(data) != 11:
            raise ValidationError(
                f'{field_label} غير صحيح',
                code='invalid',
                params={'value': data},
            )
        return str(data)

    def clean_national_num(self):
        return self.clean_national_id('national_num', 'الرقم الوطني')

    def clean_national_dad(self):
        return self.clean_national_id('national_dad', 'رقم هوية الأب')

    def clean_national_mom(self):
        return self.clean_national_id('national_mom', 'رقم هوية الأم')
'''
class Dead_in(ModelForm):
    class Meta :
        model = Dead
        fields = '__all__'

    def clean_national_num(self):
        data = self.cleaned_data['national_num']
        if not data.startswith('0') or len(data)!=11 :
            raise ValidationError('error')
        return str(data)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs) 
        self.fields['date_of_event'].widget = forms.DateTimeInput(
            attrs={
                'class': 'form-control' , 
                'type':'date' 
                })


class Parent_in(Form):
    gender_parent=[ 
        ('male','Male'),
        ('female','Female')
    ]
    national_parent_num = forms.CharField(max_length=15)
    first_parent_name = forms.CharField(max_length=15)
    last_parent_name = forms.CharField(max_length=15)
    gender_parent = forms.ChoiceField(choices=gender_parent)
    image = forms.ImageField(
        required=False,
        label='family register',
        widget=forms.ClearableFileInput(attrs={'class':'form-control'})
    )

    def clean_national_num(self):
        data = self.cleaned_data['national_parent_num']
        if not data.startswith('0') or len(data)!=11 :
            raise ValidationError('error')
        return str(data)


class Partner_in(Form):
    status_partner=[ 
        ('marrid','marrid'),
        ('divorce','divorce'),
        ('widower','widower')
    ]
    partner_national_num =  forms.CharField (max_length =15)
    marrid = forms.ChoiceField(choices=status_partner)
    place_of_event =  forms.CharField (max_length =15)
    date_of_event = forms.DateField(
        widget=forms.DateInput(
            attrs={
            'class':'form-control',
            'type':'date'
        })
        )
    image = forms.ImageField(
        required=False,
        label='family register',
        widget=forms.ClearableFileInput(attrs={'class':'form-control'})
    )

    def clean_national_num(self):
        data = self.cleaned_data['partner_national_num']
        if not data.startswith('0') or len(data)!=11 :
            raise ValidationError('error')
        return str(data)
