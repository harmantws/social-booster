from django.db import models
from django.contrib.auth import get_user_model

class SocialPlatformOrder(models.Model):
    ECOMMERCE = 'E-commerce'
    CONTENT_CREATOR = 'Content Creator and Influencers'
    HEALTH_FITNESS = 'Health and Fitness'
    TECH_SOFTWARE = 'Technology and Software Companies'
    HOSTPITAL_TOURISM = 'Hospitality and Tourism'

    AUDIENCE_CHOICES = [
        (ECOMMERCE, 'E-commerce'),
        (CONTENT_CREATOR, 'Content Creator and Influencers'),
        (HEALTH_FITNESS, 'Health and Fitness'),
        (TECH_SOFTWARE, 'Technology and Software Companies'),
        (HOSTPITAL_TOURISM, 'Hospitality and Tourism'),
    ]

    YOUTUBE = 'YouTube'
    INSTAGRAM = 'Instagram'
    FACEBOOK = 'Facebook'
    LINKEDIN = 'LinkedIn'

    SOCIAL_SERVICE_CHOICES = [
        (YOUTUBE, 'YouTube'),
        (INSTAGRAM, 'Instagram'),
        (FACEBOOK, 'Facebook'),
        (LINKEDIN, 'LinkedIn'),
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    audience_type = models.CharField(max_length=255, choices=AUDIENCE_CHOICES)
    social_service = models.CharField(max_length=255, choices=SOCIAL_SERVICE_CHOICES)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    subscriber_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=255)

    def __str__(self):
        return f"Social Service: {self.social_service}, Audience Type: {self.audience_type}"


class YouTubeAutomation(models.Model):
    PRIVACY_PUBLIC = 'public'
    PRIVACY_PRIVATE = 'private'
    PRIVACY_UNLISTED = 'unlisted'

    PRIVACY_STATUS_CHOICES = [
        (PRIVACY_PUBLIC, 'Public'),
        (PRIVACY_PRIVATE, 'Private'),
        (PRIVACY_UNLISTED, 'Unlisted'),
    ]
    
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    video_file = models.FileField(upload_to='youtube_uploads/')
    title = models.CharField(max_length=255)
    description = models.TextField()
    tags = models.CharField(max_length=255)
    privacy_status = models.CharField(max_length=20, choices=PRIVACY_STATUS_CHOICES)
    publish_date = models.DateField()
    publish_time = models.TimeField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Title: {self.title}, Uploaded by: {self.user}"


class LinkedInPost(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField()
    attachment_url = models.URLField(blank=True, null=True)
    hashtags = models.CharField(max_length=255, blank=True, null=True)
    publish_date = models.DateField(null=True, blank=True)
    publish_time = models.TimeField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s LinkedIn Post - {self.timestamp}"


class FacebookPost(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    message = models.TextField()
    link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='facebook_posts/', blank=True, null=True)
    publish_date = models.DateField(null=True)
    publish_time = models.TimeField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Facebook Post - {self.timestamp}"



