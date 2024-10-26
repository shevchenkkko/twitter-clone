from django.utils import timezone
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from main.models import *
from django.contrib.humanize.templatetags.humanize import naturaltime
from .forms import *
from django.contrib.auth import login, logout, authenticate
from django import forms
from django.contrib.auth.models import User



def home(request):
    tweets = Tweet.objects.filter(views__gt=10)
    if request.method == "POST":
        search_data = request.POST['search']
        tweets = Tweet.objects.filter(content__contains = search_data )
    else:
        tweets = Tweet.objects.filter(is_published=True).order_by("-created_at")
    for tweet in tweets:
        tweet.time_ago = naturaltime(tweet.created_at)
    return render(request, 'main/home.html', {'tweets':tweets,})


def profile_list(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            search  = request.POST['search']
            profiles = Profile.objects.filter(user__username__contains = search )
        else:
            profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'main/profile_list.html', {'profiles':profiles, 'search':search})
    else:
        messages.success(request, ("You Must Be Logged In To View This Page!"))
        return redirect('home')

def profile(request, pk ):

    if request.user.is_authenticated:
        tweets = Tweet.objects.filter(author_id = pk, is_published=True).order_by("-created_at")
        profile = Profile.objects.get(user_id=pk)
        
        for tweet in tweets:
            tweet.time_ago = naturaltime(tweet.created_at)
        
        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST['follow']
            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            else:
                current_user_profile.follows.add(profile)
            current_user_profile.save()
        return render(request, 'main/profile.html', {'profile':profile, 'tweets':tweets})
    else:
        messages.success(request, ("You Must Be Logged In To View This Page!"))
        return redirect('home')

def profile_following(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id = pk)
        return render(request, 'main/following.html', {'profile':profile})
    else:
        messages.success(request, ("You Must Be Logged In To View This Page!"))
        return redirect('home')


def profile_followers(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id = pk)
        return render(request, 'main/followers.html', {'profile':profile})
    else:
        messages.success(request, ("You Must Be Logged In To View This Page!"))
        return redirect('home')


def add_tweet(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            form = TweetForm(request.POST)
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.author = request.user
                tweet.save()
                return redirect('home')
        else:
            form = TweetForm()
    return render(request, 'main/add_tweet.html', {'form':form})


def login_user(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, ("You Have Been Successfully Logged In"))
            return redirect('home')
        else:
            messages.error(request, ("Try Again!"))
            return redirect('login')
    else:
        return render(request, 'main/login.html')        


def logout_user(request):
    logout(request)
    messages.error(request,("You have been logged out!"))
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration Was Successful')
            return redirect('home')
        else:
            messages.error(request, 'Registration Error')
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {'form':form})
    

def update_user(request):
    if request.user.is_authenticated:
        redirect_url = reverse('profile', args=[request.user.id])
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id = request.user.id)
        user_form = UserUpdateForm(request.POST or None,request.FILES or None ,instance= current_user)
        profile_form  = ProfileUpdateForm(request.POST or None, request.FILES or None,instance= profile_user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            login(request,current_user)
            messages.success(request, 'Your Profile Has Been Updated')
            return redirect(redirect_url)
        return render(request,'main/update_user.html', {'user_form':user_form,'profile_form':profile_form})
    else:
        messages.error(request, 'You Must Be Logged In To View This Page!')
        return redirect('home')


def like_post(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, pk=pk)
        is_liked = False 
        if tweet.likes.filter(pk=request.user.pk):
            tweet.likes.remove(request.user)
            is_liked = False 
        else:
            tweet.likes.add(request.user)
            is_liked = True 
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.error(request, 'You Must Be Logged In To View This Page!')
        return redirect('home')
    

def like_comment(request, pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=pk)
        if comment.likes.filter(pk=request.user.pk):
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.error(request, 'You Must Be Logged In To View This Page!')
        return redirect('home')


def follow(request, pk):
    if request.user.is_authenticated:
        user = Profile.objects.get(user_id=pk)
        request.user.profile.follows.add(user)
        request.user.profile.save()
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.error(request, 'You Must Be Logged In To View This Page!')
        return redirect('home')

def unfollow(request, pk):
    if request.user.is_authenticated:
        user = Profile.objects.get(user_id=pk)
        request.user.profile.follows.remove(user)
        request.user.profile.save()
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.error(request, 'You Must Be Logged In To View This Page!')
        return redirect('home')
    


def delete_tweet(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        if request.user.username == tweet.author.username:
            tweet.delete()
            messages.success(request, 'The Tweet Has Been Deleted')
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.error(request, 'You Do Not Own This Tweet')
            return redirect('home')
    
    else:
        messages.error(request, 'You Must Be Logged In To View This Page!')
        return redirect(request.META.get("HTTP_REFERER"))  


def edit_tweet(request, pk):
    if request.user.is_authenticated:
        redirect_url = reverse('profile', args=[request.user.id])
        tweet = get_object_or_404(Tweet, id=pk)
        if request.user.username == tweet.author.username:
            if request.method=="POST":
                form = TweetForm(request.POST or None, instance=tweet)
                if form.is_valid():
                    tweet = form.save(commit=False)
                    tweet.author = request.user
                    tweet.save()
                    messages.success(request, 'The Tweet Has Been Edited')
                    return redirect(redirect_url)
            else:
                form = TweetForm(instance=tweet)
            return render(request, 'main/edit_tweet.html', {'form':form} )

        else:
            messages.error(request, 'You Do Not Own This Tweet')
            return redirect('home')
    else:
        messages.error(request, 'You Must Be Logged In To View This Page!')
        return redirect(request.META.get("HTTP_REFERER"))  
            


def add_comment(request, pk):
    redirect_url = reverse('comment', args=[pk])
    tweet = get_object_or_404(Tweet, pk=pk)    
    if request.method=="POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                c=form.save(commit=False)
                c.user = request.user
                c.tweet = tweet
                c.save()
                return redirect(redirect_url)
            else:
                messages.error(request, 'Try again...')
        else:
            messages.error(request, 'You Must Be Logged In To View This Page!')
            return redirect(request.META.get("HTTP_REFERER")) 
    else:
        form = CommentForm()
    return render(request, 'main/comment.html', {'form':form, 'tweet':tweet})

def delete_comment(request, pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=pk)
        if request.user.username == comment.user.username:
            comment.delete()
            messages.success(request, 'The Comment Has Been Deleted')
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.error(request, 'You Do Not Own This Comment')
            return redirect('home')
    
    else:
        messages.error(request, 'You Must Be Logged In To View This Page!')
        return redirect(request.META.get("HTTP_REFERER"))  


def edit_comment(request, pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=pk)
        tweet = get_object_or_404(Tweet, pk=comment.tweet.pk)    
        redirect_url = reverse('comment', args=[comment.tweet.pk])
        if request.user.username == comment.user.username:
            if request.method=="POST":
                form = CommentForm(request.POST or None, instance=comment)
                if form.is_valid():
                    comment = form.save(commit=False)
                    comment.user = request.user
                    comment.save()
                    messages.success(request, 'The Comment Has Been Edited')
                    return redirect(redirect_url)
            else:
                form = CommentForm(instance=comment)
            return render(request, 'main/edit_comment.html', {'form':form, 'tweet':tweet} )
        else:
            messages.error(request, 'You Do Not Own This Comment')
            return redirect('home')
    else:
        messages.error(request, 'You Must Be Logged In To View This Page!')
        return redirect(request.META.get("HTTP_REFERER"))  
