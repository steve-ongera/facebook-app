# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ==================== AUTHENTICATION ====================
    path('register/', views.register_view, name='register'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.newsfeed_view, name='newsfeed'),
    path('newsfeed/', views.newsfeed_view, name='newsfeed'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    
    # ==================== POSTS ====================
    path('post/create/', views.create_post_view, name='create_post'),
    path('post/<int:post_id>/', views.post_detail_view, name='post_detail'),
    path('post/<int:post_id>/delete/', views.delete_post_view, name='delete_post'),
    path('post/<int:post_id>/react/', views.react_to_post_view, name='react_to_post'),
    path('post/<int:post_id>/comment/', views.comment_on_post_view, name='comment_on_post'),
    path('friends/', views.friends_view, name='friends'),
    path('friends/request/<int:user_id>/', views.send_friend_request_view, name='send_friend_request'),
    path('friends/accept/<int:friendship_id>/', views.accept_friend_request_view, name='accept_friend_request'),
    path('friends/unfriend/<int:user_id>/', views.unfriend_view, name='unfriend'),
    
    # ==================== MESSENGER ====================
    path('messenger/', views.messenger_view, name='messenger'),
    path('messenger/<int:conversation_id>/', views.conversation_view, name='conversation'),
    path('messenger/<int:conversation_id>/send/', views.send_message_view, name='send_message'),
    path('groups/', views.groups_view, name='groups'),
    path('groups/<int:group_id>/', views.group_detail_view, name='group_detail'),
    path('groups/<int:group_id>/join/', views.join_group_view, name='join_group'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('search/', views.search_view, name='search'),
    path('marketplace/', views.marketplace_view, name='marketplace'),
    path('watch/', views.watch_view, name='watch'),
    path('pages/', views.pages_view, name='pages'),
    path('settings/', views.settings_view, name='settings'),
]