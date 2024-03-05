# forms.py
from django import forms
from .models import *

class SocialPlatformOrderForm(forms.ModelForm):
    class Meta:
        model = SocialPlatformOrder
        fields = ['audience_type', 'like_count', 'comment_count', 'subscriber_count', 'url']
        labels = {
            'subscriber_count': 'Total subscribers or Follows',
            'like_count': 'Total Likes',
            'comment_count': 'Total Comment'
            ''
        }


class YouTubeAutomationForm(forms.ModelForm):
    class Meta:
        model = YouTubeAutomation
        fields = ['video_file', 'title', 'description', 'tags', 'privacy_status', 'publish_date', 'publish_time']

    publish_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    publish_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)
    
    privacy_status = forms.ChoiceField(choices=YouTubeAutomation.PRIVACY_STATUS_CHOICES, required=False)


class LinkedInPostForm(forms.ModelForm):
    class Meta:
        model = LinkedInPost
        fields = ['title', 'content', 'attachment_url', 'hashtags', 'publish_date', 'publish_time']

    title = forms.CharField(max_length=255, required=False)
    attachment_url = forms.URLField(required=False)
    hashtags = forms.CharField(max_length=255, required=False)
    publish_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    publish_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)


class FacebookPostForm(forms.ModelForm):
    class Meta:
        model = FacebookPost
        fields = ['message', 'link', 'image', 'publish_date', 'publish_time']

    link = forms.URLField(required=False)
    image = forms.ImageField(required=False)
    publish_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    publish_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)
    
    def clean_video_path(self):
        video_path = self.cleaned_data.get('video_path')
        # Customize the validation logic here
        return video_path


