from modeltranslation.translator import translator, TranslationOptions
from .models import Blog


class BlogTranslation(TranslationOptions):
    fields = ("title", "subject", "text")


translator.register(Blog, BlogTranslation)
