from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.core.exceptions import ValidationError

class usermanager(BaseUserManager):
    def create_user(self, email, username, password=None):#,apssid=None):
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            #apssid=apssid,
            )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, username, password):#,apssid):
        #if not username.endswith('1'):
        #    raise ValidationError(
        #        ('%(username)s is not ended with 1'),
        #        params={'username': username},
        #        )
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            #apssid=apssid,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

""" The below function is important until you delete migrations"""

class User(AbstractBaseUser):
    MALE='M'
    FEMALE='F'
    OTHER='O'
    RATHER_NOT_SAY='R'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER,'Other'),
        (RATHER_NOT_SAY,'Rather_Not_Say')
    ]
    INTERN='I'
    EMPLOYE='E'
    EMPLOYEMENT_TYPE=[
        (INTERN,'Intern'),
        (EMPLOYE,'Employe')
    ]
    #apssid=models.CharField(max_length=23,blank=True,unique=True)
    email=models.EmailField(verbose_name='email',max_length=60,unique=True)
    username=models.CharField(max_length=30,unique=True)
    gender=models.CharField(max_length=6,choices=GENDER_CHOICES)
    photo=models.ImageField(upload_to='profile_photos/')
    phone = models.IntegerField(blank=True)
    date_joined=models.DateTimeField(verbose_name='date joined',auto_now_add=True)
    emergency_contact1_name=models.CharField(max_length=25,blank=True)
    emergency_contact1=models.IntegerField(blank=True)
    emergency_contact2_name=models.CharField(max_length=25,blank=True)
    emergency_contact2=models.IntegerField(blank=True)
    employee_type=models.CharField(max_length=25,blank=True,choices=EMPLOYEMENT_TYPE)
    first_name=models.CharField(max_length=30,blank=True)
    last_name=models.CharField(max_length=30,blank=True)
    last_login=models.DateTimeField(verbose_name='last login',auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser= models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = usermanager()

    def __str__(self):
        return self.email

	# For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True



class main(models.Model):
    OFFICE='OF'
    HOME='H'
    WORK_LOCATION=[
        (OFFICE,'Office'),
        (HOME,'Home')
    ]
    email=models.CharField(max_length=234)
    name=models.CharField(max_length=234,default='apss_employee')
    month=models.CharField(max_length=234,default=None,blank=True,null=True)
    week_no=models.CharField(max_length=234,default=None,blank=True,null=True)
    date=models.CharField(max_length=234,default=None,blank=True,null=True)
    day=models.CharField(max_length=23)
    lead_name=models.CharField(max_length=50,blank=True,null=True,default=None)
    today_work_details=models.TextField(max_length=1000,blank=True  ,null=True,default=None)
    project=models.CharField(max_length=237,blank=True,null=True,default=None)
    hours=models.CharField(max_length=67,blank=True  ,null=True,default=None)
    login=models.CharField(max_length=56,blank=True  ,null=True,default=None)
    logout=models.CharField(max_length=53,blank=True  ,null=True,default=None)
    worklocationlogin=models.CharField(max_length=53,blank=True,null=True,default=None,choices=WORK_LOCATION)
    worklocationlogout=models.CharField(max_length=53,blank=True  ,null=True,default=None,choices=WORK_LOCATION)
    loginipaddress=models.GenericIPAddressField(max_length=56,blank=True,null=True,default=None)
    logoutnipaddress=models.GenericIPAddressField(max_length=56,blank=True,null=True,default=None)

    def __str__(self):
        return self.email


class Otp(models.Model):
    email=models.CharField(max_length=60,blank=True)
    otp=models.CharField(max_length=11,blank=True)
    month=models.CharField(max_length=19,blank=True)
    year=models.CharField(max_length=19,blank=True)
    date=models.CharField(max_length=15,blank=True)
    time=models.CharField(max_length=34,blank=True)
    is_success=models.BooleanField(default=False)
    def __str__(self):
            return self.email
