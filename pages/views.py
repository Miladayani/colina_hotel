from django.shortcuts import render
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'home.html'


class HomePageView2(TemplateView):
    template_name = 'home2.html'


class HomePageView3(TemplateView):
    template_name = 'home3.html'


class AboutUsPageView(TemplateView):
    template_name = 'pages/aboutus.html'


class RoomsCategoryPageView(TemplateView):
    template_name = 'pages/rooms_category.html'


class RoomOverviewPageView(TemplateView):
    template_name = 'pages/room_overview.html'


class NotFound(TemplateView):
    template_name = 'pages/404.html'

