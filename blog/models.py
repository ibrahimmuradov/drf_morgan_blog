from django.db import models
from services.mixin import DateMixin, SlugMixin
from services.uploader import Uploader
from services.choices import STATUS
from services.generator import CodeGenerator
from services.slugify import slugify
from django.contrib.auth import get_user_model
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models import Q
from ckeditor.fields import RichTextField

user = get_user_model()

class Category(DateMixin, MPTTModel):
    name = models.CharField(max_length=300)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    @property
    def blog_count(self):
        return Blog.objects.filter(Q(category_id=self.id) | Q(category__parent_id=self.id)).count()


class Tag(DateMixin):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Blog(DateMixin, SlugMixin):
    user_admin = models.ForeignKey(user, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=300)
    subject = models.TextField()
    text = RichTextField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    view_count = models.PositiveIntegerField(null=True)
    status = models.CharField(max_length=100, choices=STATUS, default='Active')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'

    def save(self, *args, **kwargs):
        self.code = CodeGenerator.create_activation_link_code(size=20, model_=Blog)
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    @property
    def popular_blogs(self):
        return Blog.objects.filter(Q(status='Active')).order_by('-view_count')[:3]

class BlogImage(DateMixin):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to=Uploader.upload_image_blog, max_length=500)

    def __str__(self):
        return self.blog.title

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'BlogImage'
        verbose_name_plural = 'BlogImages'


class Comment(DateMixin, MPTTModel):
    user = models.ForeignKey(user, on_delete=models.CASCADE, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, related_name='children')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    message = models.TextField()

    def __str__(self):
        return f'{self.user.username} --- {self.id}'

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    @property
    def comment_count(self):
        return Comment.objects.filter(blog_id=self.blog.id).count()