from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf import settings
from school.views import BaseSystemLoginView,UserDashboard,AddStudentToDatabase,ConnectionSoftwareView,\
    TeachersListView,TeachersAddView,UserSettingsView , \
    PaymentsListView,StudentListView,TeacherJurnalView,StudentAddView,StudentUpdateView, \
    StudentPaymentView,StudentPayView,JurnalWatchView,BranchChooseAdminView,TestView,\
    BranchListView,BranchCreateAdminView,BranchAdminUpdateView,BranchAdminDeleteView,\
    ManagerAddView,ManagerListView,some_view,StopStudentLesson,JurnalArchiveView
from school.ajax_views import ConfirimStudent,StudentAttendanceView,TeacherSalaryCount, \
    DeviceConnectionControls,TeacherSalaryCountForAdmin,ChangeProfilePicture, \
    TeacherArchiveSalaryCountForAdmin
from school.decorators import BaseBranchView


urlpatterns = [
    url(r'^$', BaseSystemLoginView.as_view(), name='restric-login'),
    url(r'^logout/$', auth_views.logout, name="logout",  kwargs={'next_page': settings.LOGIN_URL}),
    # Home page dashboard views
    url(r'^dashboard/$', UserDashboard.as_view(), name='dashboard'),
    # all admin panel Users settings views
    url(r'^settings/$', UserSettingsView.as_view(), name='user-settings'),
    url(r'^branch/$', BranchListView.as_view(), name='main-branch'),
    url(r'^branch/create/$', BranchCreateAdminView.as_view(), name='branch-create'),
    url(r'^branch/(?P<slug>[-\w]+)/update/$', BranchAdminUpdateView.as_view(), name='branch-update'),
    url(r'^branch/(?P<slug>[-\w]+)/delete/$', BranchAdminDeleteView.as_view(), name='branch-delete'),
    # all
    url(r'^b/(?P<slug>[-\w]+)/$', BranchChooseAdminView.as_view(), name='branch-list'),

    # Personal Jurnals for all mounth
    url(r'^jurnal/$', TeacherJurnalView.as_view(), name='teacher-jurnal'),
    # show jurnal by id
    url(r'^jurnal/(?P<pk>[0-9]+)/show/$', JurnalWatchView.as_view(), name="jurnal-show"),
    # Jurnal Arcive view
    url(r'^jurnal/(?P<pk>[0-9]+)/archive/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', JurnalArchiveView.as_view(), name="jurnal-arxiv"),
    # Teachers list view
    url(r'^teacher/list/$', TeachersListView.as_view(), name='teacher-list'),
    # Add new teacher view
    url(r'^teacher/new/$', TeachersAddView.as_view(), name='teacher-add'),
    # Add new Manager view
    url(r'^manager/new/$', ManagerAddView.as_view(), name='manager-add'),
    # Manager list View
    url(r'^manager/list/$', ManagerListView.as_view(), name='manager-list'),
    # Add new students to database
    url(r'^student/new/$', StudentAddView.as_view(), name='student-add'),
    # THis url for add some data to database
    url(r'^adddatabase/$', AddStudentToDatabase, name='add-data'),
    # This url securty for Administrator
    url(r'^security/$', ConnectionSoftwareView.as_view(), name='security'),

    # Paymant student
    url(r'^student/(?P<pk>[0-9]+)/payment/$', StudentPaymentView.as_view(), name="student-pay"),
    # all payment list
    url(r'^payments/$', PaymentsListView.as_view(), name='payment-list'),
    # all student list
    url(r'^student-list/$', StudentListView.as_view(), name='student-list'),
    # Update students
    url(r'^student/(?P<pk>[0-9]+)/update/$', StudentUpdateView.as_view(), name="student-update"),
    # Delete students
    url(r'^student/delete/$', StopStudentLesson.as_view(), name="student-delete"),

    # post requests here
    url(r'^pay/request/$', StudentPayView.as_view(), name="payment-request"),

    # CHange profile picture
    url(r'^change/image/$', ChangeProfilePicture.as_view(), name="change-profile-picture"),

    # AJAX urls hereee
    url(r'^confirmed-student/$', ConfirimStudent.as_view(), name="student-confirm"),
    url(r'^attendance/$', StudentAttendanceView.as_view(), name="attendance-confirm"),
    url(r'^hesabla/$', TeacherSalaryCount.as_view(), name="hesabla"),
    url(r'^hesabla_for_admin/$', TeacherSalaryCountForAdmin.as_view(), name="hesabla-admin"),
    # teacher arcive jurnal counter
    url(r'^hesabla_for_archive/$', TeacherArchiveSalaryCountForAdmin.as_view(), name="hesabla-arxiv"),
    url(r'^device/connection/$', DeviceConnectionControls.as_view(), name="device-connection"),
    # Just in case for admin panel excell format
    url(r'^export/excell/$', some_view, name="export-excell"),

]


