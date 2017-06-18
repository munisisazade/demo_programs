from django.views.generic import View,DetailView
from school.models import AllowedIpAddress,PandaBranch,Teacher
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.shortcuts import redirect


class IpRestrictedForArea(View):
    """
        This decorator functions get user ip address and User agent
        After check request user ip and User agent on database
        If nothing found save this data and can access to this url
    """

    def get_context_data(self,**kwargs):
        context = super(IpRestrictedForArea, self).get_context_data(**kwargs)
        ip = self.request.META.get('HTTP_X_FORWARDED_FOR', 'ipsiyoxdu').replace(' ','').split(',')[0]
        address = self.request.META.get('HTTP_USER_AGENT', 'unvaniyoxdu')
        context['allow'] = True
        try:
            a = AllowedIpAddress.objects.get(ip=ip,address=address)
        except:
            new_user = AllowedIpAddress(ip=ip, address=address)
            new_user.save()
        try:
            context['userstatus'] = self.request.user.usertype
        except:
            pass
        return context


class BaseBranchView(View):
    def get_context_data(self, **kwargs):
        context = super(BaseBranchView, self).get_context_data(**kwargs)
        if self.request.user.usertype == 3:
            context['menu_show'] = True
        return context




class LoginRestrictedMixin(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRestrictedMixin, self).dispatch(*args, **kwargs)


class LoginAllowOnlyManagerAndAdministration(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.usertype == 2 or self.request.user.usertype == 3:
            return super(LoginAllowOnlyManagerAndAdministration, self).dispatch(*args, **kwargs)
        else:
            return redirect(reverse('dashboard'))



class AllowOnlyAdministrator(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.usertype == 3:
            return super(AllowOnlyAdministrator, self).dispatch(*args, **kwargs)
        else:
            return redirect(reverse('dashboard'))


class AllowOnlyTeacher(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.usertype == 1:
            return super(AllowOnlyTeacher, self).dispatch(*args, **kwargs)
        else:
            return redirect(reverse('dashboard'))



def InvalidLoginAttempts(request):
    """
    If user want to brute force attack to Login system
    This method prevent from this attack
    And User ip address block automatic
    :param request:
    :return:
    """
    ip = request.META.get('HTTP_X_FORWARDED_FOR', 'ipsiyoxdu')
    address = request.META.get('HTTP_USER_AGENT', 'unvaniyoxdu')
    try:
        log = AllowedIpAddress.objects.get(ip=ip, address=address)
        log.failed_login +=1
        log.save()
        if log.failed_login == 5:
            log.failed_login -= 5
            log.status = False
            log.save()
        print('%s %s' % ('STATUS','[PERMISSION DENIED]'))
    except:
        print('%s %s' % ('STATUS','[OK]'))



