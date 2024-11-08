from django.contrib import admin

from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'approved', 'created_at')
    list_filter = ('approved', 'created_at')
    actions = ['approve_posts', 'disapprove_posts']

    def approve_posts(self, request, queryset):
        rows_updated = queryset.update(approved=True)
        if rows_updated == 1:
            message_bit = "1 post was"
        else:
            message_bit = f"{rows_updated} posts were"
        self.message_user(request, f"{message_bit} successfully marked as approved.")

    def disapprove_posts(self, request, queryset):
        rows_updated = queryset.update(approved=False)
        if rows_updated == 1:
            message_bit = "1 post was"
        else:
            message_bit = f"{rows_updated} posts were"
        self.message_user(request, f"{message_bit} successfully marked as disapproved.")

    approve_posts.short_description = "Approve selected posts"
    disapprove_posts.short_description = "Disapprove selected posts"

admin.site.register(Post,PostAdmin)
admin.site.register(Category)
# admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Profile)