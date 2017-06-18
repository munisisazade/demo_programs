from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse
from django.views.generic import TemplateView, FormView, ListView, CreateView, UpdateView, DetailView,DeleteView
from django.urls import reverse
from django.core.urlresolvers import reverse_lazy
from school.decorators import IpRestrictedForArea, InvalidLoginAttempts, LoginRestrictedMixin, \
    LoginAllowOnlyManagerAndAdministration, AllowOnlyAdministrator,BaseBranchView
from school.models import AllowedIpAddress, Studend, Teacher, Payment, Teacher_student, PaymentHistory, \
    PandaBranch, Attendense
from school.forms import BaseAuthenticationForm, TeachersForm, StudentAddForm, PaymentForm, UserSettingsForm, \
    BranchAddForm,ManagersForm
from school.options.tools import months,get_last_day_of_month
from django.contrib import messages
import os
import datetime
import random
from django.conf import settings
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
import json
import math
import calendar
import csv

User = get_user_model()


# Create your views here.


class BaseSystemLoginView(IpRestrictedForArea, FormView):
    model = User
    form_class = BaseAuthenticationForm
    template_name = 'base/base_index.html'
    login_template = 'base/dashboard.html'
    success_url = '/hesabla'

    def form_valid(self, form):
        user = form.cleaned_data
        login(self.request, user)
        return redirect(reverse('dashboard'))

    def form_invalid(self, form):
        InvalidLoginAttempts(self.request)
        messages.success(
            self.request, 'Təəsüflər olsunki email və ya şifrə yanlışdır'
        )
        return redirect(reverse('restric-login'))

    def get_context_data(self, **kwargs):
        context = super(BaseSystemLoginView, self).get_context_data(**kwargs)

        return context

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('dashboard'))
        else:
            return super(BaseSystemLoginView, self).dispatch(*args, **kwargs)


class UserDashboard(IpRestrictedForArea, TemplateView, LoginRestrictedMixin):
    template_name = 'home/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(UserDashboard, self).get_context_data(**kwargs)
        if self.request.user.usertype == 3:
            context['branch_list'] = PandaBranch.objects.filter(other=False,status=True)
        return context


class BranchChooseAdminView(IpRestrictedForArea, BaseBranchView, DetailView, AllowOnlyAdministrator):
    model = PandaBranch
    template_name = 'home/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(BranchChooseAdminView, self).get_context_data(**kwargs)
        if self.request.user.usertype == 3:
            try:
                obj = User.objects.get(id=self.request.user.id)
                obj.branch = self.get_object()
                obj.save()
            except:
                pass
            context['branch_list'] = PandaBranch.objects.all()

        return context


class BranchCreateAdminView(IpRestrictedForArea, CreateView, AllowOnlyAdministrator):
    model = PandaBranch
    template_name = 'administrator/branch-create.html'
    form_class = BranchAddForm
    home_page = reverse_lazy('restric-login')
    success_url = reverse_lazy('main-branch')

    def form_valid(self, form):
        branch = form.save(commit=True)
        return redirect(self.success_url)

    def handle_ajax_post(self, request, *args, **kwargs):
        form = self.get_form_class()
        return HttpResponse(form)

    def get_context_data(self, **kwargs):
        context = super(BranchCreateAdminView, self).get_context_data(**kwargs)
        return context


class BranchAdminUpdateView(IpRestrictedForArea, UpdateView, AllowOnlyAdministrator):
    model = PandaBranch
    template_name = 'administrator/branch-update.html'
    form_class = BranchAddForm
    home_page = reverse_lazy('restric-login')
    success_url = reverse_lazy('main-branch')

    def form_valid(self, form):
        student = form.save(commit=True)
        return redirect(self.success_url)


    def handle_ajax_post(self, request, *args, **kwargs):
        form = self.get_form_class()
        return HttpResponse(form)

    def get_context_data(self, **kwargs):
        context = super(BranchAdminUpdateView, self).get_context_data(**kwargs)
        return context

class BranchAdminDeleteView(IpRestrictedForArea, DeleteView, AllowOnlyAdministrator):
    model = PandaBranch
    http_method_names = ['post']
    success_url = reverse_lazy('main-branch')


class BranchListView(IpRestrictedForArea, ListView, AllowOnlyAdministrator):
    model = PandaBranch
    template_name = 'administrator/branch-list.html'

    def get_queryset(self):
        return self.model.objects.filter(other=False,status=True)


class TeachersListView(IpRestrictedForArea, BaseBranchView, ListView, LoginAllowOnlyManagerAndAdministration):
    model = Teacher
    template_name = 'teachers/teacher-list.html'


    def get_context_data(self, **kwargs):
        context = super(TeachersListView, self).get_context_data(**kwargs)
        context['kes'] = self.request.GET.get('q', False)
        return context

    def get_queryset(self):
        query = self.request.GET.get('q', False)
        if query:
            return self.model.objects.filter(
                    Q(teach__first_name__icontains=query) | Q(teach__last_name__icontains=query) & Q(
                        teach__branch=self.request.user.branch))
        else:
            return self.model.objects.filter(teach__branch=self.request.user.branch).order_by('teach__last_name')


class ManagerListView(IpRestrictedForArea, BaseBranchView, ListView, AllowOnlyAdministrator):
    model = User
    template_name = 'managers/manager-list.html'


    def get_context_data(self, **kwargs):
        context = super(ManagerListView, self).get_context_data(**kwargs)
        context['kes'] = self.request.GET.get('q', False)
        return context

    def get_queryset(self):
        query = self.request.GET.get('q', False)
        if query:
            return self.model.objects.filter(
                    Q(first_name__icontains=query) | Q(last_name__icontains=query) & Q(
                        branch=self.request.user.branch) & Q(usertype=2))
        else:
            return self.model.objects.filter(usertype=2,branch=self.request.user.branch).order_by('last_name')


class TeachersAddView(IpRestrictedForArea, BaseBranchView, CreateView, LoginAllowOnlyManagerAndAdministration):
    model = Teacher
    form_class = TeachersForm
    template_name = 'teachers/add_new_teacher.html'
    home_page = reverse_lazy('restric-login')
    success_url = reverse_lazy('teacher-list')

    def form_valid(self, form):
        teacher = form.save(commit=True)
        teacher.branch = self.request.user.branch
        teacher.set_password(form.cleaned_data['password'])
        teacher.usertype = 1
        teacher.save()
        return redirect(self.success_url)

    def handle_ajax_post(self, request, *args, **kwargs):
        form = self.get_form_class()
        return HttpResponse(form)

    def get_context_data(self, **kwargs):
        context = super(TeachersAddView, self).get_context_data(**kwargs)
        return context


class ManagerAddView(IpRestrictedForArea, BaseBranchView, CreateView, AllowOnlyAdministrator):
    model = User
    form_class = ManagersForm
    template_name = 'managers/manager-add.html'
    home_page = reverse_lazy('restric-login')
    success_url = reverse_lazy('manager-list')

    def form_valid(self, form):
        teacher = form.save(commit=True)
        teacher.branch = self.request.user.branch
        teacher.usertype = 2
        teacher.save()
        return redirect(self.success_url)

    def handle_ajax_post(self, request, *args, **kwargs):
        form = self.get_form_class()
        return HttpResponse(form)

    def get_context_data(self, **kwargs):
        context = super(ManagerAddView, self).get_context_data(**kwargs)
        return context


class PaymentsListView(TeachersListView):
    model = Payment
    template_name = 'payments/payment-list.html'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super(PaymentsListView, self).get_context_data(**kwargs)
        context['kes'] = self.request.GET.get('q', False)
        return context

    def get_queryset(self):
        query = self.request.GET.get('q', False)
        if query:
            return self.model.objects.filter(
                    Q(people__full_name__icontains=query) & Q(people__branch=self.request.user.branch) & Q(
                        people__testiq=True) & Q(people__deleted=False))
        else:
            return self.model.objects.filter(people__branch=self.request.user.branch, people__testiq=True,
                                                 people__deleted=False).order_by('people__qalan_ders')


class StudentListView(TeachersListView):
    model = Studend
    template_name = 'students/student-list.html'

    def get_context_data(self, **kwargs):
        context = super(StudentListView, self).get_context_data(**kwargs)
        context['kes'] = self.request.GET.get('q', False)
        return context

    def get_queryset(self, **kwargs):
        query = self.request.GET.get('q', False)
        if query:
            return self.model.objects.filter(
                    Q(full_name__icontains=query) & Q(branch=self.request.user.branch)).order_by('-id')
        else:
            return self.model.objects.filter(branch=self.request.user.branch).order_by('-id')


class StudentDeleteView(IpRestrictedForArea, BaseBranchView, UpdateView, AllowOnlyAdministrator):
    model = Studend
    http_method_names = ['post']
    success_url = reverse_lazy('student-list')

    def post(self, request, *args, **kwargs):
        a = self.model.objects.munis
        return redirect(self.success_url)



class StudentPaymentView(IpRestrictedForArea, BaseBranchView, FormView, LoginRestrictedMixin):
    model = Studend
    template_name = 'students/student-pay.html'
    form_class = PaymentForm
    home_page = reverse_lazy('restric-login')
    success_url = '/'  # reverse_lazy('')

    def form_valid(self, form):
        student = form.save(commit=True)
        self.relation_student_to_teacher(student)
        return redirect(reverse('student-list'))

    def relation_student_to_teacher(self, student):
        try:
            data = self.request.POST.getlist('teacher_list')
            for x in data:
                obj = Teacher_student(teach_id=x, people_id=student.id)
                obj.save()
        except:
            pass

    def handle_ajax_post(self, request, *args, **kwargs):
        form = self.get_form_class()
        return HttpResponse(form)

    def get_context_data(self, **kwargs):
        context = super(StudentPaymentView, self).get_context_data(**kwargs)
        context['base_user'] = Studend.objects.get(pk=self.kwargs['pk'])
        return context


class StudentPayView(IpRestrictedForArea, TemplateView, LoginAllowOnlyManagerAndAdministration):
    def post(self, request):
        student = request.POST.get('studend_id')
        prize = request.POST.get('prize')
        # try:
        obj = PaymentHistory(
            student_id=student,
            prize=prize,
        )
        obj.save()
        pay = Payment.objects.filter(people_id=student).last()
        if pay.people.money == int(prize) or not pay.people.money:
            pay.people.money = prize
            pay.people.qalan_ders += pay.people.plan
            pay.people.save()
            pay.date = timezone.now()
            pay.save()
        elif int(pay.people.money) > int(prize) or int(pay.people.money) < int(prize):
            new_plan = (pay.people.plan * int(prize)) / pay.people.money
            pay.people.qalan_ders += math.ceil(new_plan * 10 / 10)
            pay.people.save()
            pay.date = timezone.now()
            pay.save()
        return redirect(reverse('payment-list'))
        # except:
        #     return redirect(reverse('payment-list') + '?error')


"""
    =============================================================================================
    >>>>>>>>>>>>>>>>>>>>>>> This is all about User customization Views For admin panel <<<<<<<<<<<<<<<<<<
    =============================================================================================
"""


class UserSettingsView(IpRestrictedForArea, DetailView, LoginRestrictedMixin):
    model = User
    form_class = UserSettingsForm
    template_name = 'users/settings.html'

    def get_object(self, queryset=None):
        return User.objects.get(id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(UserSettingsView, self).get_context_data(**kwargs)
        return context


class TeacherJurnalView(IpRestrictedForArea, ListView, LoginRestrictedMixin):
    model = Teacher_student
    # form_class = TeachersForm
    template_name = 'teachers/jurnal-personal.html'

    def get_context_data(self, **kwargs):
        context = super(TeacherJurnalView, self).get_context_data(**kwargs)
        context['kes'] = self.request.GET.get('q', False)
        context['days'] = list(range(1,get_last_day_of_month()+1))
        teacher = User.objects.get(id=self.request.user.id)
        context['data'] = json.dumps(teacher.get_teacher_students_attendance())
        context['current_month'] = months[int(datetime.datetime.today().strftime("%m")) - 1]
        return context

    def get_queryset(self, **kwargs):
        query = self.request.GET.get('q', False)
        today = timezone.now().strftime("%Y-%m")
        y = int(timezone.now().strftime("%Y"))
        m = int(timezone.now().strftime("%m"))
        if query:
            return self.model.objects.filter(Q(people__full_name__icontains=query) & Q(people__branch=self.request.user.branch) & Q(teach=self.request.user) & (Q(people__testiq=True) | Q(people__cixdigi_zaman=timezone.now().strftime("%Y %m")))).order_by('people__groups') #(Q(people__deleted_date__range=[today + '-1', today + '-' + str([x for x in calendar.monthrange(y, m)][-1])]) & Q(people__new=False))
        else:
            return self.model.objects.filter(Q(people__branch=self.request.user.branch) & Q(teach=self.request.user) & (Q(people__testiq=True) | Q(people__cixdigi_zaman=timezone.now().strftime("%Y %m")))).order_by('people__groups') #(Q(people__deleted_date__range=[today + '-1', today + '-' + str([x for x in calendar.monthrange(y, m)][-1])]) & Q(people__new=False))


class JurnalWatchView(IpRestrictedForArea , BaseBranchView, DetailView, LoginAllowOnlyManagerAndAdministration):
    model = User
    # form_class = TeachersForm
    template_name = 'teachers/jurnal-personal.html'

    def get_context_data(self, **kwargs):
        today = timezone.now().strftime("%Y-%m")
        y = int(timezone.now().strftime("%Y"))
        m = int(timezone.now().strftime("%m"))
        context = super(JurnalWatchView, self).get_context_data(**kwargs)
        context['object_list'] = Teacher_student.objects.filter(Q(teach_id=self.object.pk) & (Q(people__testiq=True) | Q(people__cixdigi_zaman=timezone.now().strftime("%Y %m")))).order_by('people__groups')
        context['kes'] = self.request.GET.get('q', False)
        context['days'] = list(range(1,get_last_day_of_month()+1))
        teacher = self.model.objects.get(id=self.object.id)
        context['data'] = json.dumps(teacher.get_teacher_students_attendance())
        context['current_month'] = months[int(datetime.datetime.today().strftime("%m")) - 1]
        context['block_jurnal'] = True
        return context


        # def get_object(self,id):
        #     query = self.request.GET.get('q', False)
        #     if query:
        #         return self.model.objects.filter(
        #             Q(people__full_name__icontains=query) & Q(
        #                 people__testiq=True) & Q(teach_id=id)).order_by('-id')
        #     else:
        #         return self.model.objects.filter(teach_id=id, people__testiq=True).order_by('-id')


class JurnalArchiveView(IpRestrictedForArea,BaseBranchView, DetailView, LoginRestrictedMixin):
    model = User
    template_name = 'teachers/jurnal-archive.html'


    def get_context_data(self,**kwargs):
        teacher = self.model.objects.get(pk=self.kwargs.get("pk"))
        today = str(self.kwargs.get("year")) + "-" + str(self.kwargs.get("month"))
        y = int(self.kwargs.get("year"))
        m = int(self.kwargs.get("month"))
        context = super(JurnalArchiveView, self).get_context_data(**kwargs)
        context['object_list'] = Teacher_student.objects.filter(Q(teach=teacher) & (Q(people__testiq=True) | Q(people__cixdigi_zaman=today))).order_by('people__groups')
        context['kes'] = self.request.GET.get('q', False)
        context['days'] = list(range(1, 32))
        context['data'] = json.dumps(teacher.get_teacher_attendance_archive(y,m))
        context['current_month'] = months[int(m) - 1]
        context['block_jurnal'] = True
        return context



class StudentAddView(IpRestrictedForArea,BaseBranchView, CreateView, LoginRestrictedMixin):
    model = Studend
    template_name = 'students/student-add.html'
    form_class = StudentAddForm
    home_page = reverse_lazy('restric-login')
    success_url = reverse_lazy('student-list')

    def form_valid(self, form):
        student = form.save(commit=True)
        student.branch = self.request.user.branch
        student.save()
        self.relation_student_to_teacher(student)
        return redirect(self.success_url)

    def relation_student_to_teacher(self, student):
        try:
            data = self.request.POST.getlist('teacher_list')
            for x in data:
                obj = Teacher_student(teach_id=x, people_id=student.id)
                obj.save()
        except:
            pass

    def handle_ajax_post(self, request, *args, **kwargs):
        form = self.get_form_class()
        return HttpResponse(form)

    def get_context_data(self, **kwargs):
        context = super(StudentAddView, self).get_context_data(**kwargs)
        context['teachers'] = Teacher.objects.filter(teach__branch=self.request.user.branch, deleted=False)
        return context


class StudentUpdateView(IpRestrictedForArea, BaseBranchView, UpdateView, LoginAllowOnlyManagerAndAdministration):
    model = Studend
    template_name = 'students/student_update.html'
    form_class = StudentAddForm
    home_page = reverse_lazy('restric-login')
    success_url = reverse_lazy('student-list')

    def form_valid(self, form):
        student = form.save(commit=True)
        self.relation_student_to_teacher(student)
        return redirect(self.success_url)

    def relation_student_to_teacher(self, student):
        try:
            data = self.request.POST.getlist('teacher_list')
            for x in data:
                try:
                    obj = Teacher_student.objects.get(teach_id=x, people_id=student.id)
                    pass
                except:
                    obj = Teacher_student(teach_id=x, people_id=student.id)
                    obj.save()
        except:
            pass

    def handle_ajax_post(self, request, *args, **kwargs):
        form = self.get_form_class()
        return HttpResponse(form)

    def get_context_data(self, **kwargs):
        context = super(StudentUpdateView, self).get_context_data(**kwargs)
        context['teachers'] = Teacher.objects.filter(teach__branch=self.request.user.branch,deleted=False)
        context['student'] = Teacher_student.objects.filter(teach__branch=self.request.user.branch,
                                                            people_id=self.kwargs.get('pk')).last()
        return context


"""
    =============================================================================================
    >>>>>>>>>>>>>>>>>>>>>>> This is all about Securty Views For Administration <<<<<<<<<<<<<<<<<<
    =============================================================================================
"""


class ConnectionSoftwareView(IpRestrictedForArea, BaseBranchView,ListView, AllowOnlyAdministrator):
    model = AllowedIpAddress
    template_name = 'security/systemdevice.html'
    paginate_by = 10

    def post(self, request):
        post = request.POST
        pass

    def get_context_data(self, **kwargs):
        """
        This is for filter table for status
        :param kwargs:
        :return:
        """
        context = super(ConnectionSoftwareView, self).get_context_data(**kwargs)
        # if self.filter_for_status() == 'True':
        #     context['kes'] = "Aktiv"
        #     context['object_list'] = self.model.objects.filter(status=True)
        # elif self.filter_for_status() == "null":
        #     pass
        # else:
        #     context['kes'] = "Qeyri aktiv"
        #     context['object_list'] = self.model.objects.filter(status=False)
        return context

    def filter_for_status(self):
        """
        Check for filter database function
        :return:
        """
        if 'status' in self.request.GET:
            query = self.request.GET.get('status', "")
            if query == 'True':
                return query
            elif query == 'False':
                return query
            else:
                return ""
        else:
            return "null"

    def func(self, change_id):
        pass


"""
    =============================================================================================
    >>>>>>>>>>>>>>>>>>>>>>>This Just for aditional data to add database<<<<<<<<<<<<<<<<<<<<<<<<<<
    =============================================================================================
"""


def AddStudentToDatabase(request):
    file = os.path.join(settings.STATIC_ROOT, 'siyahi.txt')
    with open(file, 'rb') as f:
        for student in f.readlines():
            data = list(filter(('').__ne__, student.decode('utf-8').split(' ')))
            obj = Studend(
                name=data[1],
                surname=data[0],
                father_name=data[2],
                birthday=datetime.datetime.today(),
                gender=random.randint(1, 2),
                unvani="askdmasld",
                phone=random.randint(3212040432, 9212040432)
            )
            obj.save()
    return HttpResponse("done")


class StopStudentLesson(IpRestrictedForArea, BaseBranchView,TemplateView, AllowOnlyAdministrator):
    template_name = 'students/student-list.html'
    success_url = reverse_lazy('payment-list')


    def post(self,request,*args,**kwargs):
        student = request.POST.get('studend_id')
        obj = Studend.objects.get(id=student)
        obj.testiq = False
        obj.new = False
        obj.deleted_date = timezone.now()
        obj.cixdigi_zaman = timezone.now().strftime("%Y %m")
        obj.save()
        attendance = Attendense(
            people_id=student,
            teach=obj.get_teacher_obj(),
            day=timezone.now(),
            status=4
        )
        attendance.save()
        return redirect(self.success_url)
# import datetime, threading
#
# def foo():
#     a = Payment.objects.get(id=1)
#     a.prize += 1
#     a.save()
#     threading.Timer(1, foo).start()
#
# foo()

"""
    Just in case Test views
"""


class TestView(IpRestrictedForArea, TemplateView):
    template_name = 'administrator/branch-list.html'



def some_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="odenishler.csv"'

    writer = csv.writer(response)
    writer.writerow(['Ödəniş edən şəxsin adı', 'Ödəniş Məbləği', 'Müəllimin adı', 'Ödəniş tarixi'])
    for data in PaymentHistory.objects.all():
        writer.writerow([data.student.full_name, data.student.money, data.student.get_teachers(), data.date])
    return response