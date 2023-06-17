from django.shortcuts import redirect, render
from django.http import HttpResponse,HttpResponseRedirect
from category.models import Category
from .models import Blogs
from django.core.paginator import Paginator, EmptyPage, InvalidPage


# Create your views here.

def index(request):
    categories = Category.objects.all()
    blogs = Blogs.objects.all()
    
    #บทความใหม่
    latest = Blogs.objects.all().order_by('-pk')[:4]

    #บทความยอดนิยม
    popular_blog = Blogs.objects.all().order_by('-views')[:3]

    #บทความแนะนำ
    recomBlog = Blogs.objects.all().order_by('views')[:3]

    #pagination
    paginator = Paginator(blogs,3)
    try:
        page = int(request.GET.get('page','1'))
    except :
        page = 1

    try :
        blogPerpage = paginator.page(page)
    except (EmptyPage, InvalidPage):
        blogPerpage = paginator.page(paginator.num_pages)
        
    return render(request,"frontend/index.html",{'categories':categories,'blogs':blogPerpage,'latest':latest,'popularBlog':popular_blog,'recomBlog':recomBlog})
    

def blogDetail(request,id):
    categories = Category.objects.all()
    popular_blog = Blogs.objects.all().order_by('-views')[:3]
    recomBlog = Blogs.objects.all().order_by('views')[:3]
    singleBlog = Blogs.objects.get(id=id)
    singleBlog.views = singleBlog.views+1
    singleBlog.save()
    return render(request,"frontend/blogDetail.html",{"blog":singleBlog,'categories':categories,'popularBlog':popular_blog,'recomBlog':recomBlog})


#ย้อนกลับหน้าเดิมและส่ง id ไปด้วย
'''
def blogGB(request,id):
    previous_url = f'/blog/{id}'
    return HttpResponseRedirect(previous_url)
'''


def searchCategory(request,cat_id):
    blogs = Blogs.objects.filter(category_id=cat_id)
     #บทความยอดนิยม
    popular_blog = Blogs.objects.all().order_by('-views')[:3]
    #บทความแนะนำ
    recomBlog = Blogs.objects.all().order_by('views')[:3]
    categoryName = Category.objects.get(id=cat_id)
    categories = Category.objects.all()
    return render(request,"frontend/searchCategory.html",{"blogs":blogs,'categories':categories,'popularBlog':popular_blog,'recomBlog':recomBlog,'categoryName':categoryName})
    
def searchWriter(request,writer):
    blogs = Blogs.objects.filter(writer=writer)
    #บทความยอดนิยม
    popular_blog = Blogs.objects.all().order_by('-views')[:3]
    #บทความแนะนำ
    recomBlog = Blogs.objects.all().order_by('views')[:3]
    writer = blogs[0]
    categories = Category.objects.all()
    return render(request,"frontend/blogWriter.html",{"blogs":blogs,'categories':categories,'popularBlog':popular_blog,'recomBlog':recomBlog,'writerName':writer})