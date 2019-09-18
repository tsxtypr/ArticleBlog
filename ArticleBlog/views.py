from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from Article.models import *
from django.shortcuts import render
from django.core.paginator import Paginator
import json


def test(request):
    return HttpResponse('TEST')


"""
    path('about/', views.about),
    path('index/',views.index),
    path('listpic/',views.listpic),
    path('newslistpic/',views.newslistpic),
"""

def about(request):
    return render(request,'about.html')
def index(request):
    data=request.COOKIES
    print(data)
    article=Article.objects.order_by('date')[:6]
    recommend_article=Article.objects.filter(recommend=1).all()[:7]
    click_article=Article.objects.order_by('-click')[:12]
    return render(request,'index.html',locals())
def listpic(request):
    return render(request,'listpic.html')


def newslistpic(request,page=1):
    page=int(page)
    article=Article.objects.order_by('-date')
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
        article.save()

    return HttpResponse("增加数据")


def fytest(request):
    article=Article.objects.all().order_by('-date')
    # 先分页
    paginator=Paginator(article,5)
    # print(paginator.count)
    # print(paginator.page_range)
    # print(paginator.num_pages)

    # 定义一个当前页的对象
    page_obj=paginator.page(1)
    print(page_obj)
    # 输出当前页的所有内容
    for one in page_obj:
        print(one.content)

    # 当前页的页码
    # print(page_obj.number)

    # 是否有某一页
    # print(page_obj.has_next())
    # print(page_obj.has_other_pages())
    # print(page_obj.has_previous())

    # 前、后一页的页码
    # print(page_obj.next_page_number())
    # print(page_obj.previous_page_number())

    return HttpResponse("分页")

def formtest(request):
    # data=request.GET
    # title=data.get('user')
    # print(title)
    # article=Article.objects.filter(title__contains=title)
    # print(article)
    data=request.POST
    print(data.get('username'))
    print(data.get('password'))
    return render(request,'formtest.html',locals())


import hashlib
def setpassword(password):
    md5=hashlib.md5()
    md5.update(password.encode())
    result=md5.hexdigest()
    return result

from Article.forms import *
def register(request):
    before_form=Test()
    error=''
    if request.method=='POST':
        # 将post数据交给form表单
        data=Test(request.POST)
         # 判断此数据是否能够通过检验
        if data.is_valid():
            # 若通过检验，则将检验的数据拿到
            clean_data=data.cleaned_data

            # 获取想要的数据
            username=clean_data.get('name')
            password=clean_data.get('password')
            user=User()
            user.username=username
            user.password=setpassword(password)
            user.save()
            error='添加成功'
        else:
            error=data.errors
            print(error)
    # if request.method=='POST':
    #     username=request.POST.get('username')
    #     pwd=request.POST.get('password')
    #     # pwd2=request.POST.get('password2')
    #     print(username,pwd)
    #     if username and pwd:
    #         # if pwd2==pwd:
    #         user=User()
    #         user.username=username
    #         user.password=setpassword(pwd)
    #         user.save()
    return render(request,'register.html',locals())

def ajax_get(request):
    return render(request,'ajax_get.html',locals())
def ajax_get_data(request):
    result={'code':10000,'content':''}
    data = request.GET
    username=data.get('username')
    password=data.get('password')
    if username and password:
        user=User.objects.filter(username=username,password=password).first()
        if user:
            result['content'] = '登录成功'
        else:
            result['code'] = 10003
            result['content'] = '用户名或密码不正确'
    else:
        result['code']=10001
        result['content']='用户名或密码不能为空'

    return JsonResponse(result)

def ajax_post(request):
    return render(request,'ajax_post.html')
def ajax_post_data(request):
    result={'content':'登录成功'}
    data=request.POST
    username=data.get('username')
    password=data.get("password")
    print(username)
    print(password)
    return JsonResponse(result)

def checkuser(request):
    result={'code':10000,'content':''}
    username=request.GET.get('username')
    user=User.objects.filter(username=username).first()
    if user:
        result['content']='用户已存在'
        result['code']=10001
    else:
        result['content']='可用的用户'
        result['code'] = 10000
    return JsonResponse(result)


def login(request):
    if request.method=='POST':
        data=request.POST
        username=data.get('username')
        password=data.get('password')
        if username and password:
            print(username,password)
            user=User.objects.filter(username=username,password=setpassword(password)).first()
            print(user)
            if user:
                response=HttpResponseRedirect('/index/')
                response.set_cookie(key=username,value='pig')
                return response
    return render(request,'login.html')