from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import FileExtensionValidator


# ==================== USER MANAGEMENT ====================

class User(AbstractUser):
    """Extended user model for Facebook-like functionality"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer not to say')
    ]
    
    bio = models.TextField(max_length=500, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    cover_photo = models.ImageField(upload_to='cover_photos/', null=True, blank=True)
    hometown = models.CharField(max_length=100, blank=True)
    current_city = models.CharField(max_length=100, blank=True)
    relationship_status = models.CharField(max_length=50, blank=True)
    workplace = models.CharField(max_length=200, blank=True)
    education = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    is_verified = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']


class Friendship(models.Model):
    """Friend connections between users"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('blocked', 'Blocked'),
        ('declined', 'Declined')
    ]
    
    from_user = models.ForeignKey(User, related_name='friendships_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friendships_received', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'friendships'
        unique_together = ['from_user', 'to_user']
        ordering = ['-created_at']


class Follow(models.Model):
    """Allow users to follow others (like pages/profiles)"""
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'follows'
        unique_together = ['follower', 'following']
        ordering = ['-created_at']


# ==================== POSTS & CONTENT ====================

class Post(models.Model):
    """Main post model for status updates, photos, videos, etc."""
    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('friends', 'Friends'),
        ('friends_except', 'Friends Except'),
        ('specific_friends', 'Specific Friends'),
        ('only_me', 'Only Me'),
        ('custom', 'Custom')
    ]
    
    POST_TYPE_CHOICES = [
        ('status', 'Status'),
        ('photo', 'Photo'),
        ('video', 'Video'),
        ('shared', 'Shared Post'),
        ('life_event', 'Life Event')
    ]
    
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES, default='status')
    privacy = models.CharField(max_length=20, choices=PRIVACY_CHOICES, default='friends')
    feeling = models.CharField(max_length=50, blank=True)  # e.g., "feeling happy"
    location = models.CharField(max_length=200, blank=True)
    tagged_users = models.ManyToManyField(User, related_name='tagged_in_posts', blank=True)
    shared_post = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    is_pinned = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    comments_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'posts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['author', '-created_at']),
        ]


class PostMedia(models.Model):
    """Media attachments for posts (photos, videos)"""
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('gif', 'GIF')
    ]
    
    post = models.ForeignKey(Post, related_name='media', on_delete=models.CASCADE)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to='post_media/')
    thumbnail = models.ImageField(upload_to='post_thumbnails/', null=True, blank=True)
    description = models.CharField(max_length=500, blank=True)
    order = models.PositiveIntegerField(default=0)
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    duration = models.PositiveIntegerField(null=True, blank=True)  # for videos in seconds
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'post_media'
        ordering = ['order', 'created_at']


class Reaction(models.Model):
    """Reactions to posts (Like, Love, Haha, Wow, Sad, Angry)"""
    REACTION_CHOICES = [
        ('like', 'Like'),
        ('love', 'Love'),
        ('care', 'Care'),
        ('haha', 'Haha'),
        ('wow', 'Wow'),
        ('sad', 'Sad'),
        ('angry', 'Angry')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='reactions', on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'reactions'
        unique_together = ['user', 'post']
        ordering = ['-created_at']


class Comment(models.Model):
    """Comments on posts"""
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='comment_images/', null=True, blank=True)
    gif_url = models.URLField(blank=True)
    tagged_users = models.ManyToManyField(User, related_name='tagged_in_comments', blank=True)
    is_edited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'comments'
        ordering = ['created_at']


class CommentReaction(models.Model):
    """Reactions to comments"""
    REACTION_CHOICES = [
        ('like', 'Like'),
        ('love', 'Love'),
        ('haha', 'Haha'),
        ('wow', 'Wow'),
        ('sad', 'Sad'),
        ('angry', 'Angry')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='reactions', on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'comment_reactions'
        unique_together = ['user', 'comment']


# ==================== STORIES ====================

class Story(models.Model):
    """24-hour stories feature"""
    STORY_TYPE_CHOICES = [
        ('photo', 'Photo'),
        ('video', 'Video'),
        ('text', 'Text')
    ]
    
    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('friends', 'Friends'),
        ('close_friends', 'Close Friends'),
        ('custom', 'Custom')
    ]
    
    user = models.ForeignKey(User, related_name='stories', on_delete=models.CASCADE)
    story_type = models.CharField(max_length=10, choices=STORY_TYPE_CHOICES)
    media_file = models.FileField(upload_to='stories/', null=True, blank=True)
    text_content = models.TextField(blank=True)
    background_color = models.CharField(max_length=7, blank=True)  # hex color
    privacy = models.CharField(max_length=20, choices=PRIVACY_CHOICES, default='friends')
    duration = models.PositiveIntegerField(default=5)  # seconds to display
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'stories'
        ordering = ['-created_at']
        verbose_name_plural = 'Stories'


class StoryView(models.Model):
    """Track who viewed stories"""
    story = models.ForeignKey(Story, related_name='views', on_delete=models.CASCADE)
    viewer = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'story_views'
        unique_together = ['story', 'viewer']


# ==================== MESSENGER ====================

class Conversation(models.Model):
    """Chat conversations between users"""
    CONVERSATION_TYPE_CHOICES = [
        ('direct', 'Direct Message'),
        ('group', 'Group Chat')
    ]
    
    conversation_type = models.CharField(max_length=10, choices=CONVERSATION_TYPE_CHOICES, default='direct')
    name = models.CharField(max_length=100, blank=True)  # for group chats
    participants = models.ManyToManyField(User, related_name='conversations')
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='conversation_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'conversations'
        ordering = ['-updated_at']


class Message(models.Model):
    """Messages within conversations"""
    MESSAGE_TYPE_CHOICES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('file', 'File'),
        ('sticker', 'Sticker'),
        ('gif', 'GIF'),
        ('voice', 'Voice Message')
    ]
    
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES, default='text')
    content = models.TextField(blank=True)
    media_file = models.FileField(upload_to='message_media/', null=True, blank=True)
    replied_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    is_deleted = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'messages'
        ordering = ['created_at']


class MessageRead(models.Model):
    """Track message read status"""
    message = models.ForeignKey(Message, related_name='read_by', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'message_reads'
        unique_together = ['message', 'user']


class MessageReaction(models.Model):
    """Reactions to messages"""
    EMOJI_CHOICES = [
        ('❤️', 'Heart'),
        ('😂', 'Laugh'),
        ('😮', 'Wow'),
        ('😢', 'Sad'),
        ('😠', 'Angry'),
        ('👍', 'Thumbs Up'),
        ('👎', 'Thumbs Down')
    ]
    
    message = models.ForeignKey(Message, related_name='reactions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    emoji = models.CharField(max_length=10, choices=EMOJI_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'message_reactions'
        unique_together = ['message', 'user']


# ==================== PAGES ====================

class Page(models.Model):
    """Business/brand pages"""
    CATEGORY_CHOICES = [
        ('business', 'Business'),
        ('brand', 'Brand'),
        ('community', 'Community'),
        ('public_figure', 'Public Figure'),
        ('entertainment', 'Entertainment'),
        ('cause', 'Cause')
    ]
    
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    profile_picture = models.ImageField(upload_to='page_profiles/', null=True, blank=True)
    cover_photo = models.ImageField(upload_to='page_covers/', null=True, blank=True)
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'pages'
        ordering = ['-created_at']


class PageLike(models.Model):
    """Users who like pages"""
    page = models.ForeignKey(Page, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='liked_pages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'page_likes'
        unique_together = ['page', 'user']


class PageRole(models.Model):
    """Admin roles for page management"""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('moderator', 'Moderator'),
        ('advertiser', 'Advertiser'),
        ('analyst', 'Analyst')
    ]
    
    page = models.ForeignKey(Page, related_name='roles', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'page_roles'
        unique_together = ['page', 'user']


# ==================== GROUPS ====================

class Group(models.Model):
    """Facebook groups"""
    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('secret', 'Secret')
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')
    cover_photo = models.ImageField(upload_to='group_covers/', null=True, blank=True)
    rules = models.TextField(blank=True)
    tags = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=100, blank=True)
    created_by = models.ForeignKey(User, related_name='created_groups', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'groups'
        ordering = ['-created_at']


class GroupMember(models.Model):
    """Group membership"""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('member', 'Member')
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined')
    ]
    
    group = models.ForeignKey(Group, related_name='members', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='group_memberships', on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'group_members'
        unique_together = ['group', 'user']


class GroupPost(models.Model):
    """Posts within groups"""
    group = models.ForeignKey(Group, related_name='posts', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_pinned = models.BooleanField(default=False)
    is_announcement = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'group_posts'
        ordering = ['-created_at']


# ==================== EVENTS ====================

class Event(models.Model):
    """Events feature"""
    EVENT_TYPE_CHOICES = [
        ('public', 'Public Event'),
        ('private', 'Private Event'),
        ('friends', 'Friends'),
        ('group', 'Group Event')
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=10, choices=EVENT_TYPE_CHOICES)
    cover_photo = models.ImageField(upload_to='event_covers/', null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    host = models.ForeignKey(User, related_name='hosted_events', on_delete=models.CASCADE)
    co_hosts = models.ManyToManyField(User, related_name='co_hosted_events', blank=True)
    group = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'events'
        ordering = ['start_datetime']


class EventResponse(models.Model):
    """RSVP responses to events"""
    RESPONSE_CHOICES = [
        ('going', 'Going'),
        ('interested', 'Interested'),
        ('not_going', 'Not Going')
    ]
    
    event = models.ForeignKey(Event, related_name='responses', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    response = models.CharField(max_length=20, choices=RESPONSE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'event_responses'
        unique_together = ['event', 'user']


# ==================== NOTIFICATIONS ====================

class Notification(models.Model):
    """User notifications"""
    NOTIFICATION_TYPE_CHOICES = [
        ('friend_request', 'Friend Request'),
        ('friend_accepted', 'Friend Request Accepted'),
        ('post_like', 'Post Like'),
        ('post_comment', 'Post Comment'),
        ('comment_reply', 'Comment Reply'),
        ('post_share', 'Post Share'),
        ('post_tag', 'Tagged in Post'),
        ('comment_tag', 'Tagged in Comment'),
        ('birthday', 'Birthday'),
        ('event_invite', 'Event Invitation'),
        ('group_invite', 'Group Invitation'),
        ('page_like', 'Page Like'),
        ('message', 'New Message')
    ]
    
    recipient = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.URLField(blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']


# ==================== PHOTOS/ALBUMS ====================

class Album(models.Model):
    """Photo albums"""
    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('friends', 'Friends'),
        ('only_me', 'Only Me')
    ]
    
    user = models.ForeignKey(User, related_name='albums', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    privacy = models.CharField(max_length=20, choices=PRIVACY_CHOICES, default='friends')
    cover_photo = models.ForeignKey('Photo', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'albums'
        ordering = ['-created_at']


class Photo(models.Model):
    """Individual photos"""
    user = models.ForeignKey(User, related_name='photos', on_delete=models.CASCADE)
    album = models.ForeignKey(Album, null=True, blank=True, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/')
    caption = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    tagged_users = models.ManyToManyField(User, related_name='tagged_photos', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'photos'
        ordering = ['-created_at']


# ==================== MARKETPLACE ====================

class MarketplaceItem(models.Model):
    """Items for sale in marketplace"""
    CATEGORY_CHOICES = [
        ('vehicles', 'Vehicles'),
        ('property', 'Property Rentals'),
        ('apparel', 'Apparel'),
        ('classifieds', 'Classifieds'),
        ('electronics', 'Electronics'),
        ('entertainment', 'Entertainment'),
        ('family', 'Family'),
        ('free', 'Free Stuff'),
        ('garden', 'Garden & Outdoor'),
        ('hobbies', 'Hobbies'),
        ('home', 'Home Goods'),
        ('home_sales', 'Home Sales'),
        ('office', 'Office Supplies'),
        ('pets', 'Pet Supplies'),
        ('sporting', 'Sporting Goods'),
        ('toys', 'Toys & Games')
    ]
    
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used_like_new', 'Used - Like New'),
        ('used_good', 'Used - Good'),
        ('used_fair', 'Used - Fair')
    ]
    
    seller = models.ForeignKey(User, related_name='marketplace_items', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    location = models.CharField(max_length=200)
    is_available = models.BooleanField(default=True)
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'marketplace_items'
        ordering = ['-created_at']


class MarketplaceItemImage(models.Model):
    """Images for marketplace items"""
    item = models.ForeignKey(MarketplaceItem, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='marketplace/')
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        db_table = 'marketplace_item_images'
        ordering = ['order']


# ==================== SAVED ITEMS ====================

class SavedPost(models.Model):
    """Posts saved by users"""
    user = models.ForeignKey(User, related_name='saved_posts', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    collection_name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'saved_posts'
        unique_together = ['user', 'post']
        ordering = ['-created_at']


# ==================== LIVE VIDEO ====================

class LiveVideo(models.Model):
    """Live streaming videos"""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('live', 'Live'),
        ('ended', 'Ended')
    ]
    
    broadcaster = models.ForeignKey(User, related_name='live_videos', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')
    thumbnail = models.ImageField(upload_to='live_thumbnails/', null=True, blank=True)
    stream_url = models.URLField(blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'live_videos'
        ordering = ['-created_at']


class LiveVideoViewer(models.Model):
    """Track live video viewers"""
    live_video = models.ForeignKey(LiveVideo, related_name='viewers', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'live_video_viewers'


# ==================== REPORTS & MODERATION ====================

class Report(models.Model):
    """Content reporting system"""
    CONTENT_TYPE_CHOICES = [
        ('post', 'Post'),
        ('comment', 'Comment'),
        ('user', 'User Profile'),
        ('page', 'Page'),
        ('group', 'Group'),
        ('message', 'Message')
    ]
    
    REASON_CHOICES = [
        ('spam', 'Spam'),
        ('nudity', 'Nudity or Sexual Content'),
        ('hate_speech', 'Hate Speech'),
        ('violence', 'Violence or Dangerous Organizations'),
        ('harassment', 'Harassment or Bullying'),
        ('false_information', 'False Information'),
        ('scam', 'Scam or Fraud'),
        ('intellectual_property', 'Intellectual Property Violation'),
        ('sale_of_illegal_goods', 'Sale of Illegal or Regulated Goods'),
        ('suicide_or_self_injury', 'Suicide or Self-Injury'),
        ('eating_disorders', 'Eating Disorders'),
        ('other', 'Other')
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('reviewing', 'Under Review'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed')
    ]
    
    reporter = models.ForeignKey(User, related_name='reports_made', on_delete=models.CASCADE)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    content_id = models.PositiveIntegerField()  # ID of the reported content
    reason = models.CharField(max_length=30, choices=REASON_CHOICES)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.ForeignKey(User, null=True, blank=True, related_name='reports_reviewed', on_delete=models.SET_NULL)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'reports'
        ordering = ['-created_at']


class BlockedUser(models.Model):
    """Users blocked by other users"""
    blocker = models.ForeignKey(User, related_name='blocked_users', on_delete=models.CASCADE)
    blocked = models.ForeignKey(User, related_name='blocked_by', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'blocked_users'
        unique_together = ['blocker', 'blocked']


# ==================== PRIVACY & SETTINGS ====================

class PrivacySetting(models.Model):
    """User privacy settings"""
    OPTION_CHOICES = [
        ('public', 'Public'),
        ('friends', 'Friends'),
        ('friends_of_friends', 'Friends of Friends'),
        ('only_me', 'Only Me'),
        ('custom', 'Custom')
    ]
    
    user = models.OneToOneField(User, related_name='privacy_settings', on_delete=models.CASCADE)
    
    # Profile visibility
    profile_visibility = models.CharField(max_length=20, choices=OPTION_CHOICES, default='public')
    post_visibility = models.CharField(max_length=20, choices=OPTION_CHOICES, default='friends')
    friend_list_visibility = models.CharField(max_length=20, choices=OPTION_CHOICES, default='friends')
    email_visibility = models.CharField(max_length=20, choices=OPTION_CHOICES, default='only_me')
    phone_visibility = models.CharField(max_length=20, choices=OPTION_CHOICES, default='only_me')
    birthday_visibility = models.CharField(max_length=20, choices=OPTION_CHOICES, default='friends')
    
    # Who can contact you
    who_can_send_friend_requests = models.CharField(max_length=20, choices=OPTION_CHOICES, default='public')
    who_can_message_you = models.CharField(max_length=20, choices=OPTION_CHOICES, default='friends_of_friends')
    
    # Timeline and tagging
    who_can_post_on_timeline = models.CharField(max_length=20, choices=OPTION_CHOICES, default='friends')
    who_can_see_posts_on_timeline = models.CharField(max_length=20, choices=OPTION_CHOICES, default='friends')
    review_posts_tagged_in = models.BooleanField(default=True)
    review_tags_before_appearing = models.BooleanField(default=True)
    
    # Search
    allow_search_by_email = models.BooleanField(default=True)
    allow_search_by_phone = models.BooleanField(default=True)
    allow_search_engine_indexing = models.BooleanField(default=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'privacy_settings'


class NotificationSetting(models.Model):
    """User notification preferences"""
    user = models.OneToOneField(User, related_name='notification_settings', on_delete=models.CASCADE)
    
    # Push notifications
    push_post_likes = models.BooleanField(default=True)
    push_comments = models.BooleanField(default=True)
    push_friend_requests = models.BooleanField(default=True)
    push_messages = models.BooleanField(default=True)
    push_group_activity = models.BooleanField(default=True)
    push_event_reminders = models.BooleanField(default=True)
    push_birthdays = models.BooleanField(default=True)
    
    # Email notifications
    email_post_likes = models.BooleanField(default=False)
    email_comments = models.BooleanField(default=True)
    email_friend_requests = models.BooleanField(default=True)
    email_messages = models.BooleanField(default=True)
    email_group_activity = models.BooleanField(default=False)
    email_event_reminders = models.BooleanField(default=True)
    email_product_updates = models.BooleanField(default=True)
    
    # SMS notifications
    sms_login_alerts = models.BooleanField(default=True)
    sms_password_changes = models.BooleanField(default=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notification_settings'


# ==================== MEMORIES ====================

class Memory(models.Model):
    """On This Day / Memories feature"""
    user = models.ForeignKey(User, related_name='memories', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, null=True, blank=True, on_delete=models.CASCADE)
    original_date = models.DateField()
    years_ago = models.PositiveIntegerField()
    is_shared = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'memories'
        ordering = ['-original_date']
        verbose_name_plural = 'Memories'


# ==================== WATCH (VIDEO PLATFORM) ====================

class Video(models.Model):
    """Dedicated video content (like YouTube/Facebook Watch)"""
    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('friends', 'Friends'),
        ('only_me', 'Only Me')
    ]
    
    uploader = models.ForeignKey(User, related_name='videos', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='video_thumbnails/')
    duration = models.PositiveIntegerField()  # in seconds
    privacy = models.CharField(max_length=20, choices=PRIVACY_CHOICES, default='public')
    view_count = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=50, blank=True)
    tags = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'videos'
        ordering = ['-created_at']


class VideoView(models.Model):
    """Track video views"""
    video = models.ForeignKey(Video, related_name='views', on_delete=models.CASCADE)
    viewer = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    watch_duration = models.PositiveIntegerField(default=0)  # seconds watched
    completed = models.BooleanField(default=False)
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'video_views'


class Playlist(models.Model):
    """Video playlists"""
    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('unlisted', 'Unlisted'),
        ('private', 'Private')
    ]
    
    user = models.ForeignKey(User, related_name='playlists', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    privacy = models.CharField(max_length=20, choices=PRIVACY_CHOICES, default='public')
    videos = models.ManyToManyField(Video, through='PlaylistVideo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'playlists'
        ordering = ['-created_at']


class PlaylistVideo(models.Model):
    """Videos in playlists with ordering"""
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'playlist_videos'
        ordering = ['order']
        unique_together = ['playlist', 'video']


# ==================== POLLS ====================

class Poll(models.Model):
    """Polls in posts"""
    post = models.OneToOneField(Post, related_name='poll', on_delete=models.CASCADE)
    question = models.CharField(max_length=500)
    duration_hours = models.PositiveIntegerField(default=24)
    allow_multiple_votes = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'polls'


class PollOption(models.Model):
    """Options for polls"""
    poll = models.ForeignKey(Poll, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        db_table = 'poll_options'
        ordering = ['order']


class PollVote(models.Model):
    """User votes on polls"""
    poll = models.ForeignKey(Poll, related_name='votes', on_delete=models.CASCADE)
    option = models.ForeignKey(PollOption, related_name='votes', on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'poll_votes'
        unique_together = ['poll', 'voter', 'option']


# ==================== FUNDRAISERS ====================

class Fundraiser(models.Model):
    """Fundraising campaigns"""
    CATEGORY_CHOICES = [
        ('medical', 'Medical'),
        ('education', 'Education'),
        ('emergency', 'Emergency'),
        ('nonprofit', 'Nonprofit'),
        ('creative', 'Creative Project'),
        ('community', 'Community'),
        ('other', 'Other')
    ]
    
    creator = models.ForeignKey(User, related_name='fundraisers', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='USD')
    cover_photo = models.ImageField(upload_to='fundraiser_covers/', null=True, blank=True)
    beneficiary_name = models.CharField(max_length=200, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'fundraisers'
        ordering = ['-created_at']


class Donation(models.Model):
    """Donations to fundraisers"""
    fundraiser = models.ForeignKey(Fundraiser, related_name='donations', on_delete=models.CASCADE)
    donor = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_anonymous = models.BooleanField(default=False)
    message = models.TextField(blank=True)
    transaction_id = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'donations'
        ordering = ['-created_at']


# ==================== SEARCH HISTORY ====================

class SearchHistory(models.Model):
    """User search history"""
    user = models.ForeignKey(User, related_name='search_history', on_delete=models.CASCADE)
    query = models.CharField(max_length=200)
    search_type = models.CharField(max_length=20, default='general')  # people, posts, pages, groups, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'search_history'
        ordering = ['-created_at']
        verbose_name_plural = 'Search histories'


# ==================== ACTIVITY LOG ====================

class ActivityLog(models.Model):
    """Log of user activities"""
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('post_create', 'Created Post'),
        ('post_update', 'Updated Post'),
        ('post_delete', 'Deleted Post'),
        ('friend_add', 'Added Friend'),
        ('friend_remove', 'Removed Friend'),
        ('profile_update', 'Updated Profile'),
        ('password_change', 'Changed Password'),
        ('privacy_update', 'Updated Privacy Settings')
    ]
    
    user = models.ForeignKey(User, related_name='activity_logs', on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    details = models.JSONField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'activity_logs'
        ordering = ['-created_at']


# ==================== ADS SYSTEM ====================

class Advertisement(models.Model):
    """Advertisements/promoted content"""
    AD_TYPE_CHOICES = [
        ('image', 'Image Ad'),
        ('video', 'Video Ad'),
        ('carousel', 'Carousel Ad'),
        ('collection', 'Collection Ad')
    ]
    
    PLACEMENT_CHOICES = [
        ('feed', 'News Feed'),
        ('stories', 'Stories'),
        ('marketplace', 'Marketplace'),
        ('video', 'Video Feed'),
        ('right_column', 'Right Column')
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Review'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected')
    ]
    
    advertiser = models.ForeignKey(User, related_name='advertisements', on_delete=models.CASCADE)
    ad_type = models.CharField(max_length=20, choices=AD_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='ads/', null=True, blank=True)
    video = models.FileField(upload_to='ad_videos/', null=True, blank=True)
    link_url = models.URLField()
    call_to_action = models.CharField(max_length=50)
    placement = models.CharField(max_length=20, choices=PLACEMENT_CHOICES)
    target_audience = models.JSONField()  # Demographics, interests, etc.
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    impressions = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'advertisements'
        ordering = ['-created_at']


class AdImpression(models.Model):
    """Track ad impressions"""
    ad = models.ForeignKey(Advertisement, related_name='ad_impressions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ad_impressions'


class AdClick(models.Model):
    """Track ad clicks"""
    ad = models.ForeignKey(Advertisement, related_name='ad_clicks', on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ad_clicks'


# ==================== BADGES & ACHIEVEMENTS ====================

class Badge(models.Model):
    """User badges and achievements"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to='badges/')
    criteria = models.JSONField()  # Conditions to earn the badge
    
    class Meta:
        db_table = 'badges'


class UserBadge(models.Model):
    """Badges earned by users"""
    user = models.ForeignKey(User, related_name='badges', on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_badges'
        unique_together = ['user', 'badge']