from django import forms
from .models import Ad


class AdForm(forms.ModelForm):
    
    class Meta:
        model = Ad
        fields = ('img', 'city', 'category', 'ad_title', 'ad_text', 'phone')

    def __init__(self, request, *args, **kwargs):
        super(AdForm, self).__init__(*args, **kwargs)
        self.fields['ad_title'].widget.attrs['placeholder'] = 'Название объявления'
        self.fields['ad_text'].widget.attrs['placeholder'] = 'Описание объявления'
        self.fields['phone'].widget.attrs['placeholder'] = 'Номер телефона'
        self.fields['phone'].widget.attrs['value'] = request.user.phone
        self.fields['img'].widget = forms.FileInput(attrs={'multiple': 'multiple'})
        self.fields['img'].widget.attrs['class'] = 'custom-file-input'
