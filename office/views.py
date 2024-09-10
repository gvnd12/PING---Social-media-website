from django.shortcuts import render, redirect
from user.models import User, Post, Follow
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache

# Create your views here.
def admin_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username, password=password)
        if user is not None and user.is_superuser == 1:
            login(request, user)
            return redirect('users')
        else:
            return render(request, 'adminlogin.html', {'error':'Invalid Username or Password !'})
    return render(request, 'adminlogin.html')

def admin_logout(request):
    logout(request)
    return redirect('adminlogin')

def admin_home(request):
    admin_details=User.objects.get(id=request.user.id)
    return render(request, 'adminhompage.html', {'admin':admin_details})

def users(request):
    user_details=User.objects.filter(is_superuser=0)
    return render(request, 'users.html', {'users':user_details})

def create_user(request):
    if request.method=='POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        dob=request.POST.get('dob')
        mobile_no=request.POST.get('mobile_no')
        gender=request.POST.get('gender')
        if 'pic' in request.FILES and password==confirm_password:
            pic=request.FILES['pic']
            u=User.objects.create_user(profile_pic=pic, first_name=first_name, last_name=last_name, username=username, email=email, password=password, date_of_birth=dob, mobile_no=mobile_no, gender=gender)
            u.save()
            return redirect('users')
        elif password==confirm_password:
            u=User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password, date_of_birth=dob, mobile_no=mobile_no, gender=gender)
            u.save()
            return redirect('users')
        else:
            return render(request, 'adminusercreate.html', {'error':'Passwords do not match !'})
    return render(request, 'adminusercreate.html')

def create_post(request):
    if request.method=='POST':
        content=request.POST.get('postcont')
        image=request.FILES.get('postimg')
        if image is None:
            return render(request, 'admincreatepost.html', {'error':'Post cannot be empty!'})
        else:
            post=Post(user=request.user, Post_description=content, Post_image=image)
            post.save()
            return redirect('users')
    return render(request, 'admincreatepost.html')

def user_delete(request, user_id):
    user=User.objects.get(id=user_id)
    user.delete()
    return redirect('users')

def posts(request, user_id):
    user_posts=Post.objects.filter(user_id=user_id)
    user_details=User.objects.get(id=user_id)
    return render(request, 'posts.html', {'user':user_details, 'posts':user_posts})

def followers(request, user_id):
    userfollower=[]
    userfollower=Follow.objects.filter(following_id=user_id).values_list('follower_id', flat=True)
    followers=User.objects.filter(id__in=userfollower).all()
    return render(request, 'adminfollower.html', {'followers':followers})

def following(request, user_id):
    userfollowing=[]
    userfollowing=Follow.objects.filter(follower_id=user_id).values_list('following_id', flat=True)
    followings=User.objects.filter(id__in=userfollowing).all()
    return render(request, 'adminfollowing.html', {'followings':followings})

def post_delete(request, post_id):
    post=Post.objects.get(id=post_id)
    post.delete()
    return redirect('posts', post.user_id)