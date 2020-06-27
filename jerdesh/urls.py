from django.urls import path, include
from . import views


app_name = 'jerdesh'
urlpatterns = [
	path('', views.IndexPage.as_view(), name='index_url'),
	path('ads/', views.AdList.as_view(), name='ads_list_url'),
	path('ad/create/', views.AdCreate.as_view(), name='ad_create_url'),
	path('ad/update/<str:slug>/', views.AdUpdate.as_view(), name='ad_update_url'),
	path('ad/delete/<str:slug>/', views.AdDelete.as_view(), name='ad_delete_url'),
	path('ad/favorite/<str:slug>/', views.favoriteAd, name='ad_favorite_url'),
	path('ad/<str:slug>/', views.AdDetails.as_view(), name='ad_details_url'),
]
