from time import time
import calendar
from datetime import date


def get_user_profile_photo_file_name(instance, filename):
    return "profile/%s_%s" % (str(time()).replace('.', '_'), filename)

def get_slider_photo_file_name(instance, filename):
    return "slider/%s_%s" % (str(time()).replace('.', '_'), filename)

def get_news_photo_file_name(instance, filename):
    return "news/%s_%s" % (str(time()).replace('.', '_'), filename)

def get_about_us_photo_file_name(instance, filename):
    return "about-us/%s_%s" % (str(time()).replace('.', '_'), filename)


def attendance_status(arg):
    if arg == '+':
        return 1
    elif arg == '-':
        return 2
    else:
        return 3


def slugify(title):
    symbol_mapping = (
        (' ', '-'),
        ('.', '-'),
        (',', '-'),
        ('!', '-'),
        ('?', '-'),
        ("'", '-'),
        ('"', '-'),
        ('ə', 'e'),
        ('ı', 'i'),
        ('ö', 'o'),
        ('ğ', 'g'),
        ('ü', 'u'),
        ('ş', 's'),
        ('ç', 'c'),
    )

    title_url = title.strip().lower()

    for before, after in symbol_mapping:
        title_url = title_url.replace(before, after)

    return title_url


def get_last_day_of_month():
    year = int(date.today().strftime("%Y"))
    month = int(date.today().strftime("%m"))
    result = calendar.monthrange(year, month)[1]
    return result

VALID_IMAGE_FILETYPES = (
    '.jpg','.png','.tiff'
)

def parser(arr):
    student_ids = list(set([x[2] for x in arr]))
    last_arr = []
    for y in student_ids:
        new = {}
        for x in arr:
            if y == x[2]:
                if new.get('.foo'+str(x[2]),False):
                    new['.foo-'+str(x[2])] += [x]
                else:
                    new['.foo-'+str(x[2])] = [x]
        last_arr.append(new)
    return last_arr


GENDER = (
    (1,"Kişi"),
    (2,"Qadın")
)
POSITION = (
    (1,"Fənn Müəllimi"),
    (2,"Ibtidai sinif Müəllimi")
)

USERTYPES = (
    (1,"Müəllim"),
    (2,"Menecer"),
    (3,"Administrator")
)

PAYMENT_STATUS = (
    (1,"Gecikir"),
    (2,"Normal"),
    (3,"Vaxtinda")
)

ATTENDANCE = (
    (1,"plus"),
    (2,"minus"),
    (3,"icazəli"),
    (4,"çıxıb"),
)


"""
   50  --  12
   40  --  x
   x = (12 * 40) / 50
"""

months = ['Yanvar','Fevral','Mart','Aprel','May','İyun','İyul','Avqust','Sentyabr','Oktyabr','Noyabr','Dekabr']