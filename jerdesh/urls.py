from django.urls import path, include
from . import views
from users.decorators import unauthenticated_user


app_name = 'jerdesh'
urlpatterns = [
	path('', views.IndexPage.as_view(), name='index_url'),
	path('ads/', views.AdList.as_view(), name='ads_list_url'),
	path('ad/create/', unauthenticated_user(views.AdCreate.as_view()), name='ad_create_url'),
	path('ad/update/<str:slug>/', unauthenticated_user(views.AdUpdate.as_view()), name='ad_update_url'),
	path('ad/delete/<str:slug>/', unauthenticated_user(views.AdDelete.as_view()), name='ad_delete_url'),
	path('ad/up/<str:slug>/', unauthenticated_user(views.AdUp.as_view()), name='ad_up_url'),
	path('ad/favorite/<str:slug>/', unauthenticated_user(views.favoriteAd), name='ad_favorite_url'),
	path('ad/<str:slug>/', views.AdDetails.as_view(), name='ad_details_url'),
]
