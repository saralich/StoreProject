from django import forms
from django.forms import ModelForm, modelformset_factory

from .models import User, Order, Product

class RegisterForm(forms.Form):
#	class Meta:
#		model = User
#		fields = ['user_name', 'user_password', 'user_address',
#					'user_email']
#
#	def clean_user_name(self):
#		print self.cleaned_data.get('user_name')
#		return stuff
	username = forms.CharField(label='Username',min_length=6, max_length=100, required=True)
	fName = forms.CharField(label='FirstName', min_length=1, max_length=100, required=True)
	lName = forms.CharField(label='LastName', min_length=1, max_length=100, required=True)
	password = forms.CharField(label = 'Password', min_length=8,widget=forms.PasswordInput(), required=True)
	passwordCheck = forms.CharField(label='passwordCheck',min_length=8,widget=forms.PasswordInput(), required=True)
	email = forms.CharField(label='Email',max_length = 100)
	address = forms.CharField(label='Address',max_length = 100)

class SignInForm(forms.Form):
	username = forms.CharField(label='Username', min_length=8, max_length=100, required=True)
 	password = forms.CharField(label='Password', widget=forms.PasswordInput(), required=True)

class DeleteAccountForm(forms.Form):
	deleteAccount = forms.CharField(label='Enter password to finish deleting your account.')

class UpdateAccountForm(forms.Form):
 	password = forms.CharField(label = 'Password', min_length=8,widget=forms.PasswordInput(), required=True)
	passwordCheck = forms.CharField(label='passwordCheck',min_length=8,widget=forms.PasswordInput(), required=True)
	email = forms.CharField(label='Email',max_length = 100)
	address = forms.CharField(label='Address',max_length = 100)

class ProductForm(forms.Form):
	productID = forms.CharField(label='ProductID',min_length=6, max_length=100, required=True)
	productName = forms.CharField(label='productName', min_length=1, max_length=100, required=True)
	productDescription = forms.CharField(label='ProductDescription', min_length=1, max_length=100, required=True)
	productActive = forms.BooleanField(label='Active')
	productQuantity = forms.IntegerField()
	productPrice = forms.IntegerField()

