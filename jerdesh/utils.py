from django.views.generic.edit import CreateView, UpdateView
from .models import Category, AdImage


class AdCreateMixin(CreateView):
    model = None
    form_class = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        create = super(AdCreateMixin, self).get_context_data(**kwargs)
        create['categories'] = Category.objects.filter(parent=None)
        create['subcategories'] = Category.objects.exclude(parent=None)
        return create

    def form_valid(self, form):
        new_ad 			= form.save()
        new_ad.slug 	= '-'.join(new_ad.ad_title.split()) + '-id-' + str(new_ad.id)
        new_ad.author 	= self.request.user
        if self.request.FILES.getlist('img'):
            for image in self.request.FILES.getlist('img'):
                AdImage.objects.create(ad=new_ad, img=image)
        new_ad.save()
        return super(AdCreateMixin, self).form_valid(form)


class AdUpdateMixin(UpdateView):
    model = None
    form_class = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        update = super(AdUpdateMixin, self).get_context_data(**kwargs)
        update['categories'] = categories = Category.objects.filter(parent=None)
        update['subcategories'] = subcategories = Category.objects.exclude(parent=None)
        return update
		
    def form_valid(self, form):
        new_ad 			= form.save()
        new_ad.slug 	= '-'.join(new_ad.ad_title.split()) + '-id-' + str(new_ad.id)
        new_ad.author 	= self.request.user
        for image in self.request.FILES.getlist('img'):
            AdImage.objects.create(ad=new_ad, img=image)
        new_ad.save()
        return super(AdUpdateMixin, self).form_valid(form)
