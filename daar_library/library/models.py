from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    text_content = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
