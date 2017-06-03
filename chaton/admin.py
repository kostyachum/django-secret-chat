from django.contrib import admin

from . import models


class MessageInline(admin.TabularInline):
    model = models.Message
    can_delete = False
    extra = 1


class ChatAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ['title', 'hash', 'created']
    inlines = [MessageInline]


admin.site.register(models.Chat, ChatAdmin)
