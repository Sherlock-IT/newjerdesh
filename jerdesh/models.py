from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL
from django.shortcuts import reverse


class Category(models.Model):
	category_text = models.CharField(max_length=100)

	def __str__(self):
		return self.category_text


class SubCategory(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	subcategory_text = models.CharField(max_length=100)

	def __str__(self):
		return self.subcategory_text


class City(models.Model):
	city_text = models.CharField(max_length=200)

	def __str__(self):
		return self.city_text


class Ad(models.Model):
	category 			= models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, verbose_name='Категория')
	city 				= models.ForeignKey(City, on_delete=models.CASCADE, null=True, verbose_name='Город')
	author 				= models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Автор')
	favorite			= models.ManyToManyField(User, blank=True, related_name='favorite', verbose_name='Избранное')
	slug 				= models.SlugField(max_length=250, unique_for_date='pub_date')
	ad_title 			= models.CharField(max_length=200, verbose_name='Название')
	ad_text 			= models.TextField(verbose_name='Описание')
	img 				= models.ImageField(upload_to='images/')
	pub_date 			= models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.ad_text

	def get_absolute_url(self):
		return reverse('jerdesh:ad_details_url', kwargs={'slug': self.slug})

	class Meta:
		ordering = ['-pub_date']


class AdImage(models.Model):
	ad 					= models.ForeignKey(Ad, on_delete=models.CASCADE, default=None)
	img 				= models.ImageField(upload_to='images/')
