from django.db import models

class DateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True

class SlugMixin(models.Model):
    slug = models.SlugField(unique=True, editable=False, blank=True)
    code = models.SlugField(unique=True, editable=False, null=True)

    class Meta:
        abstract = True