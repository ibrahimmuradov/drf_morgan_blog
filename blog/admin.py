from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Blog, BlogImage, Tag, Category, Comment
from django import forms
from django.core.exceptions import ValidationError

class ImageInlineFormSet(forms.models.BaseInlineFormSet):
    def clean(self):
        count = 0
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                count += 1
                if count > 1:
                    raise ValidationError("You can select a maximum of 1 image.")

        super().clean()

class ImageInline(admin.TabularInline):
    model = BlogImage
    extra = 1
    formset = ImageInlineFormSet

class BlogAdmin(admin.ModelAdmin):
    readonly_fields = ('user_admin', 'view_count',)
    inlines = (ImageInline,)

admin.site.register(Blog, BlogAdmin)

admin.site.register(BlogImage)

admin.site.register(Category)

admin.site.register(Tag)

admin.site.register(Comment, MPTTModelAdmin)
