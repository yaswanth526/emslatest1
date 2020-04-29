from django.contrib import admin
from django.urls import path,include
from app import views


app_name='ems'

urlpatterns = [
    path('register',views.register,name='register'),
    path('validateemail',views.validateemail,name='validateemail'),
    path('reset',views.reset,name='reset'),
    path('user_login',views.user_login,name='user_login'),
    path('enter_ems',views.enter_ems,name='enter'),
    path('entered/',views.entered,name='entered'),
    path('fill',views.fill,name='fill'),
    path('update',views.update,name='update'),
    path('detail',views.detail,name='detail'),
    path('emergency_detail',views.emergency_detail,name='emergency_detail'),
    path('timesheets',views.view_timesheet,name='timesheets'),
    path('user_logout',views.user_logout,name='user_logout'),
]
