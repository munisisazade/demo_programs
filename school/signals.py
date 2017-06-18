from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from school.models import Studend,Payment,Teacher,Subject
from django.contrib.auth import get_user_model
User = get_user_model()


@receiver(post_save,sender=Studend,dispatch_uid='student_search_by_full_name')
def student_search_by_full_name(sender,**kwargs):
    obj = kwargs.get('instance')
    if obj.testiq:
        try:
            Payment.objects.get(people=obj)
            pass
        except:
            pay = Payment(
                people=obj,
                teach=obj.get_teacher_obj(),
                prize=obj.money,
                status=1,
            )
            pay.save()

@receiver(post_save,sender=User,dispatch_uid='add_teacher_object')
def add_teacher_object(sender,**kwargs):
    obj = kwargs.get('instance')
    if obj.usertype == 1:
        try:
            Teacher.objects.get(teach=obj)
            pass
        except:
            teach = Teacher(
                teach=obj,
                sub=obj.subjects,
            )
            teach.save()
