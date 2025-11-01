from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.db.models import Count, Q
from django.utils import timezone
from .models import (
    User, Friendship, Follow, Post, PostMedia, Reaction, Comment, CommentReaction,
    Story, StoryView, Conversation, Message, MessageRead, MessageReaction,
    Page, PageLike, PageRole, Group, GroupMember, GroupPost, Event, EventResponse,
    Notification, Album, Photo, MarketplaceItem, MarketplaceItemImage, SavedPost,
    LiveVideo, LiveVideoViewer, Report, BlockedUser, PrivacySetting, NotificationSetting,
    Memory, Video, VideoView, Playlist, PlaylistVideo, Poll, PollOption, PollVote,
    Fundraiser, Donation, SearchHistory, ActivityLog, Advertisement, AdImpression,
    AdClick, Badge, UserBadge
)


# ==================== CUSTOM FILTERS ====================

class OnlineStatusFilter(admin.SimpleListFilter):
    title = 'Online Status'
    parameter_name = 'online_status'

    def lookups(self, request, model_admin):
        return (
            ('online', 'Online'),
            ('offline', 'Offline'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'online':
            return queryset.filter(is_online=True)
        if self.value() == 'offline':
            return queryset.filter(is_online=False)


class RecentActivityFilter(admin.SimpleListFilter):
    title = 'Recent Activity'
    parameter_name = 'recent_activity'

    def lookups(self, request, model_admin):
        return (
            ('today', 'Today'),
            ('week', 'This Week'),
            ('month', 'This Month'),
        )

    def queryset(self, request, queryset):
        now = timezone.now()
        if self.value() == 'today':
            return queryset.filter(last_seen__date=now.date())
        if self.value() == 'week':
            return queryset.filter(last_seen__gte=now - timezone.timedelta(days=7))
        if self.value() == 'month':
            return queryset.filter(last_seen__gte=now - timezone.timedelta(days=30))


# ==================== INLINE ADMIN CLASSES ====================

class PostMediaInline(admin.TabularInline):
    model = PostMedia
    extra = 1
    fields = ('media_type', 'file', 'thumbnail', 'description', 'order')
    readonly_fields = ('width', 'height', 'duration')


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ('author', 'content', 'created_at')
    readonly_fields = ('created_at',)
    can_delete = False
    max_num = 5


class ReactionInline(admin.TabularInline):
    model = Reaction
    extra = 0
    fields = ('user', 'reaction_type', 'created_at')
    readonly_fields = ('created_at',)
    can_delete = False
    max_num = 10


class PageRoleInline(admin.TabularInline):
    model = PageRole
    extra = 1
    fields = ('user', 'role', 'created_at')
    readonly_fields = ('created_at',)


class GroupMemberInline(admin.TabularInline):
    model = GroupMember
    extra = 0
    fields = ('user', 'role', 'status', 'joined_at')
    readonly_fields = ('joined_at',)


class MarketplaceItemImageInline(admin.TabularInline):
    model = MarketplaceItemImage
    extra = 1
    fields = ('image', 'order')


class PollOptionInline(admin.TabularInline):
    model = PollOption
    extra = 3
    fields = ('text', 'order')


class PlaylistVideoInline(admin.TabularInline):
    model = PlaylistVideo
    extra = 1
    fields = ('video', 'order', 'added_at')
    readonly_fields = ('added_at',)


# ==================== USER ADMIN ====================

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'full_name', 'online_indicator', 'is_verified', 'date_joined', 'post_count')
    list_filter = ('is_staff', 'is_verified', OnlineStatusFilter, RecentActivityFilter, 'date_joined', 'gender')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')
    readonly_fields = ('date_joined', 'last_login', 'last_seen', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Account Info', {
            'fields': ('username', 'email', 'password', 'is_verified', 'is_online')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'date_of_birth', 'gender', 'phone_number', 'bio')
        }),
        ('Profile Media', {
            'fields': ('profile_picture', 'cover_photo')
        }),
        ('Location & Work', {
            'fields': ('hometown', 'current_city', 'workplace', 'education')
        }),
        ('Other', {
            'fields': ('relationship_status', 'website')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important Dates', {
            'fields': ('last_login', 'last_seen', 'date_joined', 'created_at', 'updated_at')
        }),
    )
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}" if obj.first_name else obj.username
    full_name.short_description = 'Full Name'
    
    def online_indicator(self, obj):
        if obj.is_online:
            return format_html('<span style="color: green;">● Online</span>')
        return format_html('<span style="color: gray;">● Offline</span>')
    online_indicator.short_description = 'Status'
    
    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Posts'


# ==================== SOCIAL CONNECTIONS ====================

@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('from_user__username', 'to_user__username')
    date_hierarchy = 'created_at'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
    search_fields = ('follower__username', 'following__username')
    date_hierarchy = 'created_at'


# ==================== POSTS & CONTENT ====================

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'post_type', 'content_preview', 'privacy', 'reaction_count', 'comment_count', 'created_at')
    list_filter = ('post_type', 'privacy', 'created_at', 'is_pinned', 'is_archived')
    search_fields = ('author__username', 'content', 'location')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    inlines = [PostMediaInline, ReactionInline, CommentInline]
    
    fieldsets = (
        ('Post Information', {
            'fields': ('author', 'post_type', 'content', 'feeling', 'location')
        }),
        ('Privacy & Settings', {
            'fields': ('privacy', 'tagged_users', 'is_pinned', 'is_archived', 'comments_enabled')
        }),
        ('Sharing', {
            'fields': ('shared_post',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
    
    def reaction_count(self, obj):
        return obj.reactions.count()
    reaction_count.short_description = 'Reactions'
    
    def comment_count(self, obj):
        return obj.comments.count()
    comment_count.short_description = 'Comments'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'content_preview', 'is_edited', 'created_at')
    list_filter = ('is_edited', 'created_at')
    search_fields = ('author__username', 'content')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'reaction_type', 'created_at')
    list_filter = ('reaction_type', 'created_at')
    search_fields = ('user__username', 'post__content')
    date_hierarchy = 'created_at'


# ==================== STORIES ====================

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'story_type', 'privacy', 'view_count', 'created_at', 'expires_at', 'is_expired')
    list_filter = ('story_type', 'privacy', 'created_at')
    search_fields = ('user__username', 'text_content')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    
    def view_count(self, obj):
        return obj.views.count()
    view_count.short_description = 'Views'
    
    def is_expired(self, obj):
        is_expired = obj.expires_at < timezone.now()
        if is_expired:
            return format_html('<span style="color: red;">Expired</span>')
        return format_html('<span style="color: green;">Active</span>')
    is_expired.short_description = 'Status'


# ==================== MESSENGER ====================

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('conversation_type', 'name', 'participant_count', 'created_by', 'created_at')
    list_filter = ('conversation_type', 'created_at')
    search_fields = ('name', 'participants__username')
    date_hierarchy = 'created_at'
    
    def participant_count(self, obj):
        return obj.participants.count()
    participant_count.short_description = 'Participants'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'conversation', 'message_type', 'content_preview', 'is_deleted', 'created_at')
    list_filter = ('message_type', 'is_deleted', 'is_edited', 'created_at')
    search_fields = ('sender__username', 'content')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    
    def content_preview(self, obj):
        if obj.content:
            return obj.content[:30] + '...' if len(obj.content) > 30 else obj.content
        return f'[{obj.message_type}]'
    content_preview.short_description = 'Content'


# ==================== PAGES ====================

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'category', 'is_verified', 'like_count', 'created_at')
    list_filter = ('category', 'is_verified', 'is_published', 'created_at')
    search_fields = ('name', 'username', 'description')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [PageRoleInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'username', 'category', 'description')
        }),
        ('Media', {
            'fields': ('profile_picture', 'cover_photo')
        }),
        ('Contact Information', {
            'fields': ('website', 'email', 'phone', 'address')
        }),
        ('Settings', {
            'fields': ('is_verified', 'is_published', 'created_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def like_count(self, obj):
        return obj.likes.count()
    like_count.short_description = 'Likes'


# ==================== GROUPS ====================

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'privacy', 'member_count', 'created_by', 'created_at')
    list_filter = ('privacy', 'created_at')
    search_fields = ('name', 'description', 'tags')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [GroupMemberInline]
    
    def member_count(self, obj):
        return obj.members.filter(status='approved').count()
    member_count.short_description = 'Members'


# ==================== EVENTS ====================

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_type', 'host', 'start_datetime', 'location', 'response_summary')
    list_filter = ('event_type', 'start_datetime')
    search_fields = ('name', 'description', 'location')
    date_hierarchy = 'start_datetime'
    readonly_fields = ('created_at', 'updated_at')
    
    def response_summary(self, obj):
        going = obj.responses.filter(response='going').count()
        interested = obj.responses.filter(response='interested').count()
        return f"Going: {going}, Interested: {interested}"
    response_summary.short_description = 'Responses'


# ==================== NOTIFICATIONS ====================

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'notification_type', 'title', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('recipient__username', 'title', 'message')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)


# ==================== MARKETPLACE ====================

@admin.register(MarketplaceItem)
class MarketplaceItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'price', 'category', 'condition', 'is_available', 'created_at')
    list_filter = ('category', 'condition', 'is_available', 'is_sold', 'created_at')
    search_fields = ('title', 'description', 'seller__username', 'location')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [MarketplaceItemImageInline]


# ==================== VIDEOS ====================

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploader', 'duration_display', 'view_count', 'privacy', 'created_at')
    list_filter = ('privacy', 'category', 'created_at')
    search_fields = ('title', 'description', 'uploader__username', 'tags')
    readonly_fields = ('view_count', 'created_at', 'updated_at')
    
    def duration_display(self, obj):
        minutes = obj.duration // 60
        seconds = obj.duration % 60
        return f"{minutes}:{seconds:02d}"
    duration_display.short_description = 'Duration'


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'privacy', 'video_count', 'created_at')
    list_filter = ('privacy', 'created_at')
    search_fields = ('name', 'description', 'user__username')
    inlines = [PlaylistVideoInline]
    
    def video_count(self, obj):
        return obj.videos.count()
    video_count.short_description = 'Videos'


# ==================== POLLS ====================

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'post', 'vote_count', 'expires_at', 'is_expired')
    list_filter = ('created_at', 'expires_at')
    search_fields = ('question',)
    inlines = [PollOptionInline]
    readonly_fields = ('created_at',)
    
    def vote_count(self, obj):
        return obj.votes.count()
    vote_count.short_description = 'Votes'
    
    def is_expired(self, obj):
        return obj.expires_at < timezone.now()
    is_expired.boolean = True
    is_expired.short_description = 'Expired'


# ==================== FUNDRAISERS ====================

@admin.register(Fundraiser)
class FundraiserAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'goal_amount', 'current_amount', 'progress_bar', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'creator__username', 'beneficiary_name')
    readonly_fields = ('current_amount', 'created_at', 'updated_at')
    
    def progress_bar(self, obj):
        if obj.goal_amount > 0:
            percentage = (obj.current_amount / obj.goal_amount) * 100
            color = 'green' if percentage >= 100 else 'orange' if percentage >= 50 else 'red'
            return format_html(
                '<div style="width:100px; background-color:#f0f0f0;">'
                '<div style="width:{}px; background-color:{}; height:20px;"></div>'
                '</div> {:.1f}%',
                min(percentage, 100), color, percentage
            )
        return '0%'
    progress_bar.short_description = 'Progress'


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('fundraiser', 'donor_display', 'amount', 'is_anonymous', 'created_at')
    list_filter = ('is_anonymous', 'created_at')
    search_fields = ('fundraiser__title', 'donor__username', 'transaction_id')
    readonly_fields = ('created_at',)
    
    def donor_display(self, obj):
        return 'Anonymous' if obj.is_anonymous else obj.donor.username
    donor_display.short_description = 'Donor'


# ==================== REPORTS & MODERATION ====================

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'content_type', 'reason', 'status', 'created_at')
    list_filter = ('content_type', 'reason', 'status', 'created_at')
    search_fields = ('reporter__username', 'description')
    readonly_fields = ('created_at', 'reviewed_at')
    date_hierarchy = 'created_at'
    
    actions = ['mark_as_resolved', 'mark_as_dismissed']
    
    def mark_as_resolved(self, request, queryset):
        queryset.update(status='resolved', reviewed_by=request.user, reviewed_at=timezone.now())
    mark_as_resolved.short_description = 'Mark selected reports as resolved'
    
    def mark_as_dismissed(self, request, queryset):
        queryset.update(status='dismissed', reviewed_by=request.user, reviewed_at=timezone.now())
    mark_as_dismissed.short_description = 'Mark selected reports as dismissed'


# ==================== ADVERTISEMENTS ====================

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'advertiser', 'ad_type', 'status', 'budget', 'spent', 'ctr', 'start_date', 'end_date')
    list_filter = ('ad_type', 'status', 'placement', 'created_at')
    search_fields = ('title', 'description', 'advertiser__username')
    readonly_fields = ('spent', 'impressions', 'clicks', 'created_at', 'updated_at')
    
    def ctr(self, obj):
        if obj.impressions > 0:
            click_through_rate = (obj.clicks / obj.impressions) * 100
            return f"{click_through_rate:.2f}%"
        return "0%"
    ctr.short_description = 'CTR'


# ==================== SETTINGS ====================

@admin.register(PrivacySetting)
class PrivacySettingAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_visibility', 'post_visibility', 'updated_at')
    search_fields = ('user__username',)
    readonly_fields = ('updated_at',)


@admin.register(NotificationSetting)
class NotificationSettingAdmin(admin.ModelAdmin):
    list_display = ('user', 'push_messages', 'email_messages', 'updated_at')
    search_fields = ('user__username',)
    readonly_fields = ('updated_at',)


# ==================== ACTIVITY & ANALYTICS ====================

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'ip_address', 'created_at')
    list_filter = ('action', 'created_at')
    search_fields = ('user__username', 'ip_address')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'


# ==================== ADMIN SITE CUSTOMIZATION ====================

admin.site.site_header = "Facebook Clone Administration"
admin.site.site_title = "Facebook Clone Admin"
admin.site.index_title = "Welcome to Facebook Clone Admin Panel"