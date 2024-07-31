from django.shortcuts import render
from django.views.generic import TemplateView


class Facilities(TemplateView):
    template_name = 'facilities/faci.html'

