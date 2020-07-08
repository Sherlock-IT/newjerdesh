from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth import urls
from django.urls import reverse_lazy

from . import views
from .forms import ResetPasswordForm, ChangePasswordForm

app_name = 'users'
urlpatterns = [
	path('registration/', views.userRegistration, name='user_registration_url'),
	path('authorization/', views.userAuthorization, name='user_authorization_url'),
	path('logout/', views.userLogout, name='user_logout_url'),
	path('admin/', views.userAdmin, name='user_admin_url'),
	path('edit/', views.userEdit, name='user_edit_url'),

	path('password_change/', auth_views.PasswordChangeView.as_view(form_class=ChangePasswordForm, success_url = reverse_lazy('users:password_change_done')), name='password_change'),
	path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

	path('password_reset/', auth_views.PasswordResetView.as_view(success_url = reverse_lazy('users:password_reset_done')), name='password_reset'),
	path('password_reset_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(form_class=ResetPasswordForm, success_url = reverse_lazy('users:password_reset_complete')), name='password_reset_confirm'),
	path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
