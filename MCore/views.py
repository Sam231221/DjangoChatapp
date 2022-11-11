from django.shortcuts import render, redirect
from MAuthentication.models import User
from django.contrib.auth.models import auth
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.shortcuts import HttpResponseRedirect
from .models import  Post, LikePost, FollowersCount
from itertools import chain
import random

from MChat.models import Thread
# Create your views here.

@login_required
def home(request):
    user_object = User.objects.get(username=request.user.username)

    user_following_list = []
    feed = []
    
    #get user's all following
    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)
    print(user_following_list)


    #Get posts of all the people that users follow
    for username in user_following_list:
        user_obj =User.objects.filter(username=username).first()
        feed_lists = Post.objects.filter(user=user_obj)
        feed.append(feed_lists)
    #posts    
    feed_list = list(chain(*feed))
    print(feed)
    print(feed_list) 

    all_users = User.objects.all()
    #list of user's followers
    user_following_all = []

    for user in user_following:
        user = User.objects.get(username=user.user)
        user_following_all.append(user)
    
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    
    context = {
        'user_profile': user_object,
        'posts':feed_list,
        'suggestions_username_list': final_suggestions_list[:4]
       }
    return render(request,'frontendbase.html', context)

class SearchEngineView(View):
    def post(self, request):
        query = request.POST['keyword']
        print(query)
        user_queryset =  User.objects.filter(username__icontains=query)
        print(user_queryset)
        if len(user_queryset) > 0 and len(query) > 0:
            product_list = [] #inititae an empty list
            
            #Append all customer obj into the list using loop.
            for obj in user_queryset:
                item= {
                    'pk': obj.id,
                    'image': obj.image.url,
                    'url': obj.get_absolute_url(),
                    'username': obj.username
                }
                product_list.append(item)
            
            #now attach customer_list  to the response
            response = product_list    
        else:
            response = "Sorry, We couldn't find any user with username '"+str(query)+"'"    

        return JsonResponse({'queryset':response}, safe=False)
     

@login_required
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

@login_required
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']
        user_obj= User.objects.filter(username=user).first()
        follower_obj = User.objects.filter(username=follower).first()

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_thread = Thread.objects.get(first_person=follower_obj, second_person=user_obj )
            delete_follower.delete()
            delete_thread.delete()
            messages.error(request, "You unfollowed user '"+user+"'.")
            return HttpResponseRedirect(request.META["HTTP_REFERER"])
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_thread = Thread.objects.create(first_person=follower_obj, second_person=user_obj )
            new_follower.save()
            new_thread.save()
            messages.success(request, "You just followed user '"+user+"'.")
            return HttpResponseRedirect(request.META["HTTP_REFERER"])
    else:
        messages.error(request, "Internal Server Error")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

class UserProfileView(View):
    def get(self, request, pk):
        user = User.objects.get(id=pk)
        user_posts = Post.objects.filter(user=user)
        user_post_length = len(user_posts)
        
        #supposing request.user is follower of this user
        follower = request.user.username
        if FollowersCount.objects.filter(follower=follower, user=user).first():
            button_text = 'Unfollow'
        else:
            button_text = 'Follow'

        user_followers = len(FollowersCount.objects.filter(user=user.username))
        user_following = len(FollowersCount.objects.filter(follower=user.username))
        context = {
            'user':user,
            'user_posts': user_posts,
            'user_post_length': user_post_length,
            'button_text': button_text,
            'user_followers': user_followers,
            'user_following': user_following,
        }        
        return render(request, 'Profile/UserProfile.html', context)