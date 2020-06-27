from django import forms
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Category, SubCategory, City, Ad, AdImage


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

		if search_title:
			ads = Ad.objects.filter(ad_title__icontains=search_title)
		else:
			ads = Ad.objects.all()

		cities 			= City.objects.all()
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
			'prev_url': prev_url
		}
		return render(request, 'jerdesh/ads_list.html', context)


# CRUD
class AdCreate(CreateView):
	subcategories = SubCategory.objects.all()
	model = Ad
	fields = ['city', 'ad_title', 'ad_text', 'img']

	def get_form(self, form_class=None):
		form = super(AdCreate, self).get_form(form_class)
		form.fields['ad_title'].widget.attrs['placeholder'] = 'Название объявления'
		form.fields['ad_text'].widget.attrs['placeholder'] = 'Описание объявления'
		form.fields['img'].widget = forms.FileInput(attrs={'multiple': 'multiple'})
		form.fields['img'].widget.attrs['class'] = 'custom-file-input'
		return form

	def get_context_data(self, **kwargs):
		ctx = super(AdCreate, self).get_context_data(**kwargs)
		ctx['subcategories'] = self.subcategories
		return ctx
		
	def form_valid(self, form):
		new_ad = form.save()
		new_ad.slug = '-'.join(new_ad.ad_title.split()) + '-id-' + str(new_ad.id)
		new_ad.author = self.request.user
		for image in self.request.FILES.getlist('img'):
			AdImage.objects.create(ad=new_ad, img=image)
		new_ad.save()
		return super(AdCreate, self).form_valid(form)


class AdUpdate(UpdateView):
	subcategories = SubCategory.objects.all()
	model = Ad
	fields = ['city', 'ad_title', 'ad_text', 'img']

	def get_context_data(self, **kwargs):
		ctx = super(AdUpdate, self).get_context_data(**kwargs)
		ctx['subcategories'] = self.subcategories
		return ctx

	def form_valid(self, form):
		new_ad = form.save()
		new_ad.slug = '-'.join(new_ad.ad_title.split()) + '-id-' + str(new_ad.id)
		new_ad.save()
		return super(AdUpdate, self).form_valid(form)


class AdDelete(DeleteView):
	model = Ad
	template_name = 'jerdesh/ad_delete.html'
	success_url = reverse_lazy('jerdesh:ads_list_url')


class AdDetails(View):
	def get(self, request, slug):
		ad = Ad.objects.get(slug__iexact=slug)
		images = AdImage.objects.filter(ad=ad)
		is_favorite = False

		if ad.favorite.filter(id=request.user.id).exists():
			is_favorite = True

		context = {
			'ad': ad,
			'images': images,
			'is_favorite': is_favorite,
		}
		return render(request, 'jerdesh/ad_details.html', context)

	
def favoriteAd(request, slug):
	ad = Ad.objects.get(slug__iexact=slug)
	if ad.favorite.filter(id=request.user.id).exists():
		ad.favorite.remove(request.user)
	else:
		ad.favorite.add(request.user)
	return redirect(ad.get_absolute_url())
