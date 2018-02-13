from django.contrib import admin

from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "publish", "created", "modified")
    list_filter = ("title", "publish", "created")
    list_editable = ("publish", )
    list_display_links = ('title', )

class CommentAdmin(admin.ModelAdmin):
    list_display = ("comment", "active")

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
