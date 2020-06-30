from django import forms
from .models import *
# from authenticate_app.forms import UserForm

class BookForm(forms.ModelForm):    
    # user = forms.CharField(widget=forms.HiddenInput())

    class Meta():
        model = Book
        fields = ('title', 'description', 'isbn','author', 'publisher','edition','image', 'upload_date', 'is_available', 'book_format', 'language', 'category_id')
        
    
    def __init__(self, *args, **kwargs):
        # user = kwargs.pop('user','')
        super(BookForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-user'
            visible.field.widget.attrs['placeholder'] = visible.field.label  

# class AuthorForm(forms.ModelForm):
#     class Meta():
#         model = Author
#         fields = ('name',)
#     def __init__(self, *args, **kwargs):
#         super(AuthorForm, self).__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'form-control form-control-user'
#             visible.field.widget.attrs['placeholder'] = visible.field.label  

# class PublisherForm(forms.ModelForm):
#     class Meta():
#         model = Publisher
#         fields = ('name',)
#     def __init__(self, *args, **kwargs):
#         super(PublisherForm, self).__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'form-control form-control-user'
#             visible.field.widget.attrs['placeholder'] = visible.field.label  

# class CategoryForm(forms.ModelForm):
#     class Meta():
#         model = Category
#         fields = ('name',)

#     def __init__(self, *args, **kwargs):
#         super(CategoryForm, self).__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'form-control form-control-user'
#             visible.field.widget.attrs['placeholder'] = visible.field.label  

# class BookUploadForm(forms.ModelForm):        
#     # password = forms.CharField(widget=forms.PasswordInput(),label="Password")

#     class Meta():
#         model = BookUploadDetails
#         fields = ('user', 'isbn','image', 'upload_date', 'is_available', 'book_format', 'language')

#     def __init__(self, *args, **kwargs):
#         super(BookUploadForm, self).__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'form-control form-control-user'
#             visible.field.widget.attrs['placeholder'] = visible.field.label          

# class AuthorOfBookForm(forms.ModelForm):        
#     class Meta():
#         model = AuthorOfBook
#         fields = ('author', 'isbn',)

#     def __init__(self, *args, **kwargs):
#         super(AuthorOfBookForm, self).__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'form-control form-control-user'
#             visible.field.widget.attrs['placeholder'] = visible.field.label          

