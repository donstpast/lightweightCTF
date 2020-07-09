from django.db import models

class Manage_Match(models.Model):
    """
    ctf_name: 平台名称
    match_name：比赛名称
    team_max_number：团队最大人数
    first_blood：一血加分
    second_blood：二血加分
    third_blood：三血加分
    start_submit：是否允许开始提交
    """
    ctf_name = models.CharField(max_length=100, default="CTF")
    match_name = models.CharField(max_length=100, default="CTF")
    team_max_number = models.IntegerField(default=3)
    first_blood = models.IntegerField(default=0)
    second_blood = models.IntegerField(default=0)
    third_blood = models.IntegerField(default=0)
    start_submit = models.BooleanField(default=False)
