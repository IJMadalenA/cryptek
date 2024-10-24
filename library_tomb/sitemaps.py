from django.contrib.sitemaps import Sitemap

from library_tomb.models.post import Post


class PostSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Post.objects.filter(status=1)

    def lastmod(self, obj):
        return obj.updated_at
