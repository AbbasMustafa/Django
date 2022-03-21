from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass

class Post(models.Model):
	post = models.CharField(max_length=1024)
	date = models.DateTimeField(default=timezone.now)
	creator = models.ForeignKey(User, on_delete=models.CASCADE,
							 related_name="get_posts")
	likes = models.ManyToManyField(User,
									blank=True, null=True,
									related_name="get_likes")

	class Meta:
		ordering = ('-id',)

	def __str__(self):
		return f"by {self.creator}"

class Follower(models.Model):
	userProfile = models.ForeignKey(User, on_delete=models.CASCADE,
									related_name="get_user_followers")
	follower = models.ManyToManyField(User,
										blank=True, null=True,
										related_name="get_followers")
	following = models.ManyToManyField(User,
										blank=True, null=True,
										related_name="get_following")

class Comments(models.Model):
	comment_by = models.ForeignKey(User, on_delete=models.CASCADE,
									 related_name="get_users")
	on_post = models.ForeignKey(Post, on_delete=models.CASCADE,
								related_name="get_comments")
	date = models.DateTimeField(default=timezone.now)
	comment = models.CharField(max_length=1024)

