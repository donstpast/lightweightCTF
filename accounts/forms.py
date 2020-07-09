from django import forms
from django.contrib.auth.forms import AuthenticationForm
from . import models

class RegisterForm(forms.Form) :
	username = forms.CharField(max_length=250, label="用户名称")
	email = forms.EmailField(max_length=250, label="电子邮箱", widget=forms.TextInput(attrs={'type':'email'}))
	teamname = forms.CharField(max_length=250, label="队伍名称")
	password = forms.CharField(max_length=250, min_length=8, label="登录密码", widget=forms.TextInput(attrs={'type':'password'}))

	class Meta :
		model = models.Teams
		fields = ["teamname","email"]

class LoginForm(AuthenticationForm) :
	username = forms.CharField(max_length=50, label="用户名称")
	password = forms.CharField(max_length=250, min_length=8, label="登录密码", widget=forms.TextInput(attrs={'type':'password'}))

class UpdateTeamUserDetails(forms.ModelForm) :
	job = forms.CharField(max_length=250, label="职位", required=False)
	company = forms.CharField(max_length=250, label="组织", required=False)

	class Meta :
		model = models.Teams
		fields = ["job","company"]
