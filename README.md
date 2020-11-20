本项目是一个轻量级的CTF竞赛平台，常用功能完善。

#### 运行截图 :
赛题
<img src="readmeimg/赛题.png" width="100%">

提交flag
<img src="readmeimg/提交flag.png" width="100%">

查看每道题排名
<img src="readmeimg/查看每道题排名.png" width="100%">

总体排名
<img src="readmeimg/总体排名.png" width="100%">

团队内部排名
<img src="readmeimg/团队内部排名.png" width="100%">

后台管理
<img src="readmeimg/后台管理.png" width="100%">

添加题目
<img src="readmeimg/添加界面.png" width="100%">


#### 使用
###### 依赖
```
Python 3.6.9
Django 2.0
```

###### 安装Django2.0

```sh
$ sudo pip3 install django==2.0
```
###### 使用该平台

```sh
$ python3 manage.py makemigrations accounts challenges
$ python3 manage.py migrate #迁移
$ python3 manage.py createsuperuser #创建管理员
$ python3 manage.py runserver #运行服务
```
使用管理员账号登录可以访问Djano管理后台或者平台后台管理平台以及添加题目等等操作，参赛选手需要注册。
