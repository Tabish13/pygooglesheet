from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('htmlparser', views.HtmlParse, name='htmlparser'),
    path('incorsheet', views.IncorGsheetParser, name='incorsheet'),
    path('godrejsheet', views.GodrejPropertiesGsheetParser, name='godrejsheet'),
]