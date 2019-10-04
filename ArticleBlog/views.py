from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from Article.models import *
from django.shortcuts import render
from django.core.paginator import Paginator
import json

def loginValid(func):
    def inner(request,*args,**kwargs):
        username=request.COOKIES.get('username')
        if username:
            return func(request,*args,**kwargs)
        else:
            return HttpResponseRedirect('/login/')
    return inner

def about(request):
    return render(request,'about.html')

# @loginValid
def index(request):
    article=Article.objects.order_by('date')[:6]
    recommend_article=Article.objects.filter(recommend=1).all()[:7]
    click_article=Article.objects.order_by('-click')[:12]
    return render(request,'index.html',locals())


def listpic(request):
    return render(request,'listpic.html')


def newslistpic(request,type,page=1):
    page=int(page)
    type=type
    article=Type.objects.get(name=type).article_set.order_by('-date')
    paginator=Paginator(article,6)
    page_obj=paginator.page(page)
    # 获得当前页
    current_page=page_obj.number
    start=current_page-3
    end = current_page + 2
    if start<1:
        start=0
        end=5
    if end>paginator.num_pages:
        end=paginator.num_pages
        start=end-5
    page_range=paginator.page_range[start:end]

    return render(request,'newslistpic.html',locals())

def base(request):
    return render(request,'base.html')

def articledetails(request,id):
    id=int(id)
    article=Article.objects.get(id=id)
    return render(request,'articledetails.html',locals())

def adddata(request):
    for i in range(100):
        article=Article()
        article.title='title_%s'%i
        article.date='date_%s'%i
        article.content='content_%s'%i
        article.description='description_%s'%i
        article.author=Author.objects.get(id=1)
        article.save()
        article.type.add(Type.objects.get(id=1))
        # article.save()

    return HttpResponse("增加数据")


import hashlib
def setpassword(password):
    md5=hashlib.md5()
    md5.update(password.encode())
    result=md5.hexdigest()
    return result

# --------------------------------------------------------------
# 公共部分
# 注册页面
def register(request):
    error=''
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        password2=request.POST.get('password2')
        user_type=request.POST.get("identify")
        print(username,email,password,password2,user_type)
        if username and email and password2 and password and user_type:
            user=User.objects.filter(email=email).first()
            if user:
                error = '该用户存在'
            else:
                if password2==password:
                    user=User()
                    user.username=username
                    user.password=setpassword(password)
                    user.email=email
                    user.user_type=int(user_type)
                    user.save()
                    return HttpResponseRedirect("/login/")
                else:
                    error='两次密码不一致'
        else:
            error='不能为空'
    return render(request,'register.html',locals())

# 登录页面
def login(request):
    error=''
    if request.method=='POST':
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        user_type=request.POST.get("identify")
        if username and email and password and user_type:
            user=User.objects.filter(username=username,email=email,user_type=int(user_type)).first()
            if user:
                check_pwd=User.objects.filter(password=setpassword(password)).first()
                if check_pwd:
                    print(user_type)
                    print(type(user_type))
                    if user_type=='1':
                        response=HttpResponseRedirect("/index/")
                    else:
                        response = HttpResponseRedirect("/admin_base/")
                    response.set_cookie('email',email)
                    response.set_cookie('username',username)
                    response.set_cookie('userid',user.id)
                    request.session['email']=email
                    return response
                else:
                    error='密码不存在'
            else:
                error="该用户不存在"
        else:
            error="不能为空"
    return render(request,'login.html',locals())

#登出
def logout(request):
    response=HttpResponseRedirect('/login/')
    response.delete_cookie('username')
    return response

# -----------------------------------------------------------
# 以上都是前端页面
# 父模板
def admin_base(request):
    return render(request,'admin_base.html')

# 主页面
def admin_index(request):
    return render(request,'admin_index.html')


# 全部文章页
def admin_all_article(request,page=1):
    articles=Article.objects.all()

    # 分页
    paginator=Paginator(articles,10)
    page_obj=paginator.page(page)

    page_num=page_obj.number
    start=page_num-3
    end=page_num+2
    if start<1:
        start=0
        end=start+5
    elif end>paginator.num_pages:
        end=paginator.num_pages
        start=end-5
    page_range=paginator.page_range[start:end]

    print(page_range)
    return render(request,'admin_all_article.html',locals())

# 增加文章页
def admin_add(request):
    if request.method=='POST':
        data=request.POST

        article=Article()
        article.title=data.get("title")
        article.date=data.get("date")
        article.content=data.get("content")
        article.description=data.get("description")
        article.recommend=data.get("recommend")
        article.picture=request.FILES.get("picture")
        article.save()
        author=data.get("author")
        if Author.objects.get(name=author):
            article.author =Author.objects.get(name=author)

        types = data.getlist("type")
        for obj in types:
            article.type.add(Type.objects.get(id=int(obj)))
            print(Type.objects.get(id=int(obj)))
        article.save()
    return render(request,'admin_add.html')