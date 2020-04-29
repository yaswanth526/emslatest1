from django import forms
from app.models import User,main
import re

class PlaceholderMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_names = [field_name for field_name, _ in self.fields.items()]
        self.fields['email'].widget.attrs.update({'pattern':'[a-zA-Z]+[a-zA-Z0-9]+.apss@gmail.com','title':'Use only endwith ".apss@gmail.com"  and starts with character'})
        self.fields['username'].widget.attrs.update({ 'pattern':'[a-zA-Z]+','title':'Use only characters'})
#        self.fields['phone'].widget.attrs.update({ 'pattern':'/(2|3|4|5|6|7|8|9)\d{9}/','title':'Use only integers'})
#        self.fields['emergency_contact1'].widget.attrs.update({ 'pattern':'/(2|3|4|5|6|7|8|9)\d{9}/','title':'Use only integers'})
#        self.fields['emergency_contact2'].widget.attrs.update({ 'pattern':'/(2|3|4|5|6|7|8|9)\d{9}/','title':'Use only integers'})
        self.fields['first_name'].widget.attrs.update({ 'pattern':'[a-zA-Z]+','title':'Use only characters'})
        self.fields['last_name'].widget.attrs.update({ 'pattern':'[a-zA-Z]+','title':'Use only characters'})
        for field_name in field_names:
            field = self.fields.get(field_name)
            field.widget.attrs.update({'placeholder': field.label,'required':True})


class registration(PlaceholderMixin,forms.ModelForm):
    email = forms.EmailField(label='Email', max_length=40, min_length=10,
                             widget=forms.EmailInput(attrs={'placeholder': 'Email',}))
    password = forms.CharField(label='Password',
                                max_length=50, min_length=8,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    class Meta():
        model=User
        fields=('username','email','gender','phone','photo','first_name','last_name','emergency_contact1_name','emergency_contact1','emergency_contact2_name','emergency_contact2','employee_type','password')


class loginform(forms.Form):
    email = forms.EmailField(label='Email', max_length=40, min_length=10,
                             widget=forms.EmailInput())
    password = forms.CharField(label='Password',
                                max_length=50, min_length=8,
                                widget=forms.PasswordInput())

OFFICE='OF'
HOME='H'
WORK_LOCATION=[
    (OFFICE,'Office'),
    (HOME,'Home')
]
class timesheetlogin(forms.Form):
    worklocationlogin=forms.ChoiceField(choices=WORK_LOCATION)
    lead_name=forms.CharField(label='last_name',max_length=100,min_length=3,widget=forms.TextInput(attrs={'class': 'form-control'}))
    project=forms.CharField(label='project',max_length=150,min_length=4,widget=forms.TextInput(attrs={'class': 'form-control'}))
    today_work_details=forms.CharField(label='today_work_details',max_length=1000,min_length=30,widget=forms.TextInput(attrs={'class': 'form-control'}))


class timesheetlogout(forms.Form):
    #today_work_details=forms.CharField(label='today_work_details',max_length=1000,min_length=30)
    worklocationlogout=forms.ChoiceField(choices=WORK_LOCATION)


class updatephone(forms.Form):
    phone=forms.CharField(label='phone',max_length=20,min_length=9)


class validateemailform(forms.Form):
    email=forms.EmailField(label='Email', max_length=40, min_length=5,
                             widget=forms.EmailInput())



class otpform(forms.Form):
    otp=forms.CharField(min_length=5,max_length=11,required=True)
    password1 = forms.CharField(label='Password1',
                                max_length=50, min_length=5,
                                widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password2',
                                max_length=50, min_length=5,
                                widget=forms.PasswordInput())
