from django.shortcuts import render, redirect,get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from .models import User, Post, Like, Follow, Notification, Message, Comment, Pings, PingReply
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.dateformat import format
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import datetime
from PIL import ImageFile
# Create your views here.
@never_cache
def user_registration(request):
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

        allusers=User.objects.all()
        mobile_no_validator=RegexValidator(regex=r'^\+?1?\d{9,15}$',message="Phone number must contain minimum 10 digits !")

        for user in allusers:
            if user.username==username:
                return render(request, 'registration.html', {'usernameerror':'Username already taken !'})
            else:
                continue
        
        try:
            mobile_no_validator(mobile_no)
        except ValidationError as e:
            return render(request, 'registration.html', {'mobileerror': e.message})
        
        if 'pic' in request.FILES and password==confirm_password:
            pic=request.FILES['pic']
            u=User.objects.create_user(profile_pic=pic, first_name=first_name, last_name=last_name, username=username, email=email, password=password, date_of_birth=dob, mobile_no=mobile_no, gender=gender)
            u.save()
            return redirect('login')
        elif password==confirm_password:
            u=User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password, date_of_birth=dob, mobile_no=mobile_no, gender=gender)
            u.save()
            return redirect('login')
        else:
            return render(request, 'registration.html', {'passworderror':'Passwords do not match !'})
    return render(request, 'registration.html')

@never_cache
def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username, password=password)
        if user is not None and user.is_superuser == 0:
            login(request, user)
            return redirect('feed')
        else:
            return render(request, 'login.html', {'login_error':'Invalid Username or Password !'})
    return render(request, 'login.html')

@never_cache
def user_logout(request):
    logout(request)
    return redirect('login')

@never_cache
def user_post(request):
    if request.method=='POST':
        content=request.POST.get('postcont')
        image=request.FILES.get('postimg')
        if image is None:
            return render(request, 'post.html', {'error':'Post cannot be empty!'})
        else:
            post=Post(user=request.user, Post_description=content, Post_image=image)
            post.save()
            return redirect('profile')
    return render(request, 'post.html')

@never_cache
def profile(request):
    user_details=User.objects.get(id=request.user.id)
    post_details = Post.objects.filter(user_id=request.user.id).order_by('-created_at')
    all_comments=request.session.get('comment')
    if all_comments:
        del request.session['comment']
        return render(request, 'profilepage.html', {'user':user_details, 'post':post_details, 'comments':all_comments})
    return render(request, 'profilepage.html', {'user':user_details, 'post':post_details})

@login_required
def feed(request):
    following=Follow.objects.filter(follower_id=request.user.id).values_list('following_id', flat=True)
    posts=Post.objects.filter(user_id__in=following).all().order_by('-created_at')
    notifications = Notification.objects.filter(user=request.user, read=False).all()
    liked_posts=[]
    liked_posts = request.user.user_likes.values_list('post_id', flat=True)
    allping=Pings.objects.filter(user__in=list(following) + [request.user]).order_by('-created_at')
    return render(request, 'feed.html', {'posts':posts, 'liked_posts':liked_posts, 'notifications':notifications, 'allping':allping})

@login_required
def edit_profile(request, userid):
    user_details=User.objects.get(id=userid)
    if request.method=='POST':
        username=request.POST.get('username')
        mobile=request.POST.get('mobile_no')
        privacy=request.POST.get('privacy')
        profile_pic=request.FILES.get('profilepic')
        
        mobile_no_validator=RegexValidator(regex=r'^\+?1?\d{9,15}$',message="Invalid phone number !")
        try:
            mobile_no_validator(mobile)
        except ValidationError as e:
            return render(request, 'edit_profile.html', {'mobileerror': e.message})
        
        
        user_details.username=username
        user_details.mobile_no=mobile
        if privacy=='on':
            user_details.account_privacy='Private'
        else:
            user_details.account_privacy='Public'
        if profile_pic:
            user_details.profile_pic=profile_pic
        user_details.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('profile')
    return render(request, 'edit_profile.html', {'user':user_details})

@never_cache
def like(request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if created:
            notification = Notification.objects.create(user_id=post.user_id, content=f'{request.user.username} liked your post!', post=post)
            likecount = Like.objects.filter(post=post).count()
            likes={'msg':"Unlike", 'count':likecount}
        if not created:
            like.delete()
            likecount = Like.objects.filter(post=post).count()
            likes={'msg':'Like', 'count':likecount}
        return JsonResponse(likes)

@never_cache
def user_comment(request, post_id):
    if request.method=='POST':
        post=Post.objects.get(id=post_id)
        content=request.POST.get('comment')
        comment = Comment.objects.create(post=post, user=request.user, content=content)
        if post.user!=request.user:
            notification= Notification.objects.create(user=post.user, post=post, content=f'{request.user.username} commented on your post!')
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            comments={'sender': request.user.username,
                    'senderid': request.user.id,
                    'content': comment.content,
                    'created_at': comment.created_at.date()
                    }
            return JsonResponse(comments)

@never_cache
def user_search(request):
    if request.method=='POST':
        search=request.POST.get('search')
        searchusers=User.objects.filter(username__contains=search).all().exclude(username=request.user.username).exclude(is_superuser=1)
        return render(request, 'searchfind.html', {'searchusers':searchusers, 'searchinput':search})

@never_cache
def searchprofile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user==request.user:
        return redirect('profile')
    else:
        follows=Follow.objects.filter(following_id=user_id).values_list('following_id', flat=True)
        post=Post.objects.filter(user_id=user.id).order_by('-created_at')
        is_following=Follow.objects.filter(follower=request.user, following=user).exists()
        liked_posts=[]
        liked_posts = request.user.user_likes.values_list('post_id', flat=True)
        all_comments=request.session.get('comment')
        if all_comments:
            del request.session['comment']
            return render(request, 'searchprofile.html', {'searchuser':user, 'follow':follows, 'searchuserpost':post, 'is_following':is_following, 'liked_posts':liked_posts, 'comments':all_comments})

        receivedmsg=Message.objects.filter(sender=request.user, receiver=user_id).order_by('timestamp')
        sendmsg=Message.objects.filter(sender=user_id, receiver=request.user).order_by('timestamp')
        allmsglist=[]
        for rmsg in receivedmsg:
            rmsg_dict = {
                'id': rmsg.id,
                'read': rmsg.read,
                'senderid': rmsg.sender.id,
                'sendername': rmsg.sender.username,
                'content': rmsg.content,
                'timestamp': rmsg.timestamp.isoformat()
            }
            allmsglist.append(rmsg_dict)
        for smsg in sendmsg:
            smsg_dict = {
                'id': smsg.id,
                'read': smsg.read,
                'senderid': smsg.sender.id,
                'sendername': smsg.sender.username,
                'content': smsg.content,
                'timestamp': smsg.timestamp.isoformat()
            }
            allmsglist.append(smsg_dict)
        sortedmsglist=sorted(allmsglist, key=lambda msg:msg['timestamp'])
        return render(request, 'searchprofile.html', {'allmsg':sortedmsglist, 'searchuser':user, 'follow':follows, 'searchuserpost':post, 'is_following':is_following, 'liked_posts':liked_posts})

@never_cache
def follow_unfollow(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    follow, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    if created:
        notification = Notification.objects.create(user=user_to_follow, content=f'{request.user.username} started following you!', post=None)
        return JsonResponse({'status': 'followed', 'msg': 'Unfollow'})
    else:
        follow.delete()
        return JsonResponse({'status': 'unfollowed', 'msg': 'Follow'})

@never_cache
def user_followers(request, user_id):
    userfollower=[]
    userfollower=Follow.objects.filter(following_id=user_id).values_list('follower_id', flat=True)
    userfollowers=User.objects.filter(id__in=userfollower).all()
    return render(request, 'followers.html', {'followers':userfollowers})

@never_cache
def user_following(request, user_id):
    userfollowing=[]
    userfollowing=Follow.objects.filter(follower_id=user_id).values_list('following_id', flat=True)
    userfollowings=User.objects.filter(id__in=userfollowing).all()
    return render(request, 'following.html', {'followings':userfollowings})

@never_cache
def view_notifications(request):
    notifications = Notification.objects.filter(user=request.user, read=False).all()
    for notification in notifications:
        notification.read = True
        notification.save()
    return render(request, 'notifications.html', {'notifications': notifications})

@never_cache
def view_comments(request, post_id):
    comments = Comment.objects.filter(post_id=post_id).order_by('-created_at')
    comments_list = [{
        'id': c.id,
        'post_id': c.post_id,
        'user_id': c.user_id,
        'username': c.user.username,
        'content': c.content,
        'created_at':c.created_at.date()
    } for c in comments]
    return JsonResponse(comments_list, safe=False)

@never_cache
def msgsend(request, receiver_id):
    receiver=User.objects.get(id=receiver_id)
    if request.method=='POST':
        content=request.POST.get('msg')
        msg=Message.objects.create(content=content, receiver=receiver, sender=request.user)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            message={'sender': msg.sender.username,
                    'content': msg.content}
            return JsonResponse(message)
    else:
        return redirect('searchprofile', receiver_id)

def user_ping(request):
    if request.method=='POST':
        content=request.POST.get('pinginput')
        ping=Pings.objects.create(content=content, user=request.user)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            pings={'id': ping.id,
                    'user': ping.user.username,
                    'content': ping.content,
                    'date':ping.created_at.date()}
            return JsonResponse(pings)

def  view_ping_reply(request, ping_id):
    reply = PingReply.objects.filter(ping_id=ping_id).order_by('-created_at')
    print(reply)
    reply_list = [{
        'id': r.id,
        'ping_id': r.ping_id,
        'user_id': r.user_id,
        'username': r.user.username,
        'content': r.content,
        'created_at':r.created_at.date()
    } for r in reply]
    return JsonResponse(reply_list, safe=False)

def ping_reply(request, ping_id):
    if request.method=='POST':
        ping=Pings.objects.get(id=ping_id)
        content=request.POST.get('reply')
        reply = PingReply.objects.create(ping=ping, user=request.user, content=content)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            replys={'sender': request.user.username,
                    'senderid': request.user.id,
                    'content': reply.content,
                    'created_at': reply.created_at.date()
                    }
            return JsonResponse(replys)
    
@never_cache
def userdeletepost(request, post_id):
    post=Post.objects.get(id=post_id)
    post.delete()
    return redirect('profile')