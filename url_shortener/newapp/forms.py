from django import forms
from .models import Url


class ShortenerForm(forms.ModelForm):

    class Meta:
        model = Url
        fields = ['url']
        widgets = {
            'url': forms.URLInput(attrs={'class': 'input is-rounded is-medium', 'placeholder': 'URL'})
        }
