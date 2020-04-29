from django.shortcuts import render
from django.http  import HttpResponse,HttpResponseRedirect,Http404
from app.models import main,User
from app.forms import loginform,timesheetlogin,timesheetlogout
# Create your views here.
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
#from django.contrib.auth.models import User
from datetime import datetime
from django.contrib import messages
import socket
# Create your views here.

def ip():
    ip=socket.gethostbyname(socket.gethostname())
    return ip

def index(request):
    return render(request,'base.html')

def user_login(request):
    form=loginform()
    d=False
    if request.method=='POST':
        form=loginform(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user=authenticate(email=email,password=password)
            if user:
                if user.is_admin:
                    login(request,user)
                    return HttpResponseRedirect('choice')

                elif user.is_active:
                    login(request,user)
                    request.session['user_id']=user.id
                    dt=datetime.now()
                    day_name=dt.strftime('%A')
                    today_date=dt.strftime('%Y-%m-%d')
                    month=dt.strftime('%m')
                    week=dt.strftime('%W')
                    store=main.objects.filter(email=email,date=today_date)
                    if store:
                        request.session['main_id']=store[0].id
                        return HttpResponseRedirect('emsentered')
                    else:
                        store=main.objects.create(email=email,date=today_date,day=day_name,week_no=week,month=month)
                        ip_address = ip()
                        store.loginipaddress=ip_address
                        store.save()
                        request.session['main_id']=store.id
                    return HttpResponseRedirect('emsenter_ems')
            else:
                d=True

    return render(request,'login.html',{'form':form,'d':d})

@login_required
def enter_ems(request):
    id=request.session.get('user_id')
    user=User.objects.get(id=id)
    return render(request,'enter.html',{'user':user})

@login_required
def entered(request):
    main_id=request.session.get('main_id')
    store=main.objects.get(id=main_id)
    user_id=request.session.get('user_id')
    user=User.objects.get(id=user_id)
    return render(request,'entered.html',{'user':user,'store':store})

@login_required
def detail(request):
    user_id=request.session.get('user_id')
    user=User.objects.get(id=user_id)
    return render(request,'detail.html',{'user':user})

@login_required
def emergency_detail(request):
    user_id=request.session.get('user_id')
    user=User.objects.get(id=user_id)
    return render(request,'emergency_detail.html',{'user':user})

@login_required
def view_timesheet(request):
    main_id=request.session.get('main_id')
    store=main.objects.get(id=main_id)
    timesheets=main.objects.filter(email=store.email)
    return render(request,'timesheets.html',{'obj':timesheets})

@login_required
def fill(request):
    dt=datetime.now()
    today_date=dt.strftime('%Y-%m-%d')
    id=request.session.get('main_id')
    store=main.objects.get(id=id,date=today_date)
    form1=timesheetlogin()
    form2=timesheetlogout()
    d=True
    b=True
    c=True
    a=True
    tod=store.today_work_details
    pro=store.project
    if request.method=='POST' and 'timesheetloginbutton' in request.POST:
        form1=timesheetlogin(request.POST)
        if form1.is_valid():
            if store.login:
                d=False
                tod=store.today_work_details
                pro=store.project
            else:
                store.project=form1.cleaned_data['project']
                store.worklocationlogin=form1.cleaned_data['worklocationlogin']
                store.today_work_details=form1.cleaned_data['today_work_details']
                store.lead_name=form1.cleaned_data['lead_name']
                store.save()
                print(store.project)
                dt=datetime.now()
                logintime=dt.strftime('%X')
                store.login=logintime
                store.save()
                d=False
                c=False
                tod=store.today_work_details
                pro=store.project
        else:
            form1=timesheetlogin()
    elif request.method=='POST' and 'timesheetlogoutbutton' in request.POST:
        form2=timesheetlogout(request.POST)
        if form2.is_valid():
            store.worklocationlogout=form2.cleaned_data['worklocationlogout']
            dt=datetime.now()
            logout_time=dt.strftime('%X')
            if store.logout:
                b=False
            else:
                store.logout=logout_time
                today_work_details_updated=request.POST.get('today_work_details_updated')
                project_updated=request.POST.get('project_updated')
                store.today_work_details=today_work_details_updated
                store.project=project_updated
                ip_address = ip()
                store.logoutnipaddress=ip_address
                FMT = '%H:%M:%S'
                logintime=store.login
                workhours = datetime.strptime(logout_time, FMT) - datetime.strptime(logintime, FMT)
                store.hours=workhours
                store.save()
                b=False
                a=False
        else:
            form2=timesheetlogout()
    if store.project and store.login:
        d=False
        if store.logout:
            b=False
        else:
            b=True
    else:
        d=True

    return render(request,'fill.html',{'store':store,'form1':form1,'form2':form2,'d':d,'b':b,'c':c,'a':a,'tod':tod,'pro':pro})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

from app.forms import registration
def register(request):
    form=registration()
    d=False
    b=False
    if request.method=='POST':
        form=registration(request.POST,request.FILES)
        if form.is_valid():
            if form.cleaned_data['password']==request.POST.get('re_password'):
                fo=form.save()
                fo.set_password(fo.password)
                if 'photo' in request.FILES:
                    fo.photo=request.FILES['photo']
                print('successfully saved')
                fo.save()
                b=True
                #return HttpResponseRedirect(reverse('index'))
            else:
                d=True
    return render(request,'register.html',{'form':form,'d':d,'b':b})

from app.forms import updatephone
@login_required
def update(request):
    user_id=request.session.get('user_id')
    user=User.objects.get(id=user_id)
    form=updatephone()
    if request.method=='POST':
        form=updatephone(request.POST)
        if form.is_valid():
            d=form.cleaned_data['phone']
            user.phone=d
            user.save()
            return HttpResponseRedirect('emsentered')
    return render(request,'updatephone.html',{'form':form})
##########################################################################################################################################
'''FORGOT PASSWORD'''

import random
import string
from random import randrange
def randomString():
    """Generate a random string with the combination of lowercase and uppercase letters """
    numbers=string.digits
    letter=numbers#letters+numbers
    stringLength=randrange(6,10)
    return ''.join(random.choice(letter) for i in range(stringLength))

from app.forms import validateemailform,otpform
from django.core.mail import send_mail
from app.models import Otp
def validateemail(request):
    form1=validateemailform()
    d=False
    dt=datetime.now()
    today_date=dt.strftime('%Y-%m-%d')
    if request.method=='POST' and 'validateemailbutton' in request.POST:
        form1=validateemailform(request.POST)
        if form1.is_valid():
            email=form1.cleaned_data['email']
            validate=User.objects.filter(email=email)
            if validate:
                al=Otp.objects.filter(email=email,date=today_date)
                if al:
                    al.delete()
                    dt=datetime.now()
                    o=Otp.objects.create(email=email,otp=randomString(),month=dt.strftime('%m'),year=dt.strftime('%Y'),date=today_date,time=dt.strftime('%X'))
                    request.session['user_id']=validate[0].id
                    a=send_mail('EMS OTP','YOUR OTP IS '+ o.otp+'','emsappindia@gmail.com',[email])
                    d=False
                    return HttpResponseRedirect('emsreset')
                else:
                    dt=datetime.now()
                    o=Otp.objects.create(email=email,otp=randomString(),month=dt.strftime('%m'),year=dt.strftime('%Y'),date=today_date,time=dt.strftime('%X'))
                    request.session['user_id']=validate[0].id
                    a=send_mail('EMS OTP','YOUR OTP IS '+ o.otp+'','emsappindia@gmail.com',[email])
                    d=False
                    return HttpResponseRedirect('emsreset')
            else:
                d=True
    return render(request,'validateemail.html',{'form':form1,'d':d})


def reset(request):
    form=otpform()
    id=request.session.get('user_id')
    otpflag=False
    pasflag=False
    resetSuccess=False
    dt=datetime.now()
    today_date=dt.strftime('%Y-%m-%d')
    if request.method=='POST':
        form=otpform(request.POST)
        if form.is_valid():
            otp=form.cleaned_data['otp']
            user=User.objects.get(id=id)
            o=Otp.objects.filter(email=user.email,otp=otp,date=today_date)

            if o:
                p1=form.cleaned_data['password1']
                p2=form.cleaned_data['password2']
                if p1==p2:
                    o[0].is_success=True
                    o[0].save()
                    user=User.objects.get(id=id)
                    user.set_password(p1)
                    user.save()
                    a=send_mail('Password Reset','Your Password Changed successFully','emsappindia@gmail.com',[user.email])
                    print('Password Changed SuccessFully')
                    resetSuccess=True
                    #ol.delete()
                    #return HttpResponseRedirect(reverse('index'))
                else:
                    pasflag=True
            else:
                otpflag=True
    return render(request,'resetpassword.html',{'otpflag':otpflag,'pasflag':pasflag,'form':form,'resetSuccess':resetSuccess})
####################################################################################################################################
'''ADMIN PAGE'''

@login_required
def choiceview(request):
    d=None
    email_flag=None
    cemail=None
    cmonth=None
    cweek=None
    emails=User.objects.all()
    if request.method=='POST':
        email_flag=None
        d=None
        cemail=None
        cmonth=None
        cweek=None
        email=request.POST.get('email')
        all=main.objects.filter(email=email)
        print(email)
        month=request.POST.get('month')
        week=request.POST.get('week')
        emo='f'
        if month!="":
            d='fds'
            emo=main.objects.filter(email=email,month=month)
            cemail=email
            cmonth=month
            if week=="":
                print('week is not there')
            else:
                cweek=week
                emo=main.objects.filter(email=email,month=month,week_no=week)
        else:
            email_flag='True'
            emo=User.objects.get(email=email)
            cemail=emo.email
            print(emo.email,'ff')
        return render(request,'choices.html',context={'all':all,'ob':emo,'d':d,'email':emails,'email_flag':email_flag,'cemail':cemail,'cmonth':cmonth,'cweek':cweek})
    return render(request,'choices.html',{'email':emails,'d':d,'email_flag':email_flag,'cemail':cemail,'cmonth':cmonth,'cweek':cweek})


from django.http import JsonResponse

@login_required
def ajaxweek(request):
    month = request.GET.get('month', None)
    email=request.GET.get('email',None)
    print(month)
    cd=main.objects.filter(email=email,month=month)
    a=[]
    for i in cd:
        if i.week_no in a:
            pass
        else:
            a.append(i.week_no)
    print(a)
    data = {
        'a': a
    }
    return JsonResponse(data)

@login_required
def ajaxmonth(request):
    email = request.GET.get('email', None)
    print(email)
    cd=main.objects.filter(email=email)
    a=[]
    for i in cd:
        if i.month in a:
            pass
        else:
            a.append(i.month)
    print(a)
    data = {
        'a1': a
    }
    return JsonResponse(data)
################################################################################################################################################
