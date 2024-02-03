from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
import os
from django.utils import timezone

def user_profile_photo_path(instance, filename):
    # Отримати розширення файлу
    extension = filename.split('.')[-1]
    # Створити нове ім'я файлу, щоб уникнути конфліктів імен
    filename = f"profile_photo_{timezone.now().strftime('%Y%m%d%H%M%S')}.{extension}"
    # Повернути шлях для збереження файлу
    return os.path.join('images/', filename)


  

class Tweet(models.Model):
    title = models.CharField(max_length=255,verbose_name = 'Заголовок')
    author = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name = 'Автор')
    content = models.TextField(max_length= 350, verbose_name = 'Контент')
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True,verbose_name='Змінено')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d',verbose_name = 'Фото', blank=True)
    is_published = models.BooleanField(default=True,verbose_name = 'Опубліковано?' )
    views = models.IntegerField(default = 0,verbose_name = 'Перегляди')
    likes = models.ManyToManyField(User, related_name='tweet_likes', blank=True,verbose_name = 'Вподобання')
    retweets = models.ManyToManyField(User, related_name='tweet_retweets', blank=True,verbose_name = 'Поширення')
    

    class Meta:
        verbose_name = 'Tweet'
        verbose_name_plural = 'Tweets'
        ordering = ('-created_at',)
    
    # def get_absolute_url(self):
    #     return reverse("", kwargs={"id": self.pk}) #TODO

    def __str__(self):
        return self.title[:20]
    
    def count_likes(self):
        return self.likes.count()

    def count_comments(self):
        return self.comments.count()


class Comment(models.Model):
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey('Tweet', on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'{self.user.username} - {self.content[:50]}'
  

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, verbose_name = 'Користувач')
    bio = models.TextField(max_length=300, blank=True, verbose_name = 'Про користувача', null=True )
    profile_photo = models.ImageField(upload_to=user_profile_photo_path, blank=True, null=True, verbose_name = 'Фото корстувача')
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True) 
    youtube_link = models.URLField(verbose_name="Youtube", blank=True, null=True)
    insta_link = models.URLField(verbose_name="Instagram", blank=True, null=True)
    #ПОПИТАТИ ЗА related_name='followed_by' 
    #symmetrical=False бо ми можемо підписатися на людину, а вона може не підписуватися

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
    
    def __str__(self):
        return self.user.username
    
    def count_follows(self):
        return self.follows.count()
    
    def count_followers(self):
        return self.followed_by.count()



#Create profile when new user signs up
def create_profile(sender, instance,created,**kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()

post_save.connect(create_profile, sender=User)