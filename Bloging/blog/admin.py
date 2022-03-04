from csv import list_dialects
from django.contrib import admin
from .models import Post_blog
# Register your models here.
@admin.register(Post_blog)

class PostModelAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'created_Date', 'owner', 'desc', 'is_Published']