from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import SetPasswordForm
from .models import Account


class UserRegistrationForm(UserCreationForm):

	class Meta:
		model = Account
		fields = ('email', 'phone', 'username', 'password1', 'password2')
		error_messages = {
			'email' : {
				'unique': 'Пользователь с таким email уже зарегистрирован'
			},
			'username' : {
				'unique': 'Пользователь с таким username уже зарегистрирован'
			},
			'phone' : {
				'invalid': 'Номер введен некорректно. Формат: "+996" или "0 номер"',
				'unique': 'Пользователь с таким номером уже зарегистрирован'
			},
		}

	def __init__(self, *args, **kwargs):
		super(UserRegistrationForm, self).__init__(*args, **kwargs)

		self.fields['email'].widget.attrs['class'] 				= 'input-text'
		self.fields['email'].widget.attrs['id'] 				= 'your-email'
		self.fields['email'].widget.attrs['placeholder'] 		= 'Ваш email'

		self.fields['phone'].widget.attrs['class'] 				= 'input-text'
		self.fields['phone'].widget.attrs['id'] 				= 'your-email'
		self.fields['phone'].widget.attrs['placeholder'] 		= 'Номер телефона'

		self.fields['username'].widget.attrs['class'] 			= 'input-text'
		self.fields['username'].widget.attrs['id'] 				= 'full-name'
		self.fields['username'].widget.attrs['placeholder'] 	= 'Логин'

		self.fields['password1'].widget.attrs['class'] 			= 'input-text'
		self.fields['password1'].widget.attrs['id'] 			= 'password'
		self.fields['password1'].widget.attrs['placeholder'] 	= 'Пароль'

		self.fields['password2'].widget.attrs['class'] 			= 'input-text'
		self.fields['password2'].widget.attrs['id'] 			= 'comfirm-password'
		self.fields['password2'].widget.attrs['placeholder'] 	= 'Повторите пароль'


class EditProfileForm(UserChangeForm):
	class Meta:
		model = Account
		fields = ('email', 'phone', 'username', 'password')
		error_messages = {
			'email' : {
				'unique': 'Пользователь с таким email уже зарегистрирован'
			},
			'username' : {
				'unique': 'Пользователь с таким username уже зарегистрирован'
			},
			'phone' : {
				'invalid': 'Номер введен некорректно. Формат: "+996" или "0 номер"',
				'unique': 'Пользователь с таким номером уже зарегистрирован'
			},
		}
	
	def __init__(self, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)

		self.fields['email'].widget.attrs['class'] = 'form-control'
		self.fields['phone'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['class'] = 'form-control'


class ChangePasswordForm(PasswordChangeForm):

	def __init__(self, *args, **kwargs):
		super(ChangePasswordForm, self).__init__(*args, **kwargs)
		for field in ('old_password', 'new_password1', 'new_password2'):
			self.fields[field].widget.attrs = {'class': 'form-control'}


class ResetPasswordForm(SetPasswordForm):

	def __init__(self, *args, **kwargs):
		super(ResetPasswordForm, self).__init__(*args, **kwargs)
		for field in ('new_password1', 'new_password2'):
			self.fields[field].widget.attrs = {'class': 'form-control'}
