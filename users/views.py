from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from jerdesh.models import Ad
from .forms import UserRegistrationForm
from .decorators import unauthenticated_user


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
