# Facebook Clone - Full-Stack Social Media Platform

A comprehensive Facebook clone built with Django, featuring all major Facebook functionalities including posts, stories, messaging, groups, events, marketplace, and more.

## 👨‍💻 Developer Information

**Developer:** Steve Ongera  
**Contact:** 0112284093  
**Email:** steveongera001@gmail.com  
**Project Type:** Full-Stack Social Media Platform  
**Framework:** Django (Python)

---

## 🚀 Features

### Core Social Features
- ✅ **User Profiles** - Complete profile management with bio, photos, and personal information
- ✅ **Friend System** - Send, accept, decline friend requests with blocking capability
- ✅ **Follow System** - Follow users and pages
- ✅ **News Feed** - Dynamic feed with posts from friends and followed pages
- ✅ **Post Creation** - Text, photo, video posts with privacy controls
- ✅ **Reactions** - Like, Love, Haha, Wow, Sad, Angry reactions
- ✅ **Comments** - Nested comments with reactions and media attachments
- ✅ **Sharing** - Share posts with custom messages

### Content Features
- 📖 **Stories** - 24-hour disappearing stories (photo/video/text)
- 📸 **Photo Albums** - Create albums and organize photos
- 🎥 **Video Platform** - Upload videos with playlists (Watch feature)
- 🎬 **Live Streaming** - Broadcast live videos
- 🗳️ **Polls** - Create polls in posts
- 💾 **Saved Posts** - Save posts for later viewing

### Communication
- 💬 **Messenger** - Real-time messaging with text, images, videos, audio
- 👥 **Group Chats** - Multi-user conversations
- 👁️ **Read Receipts** - Message read status
- 😊 **Message Reactions** - React to messages with emojis
- 📎 **File Sharing** - Send files, GIFs, stickers

### Pages & Groups
- 📄 **Pages** - Create business/brand pages with role management
- 👥 **Groups** - Public, private, and secret groups
- 🎯 **Group Posts** - Post and interact within groups
- 👔 **Page Roles** - Admin, Editor, Moderator, Advertiser, Analyst

### Events
- 📅 **Event Creation** - Create and manage events
- ✅ **RSVP System** - Going, Interested, Not Going responses
- 👥 **Co-Hosts** - Multiple event hosts
- 🔔 **Event Reminders** - Notification system for events

### Marketplace
- 🛍️ **Item Listings** - Buy and sell items
- 📷 **Multiple Images** - Upload multiple product photos
- 🏷️ **Categories** - Organized product categories
- 💰 **Pricing** - Set prices and conditions

### Additional Features
- 🔔 **Notifications** - Comprehensive notification system
- 🔒 **Privacy Controls** - Granular privacy settings
- 🚫 **Blocking & Reporting** - User safety features
- 📊 **Activity Logs** - Track user activities
- 💰 **Fundraisers** - Create fundraising campaigns
- 🎯 **Advertisements** - Ad system with targeting
- 🏆 **Badges** - User achievements and badges
- 🕰️ **Memories** - "On This Day" feature
- 🔍 **Search** - Search users, posts, pages, groups

---

## 📋 Prerequisites

- Python 3.8+
- Django 4.2+
- PostgreSQL 12+ (recommended) or SQLite for development
- Redis (for caching and real-time features)
- Celery (for background tasks)

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd facebook-clone
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the root directory:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL)
DB_NAME=facebook_clone
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# AWS S3 (for media storage in production)
USE_S3=False
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1

# Cloudinary (alternative for media)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

### 5. Database Setup

```bash
# Create PostgreSQL database
createdb facebook_clone

# Run migrations
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Collect Static Files

```bash
python manage.py collectstatic
```

### 8. Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` to see the application.

---

## 📦 Required Dependencies

Create a `requirements.txt` file:

```txt
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.0
Pillow==10.1.0
psycopg2-binary==2.9.9
python-decouple==3.8
celery==5.3.4
redis==5.0.1
django-redis==5.4.0
channels==4.0.0
channels-redis==4.1.0
daphne==4.0.0
django-filter==23.3
django-storages==1.14.2
boto3==1.29.7
cloudinary==1.36.0
django-cloudinary-storage==0.3.0
stripe==7.4.0
gunicorn==21.2.0
whitenoise==6.6.0
```

---

## 🗄️ Database Schema

### Main Tables

1. **Users** - Extended Django user model
2. **Friendships** - Friend connections
3. **Posts** - User posts with media
4. **Comments** - Post comments with nesting
5. **Reactions** - Post and comment reactions
6. **Stories** - 24-hour stories
7. **Messages** - Chat messages
8. **Conversations** - Chat threads
9. **Pages** - Business pages
10. **Groups** - User groups
11. **Events** - Social events
12. **Notifications** - User notifications
13. **MarketplaceItems** - Items for sale
14. **Videos** - Video content
15. **LiveVideos** - Live streaming
16. **Polls** - Post polls
17. **Fundraisers** - Fundraising campaigns

---

## 🔧 Configuration

### Settings Structure

```
facebook_clone/
├── settings/
│   ├── base.py        # Base settings
│   ├── development.py # Development settings
│   ├── production.py  # Production settings
│   └── testing.py     # Testing settings
```

### Media Files

Configure media file handling in `settings/base.py`:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# For production with S3
if USE_S3:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

---

## 🚀 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/refresh/` - Refresh token

### Users
- `GET /api/users/` - List users
- `GET /api/users/:id/` - User details
- `PATCH /api/users/:id/` - Update user
- `GET /api/users/:id/friends/` - User's friends
- `POST /api/users/:id/friend-request/` - Send friend request

### Posts
- `GET /api/posts/` - List posts (feed)
- `POST /api/posts/` - Create post
- `GET /api/posts/:id/` - Post details
- `PATCH /api/posts/:id/` - Update post
- `DELETE /api/posts/:id/` - Delete post
- `POST /api/posts/:id/react/` - React to post
- `POST /api/posts/:id/comment/` - Comment on post

### Stories
- `GET /api/stories/` - List active stories
- `POST /api/stories/` - Create story
- `DELETE /api/stories/:id/` - Delete story
- `POST /api/stories/:id/view/` - Mark story as viewed

### Messages
- `GET /api/conversations/` - List conversations
- `POST /api/conversations/` - Create conversation
- `GET /api/conversations/:id/messages/` - Get messages
- `POST /api/conversations/:id/messages/` - Send message
- `POST /api/messages/:id/react/` - React to message

### Pages
- `GET /api/pages/` - List pages
- `POST /api/pages/` - Create page
- `GET /api/pages/:id/` - Page details
- `POST /api/pages/:id/like/` - Like page

### Groups
- `GET /api/groups/` - List groups
- `POST /api/groups/` - Create group
- `GET /api/groups/:id/` - Group details
- `POST /api/groups/:id/join/` - Join group
- `GET /api/groups/:id/posts/` - Group posts

### Events
- `GET /api/events/` - List events
- `POST /api/events/` - Create event
- `GET /api/events/:id/` - Event details
- `POST /api/events/:id/respond/` - RSVP to event

### Marketplace
- `GET /api/marketplace/` - List items
- `POST /api/marketplace/` - Create listing
- `GET /api/marketplace/:id/` - Item details

---

## 🔐 Authentication

The project uses JWT (JSON Web Tokens) for authentication:

```python
# Install JWT package
pip install djangorestframework-simplejwt

# Add to settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

# Token expiration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}
```

---

## 🎨 Frontend Integration

### Recommended Frontend Stack

- **React.js** or **Vue.js** for UI
- **Redux** or **Vuex** for state management
- **Socket.io** for real-time features
- **Tailwind CSS** for styling
- **Axios** for API requests

### Example API Call (React)

```javascript
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

// Get posts
const getPosts = async () => {
  const response = await axios.get(`${API_URL}/posts/`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  return response.data;
};

// Create post
const createPost = async (postData) => {
  const response = await axios.post(`${API_URL}/posts/`, postData, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'multipart/form-data'
    }
  });
  return response.data;
};
```

---

## 🔄 Real-Time Features (WebSockets)

### Setup Channels for WebSockets

```python
# Install channels
pip install channels channels-redis

# Add to INSTALLED_APPS
INSTALLED_APPS = [
    'channels',
    # ...
]

# Configure ASGI
ASGI_APPLICATION = 'facebook_clone.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}
```

### Consumer Example (Messaging)

```python
# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
```

---

## 📧 Email Configuration

### Gmail SMTP Setup

```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Generate from Google
```

### Sending Notifications

```python
from django.core.mail import send_mail

def send_friend_request_email(to_user, from_user):
    send_mail(
        subject=f'{from_user.username} sent you a friend request',
        message=f'{from_user.username} wants to be your friend on Facebook Clone.',
        from_email='noreply@facebookclone.com',
        recipient_list=[to_user.email],
        fail_silently=False,
    )
```

---

## ⚡ Performance Optimization

### Caching with Redis

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Cache timeout
CACHE_TTL = 60 * 15  # 15 minutes

# views.py
from django.core.cache import cache

def get_user_feed(user_id):
    cache_key = f'user_feed_{user_id}'
    feed = cache.get(cache_key)
    
    if not feed:
        feed = Post.objects.filter(
            author__in=user.friends.all()
        ).order_by('-created_at')[:50]
        cache.set(cache_key, feed, CACHE_TTL)
    
    return feed
```

### Database Query Optimization

```python
# Use select_related for foreign keys
posts = Post.objects.select_related('author').all()

# Use prefetch_related for many-to-many
posts = Post.objects.prefetch_related('reactions', 'comments').all()

# Use only() to fetch specific fields
users = User.objects.only('username', 'profile_picture').all()
```

---

## 🧪 Testing

### Run Tests

```bash
python manage.py test
```

### Example Test

```python
# tests.py
from django.test import TestCase
from .models import User, Post

class PostTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_post_creation(self):
        post = Post.objects.create(
            author=self.user,
            content='Test post',
            privacy='public'
        )
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.content, 'Test post')
```

---

## 🚀 Deployment

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure proper `SECRET_KEY`
- [ ] Set up PostgreSQL database
- [ ] Configure S3 or Cloudinary for media
- [ ] Set up Redis for caching
- [ ] Configure email service
- [ ] Set up SSL certificate
- [ ] Configure domain and DNS
- [ ] Set up monitoring (Sentry)
- [ ] Configure backup system

### Deploy to Heroku

```bash
# Install Heroku CLI
heroku login

# Create app
heroku create facebook-clone-app

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Add Redis
heroku addons:create heroku-redis:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser
```

### Deploy to AWS

1. **EC2 Instance Setup**
2. **Install dependencies**
3. **Configure Nginx**
4. **Set up Gunicorn**
5. **Configure Supervisor**
6. **Set up RDS (PostgreSQL)**
7. **Configure S3 for media**
8. **Set up CloudFront CDN**

---

## 📊 Admin Panel

Access the Django admin panel at `/admin/`

**Features:**
- User management
- Content moderation
- Post/comment management
- Report handling
- Advertisement management
- Analytics dashboard

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License.

---

## 📞 Support & Contact

**Developer:** Steve Ongera  
**Phone:** 0112284093  
**Email:** steveongera001@gmail.com

For bug reports and feature requests, please create an issue on GitHub.

---

## 🙏 Acknowledgments

- Django Documentation
- Django REST Framework
- Django Channels
- Facebook for inspiration
- Open source community

---

## 🔮 Future Enhancements

- [ ] Voice/Video calls
- [ ] Dating feature
- [ ] Job listings
- [ ] Gaming integration
- [ ] Reels/Short videos
- [ ] AI-powered recommendations
- [ ] Advanced analytics
- [ ] Multi-language support
- [ ] Progressive Web App (PWA)
- [ ] Mobile apps (React Native)

---

**Made with ❤️ by Steve Ongera**