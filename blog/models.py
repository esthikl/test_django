from django.db import models
from django.contrib import admin
from django.utils import timezone
from taggit.managers import TaggableManager


class Post(models.Model):
    objects = models.Manager()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)
    tags = TaggableManager()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class PostAdmin(admin.ModelAdmin):
    list_display = ['tag_list']

    def get_queryset(self, request):
        return super(PostAdmin, self).get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.title for o in obj.tags.all())