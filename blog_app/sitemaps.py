from django.contrib.sitemaps import Sitemap

from library_tomb.models.entry import Entry


class EntrySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Entry.objects.filter(status=1)

    def lastmod(self, obj):
        return obj.updated_at
