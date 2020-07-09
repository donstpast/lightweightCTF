from django.db import models
from django.contrib.auth.models import User


class TeamUser(User):
	"""
	团队成员models类
	username:用户名称（登录名称）
	email:电子邮件(联系方式)
	password:密码

	job:工作|职位
	company:公司|组织
	is_leader:是否是队长
	"""
	team = models.ForeignKey(to='Teams', on_delete=models.CASCADE, default="")
	job = models.CharField(max_length=100, null=True, default="")
	create_time = models.DateTimeField(auto_now_add=True)
	company = models.CharField(max_length=250, null=True, default="")
	is_leader = models.BooleanField(default=False)
	points = models.IntegerField(default=0)

class Teams(models.Model) :
	"""
	teamname:队伍名称
	email:电子邮件(联系方式)
	number:队伍当前人数
	points:分值
	"""
	teamname = models.CharField(max_length=250, primary_key=True)
	create_time = models.DateTimeField(auto_now_add=True)
	email = models.EmailField(max_length=250)
	number = models.IntegerField(default=0)
	points = models.IntegerField(default=0)
	# def __str__(self):
	# 	return slef.teamname
