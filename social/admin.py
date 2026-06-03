from django.contrib import admin
from .models import Post,Profile,Like,Comment,Follow 

admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Follow)
