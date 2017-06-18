import json
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View,FormView
from django.contrib.auth import get_user_model
from school.models import Studend,Attendense,Payment,AllowedIpAddress,PaymentException,Teacher
from school.options.tools import attendance_status
from school.forms import ChangePictureForm
from datetime import datetime as d
import calendar
import math
User = get_user_model()
# just for security issues




# class BaseSchoolAjaxView(AllowedIpAddress,View,AllowOnlyTeacher):
#     """
#         Base ajax views for Teachers check
#         Students attendance "+","-" or "i"
#         "+" - means that Student is have been at lesson
#         "-" - means that Student have't been at lesson
#         "i" - means that Student permitted
#         "+" and "-" - all student attendace time minus
#         "i" - student attendance nothing due
#     """
#     def get_post_ajax_data(self):
#         """
#         :param: student id, teacher_id,status_id
#         :return:
#         """
#         if self.request.is_ajax():
#             data = self.request.POST.copy()
#             data.get('data_id')
#             pass

def check_exception(teacher):
    try:
        teach = Teacher.objects.get(teach=teacher)
        check = PaymentException.objects.get(subj=teach.sub,filyal=teach.teach.branch)
        return True
    except:
        return False


class ConfirimStudent(View):

    def post(self,request):
        if request.is_ajax():
            data_id = request.POST.get('student_id')
            obj = Studend.objects.get(id=data_id)
            obj.testiq = True
            obj.save()
            return HttpResponse('success')


class StudentAttendanceView(View):
    def post(self,request):
        if request.is_ajax():
            today = d.today().strftime("%Y.%m")
            studend_id = request.POST.get('student_id')
            attendance_day = request.POST.get('day')
            attendance_type = request.POST.get('type')
            day = d.strptime(today+'.'+str(attendance_day),"%Y.%m.%d")
            try:
                obj = Attendense.objects.get(people_id=studend_id,teach_id=request.user.id,day=day)
                obj.status = attendance_status(attendance_type)
                obj.save()
                self.hesabla(attendance_status(attendance_type),studend_id)
            except:
                obj = Attendense(
                    people_id=studend_id,
                    teach_id=request.user.id,
                    day=day,
                    status=attendance_status(attendance_type),
                )
                obj.save()
                self.hesabla(attendance_status(attendance_type), studend_id)
            return HttpResponse('success')

    def hesabla(self,at_type,studend_id):
        if at_type == 1:
            obj = Studend.objects.get(id=studend_id)
            obj.qalan_ders -= 1
            obj.save()
        elif at_type == 2:
            obj = Studend.objects.get(id=studend_id)
            obj.qalan_ders += 0
            obj.save()
        else:
            obj = Studend.objects.get(id=studend_id)
            obj.qalan_ders += 1
            obj.save()



class TeacherSalaryCount(View):
    def post(self,request):
        if request.is_ajax():
            teacher = request.user
            today = d.today().strftime("%Y-%m")
            y = int(d.today().strftime("%Y"))
            m = int(d.today().strftime("%m"))
            arr = []
            prize = []
            obj = Attendense.objects.filter(teach=teacher,day__range=[today + '-1', today + '-' + str([x for x in calendar.monthrange(y, m)][-1])])
            for x in obj:
                arr.append(x.people)
            if check_exception(teacher):
                for student in list(set(arr)):
                    say = Attendense.objects.filter(teach=teacher,people=student,status__range=[1,2],day__range=[today + '-1', today + '-' + str([x for x in calendar.monthrange(y, m)][-1])]).count()
                    teach = Teacher.objects.get(teach=teacher)
                    qiymet = teach.sub.get_istisna_prize()
                    prize.append(qiymet*say)
            else:
                for student in list(set(arr)):
                    say = Attendense.objects.filter(teach=teacher,people=student,status__range=[1,2],day__range=[today + '-1', today + '-' + str([x for x in calendar.monthrange(y, m)][-1])]).count()
                    if student.money:
                        qiymet = student.money / 2
                        plan = student.plan
                        prize.append(qiymet * say / plan)
                    else:
                        qiymet = 0
                        prize.append(0)
            return HttpResponse(math.ceil(sum(prize)*100)/100)


class TeacherSalaryCountForAdmin(View):
    def post(self,request):
        if request.is_ajax():
            id = self.request.POST.get('teach')
            teacher = User.objects.filter(id=id).last()
            today = d.today().strftime("%Y-%m")
            y = int(d.today().strftime("%Y"))
            m = int(d.today().strftime("%m"))
            arr = []
            prize = []
            obj = Attendense.objects.filter(teach=teacher,day__range=[today + '-1', today + '-' + str([x for x in calendar.monthrange(y, m)][-1])])
            for x in obj:
                arr.append(x.people)
            if check_exception(teacher):
                for student in list(set(arr)):
                    say = Attendense.objects.filter(teach=teacher,people=student,status__range=[1,2],day__range=[today + '-1', today + '-' + str([x for x in calendar.monthrange(y, m)][-1])]).count()
                    teach = Teacher.objects.get(teach=teacher)
                    qiymet = teach.sub.get_istisna_prize()
                    prize.append(qiymet*say)
            else:
                for student in list(set(arr)):
                    say = Attendense.objects.filter(teach=teacher,people=student,status__range=[1,2],day__range=[today + '-1', today + '-' + str([x for x in calendar.monthrange(y, m)][-1])]).count()
                    if student.money:
                        qiymet = student.money / 2
                        plan = student.plan
                        prize.append(qiymet * say / plan)
                    else:
                        qiymet = 0
                        prize.append(0)
            return HttpResponse(math.ceil(sum(prize)*100)/100)


class TeacherArchiveSalaryCountForAdmin(View):
    def post(self,request):
        if request.is_ajax():
            id = self.request.POST.get('teach')
            teacher = User.objects.filter(id=id).last()
            today = "2017-05"
            y = int("2017")
            m = int("05")
            arr = []
            prize = []
            obj = Attendense.objects.filter(teach=teacher,day__range=[today + '-1', today + '-' + str([x for x in calendar.monthrange(y, m)][-1])])
            for x in obj:
                arr.append(x.people)
            if check_exception(teacher):
                for student in list(set(arr)):
                    say = Attendense.objects.filter(teach=teacher,people=student,status__range=[1,2],day__range=[today + '-1', today + '-' + str([x for x in calendar.monthrange(y, m)][-1])]).count()
                    teach = Teacher.objects.get(teach=teacher)
                    qiymet = teach.sub.get_istisna_prize()
                    prize.append(qiymet*say)
            else:
                for student in list(set(arr)):
                    say = Attendense.objects.filter(teach=teacher,people=student,status__range=[1,2],day__range=[today + '-1', today + '-' + str([x for x in calendar.monthrange(y, m)][-1])]).count()
                    if student.money:
                        qiymet = student.money / 2
                        plan = student.plan
                        prize.append(qiymet * say / plan)
                    else:
                        qiymet = 0
                        prize.append(0)
            return HttpResponse(math.ceil(sum(prize)*100)/100)


class DeviceConnectionControls(View):
    def post(self,request):
        if request.is_ajax() and request.user.usertype == 3:
            device = request.POST.get('device_id')
            try:
                obj = AllowedIpAddress.objects.filter(id=device).last()
                if obj.status:
                    obj.status = False
                    obj.save()
                    return HttpResponse('false')
                else:
                    obj.status = True
                    obj.save()
                    return HttpResponse('true')
            except:
                return HttpResponse('error')



class ChangeProfilePicture(FormView):
    form_class = ChangePictureForm
    template_name = 'home/dashboard.html'
    home_page = '/'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        return HttpResponse("Hacking attemp")

    def post(self, request):
        if request.is_ajax():
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            file = request.FILES
            if form.is_valid():
                object = User.objects.get(id=request.user.id)
                object.profile_picture = form.cleaned_data['profile_image']
                object.save()
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            return HttpResponse('not allowed')