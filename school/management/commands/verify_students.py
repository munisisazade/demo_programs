from django.core.management.base import BaseCommand
from school.models import Studend


class Command(BaseCommand):
    help = "This command automatically create sulg field all Tags model"

    def handle(self, *args, **options):
        print("Let's started ...")

        all_tag = Studend.objects.all()
        for slug in all_tag:
            slug.testiq = True
            slug.save()

        print("-- All tag objects create slug completed")

