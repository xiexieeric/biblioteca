from django import forms

class SignupForm(forms.Form):
	fname = forms.CharField(label='First Name', max_length=100)
	lname= forms.CharField(label='Last Name', max_length=100)
	username = forms.CharField(label='Username', max_length=100)
	password = forms.CharField(widget=forms.PasswordInput)

class LoginForm(forms.Form):
	username = forms.CharField(label='Username', max_length=100)
	password = forms.CharField(widget=forms.PasswordInput)

class CreateBookForm(forms.Form):
	book = forms.IntegerField(label="Book ID")
	price = forms.FloatField()