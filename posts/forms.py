from django.forms import ModelForm
from django import forms
from .models import Post, Comment
from ckeditor.widgets import CKEditorWidget

class PostModelForm(ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post
        fields = ['title', 'description', 'image', 'published', 'slug', 'category']


class AddCommentModelForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
