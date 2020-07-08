from datetime import timedelta
from django.utils import timezone
from django import forms
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Category, City, Ad, AdImage
from .utils import AdCreateMixin, AdUpdateMixin
from .forms import AdForm


class IndexPage(View):

	def get(self, request, *args, **kwargs):
		ads 				= Ad.objects.order_by('-last_up')[:5]
		categories			= Category.objects.all()
		cities				= City.objects.all()
		main_category		= Category.objects.filter(parent=None)
		subcategory			= Category.objects.exclude(parent=None)

		context = {
			'ads': ads,
			'categories': categories,
			'main_category': main_category,
			'subcategory': subcategory,
			'cities': cities,
		}
		return render(request, 'jerdesh/index.html', context)


class AdList(View):

	def get(self, request):
		search_title 	= request.GET.get('search', None)
		search_city 	= request.GET.get('location', None)
		search_category = request.GET.get('category', None)

		if search_title or search_city or search_category:
			ads = Ad.objects.filter(ad_title__icontains=search_title, city_id=search_city, category_id=search_category)
		else:
			ads = Ad.objects.order_by('-last_up')

		categories		= Category.objects.all()
		cities			= City.objects.all()
		paginator 		= Paginator(ads, 10)
		page_number 	= request.GET.get('page', 1)
		page 			= paginator.get_page(page_number)
		is_paginated 	= page.has_other_pages()

		if page.has_previous():
			prev_url = f'?page={page.previous_page_number()}'
		else:
			prev_url = ''

		if page.has_next():
			next_url = f'?page={page.next_page_number()}'
		else:
			next_url = ''

		context = {
			'ads': page,
			'is_paginated': is_paginated,
			'next_url': next_url,
			'prev_url': prev_url,
			'categories': categories,
			'cities': cities,
		}
		return render(request, 'jerdesh/ads_list.html', context)


class AdCategoryList(View):

	def get(self, request, category_id):
		
		ads = Ad.objects.filter(category__id=category_id)

		paginator 		= Paginator(ads, 10)
		page_number 	= request.GET.get('page', 1)
		page 			= paginator.get_page(page_number)
		is_paginated 	= page.has_other_pages()

		if page.has_previous():
			prev_url = f'?page={page.previous_page_number()}'
		else:
			prev_url = ''

		if page.has_next():
			next_url = f'?page={page.next_page_number()}'
		else:
			next_url = ''

		context = {
			'ads': page,
			'is_paginated': is_paginated,
			'next_url': next_url,
			'prev_url': prev_url,
		}
		return render(request, 'jerdesh/category_list.html', context)


# CRUD
class AdCreate(AdCreateMixin):
	model = Ad
	form_class = AdForm


class AdUpdate(AdUpdateMixin):
	model = Ad
	form_class = AdForm


class AdDelete(DeleteView):
	model = Ad
	template_name = 'jerdesh/ad_delete.html'
	success_url = reverse_lazy('jerdesh:ads_list_url')


class AdDetails(View):

	def get(self, request, slug):
		ad = Ad.objects.get(slug__iexact=slug)
		images = AdImage.objects.filter(ad=ad)
		time = False
		is_favorite = False

		if (ad.last_up + timedelta(hours=10)) < timezone.now():
			time = True

		if ad.favorite.filter(id=request.user.id).exists():
			is_favorite = True

		context = {
			'ad': ad,
			'images': images,
			'time': time,
			'is_favorite': is_favorite,
		}
		return render(request, 'jerdesh/ad_details.html', context)


class AdUp(View):

	def post(self, request, slug):
		ad = Ad.objects.get(slug__iexact=slug)
		if (ad.last_up + timedelta(hours=10)) < timezone.now():
			ad.last_up = timezone.now()
			ad.save()
			return redirect(ad.get_absolute_url())
		else:
			return redirect('jerdesh:index_url')


def favoriteAd(request, slug):
	ad = Ad.objects.get(slug__iexact=slug)
	if ad.favorite.filter(id=request.user.id).exists():
		ad.favorite.remove(request.user)
	else:
		ad.favorite.add(request.user)
	return redirect(ad.get_absolute_url())
