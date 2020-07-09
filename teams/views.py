from django.shortcuts import render
from accounts.models import TeamUser
from django.contrib.auth.decorators import login_required
from accounts.models import TeamUser, Teams
  
  
@login_required(login_url="/accounts/login/")
def teams(request) :
	"""
	该用户所在团队的所有成员的信息
	"""
	if not request.user.is_superuser:
		username = request.user.username
		user = TeamUser.objects.get(username=username)
		team_users = TeamUser.objects.filter(team=user.team)
		# print(user.team)
		return render(request, 'teams.html', {'team_users':team_users})
	else:
		superuser_info = '管理员您好，请访问管理后台!'
		return render(request, 'teams.html', {'superuser_info':superuser_info})
