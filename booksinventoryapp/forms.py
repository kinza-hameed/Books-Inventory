import datetime
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from .models import Book
from django.forms import ModelForm


class RegistrationForm(UserCreationForm):
 
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']

        def clean_form(self):
            first_name = self.cleaned_data['first_name']
            last_name = self.cleaned_data['last_name']
            email = self.cleaned_data['email']
            username = self.cleaned_data['username']
            password1 = self.cleaned_data['password1']
        


            return first_name,last_name,email, username


class AddBookForm(forms.Form):
    isbn = forms.IntegerField(required = True)
    quantity = forms.IntegerField(required = True)
    price = forms.IntegerField(required = True)

class AddBookDetailsForm(forms.ModelForm):
    isbn = forms.IntegerField(required = False)
    seller = forms.IntegerField(required = False)
    quantity_and_price = forms.IntegerField(required = False)
    class Meta:
        model = Book
        fields = ['isbn','seller','title','author','publisher','publication_date','quantity_and_price','cover_page']

class SearchForm(forms.Form):
    
    OPTIONS = (
        ('isbn', "ISBN"),
        ('title', "Title"),
        ('author', "Author"),
        ('publisher', "Publisher")
    )
    CHOICES = (
        ('4','4'),
        ('2','2'),
        ('1','1'),
    )
    keyword = forms.CharField(required=True)
    books_per_page = forms.IntegerField(label='Books per page', widget=forms.Select(choices=CHOICES))
    checks = forms.MultipleChoiceField(required= False, widget=forms.CheckboxSelectMultiple, choices=OPTIONS)
    fields = ['keyword','checks', 'books_per_page']

# class PaginationForm(forms.Form):
#     CHOICES = (
#         ('4','4'),
#         ('2','2'),
#         ('1','1'),
#     )
#     books_per_page = forms.IntegerField(label='Books per page', widget=forms.Select(choices=CHOICES))
