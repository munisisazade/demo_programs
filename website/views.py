from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic import TemplateView, View, ListView
from website.models import Menu, SocialLinks, Slider, About_us, Programs_Header, Programs, Events, \
    News, Multimedia, Collective, Contact_us, VacancyMenu, Vacancy


# Create your views here.


class PandaSchoolBaseView(View):
    def get_nav_menu_items(self):
        obj = Menu.objects.filter(status=True)
        return obj

    def get_footer_links(self):
        obj = SocialLinks.objects.filter(status=True)
        return obj

    def get_vacancy_menu(self):
        obj = VacancyMenu.objects.all()
        return obj

    def get_context_data(self, **kwargs):
        context = {}
        context['base_menu'] = self.get_nav_menu_items()
        context['footer_links'] = self.get_footer_links()
        context['vacancy_list'] = self.get_vacancy_menu()
        return context


class BaseIndexView(PandaSchoolBaseView):
    template_name = 'html/index.html'
    additional = 'home/index.html'

    def get_all_sliders(self):
        obj = Slider.objects.filter(status=True)
        return obj

    def get_last_about_us(self):
        obj = About_us.objects.filter(status=True).last()
        return obj

    def get_programs_head(self):
        obj = Programs_Header.objects.filter(status=True).last()
        return obj

    def get_events(self):
        obj = Events.objects.filter(status=True)[:3]
        return obj

    def get_all_news(self):
        obj = News.objects.filter(status=True)[:3]
        return obj

    def get_multimedia(self):
        obj = Multimedia.objects.filter(status=True)[:3]
        return obj

    def get_collective(self):
        obj = Collective.objects.filter(status=True)[:3]
        return obj

    def get_contact_us(self):
        obj = Contact_us.objects.all().last()
        return obj

    def get_context_data(self, **kwargs):
        context = super(BaseIndexView, self).get_context_data(**kwargs)
        context['sliders'] = self.get_all_sliders()
        context['about_us'] = self.get_last_about_us()
        context['program_head'] = self.get_programs_head()
        context['program_list'] = Programs.objects.filter(status=True)
        context['event_list'] = self.get_events()
        context['news_list'] = self.get_all_news()
        context['multimedia_list'] = self.get_multimedia()
        context['collective_list'] = self.get_collective()
        context['contact_us'] = self.get_contact_us()
        return context

    def get(self, request):
        if '/panda.' in request.build_absolute_uri():
            return render(request, self.additional, self.get_context_data())
        else:
            return render(request, self.additional,
                          self.get_context_data())  # return render(request,self.template_name)


class AboutUsView(PandaSchoolBaseView):
    template_name = 'html/about.html'

    def get_context_data(self, **kwargs):
        context = super(AboutUsView, self).get_context_data(**kwargs)
        context['title'] = Menu.objects.filter(link__icontains='about').last()
        context['about'] = About_us.objects.filter(status=True)
        return context

    def get(self, request):
        return render(request, self.template_name, self.get_context_data())


class MyTemplate(TemplateView):
    template_name = '404.html'


class VacancyListView(PandaSchoolBaseView,ListView):
    model = Vacancy
