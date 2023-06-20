from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm



class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()
	
	first_name = forms.CharField(max_length = 20)
	last_name = forms.CharField(max_length = 20)
	class Meta:
		model = CustomUser
		fields = ['username', 'email','password1', 'password2']
