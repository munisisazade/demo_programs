from django.contrib import admin
from school.models import MyUser
# Register your models here.
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from school.forms import *
from school.models import *

User = get_user_model()


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
        'first_name', 'last_name', 'email', 'username', 'birthday', 'gender', 'unvani', 'phone', 'study', 'subjects',
        'profile_picture', 'branch', 'branch_status', 'position', 'usertype')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ("first_name", "last_name", 'username', 'password1', 'password2'),
        }),
    )
    # The forms to add and change user instances
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'username', 'email')
    ordering = ('-date_joined',)
    filter_horizontal = ('groups', 'user_permissions',)


class AllowedIpAddressAdmin(admin.ModelAdmin):
    list_display = ('ip', 'address', 'status')


class StudendAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'prize', 'plan', 'testiq')
    search_fields = ('full_name',)
    list_filter = ('gender',)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order_full_name', 'order_teacher_name', 'prize', 'date', 'qalan_plan', 'status')
    list_filter = ('status', 'prize', 'date')


class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'date', 'prize')
    search_fields = ('student__full_name',)
    list_filter = ('date',)


def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance

    return Wrapper


class AttendenseAdmin(admin.ModelAdmin):
    list_display = ('people_full_name', 'order_teacher_name', 'day', 'status')
    search_fields = ('people__full_name',)
    list_filter = ('day', ('status', custom_titled_filter("Davamiyyətin statusuna ")),
                   ('teach__first_name', custom_titled_filter("Müəllimin adına ")),
                   ('people__full_name', custom_titled_filter("Tələbənin adına ")))


class PaymentExceptionAdmin(admin.ModelAdmin):
    list_display = ('subj', 'prize')
    readonly_fields = ('get_description',)


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'get_student_count', 'get_subject')
    search_fields = ('teach__first_name',)
    list_filter = ('deleted',)


class JurnalArchiveAdmin(admin.ModelAdmin):
    list_display = ('get_teacher_name', 'month')
    search_fields = ('teach__first_name',)
    list_filter = ('month',)


class PandaBranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'date')
    search_fields = ('name',)
    list_filter = ('other','status')
    readonly_fields = ('slug','color_picker')


admin.site.register(User, MyUserAdmin)
admin.site.register(AdminPanelUrl)
admin.site.register(AllowedIpAddress, AllowedIpAddressAdmin)
admin.site.register(Studend, StudendAdmin)
admin.site.register(Subject)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Teacher_student)
admin.site.register(Teacher_lesson)
admin.site.register(RelationDateLesson)
admin.site.register(Attendense, AttendenseAdmin)
admin.site.register(PandaBranch, PandaBranchAdmin)
admin.site.register(PaymentHistory, PaymentHistoryAdmin)
admin.site.register(PaymentException, PaymentExceptionAdmin)
admin.site.register(JurnalArchive, JurnalArchiveAdmin)
