from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from posts.models import Post
from comments.models import Comment
from likes.models import Like
from followers.models import Follower
from messaging.models import Message
from django.utils import timezone
from datetime import timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **kwargs):
        # Create users
        users = []
        for i in range(5):
            user = User.objects.create_user(
                username=f'user{i}',
                password='testpass123',
                name=f'User {i}'
            )
            users.append(user)
            self.stdout.write(f'Created user: {user.username}')

        # Create posts
        posts = []
        for user in users:
            for i in range(3):
                post = Post.objects.create(
                    owner=user,
                    title=f'Post {i} by {user.username}',
                    content=f'Content of post {i} by {user.username}'
                )
                posts.append(post)
                self.stdout.write(f'Created post: {post.title}')

        # Create comments
        for post in posts:
            for i in range(2):
                commenter = random.choice(users)
                comment = Comment.objects.create(
                    owner=commenter,
                    post=post,
                    content=f'Comment {i} on {post.title} by {commenter.username}'
                )
                self.stdout.write(f'Created comment: {comment}')

        # Create likes
        for post in posts:
            for i in range(random.randint(1, 3)):
                liker = random.choice(users)
                try:
                    like = Like.objects.create(
                        owner=liker,
                        post=post
                    )
                    self.stdout.write(f'Created like: {like}')
                except:
                    pass  # Skip if user already liked the post

        # Create followers
        for user in users:
            for i in range(random.randint(1, 4)):
                follower = random.choice(users)
                if follower != user:
                    try:
                        follow = Follower.objects.create(
                            owner=follower,
                            followed=user
                        )
                        self.stdout.write(f'Created follower: {follow}')
                    except:
                        pass  # Skip if already following

        # Create messages
        for i in range(10):
            sender = random.choice(users)
            recipient = random.choice([u for u in users if u != sender])
            message = Message.objects.create(
                sender=sender,
                recipient=recipient,
                content=f'Message {i} from {sender.username} to {recipient.username}',
                timestamp=timezone.now() - timedelta(minutes=random.randint(1, 1000))
            )
            self.stdout.write(f'Created message: {message}')

        self.stdout.write(self.style.SUCCESS('Successfully populated database'))