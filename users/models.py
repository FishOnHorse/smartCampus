from django.db import models
from django.contrib.auth.models import AbstractBaseUser,UserManager, PermissionsMixin,BaseUserManager
from django.utils import timezone

# Create your models here.
class MyUserManager(BaseUserManager):
    """
    The default User Model is too crowd, we use Custom BaseUserManager instead
    """

    def create_user(self, username, password=None):
        """
        create a user
        :param username: username of new User
        :param password: password of new User
        :return: A BaseUser object
        """

        user = self.model(
            username=username,
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        """
        create a superuser, this is use for "python manage createsuperuser"
        :param username: name of new superuser
        :param password: password of new superuser
        :return: a BaseUser object with is_admin set to True
        """

        user = self.create_user(username, password)
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class BaseUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name="身份证号",max_length=18, unique=True, primary_key=True)
    phone = models.CharField(verbose_name="手机号码", unique=True, max_length=15, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ()

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
        return self.is_admin

    def is_superuser(self):
        return self.is_admin

class Department(models.Model):
    """
    学校/校区/年级/班级
    """
    name = models.CharField(max_length=30, verbose_name="机构名称")
    super_department = models.ForeignKey('self')

class Campus(models.Model):
    name = models.CharField(max_length=30, verbose_name="校区")


class Student(BaseUser):
    """
    学生模型
    """
    name = models.CharField(max_length=30, verbose_name="姓名")
    sex = models.CharField(max_length=30, null=True, verbose_name="性别", blank=True)
    grade = models.CharField(max_length=30, null=True, blank=True, verbose_name="学校",db_index=True)
    grade = models.CharField(max_length=30, null=True, blank=True, verbose_name="校区",db_index=True)
    grade = models.CharField(max_length=30, null=True, blank=True, verbose_name="年级",db_index=True)
    grade = models.CharField(max_length=30, null=True, blank=True, verbose_name="班级",db_index=True)
    birthday = models.DateField(null=True, blank=True, verbose_name="生日")
    province = models.CharField(max_length=30, null=True, blank=True, verbose_name="省份")
    city = models.CharField(max_length=30, null=True, blank=True, verbose_name="城市")
    district = models.CharField(max_length=30, null=True, blank=True, verbose_name="地区")
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间',db_index=True)