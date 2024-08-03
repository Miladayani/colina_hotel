from django.shortcuts import render
from django.views.generic import TemplateView


class ContactPageView(TemplateView):
    template_name = 'contacts/contact.html'
