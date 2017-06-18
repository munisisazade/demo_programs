from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from school.options.tools import slugify, GENDER, POSITION, USERTYPES, PAYMENT_STATUS, ATTENDANCE
from datetime import datetime as d
import calendar
from django.db.models import Q
# My custom tools import
from school.options.tools import get_user_profile_photo_file_name
# Create your models here.
USER_MODEL = settings.AUTH_USER_MODEL
import random


#Customize User model
class MyUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """

    username = models.CharField(_('username'), max_length=100, unique=True,
                                help_text=_('Tələb olunur. 75 simvol və ya az. Hərflər, Rəqəmlər və '
                                            '@/./+/-/_ simvollar.'),
                                validators=[
                                    validators.RegexValidator(r'^[\w.@+-]+$', _('Düzgün istifadəçi adı daxil edin.'), 'yanlışdır')
                                ])
    first_name = models.CharField(_('first name'), max_length=255, blank=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True)
    email = models.EmailField(_('email address'), max_length=255)
    birthday = models.DateField(verbose_name="ad günü",default=timezone.now)
    profile_picture = models.ImageField(upload_to=get_user_profile_photo_file_name,null=True,blank=True)
    gender = models.IntegerField(choices=GENDER, verbose_name="cinsi",null=True,blank=True)
    unvani = models.CharField(max_length=255, verbose_name="ünvanı",null=True,blank=True)
    phone = models.CharField(max_length=100, verbose_name="Telefonu",null=True,blank=True)
    study = models.CharField(max_length=200, verbose_name="Təhsili",null=True,blank=True)
    subjects = models.ForeignKey('Subject',null=True,blank=True,verbose_name="Keçdiyi fənn")
    branch = models.ForeignKey('PandaBranch',null=True,blank=True, verbose_name="Filial")
    branch_status = models.BooleanField(default=False, verbose_name="Yalniz bir filiali gore biler")
    position = models.IntegerField(choices=POSITION, verbose_name="Vəzifəsi",null=True,blank=True)
    usertype = models.IntegerField(choices=USERTYPES, verbose_name="Sistemdəki statusu",null=True,blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    """
        Important non-field stuff
    """
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'İstifadəçi'
        verbose_name_plural = 'İstifadəçilər'

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def get_teacher_subject(self):
        try:
            obj = Teacher.objects.get(teach=self)
            return obj.sub.name
        except:
            return False

    def get_teacher_pk(self):
        try:
            obj = Teacher.objects.get(teach=self)
            return obj.pk
        except:
            return False

    def get_teacher_students_attendance(self):
        try:
            today = d.today().strftime("%Y-%m")
            y = int(d.today().strftime("%Y"))
            m = int(d.today().strftime("%m"))
            obj = Attendense.objects.filter(teach=self, day__range=[today + '-1', today + '-' + str([x for x in calendar.monthrange(y, m)][-1])]).order_by('people')
            arr = []
            for x in obj:
                arr.append([int(x.day.strftime('%d')), x.status, x.people.id])
            return arr
        except:
            return []

    def get_teacher_attendance_archive(self,year,month):
        try:
            today = str(year)+"-"+str(month)
            y = int(year)
            m = int(month)
            obj = Attendense.objects.filter(teach=self, day__range=[today + '-1', today + '-' + str([x for x in calendar.monthrange(y, m)][-1])]).order_by('people')
            arr = []
            for x in obj:
                arr.append([int(x.day.strftime('%d')), x.status, x.people.id])
            return arr
        except:
            return []


class Studend(models.Model):
    full_name = models.CharField(max_length=100,verbose_name="Tam adi",default="")
    birthday = models.DateField(default=timezone.now, verbose_name="Doğum tarixi")
    gender = models.IntegerField(choices=GENDER,null=True,blank=True, verbose_name="cinsi")
    unvani = models.CharField(max_length=255,null=True,blank=True, verbose_name="ünvanı")
    phone = models.CharField(max_length=100,null=True,blank=True, verbose_name="Telefonu")
    plan = models.IntegerField(null=True,blank=True,verbose_name="Dərs planı")
    branch = models.ForeignKey('PandaBranch',null=True, blank=True, verbose_name="Tələbənin filialı")
    start = models.DateTimeField(default=timezone.now,verbose_name="Qeydiyyat vaxtı")
    testiq = models.BooleanField(default=False)
    groups = models.CharField(max_length=255,null=True,blank=True,verbose_name="Qrupun adı")
    money = models.FloatField(null=True,blank=True,verbose_name="Aylıq pulu")
    qalan_ders = models.IntegerField(default=0, verbose_name="Qalan dərs sayı")
    deleted_date = models.DateTimeField(default=timezone.now)
    join_date = models.DateTimeField(default=timezone.now)
    new = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    cixdigi_zaman = models.CharField(max_length=100,default="")

    class Meta:
        verbose_name_plural = 'Tələbələr'
        verbose_name = 'Tələbə'

    def ab(self):
        return ["+",''][random.randint(0,1)]

    ab.short_description = "1"
    ab.allow_tags = True

    def get_subject(self):
        try:
            obj = Teacher_student.objects.filter(people=self)
            if obj:
                arr = []
                for x in obj:
                    arr.append(x.teach.get_teacher_subject())
                return arr
        except:
            return "Fenn yoxdu"

    def get_teachers(self):
        try:
            obj = Teacher_student.objects.filter(people=self)
            if obj:
                arr = []
                for x in obj:
                    arr.append(x.teach)
                return arr[0].get_full_name()
        except:
            return "Müəllim seçilməyib"


    def get_teacher_obj(self):
        try:
            obj = Teacher_student.objects.filter(people=self)
            if obj:
                arr = []
                for x in obj:
                    arr.append(x.teach)
                return arr[0]
        except:
            return "Müəllim seçilməyib"

    def get_attendance(self):
        try:
            today = d.today().strftime("%Y-%m")
            y = int(d.today().strftime("%Y"))
            m = int(d.today().strftime("%m"))
            obj = Attendense.objects.filter(people=self,day__range=[today+'-1',today+'-'+str([x for x in calendar.monthrange(y,m)][-1])])
            arr = []
            for x in obj:
                arr.append([int(x.day.strftime('%d')),x.status,x.teach])
            return arr
        except:
            return []

    def prize(self):
        try:
            obj = Payment.objects.get(people=self)
            return obj
        except:
            return random.randint(10,100)

    prize.short_description = "Qiymət"
    prize.allow_tags = True

    def __str__(self):
        return "%s" % (self.full_name)

    def get_prize(self):
        try:
            obj = Payment.objects.get(people=self)
            return obj.prize
        except:
            return "0"



class PaymentHistory(models.Model):
    student = models.ForeignKey('Studend')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Ödəniş vaxtı')
    prize = models.IntegerField(null=True,blank=True, verbose_name='Qiymət (azn ilə)')

    class Meta:
        verbose_name = 'Əməliyyatlar'
        verbose_name_plural = 'Əməliyyatlar'
        ordering = ('-id',)

    def __str__(self):
        return "%s" % self.student.full_name

    def full_name(self):
        return "%s" % self.student.full_name

    full_name.short_description = "Ödəyən şəxsin A.S.A"
    full_name.allow_tags = True





class Subject(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Fənnlər'
        verbose_name = 'Fənn'

    def __str__(self):
        return "%s" % self.name

    def get_istisna_prize(self):
        try:
            new_object = PaymentException.objects.get(subj=self)
            return new_object.prize
        except:
            return False


"""
    ==============================================================================================
    Manager views Script >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    ==============================================================================================
"""

class Payment(models.Model):
    people = models.ForeignKey('Studend')
    teach = models.ForeignKey('MyUser')
    prize = models.FloatField(max_length=255,verbose_name='Ödəniş məbləği')
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(default=timezone.now)
    date = models.DateTimeField(default=timezone.now,verbose_name='Tarix')
    qalan_plan = models.IntegerField(default=0,verbose_name='Qalan dərs sayı')
    status = models.IntegerField(default=0,choices=PAYMENT_STATUS,verbose_name='Ödəniş statusuna')

    class Meta:
        verbose_name = "Ödəniş cədvəli"
        ordering = ('-id',)

    def __str__(self):
        return "%s" % (self.prize)

    def order_full_name(self):
        return "%s" % self.people.full_name

    order_full_name.short_description = "Sifarişçi"
    order_full_name.allow_tags = True

    def order_teacher_name(self):
        return "%s" % self.teach.get_full_name()

    order_teacher_name.short_description = "Müəllimin adı"
    order_teacher_name.allow_tags = True



class PaymentException(models.Model):
    prize = models.FloatField(default=0,verbose_name="Qiymət")
    filyal = models.ForeignKey('PandaBranch',null=True, blank=True, verbose_name="Filial")
    subj = models.ForeignKey('Subject',verbose_name='Fənnin adı')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Maaşın hesablanmasında istisna'
        verbose_name_plural = 'Maaşın hesablanmasında istisnalar'

    def __str__(self):
        return "%d" % self.prize

    def get_description(self):
        return "<p>Deməli siz Qiymət daxil edən zaman Həmin fənni keçən müəllimlərin maaşının hesablanması Hər plusa görə həmin qiymət qədər artacaq</p>"

    get_description.short_description = "İstifadə qaydası"
    get_description.allow_tags = True




"""
    #######################################################################################333
    Jurnal views scriming ____________________________________________________________________
    ###########################################################################################
"""

class Teacher(models.Model):
    teach = models.ForeignKey('MyUser')
    sub = models.ForeignKey('Subject')
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Müəllim'
        verbose_name_plural = 'Müəllimlər'

    def get_student_count(self):
        try:
            today = timezone.now().strftime("%Y-%m")
            y = int(timezone.now().strftime("%Y"))
            m = int(timezone.now().strftime("%m"))
            if Teacher_student.objects.filter(Q(teach=self.teach) & Q(people__testiq=True)).count() == 0:
                return "Şagirdi yoxdur"
            else:
                return Teacher_student.objects.filter(Q(teach=self.teach) & Q(people__testiq=True)).count()
        except:
            return "Şagirdi yoxdur"

  

    get_student_count.short_description = "Şagirdlərinin sayı"
    get_student_count.allow_tags = True

    def get_full_name(self):
        return "%s" % self.teach.get_full_name()

    get_full_name.short_description = "Müəllimin adı"
    get_full_name.allow_tags = True

    def get_subject(self):
        return self.sub.name
    get_subject.short_description = "Fənnin adı"
    get_subject.allow_tags = True


class JurnalArchive(models.Model):
    teach = models.ForeignKey('MyUser')
    data = models.TextField(default="")
    month = models.CharField(verbose_name="Ayliq Tarix",max_length=255)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Arxiv Jurnal'
        verbose_name_plural = 'Arxiv Jurnallar'

    def __str__(self):
        return self.teacher.get_full_name()

    def get_teacher_name(self):
        return self.teach.get_full_name()

    get_teacher_name.short_description = "Müəllimin adı"
    get_teacher_name.allow_tags = True




class Teacher_student(models.Model):
    teach = models.ForeignKey('MyUser')
    people = models.ForeignKey('Studend')
    group = models.CharField(max_length=200,null=True,blank=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Müəllimin şagirdi'
        verbose_name_plural = 'Müəllimin şagirdi'

    def __str__(self):
        return "%s %s" % (self.teach.get_full_name(),self.people.full_name)


class Teacher_lesson(models.Model):
    teach = models.ForeignKey('MyUser')

    class Meta:
        verbose_name = 'Müəllimin dərsi'
        verbose_name_plural = 'Müəllimin dərsləri'


class RelationDateLesson(models.Model):
    object = models.ForeignKey('Teacher_lesson')
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Dərs'
        verbose_name_plural = 'Dərslər'



class Attendense(models.Model):
    people = models.ForeignKey('Studend')
    teach = models.ForeignKey('MyUser')
    take_part = models.BooleanField(default=False)
    day = models.DateField(null=True,blank=True,verbose_name="iştirak etdiyi gün")
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=ATTENDANCE,null=True,blank=True)

    class Meta:
        verbose_name = 'Davamiyyət cədvəli'
        verbose_name_plural = 'Davamiyyət cədvəli'

    def people_full_name(self):
        return "%s" % self.people.full_name

    people_full_name.short_description = "Tələbənin adı"
    people_full_name.allow_tags = True

    def order_teacher_name(self):
        return "%s" % self.teach.get_full_name()

    order_teacher_name.short_description = "Müəllimin adı"
    order_teacher_name.allow_tags = True

"""
    This is System into places
"""
class PandaBranch(models.Model):
    name = models.CharField(max_length=255,verbose_name="Filialın adı")
    slug = models.SlugField(verbose_name="Slug", blank=True, null=True)
    status = models.BooleanField(default=True,verbose_name="Sistemdə görünməyi")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Şöbə'
        verbose_name_plural = 'Şöbələr'

    def __str__(self):
        return "%s" % self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(PandaBranch, self).save(*args, **kwargs)



# class DeletedStudent(models.Model):
#     student = models.ForeignKey('Studend')
#     date = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.student.full_name



"""
    This is just a security ___________________________________________________________________
    ###########################################################################################
    ###########################################################################################
"""

class AdminPanelUrl(models.Model):
    key = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Lazimsiz'
        verbose_name = 'Lazimsiz'

    def __str__(self):
        return self.key

class AllowedIpAddress(models.Model):
    ip = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    failed_login = models.IntegerField(default=0)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'İcazə verilmiş cihazlar'
        verbose_name_plural = 'Təhlükəsizlik'

    def __str__(self):
        return "%s" % self.ip

    def get_ip(self):
        return self.ip.split(',')[0]

    def get_platform(self):
        if 'android' in self.address.lower() and 'linux' in self.address.lower():
            return 'Android'
        elif 'windows' in self.address.lower():
            return 'Windows'
        elif 'linux' in self.address.lower():
            return 'Linux'
        elif 'macintosh' in self.address.lower():
            return 'MacBook'
        elif 'iphone' in self.address.lower():
            return 'Iphone'
        elif 'ipad' in self.address.lower():
            return 'Ipad'
        else:
            return 'Black Berry'

    def get_device(self):
        if 'mobile' in self.address.lower():
            return 'Telefon'
        else:
            return 'Komputer'


