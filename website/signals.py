from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from website.models import News,Programs
from django.conf import settings
import os

from PIL import Image


@receiver(post_save,sender=News,dispatch_uid='crop_imag_task')
def crop_image_task(sender,**kwargs):
    obj = kwargs.get('instance')
    created = kwargs.get('created')
    if created:
        file = Image.open(os.path.join(settings.MEDIA_ROOT,obj.cover_picture))
        new_file = file.resize((223, 137), Image.ANTIALIAS)
        new_file.save('/resize/%s' % obj.cover_picture.name,quality=100)



@receiver(post_save,sender=Programs,dispatch_uid='crop_imag_task_program')
def crop_image_task_progrm(sender,**kwargs):
    obj = kwargs.get('instance')
    file = Image.open(os.path.join(settings.MEDIA_ROOT,obj.cover_picture))
    new_file = file.resize((223, 137), Image.ANTIALIAS)
    new_file.save('/resize/%s' % obj.cover_picture.name,quality=100)