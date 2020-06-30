from django import forms

# import forms
# from django.contrib.auth.forms import User
from .models import User,UserProfileInfo, Student, Faculty, Alumni
# from authenticate_app.forms import UserForm

class StudentForm(forms.ModelForm):
    class Meta():
        model = Student
        fields = ('branch', 'semester', 'year', 'cpi','enrollment_no',)
    
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-user'
            visible.field.widget.attrs['placeholder'] = visible.field.label  

class FacultyForm(forms.ModelForm):
    class Meta():
        model = Faculty
        fields = ('branch',)
    def __init__(self, *args, **kwargs):
        super(FacultyForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-user'
            visible.field.widget.attrs['placeholder'] = visible.field.label  

class AlumniForm(forms.ModelForm):
    class Meta():
        model = Alumni
        fields = ('branch', 'company', 'post',)
    def __init__(self, *args, **kwargs):
        super(AlumniForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-user'
            visible.field.widget.attrs['placeholder'] = visible.field.label  

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('mobile_no', 'city',)

    def __init__(self, *args, **kwargs):
        super(UserProfileInfoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-user'
            visible.field.widget.attrs['placeholder'] = visible.field.label  

class UserForm(forms.ModelForm):        
    # password = forms.CharField(widget=forms.PasswordInput(),label="Password")

    class Meta():
        model = User
        fields = ('username', 'email','first_name', 'last_name',)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-user'
            visible.field.widget.attrs['placeholder'] = visible.field.label          

        for field in self.Meta.fields:
            self.fields[field].required = True  
