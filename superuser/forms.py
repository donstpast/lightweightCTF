from django import forms
from . import models


start_submit_list = [
	(False,'关闭'),
	(True,'开启'),
]
class ManageForm(forms.Form) :
	ctf_name = forms.CharField(max_length=100, label="平台名称*", widget=forms.TextInput(attrs={'placeholder':'平台名称','class':'form-control'}))
	match_name = forms.CharField(max_length=100, label="比赛名称*", widget=forms.TextInput(attrs={'placeholder':'比赛名称','class':'form-control'}))
	team_max_number = forms.IntegerField(label="团队最大人数*", widget=forms.NumberInput(attrs={'class':'form-control'}))
	first_blood = forms.IntegerField(label="一血加分*", widget=forms.NumberInput(attrs={'class':'form-control'}))
	second_blood = forms.IntegerField(label="二血加分*", widget=forms.NumberInput(attrs={'class':'form-control'}))
	third_blood = forms.IntegerField(label="三血加分*", widget=forms.NumberInput(attrs={'class':'form-control'}))
	start_submit = forms.BooleanField(label="允许提交flag*", help_text='开启后允许提交flag', widget=forms.Select(choices=start_submit_list, attrs={'class':'form-control'}), required=False)
