from django.db import models

from django.conf import settings
from ckeditor.fields import RichTextField
import datetime
# Create your models here.

User = settings.AUTH_USER_MODEL

class Category(models.Model):
    Category = models.CharField(blank=False, null=False, max_length=100)
    def __str__(self):
        return self.Category

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description = RichTextField()
    image = models.ImageField(upload_to='posts_imgs/', help_text = '''It is recommended to upload a 'JPEG' image with the following dimensions 400x400''')
    slug = models.SlugField(unique=True, error_messages = {'required': 'Slug cannot be blank!'})
    published = models.BooleanField(default=True)

    # webDevelopment = 'Web Development'
    # security = 'Security'
    # programming = 'Programming'
    # categories = (
    #         (webDevelopment, 'Web Development'),
    #         (security, 'Security'),
    #         (programming, 'Programming')
    # )

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # category = models.CharField(null=False, max_length=100, choices= categories, default= webDevelopment)

    def __str__(self):
        return self.title

    def get_path(self):
        return "/posts/{}".format(self.pk)

    def add_comment(self):
        return "/posts/addcomment/{}".format(self.pk)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} comment, on {}".format(self.user.username, self.post.slug)
