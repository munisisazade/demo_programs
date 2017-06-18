from django.contrib import admin
from website.models import Menu,SocialLinks,Slider,About_us,Programs_Header, News, Sections, \
    Programs,Events,Multimedia,Contact_us, VacancyMenu, Vacancy
# Register your models here.

class VacancyMenuAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name',)
    search_fields = ('name',)
    list_filter = ('date',)

class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'status','date')
    search_fields = ('name',)
    list_filter = ('status','date')

class SocalLinksAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'status', 'date')
    search_fields = ('name',)
    list_filter = ('status', 'date')

class SliderAdmin(admin.ModelAdmin):
    list_display = ('get_slider_picture', 'title', 'content','status', 'date')
    search_fields = ('title','content')
    list_filter = ('status', 'date')
    readonly_fields = ('get_slider_picture',)

class About_usAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'date')
    search_fields = ('title',)
    list_filter = ('status', 'date')
    readonly_fields = ('get_video_preview',)

class Programs_HeaderAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'date')
    search_fields = ('title',)
    list_filter = ('status', 'date')

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'date')
    search_fields = ('title',)
    list_filter = ('status', 'date')

class SectionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
    search_fields = ('name',)
    list_filter = ('date', )

class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'date')
    search_fields = ('title',)
    list_filter = ('status', 'date')


class ProgramsAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'date')
    search_fields = ('title',)
    list_filter = ('status', 'date')

class EventsAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'date')
    search_fields = ('title',)
    list_filter = ('status', 'date')

class MultimediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'date')
    search_fields = ('title',)
    list_filter = ('status', 'date')

class CollectiveAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'date')
    search_fields = ('title',)
    list_filter = ('status', 'date')

class Contact_usAdmin(admin.ModelAdmin):
    list_display = ('title', 'about', 'phone_1','email_1')


admin.site.register(Menu,MenuAdmin)
admin.site.register(SocialLinks,SocalLinksAdmin)
admin.site.register(Slider,SliderAdmin)
admin.site.register(About_us,About_usAdmin)
admin.site.register(Programs_Header,Programs_HeaderAdmin)
admin.site.register(News,NewsAdmin)
admin.site.register(Sections, SectionsAdmin)
admin.site.register(Programs,ProgramsAdmin)
admin.site.register(Events,EventsAdmin)
admin.site.register(Multimedia,MultimediaAdmin)
admin.site.register(Contact_us,Contact_usAdmin)
admin.site.register(VacancyMenu, VacancyMenuAdmin)
admin.site.register(Vacancy,VacancyAdmin)