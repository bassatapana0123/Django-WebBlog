from django.shortcuts import render,redirect
from blogs.models import Blogs
from category.models import Category
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.core.files.storage import FileSystemStorage #upload image by FileSystemStorage
from django.contrib import messages


# Create your views here.

@login_required(login_url="member")
def panal(request):
    writer = auth.get_user(request)
    blogs = Blogs.objects.filter(writer=writer)
    blogCount = blogs.count()
    total = Blogs.objects.filter(writer=writer).aggregate(Sum("views"))
    return render(request,"backend/index.html",{"blogs":blogs,'writer':writer,'blogCount':blogCount,'total':total})

@login_required(login_url="member")
def displayForm(request):
    writer = auth.get_user(request)
    blogs = Blogs.objects.filter(writer=writer)
    blogCount = blogs.count()
    total = Blogs.objects.filter(writer=writer).aggregate(Sum("views"))
    categories = Category.objects.all()
    return render(request,"backend/blogForm.html",{"blogs":blogs,'writer':writer,'blogCount':blogCount,'total':total,'categories':categories})

@login_required(login_url="member")
def insertData(request):
    if request.method == "POST" and request.FILES["image"]:
        datafile = request.FILES["image"]
        #รับค่าจาก Form
        name = request.POST["name"]
        category = request.POST["category"]
        description = request.POST["description"]
        content = request.POST["content"]
        writer = auth.get_user(request)

        if str(datafile.content_type).startswith("image"):
            #อัพโหลด
            fs = FileSystemStorage()
            image_url = "blogImages/"+datafile.name
            filename = fs.save(image_url,datafile)
            #บันทึกข้อมูลบทความ
            blog = Blogs(name = name,category_id = category,description = description,content = content,writer = writer,image = image_url)
            blog.save()
            messages.info(request,"บันทึกข้อมูลเรียบร้อย")
            return redirect("displayForm")
        else:
            messages.info(request,"ไฟล์ที่อัพโหลดไม่รองรับ")
            return redirect("displayForm")

@login_required(login_url="member")
def deleteData(request,id):

    blog=Blogs.objects.get(id=id)

    #ลบภาพปกของบทความ
    fs=FileSystemStorage()
    fs.delete(str(blog.image))

    #ลบข้อมูลออกจากฐานข้อมูล
    blog.delete()
    return redirect('panel')

@login_required(login_url="member")
def editData(request,id):
    #ข้อมูลพื้นฐาน
    writer = auth.get_user(request)
    blogs = Blogs.objects.filter(writer=writer)
    blogCount = blogs.count()
    total = Blogs.objects.filter(writer=writer).aggregate(Sum("views"))
    categories = Category.objects.all()

    blogEdit = Blogs.objects.get(id=id)
    return render(request,"backend/editForm.html",{"blogEdit":blogEdit,'writer':writer,'blogCount':blogCount,'total':total,'categories':categories})

@login_required(login_url="member")
def updateData(request,id):
    try:
        if request.method == "POST":
            #ดึงข้อมูลบทความเดิมที่ต้องการแก้ไขมาใช้งาน
            blog = Blogs.objects.get(id=id)
            
            #รับค่าจาก Form
            name = request.POST["name"]
            category = request.POST["category"]
            description = request.POST["description"]
            content = request.POST["content"]
            
            #อัพเดทข้อมูล
            blog.name = name
            blog.category_id = category
            blog.description = description
            blog.content = content
            blog.save()

        #Update ภาพปก
        if request.FILES["image"]:
            datafile = request.FILES["image"]
            if str(datafile.content_type).startswith("image"):
                #ลบภาพจริงของบทความออกไปก่อน
                fs=FileSystemStorage()
                fs.delete(str(blog.image))

                #แทนที่ด้วยภาพใหม่ 
                image_url = "blogImages/"+datafile.name
                filename = fs.save(image_url,datafile)
                blog.image = image_url
                blog.save()
        return redirect("panel")
    except:
        return redirect("panel")