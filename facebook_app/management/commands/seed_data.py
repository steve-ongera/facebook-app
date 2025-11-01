"""
Django management command to seed realistic Kenyan data
Place this file at: facebook_app/management/commands/seed_data.py
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from datetime import timedelta, datetime
from decimal import Decimal
import random
from facebook_app.models import *


class Command(BaseCommand):
    help = 'Seeds the database with realistic Kenyan data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=50,
            help='Number of users to create'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding'
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            self.clear_data()
        
        num_users = options['users']
        self.stdout.write(f'Seeding database with {num_users} users...')
        
        users = self.create_users(num_users)
        self.create_friendships(users)
        self.create_follows(users)
        self.create_posts(users)
        self.create_stories(users)
        self.create_conversations(users)
        self.create_pages(users)
        self.create_groups(users)
        self.create_events(users)
        self.create_albums_photos(users)
        self.create_marketplace_items(users)
        self.create_videos(users)
        self.create_fundraisers(users)
        self.create_notifications(users)
        
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))

    def clear_data(self):
        """Clear all existing data"""
        models_to_clear = [
            ActivityLog, AdClick, AdImpression, Advertisement, UserBadge, Badge,
            Donation, Fundraiser, PollVote, PollOption, Poll, PlaylistVideo,
            Playlist, VideoView, Video, Memory, NotificationSetting, PrivacySetting,
            BlockedUser, Report, LiveVideoViewer, LiveVideo, SavedPost,
            MarketplaceItemImage, MarketplaceItem, Photo, Album, Notification,
            EventResponse, Event, GroupPost, GroupMember, Group, PageRole,
            PageLike, Page, MessageReaction, MessageRead, Message, Conversation,
            StoryView, Story, CommentReaction, Comment, Reaction, PostMedia,
            Post, Follow, Friendship, SearchHistory, User
        ]
        
        for model in models_to_clear:
            model.objects.all().delete()

    def create_users(self, count):
        """Create Kenyan users"""
        kenyan_first_names = [
            'Kamau', 'Wanjiru', 'Otieno', 'Akinyi', 'Kipchoge', 'Chebet',
            'Mwangi', 'Njeri', 'Ochieng', 'Atieno', 'Kiplagat', 'Jeptoo',
            'Kariuki', 'Wambui', 'Omondi', 'Awino', 'Rotich', 'Chepkemoi',
            'Ndung\'u', 'Nyambura', 'Onyango', 'Adhiambo', 'Kibet', 'Jepkorir',
            'Githinji', 'Waithera', 'Ouma', 'Akoth', 'Kirui', 'Chepkoech',
            'Muturi', 'Wangari', 'Okoth', 'Apiyo', 'Koech', 'Chepngetich',
            'Njoroge', 'Wanjiku', 'Owino', 'Auma', 'Kiptoo', 'Chepchirchir'
        ]
        
        kenyan_last_names = [
            'Kamau', 'Kipchoge', 'Omondi', 'Wanjiru', 'Mwangi', 'Rotich',
            'Otieno', 'Njeri', 'Kibet', 'Akinyi', 'Kariuki', 'Koech',
            'Ochieng', 'Wambui', 'Kiplagat', 'Adhiambo', 'Muturi', 'Kirui',
            'Onyango', 'Nyambura', 'Kiptoo', 'Awino', 'Githinji', 'Chebet'
        ]
        
        kenyan_cities = [
            'Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret', 'Thika',
            'Malindi', 'Kitale', 'Garissa', 'Kakamega', 'Meru', 'Nyeri',
            'Machakos', 'Kericho', 'Naivasha', 'Kiambu', 'Ruiru', 'Athi River'
        ]
        
        kenyan_workplaces = [
            'Safaricom PLC', 'Kenya Airways', 'Equity Bank', 'KCB Bank',
            'Co-operative Bank', 'Nation Media Group', 'Standard Group',
            'Brookside Dairy', 'East African Breweries', 'Kenya Power',
            'Nairobi Hospital', 'Aga Khan Hospital', 'University of Nairobi',
            'Strathmore University', 'KPMG Kenya', 'Deloitte Kenya',
            'Tusker Mattresses', 'Kenya Tourism Board', 'Bamburi Cement',
            'Bidco Africa', 'Ministry of Health', 'Ministry of Education'
        ]
        
        bios = [
            '🇰🇪 Proud Kenyan | Living life one day at a time',
            'Nairobi born and raised ✨ | Coffee enthusiast ☕',
            'Entrepreneur | Hustler | Dream Chaser 💪',
            'Tech enthusiast | Innovation lover | Nairobi',
            'Travel, Food, Music 🎵 | Exploring Kenya 🌍',
            'Family first ❤️ | Faith over everything 🙏',
            'Sports fanatic | Arsenal supporter ⚽',
            'Fitness enthusiast | Healthy living 💪',
            'Photographer | Capturing Kenya\'s beauty 📸',
            'Foodie | Nyama choma lover 🍖'
        ]
        
        users = []
        for i in range(count):
            first_name = random.choice(kenyan_first_names)
            last_name = random.choice(kenyan_last_names)
            username = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}"
            email = f"{username}@example.com"
            
            user = User.objects.create(
                username=username,
                email=email,
                password=make_password('password123'),
                first_name=first_name,
                last_name=last_name,
                bio=random.choice(bios),
                date_of_birth=datetime(
                    random.randint(1985, 2005),
                    random.randint(1, 12),
                    random.randint(1, 28)
                ).date(),
                gender=random.choice(['M', 'F']),
                phone_number=f"+254{random.randint(700000000, 799999999)}",
                hometown=random.choice(kenyan_cities),
                current_city=random.choice(kenyan_cities),
                relationship_status=random.choice(['Single', 'In a relationship', 'Married', 'It\'s complicated', '']),
                workplace=random.choice(kenyan_workplaces),
                education=random.choice(['University of Nairobi', 'Kenyatta University', 'Strathmore University', 
                                        'JKUAT', 'Moi University', 'Egerton University']),
                is_verified=random.choice([True] + [False] * 9),
                is_online=random.choice([True, False]),
                last_seen=timezone.now() - timedelta(minutes=random.randint(0, 1440))
            )
            users.append(user)
            
            # Create privacy settings
            PrivacySetting.objects.create(user=user)
            
            # Create notification settings
            NotificationSetting.objects.create(user=user)
        
        self.stdout.write(self.style.SUCCESS(f'Created {count} users'))
        return users

    def create_friendships(self, users):
        """Create friend connections"""
        friendships = []
        for user in users:
            num_friends = random.randint(5, 20)
            potential_friends = [u for u in users if u != user]
            friends = random.sample(potential_friends, min(num_friends, len(potential_friends)))
            
            for friend in friends:
                if not Friendship.objects.filter(
                    from_user=user, to_user=friend
                ).exists() and not Friendship.objects.filter(
                    from_user=friend, to_user=user
                ).exists():
                    Friendship.objects.create(
                        from_user=user,
                        to_user=friend,
                        status=random.choice(['accepted'] * 7 + ['pending'] * 2 + ['declined']),
                        created_at=timezone.now() - timedelta(days=random.randint(1, 365))
                    )
        
        self.stdout.write(self.style.SUCCESS(f'Created friendships'))

    def create_follows(self, users):
        """Create follow relationships"""
        for user in users:
            num_following = random.randint(3, 15)
            to_follow = random.sample([u for u in users if u != user], min(num_following, len(users)-1))
            
            for followed in to_follow:
                Follow.objects.create(
                    follower=user,
                    following=followed,
                    created_at=timezone.now() - timedelta(days=random.randint(1, 200))
                )
        
        self.stdout.write(self.style.SUCCESS(f'Created follows'))

    def create_posts(self, users):
        """Create posts with Kenyan content"""
        kenyan_statuses = [
            "Just had the best nyama choma at Carnivore! 🍖 #NairobiLife",
            "Traffic on Thika Road is crazy today 😤 #NairobiTraffic",
            "Watching the sunset at Diani Beach 🌅 Beautiful Kenya!",
            "Mpesa is down again? How am I supposed to live? 😭",
            "Congratulations to our national team! 🇰🇪 Proud moment!",
            "Nothing beats a cold Tusker after a long day 🍺",
            "Matatus and their music 🎵 Only in Kenya 😂",
            "Safari ya Mombasa road... ukiona gari imeanguka usishangae",
            "Sunday service was so powerful today! 🙏 Blessed",
            "New job alert! God is good 🙌 #Blessed #NewBeginnings",
            "Githeri for lunch. Simple pleasures 😊",
            "The rain in Nairobi is no joke! Everyone running for cover ☔",
            "Rift Valley views never disappoint 🏔️ #MagicalKenya",
            "Kwani KPLC what's happening? Power off the whole day 😤",
            "Family time is the best time ❤️ #FamilyFirst",
            "Ugali na sukuma wiki hits different 🍽️",
            "Morning run at Karura Forest 🏃‍♂️ Fresh air!",
            "Who else is ready for the weekend? 🎉 #TGIF",
            "Chapati Tuesday! Who's with me? 😋",
            "Kenya is beautiful! We need to appreciate what we have 🇰🇪"
        ]
        
        locations = [
            'Nairobi, Kenya', 'Mombasa, Kenya', 'Kisumu, Kenya', 'Nakuru, Kenya',
            'Eldoret, Kenya', 'Westlands, Nairobi', 'Karen, Nairobi', 'Kilimani, Nairobi',
            'Diani Beach, Kenya', 'Maasai Mara', 'Mount Kenya', 'Lake Nakuru'
        ]
        
        feelings = [
            'happy', 'excited', 'blessed', 'grateful', 'loved', 'motivated',
            'tired', 'frustrated', 'hungry', 'relaxed', 'inspired', 'proud'
        ]
        
        posts = []
        for user in users:
            num_posts = random.randint(3, 15)
            for _ in range(num_posts):
                post = Post.objects.create(
                    author=user,
                    content=random.choice(kenyan_statuses),
                    post_type=random.choice(['status'] * 6 + ['photo'] * 3 + ['video']),
                    privacy=random.choice(['public'] * 5 + ['friends'] * 4 + ['only_me']),
                    feeling=random.choice([''] * 5 + feelings),
                    location=random.choice([''] * 3 + locations),
                    created_at=timezone.now() - timedelta(days=random.randint(0, 180))
                )
                posts.append(post)
                
                # Add reactions
                num_reactions = random.randint(0, 30)
                reactors = random.sample(users, min(num_reactions, len(users)))
                for reactor in reactors:
                    Reaction.objects.create(
                        user=reactor,
                        post=post,
                        reaction_type=random.choice(['like'] * 5 + ['love'] * 2 + ['haha', 'wow', 'sad']),
                        created_at=post.created_at + timedelta(minutes=random.randint(1, 1000))
                    )
                
                # Add comments
                num_comments = random.randint(0, 10)
                comment_texts = [
                    "Nice one! 👏", "Love this! ❤️", "So true 😂", "Congratulations! 🎉",
                    "I agree with you", "Exactly! 💯", "Amen 🙏", "Facts!", "Amazing! 😍",
                    "Haha too funny 😂", "Missing this!", "Can relate 😅", "Well said! 👌"
                ]
                
                for _ in range(num_comments):
                    commenter = random.choice(users)
                    Comment.objects.create(
                        post=post,
                        author=commenter,
                        content=random.choice(comment_texts),
                        created_at=post.created_at + timedelta(minutes=random.randint(1, 2000))
                    )
        
        # Create some polls
        for _ in range(len(users) // 5):
            post = Post.objects.create(
                author=random.choice(users),
                content="Quick poll for you all!",
                post_type='status',
                privacy='public',
                created_at=timezone.now() - timedelta(days=random.randint(0, 30))
            )
            
            poll = Poll.objects.create(
                post=post,
                question=random.choice([
                    "Best Kenyan food?", "Favorite local artist?",
                    "Which city is better?", "Weekend plans?"
                ]),
                duration_hours=24,
                expires_at=timezone.now() + timedelta(hours=24)
            )
            
            options = ["Option A", "Option B", "Option C", "Option D"]
            for i, opt in enumerate(options):
                PollOption.objects.create(poll=poll, text=opt, order=i)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(posts)} posts'))

    def create_stories(self, users):
        """Create stories"""
        for user in random.sample(users, len(users) // 3):
            Story.objects.create(
                user=user,
                story_type=random.choice(['photo', 'video', 'text']),
                text_content=random.choice(['Good morning! ☀️', 'Having a great day!', 'Vibes! ✨']),
                background_color='#' + ''.join(random.choices('0123456789ABCDEF', k=6)),
                privacy='friends',
                expires_at=timezone.now() + timedelta(hours=24),
                created_at=timezone.now() - timedelta(hours=random.randint(0, 23))
            )
        
        self.stdout.write(self.style.SUCCESS(f'Created stories'))

    def create_conversations(self, users):
        """Create conversations and messages"""
        kenyan_messages = [
            "Niaje bro? 😊", "Mambo vipi?", "Habari yako?", "Sasa?",
            "Uko wapi?", "Tutaonana lini?", "Ngoja nikam", "Niko njiani",
            "Sawa tu", "Poa sana", "Sina stress", "Enyewe life inaendelea",
            "Tupatane town", "Unafanya nini?", "Call me", "Tutaongea baadaye",
            "Niko busy sasa", "Ngoja kidogo", "Okay boss", "Sawa nakuja"
        ]
        
        conversations = []
        for _ in range(len(users) * 2):
            conv_type = random.choice(['direct'] * 7 + ['group'] * 3)
            
            if conv_type == 'direct':
                participants = random.sample(users, 2)
            else:
                participants = random.sample(users, random.randint(3, 8))
            
            conv = Conversation.objects.create(
                conversation_type=conv_type,
                name=f"Group Chat {random.randint(1, 100)}" if conv_type == 'group' else "",
                created_by=participants[0],
                created_at=timezone.now() - timedelta(days=random.randint(1, 90))
            )
            conv.participants.set(participants)
            conversations.append(conv)
            
            # Create messages
            num_messages = random.randint(5, 30)
            for _ in range(num_messages):
                sender = random.choice(participants)
                msg = Message.objects.create(
                    conversation=conv,
                    sender=sender,
                    message_type='text',
                    content=random.choice(kenyan_messages),
                    created_at=conv.created_at + timedelta(minutes=random.randint(1, 5000))
                )
                
                # Mark some as read
                for participant in participants:
                    if participant != sender and random.choice([True, False]):
                        MessageRead.objects.create(
                            message=msg,
                            user=participant,
                            read_at=msg.created_at + timedelta(minutes=random.randint(1, 10))
                        )
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(conversations)} conversations'))

    def create_pages(self, users):
        """Create Kenyan business pages"""
        kenyan_pages = [
            ('Nairobi Coffee House', 'business', 'Best coffee in Nairobi ☕ Visit us!'),
            ('Mombasa Tours & Travel', 'business', 'Explore the beautiful coast of Kenya 🌊'),
            ('Tech Hub Kenya', 'business', 'Innovation and technology solutions'),
            ('Mama Oliech Restaurant', 'business', 'Authentic Kenyan cuisine 🍲'),
            ('Artcaffe Kenya', 'business', 'Coffee, food, and good vibes'),
            ('Nairobi Barbershop', 'business', 'Fresh cuts and clean shaves ✂️'),
            ('Kenya Wildlife Tours', 'business', 'Experience the wild side of Kenya 🦁'),
            ('Fitness First Nairobi', 'business', 'Your health, our priority 💪'),
            ('DJ Kalonje', 'public_figure', 'Official page of DJ Kalonje 🎵'),
            ('Kenyan Foodies', 'community', 'Food lovers unite! 🍽️'),
        ]
        
        pages = []
        for name, category, desc in kenyan_pages:
            page = Page.objects.create(
                name=name,
                username=name.lower().replace(' ', '_'),
                category=category,
                description=desc,
                is_verified=random.choice([True, False]),
                created_by=random.choice(users),
                created_at=timezone.now() - timedelta(days=random.randint(30, 500))
            )
            pages.append(page)
            
            # Add page likes
            num_likes = random.randint(50, 500)
            likers = random.sample(users, min(num_likes, len(users)))
            for liker in likers:
                PageLike.objects.create(page=page, user=liker)
            
            # Add page roles
            PageRole.objects.create(
                page=page,
                user=page.created_by,
                role='admin'
            )
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(pages)} pages'))

    def create_groups(self, users):
        """Create Kenyan groups"""
        kenyan_groups = [
            ('Nairobi Entrepreneurs', 'Business networking and opportunities', 'public'),
            ('Kenya Tech Community', 'For tech enthusiasts in Kenya', 'public'),
            ('Mombasa Foodies', 'Best food spots on the coast', 'public'),
            ('University of Nairobi Alumni', 'Connect with fellow alumni', 'private'),
            ('Nairobi Single Parents', 'Support group', 'private'),
            ('Kenya Travel Squad', 'Travel buddies and tips', 'public'),
            ('Fitness Kenya', 'Health and fitness community', 'public'),
            ('Kenyan Musicians', 'Platform for Kenyan artists', 'public'),
            ('Nairobi Property Market', 'Real estate discussions', 'public'),
            ('Kenya Job Opportunities', 'Job postings and career advice', 'public'),
        ]
        
        groups = []
        for name, desc, privacy in kenyan_groups:
            group = Group.objects.create(
                name=name,
                description=desc,
                privacy=privacy,
                created_by=random.choice(users),
                created_at=timezone.now() - timedelta(days=random.randint(30, 700))
            )
            groups.append(group)
            
            # Add members
            num_members = random.randint(20, 100)
            members = random.sample(users, min(num_members, len(users)))
            for member in members:
                GroupMember.objects.create(
                    group=group,
                    user=member,
                    role='admin' if member == group.created_by else random.choice(['moderator'] + ['member'] * 9),
                    status='approved',
                    joined_at=group.created_at + timedelta(days=random.randint(0, 100))
                )
            
            # Create group posts
            for _ in range(random.randint(5, 20)):
                GroupPost.objects.create(
                    group=group,
                    author=random.choice(members),
                    content=f"Discussion topic in {name}",
                    created_at=group.created_at + timedelta(days=random.randint(1, 200))
                )
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(groups)} groups'))

    def create_events(self, users):
        """Create Kenyan events"""
        kenyan_events = [
            'Nairobi Marathon 2025', 'Tech Conference Nairobi', 'Coastal Food Festival',
            'Nairobi Business Expo', 'Kenyan Music Awards', 'Charity Run for Kids',
            'Startup Weekend Nairobi', 'Art Exhibition Karen', 'Sunday Brunch Meetup',
            'Beach Cleanup Mombasa', 'Networking Event CBD', 'Comedy Night Nairobi'
        ]
        
        for event_name in kenyan_events:
            start = timezone.now() + timedelta(days=random.randint(1, 90))
            Event.objects.create(
                name=event_name,
                description=f"Join us for {event_name}! It's going to be amazing!",
                event_type=random.choice(['public'] * 7 + ['private'] * 3),
                location=random.choice(['KICC Nairobi', 'Carnivore Nairobi', 'Mombasa Beach',
                                       'Uhuru Gardens', 'Westlands', 'Karen Blixen']),
                start_datetime=start,
                end_datetime=start + timedelta(hours=random.randint(2, 8)),
                host=random.choice(users),
                created_at=start - timedelta(days=random.randint(7, 60))
            )
        
        self.stdout.write(self.style.SUCCESS(f'Created events'))

    def create_albums_photos(self, users):
        """Create photo albums"""
        album_names = [
            'Mombasa Trip 2024', 'Family Moments', 'Nairobi Adventures',
            'Weekend Vibes', 'Graduation Day', 'Safari Photos',
            'Friends Forever', 'Food Diary', 'Travel Kenya'
        ]
        
        for user in random.sample(users, len(users) // 2):
            for _ in range(random.randint(1, 3)):
                Album.objects.create(
                    user=user,
                    name=random.choice(album_names),
                    description="Great memories!",
                    privacy='friends',
                    created_at=timezone.now() - timedelta(days=random.randint(1, 365))
                )
        
        self.stdout.write(self.style.SUCCESS(f'Created albums'))

    def create_marketplace_items(self, users):
        """Create Kenyan marketplace items"""
        items = [
            ('iPhone 13 Pro', 'electronics', 75000, 'used_like_new', 'Slightly used, excellent condition'),
            ('Sofa Set 5-Seater', 'home', 45000, 'used_good', 'Comfortable sofa set'),
            ('Toyota Fielder 2015', 'vehicles', 1200000, 'used_good', 'Well maintained, local assembly'),
            ('Samsung 55" TV', 'electronics', 55000, 'new', 'Brand new smart TV'),
            ('Laptop HP Core i5', 'electronics', 35000, 'used_good', 'Great for students'),
            ('Dining Table', 'home', 18000, 'used_like_new', '6-seater wooden table'),
            ('PlayStation 5', 'entertainment', 65000, 'new', 'Latest gaming console'),
            ('Mountain Bike', 'sporting', 25000, 'used_good', 'Perfect for trails'),
            ('Office Desk', 'office', 12000, 'used_fair', 'Solid desk'),
            ('Baby Cot', 'family', 8000, 'used_like_new', 'Barely used')
        ]
        
        for title, category, price, condition, desc in items:
            MarketplaceItem.objects.create(
                seller=random.choice(users),
                title=title,
                description=desc,
                price=Decimal(price),
                category=category,
                condition=condition,
                location=random.choice(['Nairobi', 'Mombasa', 'Kisumu', 'Nakuru']),
                is_available=random.choice([True] * 8 + [False] * 2),
                created_at=timezone.now() - timedelta(days=random.randint(1, 60))
            )
        
        self.stdout.write(self.style.SUCCESS(f'Created marketplace items'))

    def create_videos(self, users):
        """Create videos"""
        video_titles = [
            'Nairobi City Tour', 'Kenyan Food Review', 'Day in My Life',
            'Travel Vlog Mombasa', 'Fitness Tips', 'Comedy Skit',
            'Music Cover', 'Product Review', 'Motivational Speech',
            'Cooking Tutorial'
        ]
        
        for _ in range(20):
            Video.objects.create(
                uploader=random.choice(users),
                title=random.choice(video_titles),
                description='Check out this awesome video!',
                duration=random.randint(60, 600),
                privacy='public',
                view_count=random.randint(10, 5000),
                category='entertainment',
                created_at=timezone.now() - timedelta(days=random.randint(1, 180))
            )
        
        self.stdout.write(self.style.SUCCESS(f'Created videos'))

    def create_fundraisers(self, users):
        """Create fundraisers"""
        fundraiser_titles = [
            'Medical Fund for Mama Jane',
            'School Fees for Bright Students',
            'Support Local Orphanage',
            'Emergency Relief Fund',
            'Community Water Project'
        ]
        
        for title in fundraiser_titles:
            Fundraiser.objects.create(
                creator=random.choice(users),
                title=title,
                description=f'Help us raise funds for {title}. Every contribution counts!',
                category='medical' if 'Medical' in title else 'education' if 'School' in title else 'community',
                goal_amount=Decimal(random.randint(50000, 500000)),
                current_amount=Decimal(random.randint(5000, 100000)),
                currency='KES',
                is_active=True,
                created_at=timezone.now() - timedelta(days=random.randint(1, 60))
            )
        
        self.stdout.write(self.style.SUCCESS(f'Created fundraisers'))

    def create_notifications(self, users):
        """Create notifications"""
        for user in random.sample(users, len(users) // 2):
            for _ in range(random.randint(3, 10)):
                Notification.objects.create(
                    recipient=user,
                    sender=random.choice([u for u in users if u != user]),
                    notification_type=random.choice([
                        'friend_request', 'post_like', 'post_comment',
                        'friend_accepted', 'post_tag', 'birthday'
                    ]),
                    title='New notification',
                    message='You have a new notification',
                    is_read=random.choice([True, False]),
                    created_at=timezone.now() - timedelta(hours=random.randint(1, 72))
                )