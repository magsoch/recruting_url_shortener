from django.db import models
from django.urls import reverse
from hashids import Hashids
import datetime


class UrlQuerySet(models.QuerySet):
    def decode_url(self, short_code):
        decode = Hashids(min_length=4, alphabet='abcdefghijklmnoprstuvwxyz').decode(short_code)[0]
        self.filter(pk=decode).update(counted = models.F('counted') + 1)
        return self.filter(pk=decode).first().url

    def total_urls(self):
        return self.count()

    def total_redirections(self):
        return self.aggregate(redirections = models.Sum('counted'))

    def dates(self, pk):
        return self.values('date').annotate( june = models.Sum(
            'counted', filter=models.Q(filter__gte = datetime.date(2019, 6, 1),
                                       filter__lte=datetime.date(2019, 6, 31)))).filter(pk=pk)


class Url(models.Model):
    url = models.URLField()
    short_code = models.CharField(max_length=8, blank=True)
    date = models.DateField(auto_now_add=True)
    counted = models.PositiveIntegerField(default=0)

    urls = UrlQuerySet.as_manager()

    class Meta:
        verbose_name_plural = 'Urls'

    def __str__(self):
        return f"URL: {self.url} short_code: {self.short_code}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.short_code:
            self.short_code = Hashids(min_length=4, alphabet='abcdefghijklmnoprstuvwxyz').encode(self.pk)
            self.save()

    def get_absolute_url(self):
        return reverse('newapp:detail', kwargs='pk')
