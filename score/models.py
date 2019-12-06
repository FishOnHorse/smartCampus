from django.db import models
from users.models import Student,Subject
from django.utils import timezone
# Create your models here.

class Exam(models.Model):
    name = models.CharField(max_length=30, verbose_name="考试名称")

class Score(models.Model):
    owner = models.ForeignKey('users.Student',on_delete=models.CASCADE)
    subject = models.ForeignKey('users.Subject',on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField(verbose_name='分值')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='录入时间',db_index=True)
    is_final = models.BooleanField(default=False,verbose_name="是否期末考试")
    class Meta:
       #('add', 'change', 'delete', 'view')
        default_permissions = []
        permissions = [
            ("add_score", "添加成绩"),
            ("change_score", "修改成绩"),
            ("delete_score", "删除成绩"),
            ("view_score", "查看成绩"),
        ]