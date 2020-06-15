from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic.edit import CreateView
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Category, City, Ad


class IndexPage(View):
	def get(self, request, *args, **kwargs):
		ads 			= Ad.objects.order_by('id')[:5]
		categories		= Category.objects.all()
		cities			= City.objects.all()
		context = {
			'ads': ads,
			'categories': categories,
			'cities': cities,
		}
		return render(request, 'jerdesh/index.html', context)


class AdList(View):
	def get(self, request):
		search_title 	= request.GET.get('search', '')
		search_city 	= request.GET.get('location', '')
		search_category = request.GET.get('category', '')

		if search_title or search_city or search_category:
			ads = Ad.objects.filter(Q(ad_title__icontains=search_title) | Q(city__city_text=search_city) | Q(category__category_text=search_category))
		else:
			ads = Ad.objects.all()

		cities 			= City.objects.all()
		categories 		= Category.objects.all()
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
			'cities': cities,
			'categories': categories,
			'ads': page,
			'is_paginated': is_paginated,
			'next_url': next_url,
			'prev_url': prev_url
		}
		return render(request, 'jerdesh/ads_list.html', context)


# CRUD
class AdCreate(CreateView):
	model = Ad
	template_name = 'jerdesh/ad_create.html'
	fields = ['category', 'city', 'ad_title', 'ad_text', 'img']

	def form_valid(self, form):
		new_ad = form.save(commit=False)
		new_ad.author = self.request.user
		new_ad.save()
		return super().form_valid(form)


class AdDetails(View):
	def get(self, request, slug):
		ad = Ad.objects.get(slug__iexact=slug)
		return render(request, 'jerdesh/ad_details.html', {'ad': ad})
