from django.conf.urls import url
from website.views import BaseIndexView, AboutUsView, MyTemplate
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^$', BaseIndexView.as_view(), name='index'),
    url(r'^c77151bf83ab.html$', TemplateView.as_view(template_name='c77151bf83ab.html'), name='template'),
    url(r'^about-us/$', AboutUsView.as_view(), name='about-us'),
    url(r'^vacancy.html$', AboutUsView.as_view(), name='vacancy-list'),
    url(r'^test/$', MyTemplate.as_view(), name='test'),
    url(r'^index.html$', TemplateView.as_view(template_name='html/new_index.html'), name='base'),
    url(r'^about.html$', TemplateView.as_view(template_name='html/about.html'), name='base'),
    url(r'^all.html$', TemplateView.as_view(template_name='html/all.html'), name='all'),
    url(r'^contact.html$', TemplateView.as_view(template_name='html/contact.html'), name='contact'),
    url(r'^newsmore.html$', TemplateView.as_view(template_name='html/newsmore.html'), name='newsmore'),
]
