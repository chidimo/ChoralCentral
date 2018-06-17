from django.contrib import admin

from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'song', 'like_count', 'publish', 'created', 'modified', 'likers')
    list_filter = ('title', 'publish', 'created')
    list_editable = ('publish', )
    list_display_links = ('title', )

    def likers(self, obj):
        return ", ".join([each.screen_name for each in obj.likes.all()])

class CommentAdmin(admin.ModelAdmin):
    list_display = ('creator', 'post', 'comment', 'active')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
