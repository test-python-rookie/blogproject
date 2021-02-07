from django.shortcuts import render, get_object_or_404
from .models import Post, Category
import markdown
from comments.forms import CommentForm
import re
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

def index(request):
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={
        'title': '我的博客首页',
        'welcome': '欢迎访问我的博客首页！',
        'post_list': post_list
    })

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 阅读量+1
    post.read()
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        TocExtension(slugify=slugify),
        # 'markdown.extensions.toc',
                      ])
    post.body = md.convert(post.body)
    # 侧边栏自动生成目录
    post.toc = md.toc
    # 没有目录不显示
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''

    form = CommentForm()
    # 获取这篇文章下的全部评论
    comment_list = post.comment_set.all()
    # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
    context = {'post':post,
               'form':form,
               'comment_list':comment_list
               }
    return render(request, 'blog/detail.html', context=context)

def archives(request, year, month):
    post_list = Post.objects.filter(created__year=year,
                                    created__month=month
                                    )
    return render(request, 'blog/index.html', context={'post_list':post_list})

def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list':post_list})
