from django.contrib import admin
from .models import Book, Library, Librarian
# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author")
    list_filter = ("title", "author")
    search_fields = ("title", "author")
admin.site.register(Book, BookAdmin)

class LibraryAdmin(admin.ModelAdmin):
    
    list_filter = ("name", "books")
    search_fields = ("name", "books")
admin.site.register(Library, LibraryAdmin)