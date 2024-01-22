from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


class ProfileInline(admin.StackedInline):
    model=Profile


class UserAdmin(admin.ModelAdmin):
    model=User
    fields = ['username']
    inlines=[ProfileInline]


class TweetAdmin(admin.ModelAdmin):
    list_display=['id','title','author','get_photo','created_at','is_published',] 
    list_display_links=['id','title']
    search_fields=['title', 'content']
    list_editable=['is_published']
    list_filter=['is_published','author']
    fields = ('title','content','author', 'photo', 'get_photo','created_at','updated_at', 'is_published', 'views', 'likes','retweets','comments')
    readonly_fields = ('get_photo', 'created_at','updated_at') 
    save_on_top= True

    def get_photo (self, obj):
        if obj.photo:
            return mark_safe (f'<img src="{obj.photo.url}" width=75>')
        else:
            return '-'

    get_photo.short_description='Мініатюра'



class ProfileAdmin(admin.ModelAdmin):
    list_display=['id','user','get_photo'] 
    list_display_links=['id','user']
    search_fields=['user']
    fields = ('user','bio', 'profile_photo', 'get_photo','follows', 'youtube_link','insta_link')
    readonly_fields = ('get_photo',)
    save_on_top= True

    def get_photo (self, obj):
        if obj.profile_photo:
            return mark_safe (f'<img src="{obj.profile_photo.url}" width=75>')
        else:
            return '-'
    get_photo.short_description='Мініатюра'


class CommentAdmin(admin.ModelAdmin):
    list_display=['id','user','content','tweet','created_at'] 
    list_display_links=['id','user','content']
    search_fields=['content','user']
    list_filter=['user','tweet']
    fields=('content','user', 'created_at','tweet')
    readonly_fields = ('created_at',) 
    save_on_top= True



admin.site.unregister(User)

admin.site.register(User, UserAdmin)
admin.site.register(Tweet, TweetAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Comment, CommentAdmin)