from django.contrib import admin
from fatalities.models import Comment

# Register your models here.

@admin.register(Comment)
class AuthorAdmin(admin.ModelAdmin):
    fields = ["comment"]