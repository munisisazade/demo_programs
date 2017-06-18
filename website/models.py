from django.db import models
from school.options.tools import get_slider_photo_file_name, get_news_photo_file_name, \
    get_about_us_photo_file_name, get_user_profile_photo_file_name, slugify
from ckeditor.fields import RichTextField
from website.helper import VideoPreview


# Create your models here.





class Menu(models.Model):
    name = models.CharField(max_length=255, verbose_name='Adı')
    link = models.CharField(max_length=255, verbose_name='Əlaqəsi')
    status = models.BooleanField(default=True, verbose_name='Saytda görünməsi')
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Menu'
        verbose_name_plural = 'Menular'

    def __str__(self):
        return '%s' % self.name


class Slider(models.Model):
    title = models.CharField(max_length=255, verbose_name="Slider başlığı", null=True, blank=True)
    content = models.CharField(max_length=255, verbose_name="Kontenti", null=True, blank=True)
    button = models.BooleanField(default=False)
    photo = models.ImageField(upload_to=get_slider_photo_file_name)
    link = models.URLField(null=True, blank=True, verbose_name='Xeberin linki')
    status = models.BooleanField(default=True, verbose_name='Saytda görünməsi')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Slayd'
        verbose_name_plural = 'Slayder'

    def __str__(self):
        return "%s" % self.title

    def get_slider_picture(self):
        return '<img src="/media/%s" style="width: 189px;height: auto" alt="%s">' % (self.photo.name, self.title)

    get_slider_picture.short_description = "Slayder şəkli"
    get_slider_picture.allow_tags = True


class About_us(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextField(config_name='awesome_ckeditor', null=True, blank=True)
    status = models.BooleanField(default=True)
    video = models.CharField(max_length=255, null=True, blank=True)
    picture = models.ImageField(upload_to=get_about_us_photo_file_name, null=True, blank=True, verbose_name="Şəkil")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Haqqımızda'
        verbose_name_plural = 'Haqqımızda'

    def __str__(self):
        return "%s" % self.title

    def get_video_preview(self):
        if self.video:
            return VideoPreview(self.video[-11:])
        else:
            return False

    get_video_preview.short_description = "Videoya bax"
    get_video_preview.allow_tags = True


class Programs_Header(models.Model):
    title = models.CharField(max_length=255, verbose_name='Başlıq')
    content = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True, verbose_name='Sayta görünüşü')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Bizim programlar başlığı'
        verbose_name_plural = 'Bizim programlar başlığı'

    def __str__(self):
        return "%s" % self.title


class Sections(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Bölmə'
        verbose_name_plural = 'Bölmələr'

    def __str__(self):
        return "%s" % self.name


class News(models.Model):
    title = models.CharField(max_length=255, verbose_name='Başlıq')
    content = RichTextField(config_name='awesome_ckeditor', null=True, blank=True)
    cover_picture = models.ImageField(upload_to=get_news_photo_file_name, null=True, blank=True,
                                      verbose_name="Örtük şəkli")
    status = models.BooleanField(default=True, verbose_name='Sayta görünüşü')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Məqalə'
        verbose_name_plural = 'Məqalələr'

    def __str__(self):
        return "%s" % self.title


class Programs(News):
    class Meta:
        ordering = ('-id',)
        verbose_name = 'Proqram'
        verbose_name_plural = 'Proqramlar'

    def __str__(self):
        return "%s" % self.title


class Events(News):
    class Meta:
        ordering = ('-id',)
        verbose_name = 'Tədbir'
        verbose_name_plural = 'Tədbirlər'

    def __str__(self):
        return "%s" % self.title


class Multimedia(News):
    video = models.URLField(null=True, blank=True, verbose_name="Videonun linki")

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Multimediya'
        verbose_name_plural = 'Multimediya'

    def __str__(self):
        return "%s" % self.title


class Collective(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name="Ad Soyad")
    picture = models.ImageField(upload_to=get_user_profile_photo_file_name, null=True, blank=True)
    content = RichTextField(config_name='awesome_ckeditor', null=True, blank=True)
    status = models.BooleanField(default=True, verbose_name='Sayta görünüşü')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Multimediya'
        verbose_name_plural = 'Multimediya'

    def __str__(self):
        return "%s" % self.title


class Contact_us(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name="Başlığı")
    about = models.CharField(max_length=255, null=True, blank=True, verbose_name="Haqqında")
    phone_1 = models.CharField(max_length=100, null=True, blank=True, verbose_name="Telefon nömrəsi 1")
    phone_2 = models.CharField(max_length=100, null=True, blank=True, verbose_name="Telefon nömrəsi 2")
    phone_3 = models.CharField(max_length=100, null=True, blank=True, verbose_name="Telefon nömrəsi 3")
    email_1 = models.EmailField(null=True, blank=True, verbose_name="Email 1")
    email_2 = models.EmailField(null=True, blank=True, verbose_name="Email 2")
    email_3 = models.EmailField(null=True, blank=True, verbose_name="Email 3")

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Bizimlə Əlaqə'
        verbose_name_plural = 'Bizimlə Əlaqə'

    def __str__(self):
        return "%s" % self.title


class SocialLinks(models.Model):
    name = models.CharField(max_length=255, verbose_name='Adı')
    link = models.CharField(max_length=255, verbose_name='Linki')
    status = models.BooleanField(default=True, verbose_name='Saytda görünməsi')
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Sosial Link'
        verbose_name_plural = 'Sosial Linklər'

    def __str__(self):
        return '%s' % self.name


class VacancyMenu(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Vakansiya ərazi'
        verbose_name_plural = 'Vakansiya ərazilər'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(VacancyMenu, self).save(*args, **kwargs)


class Vacancy(News):
    country = models.ForeignKey('VacancyMenu',verbose_name="ərazi",null=True,blank=True)
    class Meta:
        ordering = ('id',)
        verbose_name = 'Vakansiya'
        verbose_name_plural = 'Vakansiyalar'

    def __str__(self):
        return "%s" % self.title


        # class Slider(models.Model):
        #     title = models.CharField(max_length=255,verbose_name="Slider başlığı",null=True,blank=True)
        #     content = models.CharField(max_length=255,verbose_name="Kontenti",null=True,blank=True)
        #     button = models.BooleanField(default=False)
        #     photo = models.ImageField(upload_to=get_slider_photo_file_name)
        #     link = models.URLField(null=True,blank=True,verbose_name='Xeberin linki')
        #
        #     def __str__(self):
        #         return "%s" % self.title
        #
        #
        #
        # class About_us(models.Model):
        #     title = models.CharField(max_length='Başlıq')
        #     pass
