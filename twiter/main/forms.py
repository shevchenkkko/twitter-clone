from django import forms
from .models import Tweet,Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class TweetForm(forms.ModelForm):
    title = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class':'form-control'}))
    content = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'placeholder':'What is happening?',
        'class':'form-control',
    }))

    class Meta:
        model=Tweet
        exclude =('user', )
        fields = ('title','content',)

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(label='First name', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(label='Last name', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))


    class Meta:
        model = User
        fields = ('username','first_name','last_name','email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder']='User Name'
        self.fields['username'].label = 'Username'
        self.fields['username'].help_text = ""

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder']='Password'
        self.fields['password1'].label = 'Password'
        self.fields['password1'].help_text = ""

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder']='Confirm Password'
        self.fields['password2'].label = 'Confirm password'
        self.fields['password2'].help_text = ""



class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(label='First name', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(label='Last name', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email', )
    

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder']='User Name'
        self.fields['username'].label = 'Username'
        self.fields['username'].help_text = ""



class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(label="About Yourself", required=False, widget=forms.Textarea(attrs={'class':'form-control'}))
    profile_photo = forms.ImageField(label='Profile Image', required=False)
    youtube_link = forms.URLField(label='Youtube Link',required=False, widget=forms.URLInput(attrs={'class':'form-control'}))
    insta_link = forms.URLField(label='Instagram Link', required=False, widget=forms.URLInput(attrs={'class':'form-control'}))

    class Meta:
        model = Profile
        fields =('bio','profile_photo','youtube_link','insta_link', )