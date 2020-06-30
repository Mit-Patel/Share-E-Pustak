from django import forms

# import forms
from django.contrib.auth.forms import User
from .models import UserProfileInfo, USER_TYPE_CHOICES

# form classes
class UserForm(forms.ModelForm):        
    password = forms.CharField(widget=forms.PasswordInput(),label="Password")

    class Meta():
        model = User
        fields = ('username', 'email','password','first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-user'
            visible.field.widget.attrs['placeholder'] = visible.field.label          

        for field in self.Meta.fields:
            self.fields[field].required = True  

class UserProfileInfoForm(forms.ModelForm):
    type = forms.ChoiceField(choices=USER_TYPE_CHOICES,widget=forms.Select(attrs={'style':'padding:0.8rem 1rem;height:3rem;'}))
    class Meta():
        model  = UserProfileInfo
        fields = ('mobile_no', 'city', 'type',)

    def __init__(self, *args, **kwargs):
        super(UserProfileInfoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-user'
            visible.field.widget.attrs['placeholder'] = visible.field.label

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(),label="Password")

    class Meta():
        model = User
        fields = ('username', 'password')
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-user'
            visible.field.widget.attrs['placeholder'] = visible.field.label
