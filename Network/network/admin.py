from django.contrib import admin
from .models import User, Post, Follower, Comments

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Follower)
admin.site.register(Comments)