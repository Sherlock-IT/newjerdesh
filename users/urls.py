from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'users'
urlpatterns = [
	path('registration/', views.userRegistration, name='user_registration_url'),
	path('authorization/', views.userAuthorization, name='user_authorization_url'),
	path('logout/', views.userLogout, name='user_logout_url'),
	path('admin/', views.userAdmin, name='user_admin_url'),
	path('edit/', views.userEdit, name='user_edit_url'),
]
