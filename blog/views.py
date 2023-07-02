from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from blog.forms import BlogForm
from blog.models import Blog


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    extra_context = {
        'title': 'Блог'
    }

class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BlogForm(instance=self.object)
        context['title'] = context['object']

        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.views_count +=1
        self.object.save()
        context = self.get_context_data(object=self.object)

        return self.render_to_response(context)

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_detail_create_save.html'
    success_url = reverse_lazy('blog:blog_list')
    extra_context = {
        'title': 'Создать рассылку'
    }

class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Удалить | {context['object']}"

        return context

class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_detail_create_save.html'
    success_url = reverse_lazy('blog:blog_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Удалить | {context['object']}"

        return context
