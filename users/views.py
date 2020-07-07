from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy

from jerdesh.models import Ad
from .forms import UserRegistrationForm
from .forms import EditProfileForm
from .forms import ChangePasswordForm, ResetPasswordForm
from .decorators import unauthenticated_user
from .models import Account


def userAuthorization(request):
	if request.method == 'POST':
		email 		= request.POST.get('email')
		password 	= request.POST.get('password')
		account 	= authenticate(email=email, password=password)
		if account is not None:
			login(request, account)
			return redirect('jerdesh:index_url')
		else:
			message = 'email или пароль введены неверно'
			return render(request, 'users/login.html', {'message': message})
	return render(request, 'users/login.html', {})


def userRegistration(request):
	context = {}
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email 			= form.cleaned_data.get('email')
			raw_password 	= form.cleaned_data.get('password1')
			account 		= authenticate(email=email, password=raw_password)
			login(request, account)
			return redirect('jerdesh:index_url')
		else:
			context['registration_form'] = form
	else:
		form = UserRegistrationForm()
		context['registration_form'] = form
	return render(request, 'users/register.html', context)


@unauthenticated_user
def userLogout(request):
	logout(request)
	return redirect('jerdesh:index_url')


@unauthenticated_user
def userAdmin(request):
	user = request.user
	favorite_posts = user.favorite.all()
	ads = Ad.objects.filter(author=request.user)

	context = {
		'favorite_posts': favorite_posts,
		'ads': ads,
	}

	return render(request, 'users/index.html', context)


@unauthenticated_user
def userEdit(request):
	context = {}
	if request.method == 'POST':
		form = EditProfileForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			return redirect(request.path_info)
		else:
			context['form'] = form
	else:
		form = EditProfileForm(instance=request.user)
		context['form'] = form
	return render(request, 'users/form.html', context)


# class PasswordChangeView(LoginRequiredMixin, FormView):
# 	model = Account
# 	form_class = ChangePasswordForm
# 	template_name = 'registration/password_change_form.html'
# 	success_url = reverse_lazy('users:password_change_done')

# 	def get_form_kwargs(self):
# 		kwargs = super(PasswordChangeView, self).get_form_kwargs()
# 		kwargs['user'] = self.request.user
# 		return kwargs

# 	def form_valid(self, form):
# 		form.save()
# 		update_session_auth_hash(self.request, form.user)        
# 		return super(PasswordChangeView, self).form_valid(form)
