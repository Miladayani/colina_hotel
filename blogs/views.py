from django.shortcuts import render
from django.views.generic import TemplateView


class BlogItemPageView(TemplateView):
    template_name = 'blogs/blog_item.html'
