from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import forms
from . import models
from superuser.models import Manage_Match
from accounts import models as accounts_models
import json

class PassInsideView() :
	name = ''
	challenge_id = ''
	category = ''
	description = ''
	points = ''
	file = ''
	flag = ''
	author = ''

	def __init__(self, name, challenge_id, category, description, points, file, flag, author) :
		self.name = name
		self.challenge_id = challenge_id
		self.category = category
		self.description = description
		self.points = points
		self.file = file
		self.flag = flag
		self.author = author
	def __str__(self):
		return self.challenge_id
def assignID(a) :
	return a.lower().replace(' ','_')

@login_required(login_url="/accounts/login/")
def index(request) :
	"""
	赛题首页
	"""
	template_name = 'challenges.html'
	context = dict()
	challenge = models.Challenges.objects.order_by("points")
	challenge_info_stego_object = list()#保存对应题目信息
	challenge_info_for_object = list()
	challenge_info_re_object = list()
	challenge_info_pwn_object = list()
	challenge_info_web_object = list()
	challenge_info_crypto_object = list()
	solved_challenges_by_user = list() #保存该队伍已解答题目
	for c in challenge :
		if c.category == 'Stegnography' :
			s = PassInsideView(c.name, assignID(c.name), c.category, c.description, c.points, c.file, c.flag, c.author)
			challenge_info_stego_object.append(s)
		elif c.category == 'Reverse Engineering' :
			re = PassInsideView(c.name, assignID(c.name), c.category, c.description, c.points, c.file, c.flag, c.author)
			challenge_info_re_object.append(re)
		elif c.category == 'Forensics' :
			f = PassInsideView(c.name, assignID(c.name), c.category, c.description, c.points, c.file, c.flag, c.author)
			challenge_info_for_object.append(f)
		elif c.category == 'Pwning' :
			p = PassInsideView(c.name, assignID(c.name), c.category, c.description, c.points, c.file, c.flag, c.author)
			challenge_info_pwn_object.append(p)
		elif c.category == 'Web' :
			w = PassInsideView(c.name, assignID(c.name), c.category, c.description, c.points, c.file, c.flag, c.author)
			challenge_info_web_object.append(w)
		elif c.category == 'Cryptography' :
			cy = PassInsideView(c.name, assignID(c.name), c.category, c.description, c.points, c.file, c.flag, c.author)
			challenge_info_crypto_object.append(cy)
	try :
		user_team = accounts_models.TeamUser.objects.get(username=request.user.username).team.teamname
		fc = models.ChallengesSolvedBy.objects.filter(user_team=user_team)
		for f in fc :
			solved_challenges_by_user.append(f.challenge_id)
	except Exception as e:
		print(e)

	return render(request, template_name,{'data_stego':challenge_info_stego_object,
		'data_for':challenge_info_for_object,
		'data_re':challenge_info_re_object,
		'data_pwn':challenge_info_pwn_object,
		'data_web':challenge_info_web_object,
		'data_crypto':challenge_info_crypto_object,
		'user_solved':solved_challenges_by_user})

@login_required(login_url="/accounts/login/")
def flagsubmit(request) :
	"""
	检查flag
	"""
	try:
		start_submit = Manage_Match.objects.first().start_submit
	except Exception as e:
		start_submit = False
	if start_submit:
		if request.method == 'POST' :
			flag_submit = '' #用户提交的flag
			flag_submit_id = ''
			x = ''
			for k in request.POST :
				if k == 'submit' :
					continue
				if k == 'csrfmiddlewaretoken' :
					continue
				else :
					x = k
			flag_submit = request.POST[x]
			flag_submit_id = x[:-5] # 如提交字段为web1_flag，则flag_submit_id=web1
		flag = models.Challenges.objects.get(challenge_id=flag_submit_id).flag #正确的flag
		points = models.Challenges.objects.get(challenge_id=flag_submit_id).points
		if flag == flag_submit and not request.user.is_superuser :
			user_team = accounts_models.TeamUser.objects.get(username=request.user.username).team.teamname
			#flag正确且当前登录用户非管理员
			#该题已解题人数
			count = models.ChallengesSolvedBy.objects.filter(challenge_id=flag_submit_id).count()
			#前三名加分值
			extra_points = 0
			try:
				if count == 0:
					extra_points = Manage_Match.objects.first().first_blood
				elif count == 1:
					extra_points = Manage_Match.objects.first().second_blood
				elif count == 2:
					extra_points = Manage_Match.objects.first().third_blood
			except:
				pass
			fr = models.ChallengesSolvedBy(challenge_id=flag_submit_id, user_name=request.user, user_team=user_team, points=points+extra_points)
			try :
				fc = models.ChallengesSolvedBy.objects.filter(user_team=user_team)
				obs = list()
				for k in fc :
					obs.append(k.challenge_id)
				print(obs)
				#判断是否已经提交过flag
				if flag_submit_id in obs :
					response = '<div id="flag_already"><p>请勿重复提交FLAG</p></div>'
				else :
					#正确提交flag后相关操作
					fr.save()

					initial_user_points = accounts_models.TeamUser.objects.get(username=request.user.username).points
					initial_team_points = accounts_models.TeamUser.objects.get(username=request.user.username).team.points
					updated_user_points = initial_user_points + points + extra_points
					updated_team_points = initial_team_points + points + extra_points
					accounts_models.TeamUser.objects.filter(username=request.user.username).update(points=updated_user_points)
					team = accounts_models.TeamUser.objects.filter(username=request.user.username)[0].team
					team.points=updated_team_points
					team.save()
					response = '<div id="flag_correct"><p>FLAG正确</p></div>'
			except Exception as e:
				print("index Exception:",e)
				fr.save()
				initial_user_points = accounts_models.TeamUser.objects.get(username=request.user.username).points
				initial_team_points = accounts_models.TeamUser.objects.get(username=request.user.username).team.points
				updated_user_points = initial_user_points + points
				updated_team_points = initial_team_points + points
				accounts_models.TeamUser.objects.filter(username=request.user.username).update(points=updated_user_points)
				team = accounts_models.TeamUser.objects.filter(username=request.user.username)[0].team
				team.points=updated_team_points
				team.save()
				response = '<div id="flag_correct"><p>FLAG正确</p></div>'
		elif request.user.is_superuser :
			if flag == flag_submit:
				response = '<div id="flag_already"><p>FLAG正确，但是没有计分（管理员）</p></div>'
			else:
				response = '<div id="flag_incorrect"><p>FLAG错误（管理员）</p></div>'
		else :
			response = '<div id="flag_incorrect"><p>FLAG错误</p></div>'
	else:
		response = '<div id="flag_incorrect"><p>不允许提交Flag</p></div>'
	return HttpResponse(response)

@login_required(login_url="/accounts/login/")
def addchallenges(request) :
	"""
	管理员添加新的题目
	"""
	if request.user.is_superuser :
		if request.method == 'POST' :
			success = 0
			form = forms.AddChallengeForm(request.POST, request.FILES)
			if form.is_valid() :
				success = 1
				print(request.FILES)
				if request.FILES :
					i = models.Challenges(file=request.FILES['file'],
						name=request.POST['name'],
						category=request.POST['category'],
						description=request.POST['description'],
						points=request.POST['points'],
						challenge_id=assignID(request.POST['name']),
						flag=request.POST['flag'],
						author=request.POST['author'])
					i.save()
				else :
					i = models.Challenges(
						name=request.POST['name'],
						category=request.POST['category'],
						description=request.POST['description'],
						points=request.POST['points'],
						challenge_id=assignID(request.POST['name']),
						flag=request.POST['flag'],
						author=request.POST['author'])
					i.save()
				return render(request, 'addchallenges.html', {'form':form,'success':success})
		else :
			form = forms.AddChallengeForm()

		return render(request, 'addchallenges.html', {'form':form})

	else :
		return redirect("/")


def get_rank(request):
	"""
	获取每道题解题情况views
	"""
	if request.method == 'GET':
		# pageSize = int(request.GET.get('pageSize'))
		# pageNumber = int(request.GET.get('pageNumber'))
		# sortName = request.GET.get('sortName')
		# sortOrder = request.GET.get('sortOrder')
		challenge_id = request.GET.get('challenge_id')
	total = models.ChallengesSolvedBy.objects.filter(challenge_id=challenge_id).count()
	  = models.ChallengesSolvedBy.objects.filter(challenge_id=challenge_id).order_by('create_time')
	# solveds = models.ChallengesSolvedBy.objects.filter(challenge_id=challenge_id).objects.order_by('-create_time')[(pageNumber-1)*pageSize:(pageNumber)*pageSize]
	rows = []
	data = {"total": total, "rows": rows}
	for solved in solveds:
		# rows.append({'username': solved.user_name, 'create_time': solved.create_time, 'points': solved.points})
		rows.append({'username': solved.user_name, 'user_team':solved.user_team, 'create_time': solved.create_time.strftime('%Y-%m-%d %H:%M:%S'), 'points': solved.points})
	return HttpResponse(json.dumps(data), content_type="application/json")
