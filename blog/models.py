from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible    #装饰器用于兼容python2
import markdown
from django.utils.html import strip_tags

@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField(max_length=70)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    excerpt = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ForeignKey(Tag, blank=True, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 新增阅读量字段
    reads = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return self.title

    '''
    blog:detail：获取blog应用下的name=detail的函数（通过blog/urls.py设置的app_name='blog'确定）
    reverse函数会去解析这个视图函数对应的URL，并用相应的pk替换
    '''
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk' : self.pk})

    class Meta:
        ordering = ['-created']

    # 新增阅读量
    def read(self):
        self.reads += 1
        self.save(update_fields=['reads'])

    # 从文本摘取前 54 个字符赋给 excerpt
    def save(self, *args, **kwargs):
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)
