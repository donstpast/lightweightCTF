from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name="home"),
	path('challenge/add', views.addchallenges, name="add"),
	path('challenge/delete', views.deletechallenges, name="delete"),
	path('match/manage', views.manage, name="manage"),
]
