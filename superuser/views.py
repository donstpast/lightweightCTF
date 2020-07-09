from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from challenges.models import Challenges
from challenges.forms import AddChallengeForm
from challenges.views import assignID
from .forms import ManageForm
from .models import Manage_Match

@login_required(login_url="/accounts/login/")
def index(request):
	return redirect("/superuser/match/manage")

@login_required(login_url="/accounts/login/")
def addchallenges(request) :
	"""
	管理员添加新的题目
	"""
	if request.user.is_superuser :
		if request.method == 'POST' :
			success = 0
			form = AddChallengeForm(request.POST, request.FILES)
			if form.is_valid() :
				success = 1
				print(request.FILES)
				if request.FILES :
					i = Challenges(file=request.FILES['file'],
						name=request.POST['name'],
						category=request.POST['category'],
						description=request.POST['description'],
						points=request.POST['points'],
						challenge_id=assignID(request.POST['name']),
						flag=request.POST['flag'],
						author=request.POST['author'])
					i.save()
				else :
					i = Challenges(
						name=request.POST['name'],
						category=request.POST['category'],
						description=request.POST['description'],
						points=request.POST['points'],
						challenge_id=assignID(request.POST['name']),
						flag=request.POST['flag'],
						author=request.POST['author'])
					i.save()
				return render(request, 'super-addchallenges.html', {'form':form,'success':success})
		else :
			form = AddChallengeForm()

		return render(request, 'super-addchallenges.html', {'form':form})

	else :
		return redirect("/")

@login_required(login_url="/accounts/login/")
def deletechallenges(request):
    """
    管理删除题目
    """
    if request.user.is_superuser:
        if request.method == 'POST':
            form = Challenges.objects.all()
            return render(request, "super-deletechallenges.html", {"form":form})
        else:
            if request.GET.get('id', None)==None:
                form = Challenges.objects.all()
                return render(request, "super-deletechallenges.html", {"form":form})
            else:
                try:
                    challenge_id = request.GET.get('id', None)
                    Challenges.objects.get(challenge_id=challenge_id).delete()
                    form = Challenges.objects.all()
                    success = "删除成功！"
                    return redirect("/superuser/challenge/delete")
                except Exception as e:
                    form = Challenges.objects.all()
                    error = "删除失败！"+str(e)
                    print(error)
                    return render(request, "super-deletechallenges.html", {"form":form,"error":error})
    else:
        return redirect("/")

def manage(request):
	"""
	管理员管理比赛views
	"""
	error = ""
	success = ""
	if request.user.is_superuser:
		if request.method == "POST":
			form = ManageForm(request.POST)
			if form.is_valid():
				ctf_name = form.cleaned_data.get("ctf_name")
				match_name = form.cleaned_data.get("match_name")
				first_blood = form.cleaned_data.get("first_blood")
				second_blood = form.cleaned_data.get("second_blood")
				third_blood = form.cleaned_data.get("third_blood")
				start_submit = form.cleaned_data.get("start_submit")
				team_max_number = form.cleaned_data.get("team_max_number")
				if Manage_Match.objects.count() == 0:
					m = Manage_Match(ctf_name=ctf_name, match_name=match_name, first_blood=first_blood, second_blood=second_blood, third_blood=third_blood, start_submit=start_submit, team_max_number=team_max_number)
					m.save()
					success = "添加成功！"
				else:
					m = Manage_Match.objects.first()
					m.ctf_name = ctf_name
					m.match_name = match_name
					m.first_blood = first_blood
					m.second_blood = second_blood
					m.third_blood = third_blood
					m.start_submit = start_submit
					m.team_max_number = team_max_number
					m.save()
					success = "修改成功！"
				return render(request, "super-managematch.html", {"success":success, 'form':form})
			else:
				error = "添加或者修改失败，数据非法！"
				return render(request, "super-managematch.html", {"error":error, 'form':form})
		else:
			m = Manage_Match.objects.first()
			try:
				values = {"ctf_name":m.ctf_name, "match_name":m.match_name, "team_max_number":m.team_max_number, "first_blood":m.first_blood, "second_blood":m.second_blood, "third_blood":m.third_blood,"start_submit":m.start_submit}
			except Exception as e:
				print(e)
				values = {"ctf_name":"CTF", "match_name":"CTF", "first_blood":0,"team_max_number":3, "second_blood":0, "third_blood":0,"start_submit":False}
		form = ManageForm(values)
		return render(request, "super-managematch.html", {"form":form})
	else:
		return redirect("/")
