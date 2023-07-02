from django.urls import path
from blog.apps import BlogConfig
from blog.views import BlogListView, BlogDeleteView, BlogCreateView, BlogDetailView, BlogUpdateView


app_name = BlogConfig.name

urlpatterns = [
    path('blog/', BlogListView.as_view(), name='blog_list'),
    path('blog/create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'),
    path('blog/update/<int:pk>/', BlogUpdateView.as_view(), name='blog_update'),
]

