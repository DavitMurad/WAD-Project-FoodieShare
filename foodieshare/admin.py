from django.contrib import admin
from foodieshare.models import *

admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)