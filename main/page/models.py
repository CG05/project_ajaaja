from django.db import models

# Create your models here.
class Page(models.Model):
    username = models.CharField(max_length=100, null=False, blank=False)
    pagepath = models.CharField(max_length=100, null=False, blank=False)
    title = models.CharField(max_length=100)
    content = models.JSONField('json', default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title