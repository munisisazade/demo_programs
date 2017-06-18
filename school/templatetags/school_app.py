from django import template

register = template.Library()


@register.filter
def find_usertype(usertype):
    if usertype == 1:
        return "Müəllim"
    elif usertype == 2:
        return "Menecer"
    else:
        return "Administrator"

@register.filter
def branch_status(obj):
    if obj.status:
        return "green"
    else:
        return "red"



@register.filter
def status(pay):
    if pay.people.qalan_ders < 3:
        return "red"
    elif pay.people.qalan_ders < pay.people.plan:
        return "yellow"
    else:
        return "green"


@register.filter
def check_type(arg):
    if arg[1] == 1:
        return "<i class='fa fa-plus'></i>"
    elif arg[1] == 2:
        return "<i class='fa fa-minus'></i>"
    elif arg[1] == 3:
        return "<i class='fa fa-info'></i>"
    else:
        return "<i class='fa fa-times' style='color:red'></i>"

@register.filter
def is_null(arg):
    if arg == 0:
        return ""
    else:
        return arg


@register.filter
def is_none(arg):
    if not arg:
        return "0,0"
    else:
        return arg


@register.filter
def get_image_path(arg):
    return '/media/' + str(arg)

@register.filter
def convert_int(arg):
    return int(arg)

@register.assignment_tag
def find_group(var,group):
    colors = ['','#6d63be','rgba(82, 181, 181, 0.72)','rgba(155, 142, 141, 0.93)','rgba(153, 255, 153, 0.72)','rgba(156, 215, 234, 0.72)','rgba(76, 54, 190, 0.72)','rgba(32, 45, 67, 0.72)','rgba(43, 34, 43, 0.72)','rgba(23, 42, 32, 0.72)','rgba(15, 25, 25, 0.72)','rgba(153, 255, 55, 0.72)''rgba(153, 25, 255, 0.72)''rgba(13, 255, 25, 0.72)''rgba(153, 55, 22, 0.72)','rgba(153, 255, 212, 0.72)']
    arr = []
    for x in var:
        arr.append(x.people.groups)
    group_list = list(set(arr))
    try:
        data_last = group_list.index(group)
    except:
        data_last = -1
    if data_last >= len(colors):
        data_last -= len(colors)
    return colors[data_last]
