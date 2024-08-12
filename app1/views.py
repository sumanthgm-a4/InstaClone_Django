from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from app1.models import *

# Create your views here.

def render_home(request):
    all = Post.objects.all()[::-1]
    if request.method == "POST":
        search = request.POST.get("search")
        if search:
            objs = Post.objects.filter(caption__icontains=search)
            print(objs[0].caption)
            return render(request, "index.html", {"all": objs})
        return render(request, "index.html", {"all": all})
    return render(request, "index.html", {"all": all})



@login_required(login_url="loginpage")
def render_post(request):
    if request.method == "POST":
        pic = request.FILES.get('pic')
        caption = request.POST.get('caption')
        print(pic)
        new_post = Post(user_obj=request.user, pic=pic, caption=caption)
        new_post.save()
        messages.success(request, "Successfully posted")
        return redirect("homepage")
    return render(request, "create.html")



def render_register(request):
    if request.method == "POST":
        uname = request.POST.get('uname')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        emailid = request.POST.get('emailid')
        pword = request.POST.get('pword')
        cpword = request.POST.get('cpword')
        if len(pword) < 8:
            messages.error(request, "Your password is too short")
            return redirect("registerpage")
        if cpword != pword:
            messages.error(request, "Passwords don't match")
            return redirect("registerpage")
        new_user = User(username=uname, email=emailid, first_name=fname, last_name=lname)
        new_user.set_password(pword)
        new_user.save()
        messages.success(request, f"@{uname} successfully registered")
        return redirect("loginpage")
    return render(request, "register.html")



def render_login(request):
    if request.method == "POST":
        username = request.POST.get("uname")
        password = request.POST.get("pword")
        if not User.objects.filter(username=username).exists():
            messages.warning(request, "Username doesn't exist, please register to continue")
            return redirect("registerpage")
        login_user = authenticate(request, username=username, password=password)
        if login_user:
            if login_user.is_superuser:
                login(request, login_user)
                return redirect("admin/")
            login(request, login_user)
            messages.success(request, "You are successfully logged in")
            return redirect("homepage")
        messages.error(request, "Please enter correct credentials")
        return redirect("loginpage")
    return render(request, "login.html")



def render_logout(request):
    logout(request)
    messages.success(request, "You are successfully logged out")
    return redirect("homepage")



def render_display(request, rid):
    obj = Post.objects.filter(id=rid)[0]
    if request.method == "POST":
        if request.user.username == obj.user_obj.username:
            pi = request.FILES.get("picture")
            print(pi)
            capt = request.POST.get("caption")
            print(obj.caption)
            print(capt)
            if pi:
                obj.pic = pi
                obj.caption = capt
                obj.save()
            else:
                obj.caption = capt
                obj.save()
            messages.success(request, "Successfully updated")
            return redirect("homepage")
        messages.error(request, f"Only @{obj.user_obj.username} can update this post")
        return redirect("homepage")
    return render(request, "single.html", {"obj": obj})



def render_delete(request, rid):
    obj = Post.objects.filter(id=rid)[0]
    print(obj)
    if request.user.username == obj.user_obj.username:
        obj.delete()
        messages.success(request, "Post deleted successfully")
        return redirect("homepage")
    messages.error(request, f"Only @{obj.user_obj.username} can delete this post")
    return redirect("homepage")



def render_profile(request, rid):
    pass



