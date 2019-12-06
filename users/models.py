from django.db import models
from django.contrib.auth.models import AbstractBaseUser,UserManager, PermissionsMixin,BaseUserManager
from django.utils import timezone

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, username = None, phone = None, password = None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username and not phone:
            raise ValueError('Users must have an username or phone')

        user = self.model(
            username = username,
            phone = phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, phone, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            phone,
            password=password,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user

class BaseUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name="身份证号",max_length=18, unique=True, primary_key=True)
    phone = models.CharField(verbose_name="手机号码", unique=True, max_length=15, null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone']

    class Meta:
        ordering = ('-username',)

    def __unicode__(self):
        return self.username

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_superuser

    def is_superuser(self):
        return self.is_superuser

class Department(models.Model):
    """
    学校/校区/年级/班级
    """
    name = models.CharField(max_length=30, verbose_name="机构名称")
    code = models.CharField(max_length=30, verbose_name="机构代码")
    super_department = models.ForeignKey('self',on_delete=models.CASCADE)


class Student(BaseUser):
    """
    学生模型
    """
    name = models.CharField(max_length=30, verbose_name="姓名")
    eid = models.CharField(max_length=30, verbose_name="学籍号")
    sex = models.CharField(max_length=30, null=True, verbose_name="性别", blank=True)
    school = models.CharField(max_length=30, null=True, blank=True, verbose_name="学校",db_index=True)
    campus = models.CharField(max_length=30, null=True, blank=True, verbose_name="校区",db_index=True)
    grade = models.CharField(max_length=30, null=True, blank=True, verbose_name="年级",db_index=True)
    student_class = models.CharField(max_length=30, null=True, blank=True, verbose_name="班级",db_index=True)
    province = models.CharField(max_length=30, null=True, blank=True, verbose_name="省份")
    city = models.CharField(max_length=30, null=True, blank=True, verbose_name="城市")
    district = models.CharField(max_length=30, null=True, blank=True, verbose_name="地区")
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间',db_index=True)

class Teacher(BaseUser):
    """
    学生模型
    """
    name = models.CharField(max_length=30, verbose_name="姓名")
    sex = models.CharField(max_length=30, null=True, verbose_name="性别", blank=True)
    school = models.CharField(max_length=30, null=True, blank=True, verbose_name="学校",db_index=True)
    campus = models.CharField(max_length=30, null=True, blank=True, verbose_name="校区",db_index=True)
    grade = models.CharField(max_length=30, null=True, blank=True, verbose_name="年级",db_index=True)
    study_class = models.CharField(max_length=30, null=True, blank=True, verbose_name="班级",db_index=True)
    province = models.CharField(max_length=30, null=True, blank=True, verbose_name="省份")
    city = models.CharField(max_length=30, null=True, blank=True, verbose_name="城市")
    district = models.CharField(max_length=30, null=True, blank=True, verbose_name="地区")
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间',db_index=True)

class Subject(models.Model):
    name = models.CharField(max_length=30, verbose_name="学科名称")

class Course(models.Model):
    """
    课程-任课老师关联表
    """
    teacher = models.ForeignKey('Teacher',on_delete=models.CASCADE,verbose_name="任课老师",db_index=True)
    subject = models.ForeignKey('Subject',on_delete=models.CASCADE,verbose_name="学科",db_index=True)
    teach_class = models.CharField(max_length=30, verbose_name="班级",db_index=True)
