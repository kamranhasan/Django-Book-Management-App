from django.contrib import admin
from .models import *

admin.site.register(Book)

admin.site.register(Section)

admin.site.register(Subsection)
# class BookAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'created_at', 'updated_at')
#     list_filter = ('author', 'created_at', 'updated_at')
#     search_fields = ('title', 'author__username')
#     date_hierarchy = 'created_at'