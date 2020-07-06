from django.db import models
from datetime import datetime
from django.conf import settings
User = settings.AUTH_USER_MODEL
from django.shortcuts import reverse
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image
from djmoney.models.fields import MoneyField


class Category(models.Model):
	parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Основная категория')
	category_text = models.CharField(max_length=100, verbose_name='Название')

	def __str__(self):
		return self.category_text


class City(models.Model):
	city_text = models.CharField(max_length=200)

	def __str__(self):
		return self.city_text


class Ad(models.Model):
	category 			= models.ForeignKey(Category, on_delete=models.CASCADE, null=True, verbose_name='Категория')
	city 				= models.ForeignKey(City, on_delete=models.CASCADE, null=True, verbose_name='Город')
	author 				= models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Автор')
	favorite			= models.ManyToManyField(User, blank=True, related_name='favorite', verbose_name='Избранное')
	slug 				= models.SlugField(max_length=250)
	ad_title 			= models.CharField(max_length=200, verbose_name='Название')
	ad_text 			= models.TextField(verbose_name='Описание')
	price 				= MoneyField(max_digits=14, decimal_places=0, default_currency='KGS')
	phone 				= PhoneNumberField(verbose_name='Номер телефона')
	img 				= models.ImageField(upload_to='images/')
	pub_date 			= models.DateTimeField(auto_now_add=True)
	last_up				= models.DateTimeField(default=datetime.now())

	def save(self):
		super().save()
		img = Image.open(self.img.path)

		if img.height > 500 or img.width > 500:
			output_size = (500, 500)
			img.thumbnail(output_size)
			img.save(self.img.path)

	def __str__(self):
		return self.ad_title

	def get_absolute_url(self):
		return reverse('jerdesh:ad_details_url', kwargs={'slug': self.slug})

	class Meta:
		ordering = ['-pub_date']


class AdImage(models.Model):
	ad 					= models.ForeignKey(Ad, on_delete=models.CASCADE, default=None)
	img 				= models.ImageField(upload_to='images/')

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		img = Image.open(self.img.path)

		if img.height > 500 or img.width > 500:
			output_size = (500, 500)
			img.thumbnail(output_size)
			img.save(self.img.path)
