from django.utils.translation import gettext as _
from django.db import models
from django.urls import reverse


class Author(models.Model):
    # id = models.UUIDField(default=uuid.uuid4, primary_key=True,
    #                       verbose_name=_("Уникальный ключ"))
    full_name = models.TextField(verbose_name=_("Имя автора"))
    birth_year = models.SmallIntegerField(verbose_name=_("Год рожения"))
    country = models.CharField(max_length=2, verbose_name=_("Страна"))

    def __str__(self):
        return self.full_name


class Book(models.Model):
    # id = models.UUIDField(default=uuid.uuid4, primary_key=True,
    #                       verbose_name=_("Уникальный ключ"))
    ISBN = models.CharField(max_length=13,
                            verbose_name=_("Международный стандартный "
                                           "книжный номер"))
    title = models.TextField(verbose_name=_("Название"))
    description = models.TextField(verbose_name=_("Аннотация"))
    year_release = models.SmallIntegerField(verbose_name=_("Год издания"))
    copy_count = models.SmallIntegerField(verbose_name=_("Число копий"))
    price = models.DecimalField(max_digits=12, decimal_places=2,
                                verbose_name=_("Цена"))
    author = models.ForeignKey("p_library.Author", on_delete=models.CASCADE,
                               verbose_name=_("Автор"),
                               related_name="book_author")
    cover = models.ImageField(upload_to='cover_photo', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('author', kwargs={'pk': self.pk})


class Publisher(models.Model):
    name = models.TextField(verbose_name=_("Название издательства"))

    books = models.ManyToManyField("p_library.Book", verbose_name=_("Книги"),
                                   through="p_library.BookPublishing")
    def __str__(self):
        return self.name

class Reader(models.Model):
    # id = models.UUIDField(default=uuid.uuid4, primary_key=True,
    #                       verbose_name=_("Уникальный ключ"))
    name = models.CharField(max_length=256, verbose_name=_("Имя"))

    books = models.ManyToManyField("p_library.Book", verbose_name=_("Книги"),
                                   through="p_library.BookReading")

    def __str__(self):
        return self.name


class BookReading(models.Model):
    # id = models.UUIDField(default=uuid.uuid4, primary_key=True,
    #                       verbose_name=_("Уникальный ключ"))
    book = models.ForeignKey("p_library.Book", on_delete=models.CASCADE,
                             verbose_name=_("Книга"),
                             related_name="bookreading_book")
    reader = models.ForeignKey("p_library.Reader", on_delete=models.CASCADE,
                               verbose_name=_("Читатель"),
                               related_name="bookreading_reader")
    completion = models.NullBooleanField(default=None,
                                         verbose_name=_("Чтение завершено"))

    def __str__(self):
        return "-".join((str(self.book),
                         str(self.reader),
                         str(self.completion),))

class BookPublishing(models.Model):

    book = models.ForeignKey("p_library.Book", on_delete=models.CASCADE,
                             verbose_name=_("Книга"),
                             related_name="bookpublishing_book")

    publisher = models.ForeignKey("p_library.Publisher", on_delete=models.CASCADE,
                               verbose_name=_("Издательство"),
                               related_name="bookpublishing_publisher")

    year = models.SmallIntegerField(verbose_name=_("Год публикации"))

    def __str__(self):
        return "-".join((str(self.book),
                         str(self.publisher),
                         str(self.year),))