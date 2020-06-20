from django.contrib import admin
from django.utils import timezone
from .models import Category, SubCategory, City, Ad, AdImage


admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(City)


class AdImageAdmin(admin.StackedInline):
	model = AdImage


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
	inlines = [AdImageAdmin]
	list_display = ['ad_title', 'ad_text', 'author', 'category', 'city', 'pub_date']
