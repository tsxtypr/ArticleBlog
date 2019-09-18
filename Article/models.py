from django.db import models
from ckeditor.fields import RichTextField


# Create your models here.
GENDER_LIST=(
    (1,'男'),
    (2,'女'),
)
class Author(models.Model):
    name=models.CharField(max_length=32)
    age=models.IntegerField()
    gender=models.IntegerField(choices=GENDER_LIST,default=1)
    email=models.CharField(max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        db_table='author'
        verbose_name='作者'
        verbose_name_plural=verbose_name

class Type(models.Model):
    name=models.CharField(max_length=32)
    description=models.TextField()

    def __str__(self):
        return self.name
    class Meta:
        db_table='type'
        verbose_name = '类型'
        verbose_name_plural = verbose_name


class Article(models.Model):
    title=models.CharField(max_length=32)
    date=models.DateField(auto_now=True)
    # content=models.TextField()
    content = RichTextField()
    # description=models.TextField()
    description=RichTextField()
    # upload——to 指定文件上传位置
    picture=models.ImageField(upload_to='images')
    recommend=models.IntegerField(default=0) #0代表不推荐  1代表推荐
    click=models.IntegerField(default=0)
    author=models.ForeignKey(to=Author,on_delete=models.SET_DEFAULT,default=1)
    type=models.ManyToManyField(to=Type)

    def __str__(self):
        return self.title

    class Meta:
        db_table='article'
        verbose_name = '文章'
        verbose_name_plural = verbose_name

class User(models.Model):
    username=models.CharField(max_length=32)
    password=models.CharField(max_length=50)
    class Meta:
        db_table='user'

