"""
views.py
Complete views for Facebook-like application
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db.models import Q, Count, Prefetch
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta
from .models import *


# ==================== AUTHENTICATION ====================

def register_view(request):
    """User registration"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            gender=gender
        )
        
        # Create privacy and notification settings
        PrivacySetting.objects.create(user=user)
        NotificationSetting.objects.create(user=user)
        
        login(request, user)
        messages.success(request, 'Registration successful!')
        return redirect('newsfeed')
    
    return render(request, 'register.html')


def login_view(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            user.is_online = True
            user.save()
            
            # Log activity
            ActivityLog.objects.create(
                user=user,
                action='login',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            return redirect('newsfeed')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'login.html')


@login_required
def logout_view(request):
    """User logout"""
    request.user.is_online = False
    request.user.save()
    
    ActivityLog.objects.create(
        user=request.user,
        action='logout',
        ip_address=request.META.get('REMOTE_ADDR')
    )
    
    logout(request)
    return redirect('login')


# ==================== NEWSFEED ====================

@login_required
def newsfeed_view(request):
    """Main newsfeed"""
    # Get friends
    friends = User.objects.filter(
        Q(friendships_received__from_user=request.user, friendships_received__status='accepted') |
        Q(friendships_sent__to_user=request.user, friendships_sent__status='accepted')
    ).distinct()
    
    # Get posts from friends and self
    posts = Post.objects.filter(
        Q(author=request.user) | Q(author__in=friends),
        is_archived=False
    ).select_related('author').prefetch_related(
        'reactions', 'comments', 'media', 'tagged_users'
    ).order_by('-created_at')[:50]
    
    # Get stories
    stories = Story.objects.filter(
        Q(user=request.user) | Q(user__in=friends),
        expires_at__gt=timezone.now()
    ).select_related('user').order_by('-created_at')
    
    # Friend suggestions
    friend_suggestions = User.objects.exclude(
        Q(id=request.user.id) |
        Q(friendships_received__from_user=request.user) |
        Q(friendships_sent__to_user=request.user)
    )[:10]
    
    context = {
        'posts': posts,
        'stories': stories,
        'friend_suggestions': friend_suggestions,
    }
    
    return render(request, 'newsfeed.html', context)


# ==================== PROFILE ====================

@login_required
def profile_view(request, username):
    """User profile"""
    profile_user = get_object_or_404(User, username=username)
    
    # Check friendship status
    is_friend = Friendship.objects.filter(
        Q(from_user=request.user, to_user=profile_user, status='accepted') |
        Q(from_user=profile_user, to_user=request.user, status='accepted')
    ).exists()
    
    friend_request_sent = Friendship.objects.filter(
        from_user=request.user, to_user=profile_user, status='pending'
    ).exists()
    
    friend_request_received = Friendship.objects.filter(
        from_user=profile_user, to_user=request.user, status='pending'
    ).exists()
    
    # Get user's posts
    posts = Post.objects.filter(
        author=profile_user,
        is_archived=False
    ).select_related('author').prefetch_related(
        'reactions', 'comments', 'media'
    ).order_by('-created_at')[:20]
    
    # Get friends count
    friends_count = Friendship.objects.filter(
        Q(from_user=profile_user, status='accepted') |
        Q(to_user=profile_user, status='accepted')
    ).count()
    
    # Get photos
    photos = Photo.objects.filter(user=profile_user).order_by('-created_at')[:9]
    
    context = {
        'profile_user': profile_user,
        'is_friend': is_friend,
        'friend_request_sent': friend_request_sent,
        'friend_request_received': friend_request_received,
        'posts': posts,
        'friends_count': friends_count,
        'photos': photos,
    }
    
    return render(request, 'profile.html', context)


@login_required
def edit_profile_view(request):
    """Edit user profile"""
    if request.method == 'POST':
        user = request.user
        user.bio = request.POST.get('bio', '')
        user.hometown = request.POST.get('hometown', '')
        user.current_city = request.POST.get('current_city', '')
        user.relationship_status = request.POST.get('relationship_status', '')
        user.workplace = request.POST.get('workplace', '')
        user.education = request.POST.get('education', '')
        user.website = request.POST.get('website', '')
        
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        
        if 'cover_photo' in request.FILES:
            user.cover_photo = request.FILES['cover_photo']
        
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile', username=user.username)
    
    return render(request, 'edit_profile.html')


# ==================== POSTS ====================

@login_required
@require_POST
def create_post_view(request):
    """Create a new post"""
    content = request.POST.get('content', '')
    feeling = request.POST.get('feeling', '')
    location = request.POST.get('location', '')
    privacy = request.POST.get('privacy', 'friends')
    
    post = Post.objects.create(
        author=request.user,
        content=content,
        feeling=feeling,
        location=location,
        privacy=privacy
    )
    
    # Handle media uploads
    if 'media' in request.FILES:
        for media_file in request.FILES.getlist('media'):
            PostMedia.objects.create(
                post=post,
                media_type='image',
                file=media_file
            )
    
    messages.success(request, 'Post created successfully!')
    return redirect('newsfeed')


@login_required
def post_detail_view(request, post_id):
    """Single post detail"""
    post = get_object_or_404(
        Post.objects.select_related('author').prefetch_related(
            'reactions', 'comments__author', 'media'
        ),
        id=post_id
    )
    
    context = {'post': post}
    return render(request, 'post_detail.html', context)


@login_required
@require_POST
def delete_post_view(request, post_id):
    """Delete a post"""
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    messages.success(request, 'Post deleted successfully!')
    return redirect('newsfeed')


@login_required
@require_POST
def react_to_post_view(request, post_id):
    """Add reaction to post"""
    post = get_object_or_404(Post, id=post_id)
    reaction_type = request.POST.get('reaction_type', 'like')
    
    reaction, created = Reaction.objects.get_or_create(
        user=request.user,
        post=post,
        defaults={'reaction_type': reaction_type}
    )
    
    if not created:
        if reaction.reaction_type == reaction_type:
            reaction.delete()
            return JsonResponse({'status': 'removed'})
        else:
            reaction.reaction_type = reaction_type
            reaction.save()
    
    return JsonResponse({'status': 'success', 'reaction': reaction_type})


@login_required
@require_POST
def comment_on_post_view(request, post_id):
    """Add comment to post"""
    post = get_object_or_404(Post, id=post_id)
    content = request.POST.get('content', '')
    
    if content:
        Comment.objects.create(
            post=post,
            author=request.user,
            content=content
        )
        
        # Create notification for post author
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                sender=request.user,
                notification_type='post_comment',
                title='New comment on your post',
                message=f'{request.user.get_full_name()} commented on your post'
            )
    
    return redirect('post_detail', post_id=post_id)


# ==================== FRIENDS ====================

@login_required
def friends_view(request):
    """List of friends"""
    friends = User.objects.filter(
        Q(friendships_received__from_user=request.user, friendships_received__status='accepted') |
        Q(friendships_sent__to_user=request.user, friendships_sent__status='accepted')
    ).distinct()
    
    # Friend requests
    friend_requests = Friendship.objects.filter(
        to_user=request.user,
        status='pending'
    ).select_related('from_user')
    
    context = {
        'friends': friends,
        'friend_requests': friend_requests,
    }
    
    return render(request, 'friends.html', context)


@login_required
@require_POST
def send_friend_request_view(request, user_id):
    """Send friend request"""
    to_user = get_object_or_404(User, id=user_id)
    
    if request.user == to_user:
        messages.error(request, 'You cannot send friend request to yourself')
        return redirect('profile', username=to_user.username)
    
    friendship, created = Friendship.objects.get_or_create(
        from_user=request.user,
        to_user=to_user,
        defaults={'status': 'pending'}
    )
    
    if created:
        # Create notification
        Notification.objects.create(
            recipient=to_user,
            sender=request.user,
            notification_type='friend_request',
            title='New friend request',
            message=f'{request.user.get_full_name()} sent you a friend request'
        )
        messages.success(request, 'Friend request sent!')
    else:
        messages.info(request, 'Friend request already sent')
    
    return redirect('profile', username=to_user.username)


@login_required
@require_POST
def accept_friend_request_view(request, friendship_id):
    """Accept friend request"""
    friendship = get_object_or_404(
        Friendship,
        id=friendship_id,
        to_user=request.user,
        status='pending'
    )
    
    friendship.status = 'accepted'
    friendship.save()
    
    # Create notification
    Notification.objects.create(
        recipient=friendship.from_user,
        sender=request.user,
        notification_type='friend_accepted',
        title='Friend request accepted',
        message=f'{request.user.get_full_name()} accepted your friend request'
    )
    
    messages.success(request, 'Friend request accepted!')
    return redirect('friends')


@login_required
@require_POST
def unfriend_view(request, user_id):
    """Unfriend a user"""
    user = get_object_or_404(User, id=user_id)
    
    Friendship.objects.filter(
        Q(from_user=request.user, to_user=user) |
        Q(from_user=user, to_user=request.user)
    ).delete()
    
    messages.success(request, 'Unfriended successfully!')
    return redirect('friends')


# ==================== MESSENGER ====================

@login_required
def messenger_view(request):
    """Messenger inbox"""
    conversations = Conversation.objects.filter(
        participants=request.user
    ).prefetch_related('participants', 'messages').order_by('-updated_at')
    
    context = {'conversations': conversations}
    return render(request, 'messenger.html', context)


@login_required
def conversation_view(request, conversation_id):
    """Single conversation"""
    conversation = get_object_or_404(
        Conversation.objects.prefetch_related('participants', 'messages__sender'),
        id=conversation_id,
        participants=request.user
    )
    
    messages_list = conversation.messages.select_related('sender').order_by('created_at')
    
    # Mark messages as read
    unread_messages = messages_list.exclude(sender=request.user)
    for msg in unread_messages:
        MessageRead.objects.get_or_create(message=msg, user=request.user)
    
    context = {
        'conversation': conversation,
        'messages': messages_list,
    }
    
    return render(request, 'conversation.html', context)


@login_required
@require_POST
def send_message_view(request, conversation_id):
    """Send a message"""
    conversation = get_object_or_404(
        Conversation,
        id=conversation_id,
        participants=request.user
    )
    
    content = request.POST.get('content', '')
    
    if content:
        Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content
        )
        conversation.updated_at = timezone.now()
        conversation.save()
    
    return redirect('conversation', conversation_id=conversation_id)


# ==================== GROUPS ====================

@login_required
def groups_view(request):
    """List of groups"""
    my_groups = Group.objects.filter(
        members__user=request.user,
        members__status='approved'
    ).annotate(member_count=Count('members'))
    
    discover_groups = Group.objects.filter(
        privacy='public'
    ).exclude(
        members__user=request.user
    ).annotate(member_count=Count('members'))[:10]
    
    context = {
        'my_groups': my_groups,
        'discover_groups': discover_groups,
    }
    
    return render(request, 'groups.html', context)


@login_required
def group_detail_view(request, group_id):
    """Group detail page"""
    group = get_object_or_404(Group, id=group_id)
    
    is_member = GroupMember.objects.filter(
        group=group,
        user=request.user,
        status='approved'
    ).exists()
    
    posts = GroupPost.objects.filter(
        group=group
    ).select_related('author').order_by('-is_pinned', '-created_at')[:20]
    
    members = group.members.filter(status='approved').select_related('user')[:12]
    member_count = group.members.filter(status='approved').count()
    
    context = {
        'group': group,
        'is_member': is_member,
        'posts': posts,
        'members': members,
        'member_count': member_count,
    }
    
    return render(request, 'group_detail.html', context)


@login_required
@require_POST
def join_group_view(request, group_id):
    """Join a group"""
    group = get_object_or_404(Group, id=group_id)
    
    status = 'approved' if group.privacy == 'public' else 'pending'
    
    GroupMember.objects.get_or_create(
        group=group,
        user=request.user,
        defaults={'status': status}
    )
    
    messages.success(request, 'Joined group!' if status == 'approved' else 'Request sent!')
    return redirect('group_detail', group_id=group_id)


# ==================== NOTIFICATIONS ====================

@login_required
def notifications_view(request):
    """List notifications"""
    notifications = Notification.objects.filter(
        recipient=request.user
    ).select_related('sender').order_by('-created_at')[:50]
    
    # Mark as read
    notifications.filter(is_read=False).update(is_read=True)
    
    context = {'notifications': notifications}
    return render(request, 'notifications.html', context)


# ==================== SEARCH ====================

@login_required
def search_view(request):
    """Search functionality"""
    query = request.GET.get('q', '')
    
    if query:
        # Search users
        users = User.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(username__icontains=query)
        )[:20]
        
        # Search posts
        posts = Post.objects.filter(
            content__icontains=query
        ).select_related('author')[:20]
        
        # Search groups
        groups = Group.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )[:10]
        
        # Search pages
        pages = Page.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )[:10]
        
        # Save search history
        SearchHistory.objects.create(
            user=request.user,
            query=query
        )
    else:
        users = posts = groups = pages = []
    
    context = {
        'query': query,
        'users': users,
        'posts': posts,
        'groups': groups,
        'pages': pages,
    }
    
    return render(request, 'search.html', context)


# ==================== MARKETPLACE ====================

@login_required
def marketplace_view(request):
    """Marketplace listings"""
    items = MarketplaceItem.objects.filter(
        is_available=True
    ).select_related('seller').prefetch_related('images').order_by('-created_at')[:50]
    
    context = {'items': items}
    return render(request, 'marketplace.html', context)


# ==================== WATCH (VIDEOS) ====================

@login_required
def watch_view(request):
    """Watch videos"""
    videos = Video.objects.filter(
        privacy='public'
    ).select_related('uploader').order_by('-created_at')[:30]
    
    context = {'videos': videos}
    return render(request, 'watch.html', context)


# ==================== PAGES ====================

@login_required
def pages_view(request):
    """List pages"""
    my_pages = Page.objects.filter(created_by=request.user)
    liked_pages = Page.objects.filter(likes__user=request.user)
    
    context = {
        'my_pages': my_pages,
        'liked_pages': liked_pages,
    }
    
    return render(request, 'pages.html', context)


# ==================== SETTINGS ====================

@login_required
def settings_view(request):
    """User settings"""
    privacy_settings = request.user.privacy_settings
    notification_settings = request.user.notification_settings
    
    if request.method == 'POST':
        # Update settings
        privacy_settings.profile_visibility = request.POST.get('profile_visibility')
        privacy_settings.post_visibility = request.POST.get('post_visibility')
        privacy_settings.save()
        
        messages.success(request, 'Settings updated successfully!')
        return redirect('settings')
    
    context = {
        'privacy_settings': privacy_settings,
        'notification_settings': notification_settings,
    }
    
    return render(request, 'settings.html', context)