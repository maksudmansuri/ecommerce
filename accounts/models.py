from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor_uploader.fields import RichTextUploadingField
from rest_framework.authtoken.models import Token
from django.conf import settings

# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username,user_type, password=None):
        if not email:
            raise ValueError("User must have an Email Address")
        if not username:
            raise ValueError("User must have an username ")

        user = self.model(
                email=self.normalize_email(email),
                username=username,
                user_type = user_type
            )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
                email=self.normalize_email(email),
                password=password,
                username=username,
            )
        # user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser): 
    email = models.EmailField(verbose_name="email", max_length=254, unique=True)
    username = models.CharField(max_length=254,unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="date joined" ,auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # first_name = models.CharField(max_length=254)
    # last_name = models.CharField(max_length=254)
    user_type_data=((1,"Admin"),(2,"Client"),(3,"Customer"))
    user_type=models.CharField(choices=user_type_data,max_length=10)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    objects = MyAccountManager()

    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True    

class Admin(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Client(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=250,default="",null=True)
    last_name=models.CharField(max_length=250,default="",null=True)
    dob=models.DateField(blank=True,null=True)
    address=models.CharField(max_length=50,blank=True,null=True)
    city=models.CharField(max_length=50,blank=True,null=True)
    state=models.CharField(max_length=50,blank=True,null=True)
    country=models.CharField(max_length=50,blank=True,null=True)
    mobile=models.CharField(max_length=50,blank=True,null=True)
    # qualification=models.CharField(max_length=50,blank=True,null=True)
    # specialist=models.CharField(max_length=50,blank=True,null=True)
    # instructor_photo=models.FileField(upload_to="instructor/profile",null=True)
    # about=RichTextUploadingField(blank=True,null=True)
    # is_appiled=models.NullBooleanField(blank=True,default=False)
    # is_verified=models.NullBooleanField(blank=True,null=True,default=False)
    # resume=models.FileField(upload_to="instructor/resume", max_length=250,blank=True,null=True)
    # experience=models.CharField(max_length=50,blank=True,null=True)
    # working_with=models.CharField(max_length=50,blank=True,null=True)
    # website=models.URLField(max_length=200,blank=True,null=True)
    # linkdin=models.URLField(max_length=200,blank=True,null=True)
    gender=models.CharField(max_length=200,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    objects=models.Manager()
    
    def __str__(self):
        return self.first_name + last_name

class Customer(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    fisrt_name=models.CharField(max_length=250,blank=True,null=True)
    last_name=models.CharField(max_length=250,blank=True,null=True)
    address=models.CharField(max_length=500,blank=True,null=True)
    city=models.CharField(max_length=250,blank=True,null=True)
    state=models.CharField(max_length=250,blank=True,null=True)
    country=models.CharField(max_length=250,blank=True,null=True)
    # qualification =models.CharField(max_length=250,blank=True,null=True)
    dob=models.DateField(blank=True,null=True)
    phone=models.CharField(max_length=250,blank=True,null=True)
    photo=models.FileField(upload_to="student_lms/profile/images",blank=True,null=True)
    gender=models.CharField(max_length=255,null=True)
    # is_appiled=models.NullBooleanField(blank=True,null=True,default=False)
    # is_verified=models.NullBooleanField(blank=True,null=True,default=False)
    # session_start=models.DateField(null=True)
    # session_end=models.DateField(null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            Admin.objects.create(admin=instance)
        if instance.user_type==2:
            Client.objects.create(admin=instance)
        if instance.user_type==3:
            Customer.objects.create(admin=instance)
            # Students.objects.create(admin=instance,course_id=Courses.objects.get(id=1),session_start_year="2020-01-01",session_end_year="2021-01-01",address="",profile_pic="",gender="")

@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.admin.save()
    if instance.user_type==2:
        instance.client.save()
    if instance.user_type==3:
        instance.customer.save()
