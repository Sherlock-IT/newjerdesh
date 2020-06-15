from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Account


class UserRegistrationForm(UserCreationForm):
	# email 			= forms.EmailField(max_length=60, help_text='Введите корректный email адрес')
	# username 		= forms.CharField(max_length=30)
	# password1 		= forms.CharField(widget=forms.PasswordInput())
	# password2 		= forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = Account
		fields = ('email', 'username', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(UserRegistrationForm, self).__init__(*args, **kwargs)

		self.fields['email'].widget.attrs['class'] 			= 'input-text'
		self.fields['email'].widget.attrs['id'] 			= 'your-email'
		self.fields['email'].widget.attrs['placeholder'] 	= 'Ваш email'

		self.fields['username'].widget.attrs['class'] 		= 'input-text'
		self.fields['username'].widget.attrs['id'] 			= 'full-name'
		self.fields['username'].widget.attrs['placeholder'] 	= 'Логин'

		self.fields['password1'].widget.attrs['class'] 		= 'input-text'
		self.fields['password1'].widget.attrs['id'] 			= 'password'
		self.fields['password1'].widget.attrs['placeholder'] 	= 'Пароль'

		self.fields['password2'].widget.attrs['class'] = 'input-text'
		self.fields['password2'].widget.attrs['id'] = 'comfirm-password'
		self.fields['password2'].widget.attrs['placeholder'] = 'Повторите пароль'
