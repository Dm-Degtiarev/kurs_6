from blog.models import Blog
from mailing.forms import FormStyleMixin
from django import forms


class BlogForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Blog
        exclude = ('publicate_date', 'views_count')