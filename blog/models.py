from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField


# 🔹 Category (1-nhiều: 1 category có nhiều bài)
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


# 🔹 Tag (nhiều-nhiều: 1 bài có nhiều tag, 1 tag có thể gắn cho nhiều bài)
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

# 🔹 Tạo bài Post
class Post(models.Model): 
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')  # Cho phép không có category
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')  # Cho phép không có tag
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


