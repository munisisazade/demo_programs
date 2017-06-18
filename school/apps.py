from django.apps import AppConfig


class SchoolConfig(AppConfig):
    name = 'school'
    verbose_name = 'Panda sisteminin idarə paneli'

    def ready(self):
        import school.signals
