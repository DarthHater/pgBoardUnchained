from django.contrib import admin
from models import Forum, Thread, Post

admin.site.register(Forum)
admin.site.register(Post)
admin.site.register(Thread)