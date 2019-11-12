from django.shortcuts import render
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.base import RedirectView
from .forms import ShortenerForm
from .models import Url


class CreateShortener(CreateView):
    model = Url
    form_class = ShortenerForm
    template_name = 'start.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_urls'] = Url.urls.total_urls()
        context['total_redirections'] = Url.urls.total_redirections()['redirections']
        return context


class UrlSite(DetailView):
    model = Url
    template_name = 'url.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['june'] = Url.urls.dates(self.kwargs['pk'], )[0]['june']
        return context


class RedirectUrl(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        try:
            return Url.urls.decode_url(self.kwargs['short_code'])
        except IndexError:
            print('Decode without data')
