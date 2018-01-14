from django.contrib import admin

from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "created", "modified")
    list_filter = ("title", "status", "created")
    list_editable = ("status", )
    list_display_links = ('title', )

class CommentAdmin(admin.ModelAdmin):
    list_display = ("comment", "active")

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
