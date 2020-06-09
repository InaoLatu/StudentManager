from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from student_manager.models import Student


# For the fields of the User Django Model
class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email address'}))
    first_name = forms.CharField(required=True, max_length=150,
                                 widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(required=True, max_length=150,
                                widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    username = forms.CharField(required=True, max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Username'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password confirmation'})

class DateInput(forms.DateInput):
    input_type = 'date'
# For extended fields apart from the User ones
class StudentCreateForm(ModelForm):
    faculty = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Faculty'}))
    birth_date = forms.DateField(widget=DateInput)

    class Meta:
        model = Student
        fields = ('faculty', 'birth_date')
        widgets = {'birth_date': DateInput()}