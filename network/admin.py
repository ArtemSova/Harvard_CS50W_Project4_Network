from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Like)
