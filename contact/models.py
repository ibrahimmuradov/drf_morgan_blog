from django.db import models
from services.mixin import DateMixin

class Contact(DateMixin):
    name = models.CharField(max_length=300)
    email = models.CharField(max_length=320)
    subject = models.CharField(max_length=400)
    message = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-created_at", )
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
