from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.
class Image(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='images_created', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField(max_length=2000)
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True)

    users_like = models.ManyToManyField(get_user_model(), related_name='images_liked', blank=True)
    total_likes = models.PositiveIntegerField(default=0)
    # image.users_like.all()
    # user.images_liked.all()

    class Meta:
        indexes = [
            models.Index(fields=['created']),
            models.Index(fields=['-total_likes']),
        ]
        ordering = ['-created']

    def __str__(self):
        return self.title

    # Автоматическая генерация поля slug на основе значения поля title
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])
