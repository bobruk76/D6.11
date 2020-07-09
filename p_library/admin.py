from django.contrib import admin
from .models import (Book, Author, Reader, BookReading, Publisher, BookPublishing)

# [admin.site.register(item) for item in (Book, Author, Reader, BookReading)]

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_full_name')
    list_filter = (['title',])

    @staticmethod
    def author_full_name(obj):
        return obj.author.full_name

    list_display = ('title', 'author_full_name',)
    fields = ('ISBN', 'title', 'description', 'year_release', 'author', 'price','cover')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    pass

@admin.register(BookPublishing)
class BookPublishingAdmin(admin.ModelAdmin):
    pass

@admin.register(Reader)
class ReadergAdmin(admin.ModelAdmin):
    pass

@admin.register(BookReading)
class BookReadingAdmin(admin.ModelAdmin):
    pass
