from django.contrib import admin
from django.utils import timezone
from .models import Category, City, Ad, AdImage


admin.site.register(Category)
admin.site.register(City)


# class AdImageAdmin(admin.StackedInline):
# 	model = AdImage


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
	# inlines = [AdImageAdmin]
	list_display = ('ad_title', 'ad_text', 'author', 'category', 'city', 'last_up')
	readonly_fields = ('last_up', )
