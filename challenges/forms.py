from django import forms
from . import models

category_list = [
	('Web','Web'),
	('Cryptography','密码学'),
	('Stegnography','杂项'),
	('Reverse Engineering','逆向工程'),
	('Pwning','PWN'),
	('Forensics','计算机取证'),
]

class AddChallengeForm(forms.ModelForm) :
	name = forms.CharField(max_length=250, label="题目名称 *", widget=forms.TextInput(attrs={'placeholder':'题目名称','class':'form-control'}))
	category = forms.CharField(widget=forms.Select(choices=category_list, attrs={'class':'form-control'}), label="题目类别 *")
	description = forms.CharField(max_length=1000, widget=forms.TextInput(attrs={'placeholder':'题目描述', 'class':'form-control','required':'false'}), label="题目描述 *", required=False)
	points = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="题目分值 *")
	file = forms.FileField(label="附加文件（若无则无需添加）", required=False)
	flag = forms.CharField(max_length=500, label="题目FLAG *", widget=forms.TextInput(attrs={'placeholder':'题目FLAG，格式:flag{xxxx}','class':'form-control'}))
	author = forms.CharField(max_length=250, label="题目作者 *", widget=forms.TextInput(attrs={'placeholder':'题目作者','class':'form-control'}))
	#solved_by = forms.CharField(max_length=250)

	class Meta :
		model = models.Challenges
		fields = ["name","category","description","points","file","flag","author"]
