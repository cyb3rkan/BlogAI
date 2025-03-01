from django.contrib import admin
from .models import Page
# Register your models here.


class PageAdmin(admin.ModelAdmin):
    list_display = ("id","title", "last_update")
    list_filter = ("last_update",)
    ordering = ["id"]
    search_fields = ["title", "content"]


admin.site.register(Page, PageAdmin)
