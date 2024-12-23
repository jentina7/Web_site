from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin


class CommentLikeInLines(admin.TabularInline):
    model = CommentLike
    extra = 1

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    inlines = [CommentLikeInLines]


@admin.register(Post)
class PostAdmin(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


admin.site.register(UserProfile)
admin.site.register(Follow)
admin.site.register(Save)
admin.site.register(SaveItem)
admin.site.register(Story)
admin.site.register(PostLike)
