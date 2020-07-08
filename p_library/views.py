from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect, render

from django.http.response import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.forms import formset_factory
from p_library.forms import *
from p_library.models import *
from django.urls import reverse_lazy

class AuthorList(ListView):
    model = Author
    template_name = 'author_list.html'

class AuthorCreate(CreateView):
    model = Author
    form_class = AuthorForm
    success_url = reverse_lazy('p_library:author_list')
    template_name = '_edit.html'

class AuthorUpdate(UpdateView):
    model = Author
    form_class = AuthorForm
    success_url = reverse_lazy('p_library:author_list')
    template_name = '_edit.html'

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('p_library:author_list')
    template_name = '_delete.html'

class ReaderList(ListView):
    model = Reader
    template_name = 'reader_list.html'

class ReaderCreate(CreateView):
    model = Reader
    form_class = ReaderSessionForm
    success_url = reverse_lazy('p_library:reader_list')
    template_name = '_edit.html'

class ReaderDelete(DeleteView):
    model = Reader
    success_url = reverse_lazy('p_library:reader_list')
    template_name = '_delete.html'

class ReaderUpdate(UpdateView):
    model = Reader
    form_class = ReaderForm
    success_url = reverse_lazy('p_library:reader_list')
    template_name = '_edit.html'

def author_create_many(request):
    AuthorFormSet = formset_factory(AuthorForm, extra=2)  #  Первым делом, получим класс, который будет создавать наши формы. Обратите внимание на параметр `extra`, в данном случае он равен двум, это значит, что на странице с несколькими формами изначально будет появляться 2 формы создания авторов.
    if request.method == 'POST':  #  Наш обработчик будет обрабатывать и GET и POST запросы. POST запрос будет содержать в себе уже заполненные данные формы
        author_formset = AuthorFormSet(request.POST, request.FILES, prefix='authors')  #  Здесь мы заполняем формы формсета теми данными, которые пришли в запросе. Обратите внимание на параметр `prefix`. Мы можем иметь на странице не только несколько форм, но и разных формсетов, этот параметр позволяет их отличать в запросе.
        if author_formset.is_valid():  #  Проверяем, валидны ли данные формы
            for author_form in author_formset:
                author_form.save()  #  Сохраним каждую форму в формсете
            return HttpResponseRedirect(reverse_lazy('p_library:author_list'))  #  После чего, переадресуем браузер на список всех авторов.
    else:  #  Если обработчик получил GET запрос, значит в ответ нужно просто "нарисовать" формы.
        author_formset = AuthorFormSet(prefix='authors')  #  Инициализируем формсет и ниже передаём его в контекст шаблона.
    return render(request, 'manage_authors.html', {'author_formset': author_formset})

def books_authors_create_many(request):
    AuthorFormSet = formset_factory(AuthorForm, extra=2)
    BookFormSet = formset_factory(BookForm, extra=2)
    if request.method == 'POST':
        author_formset = AuthorFormSet(request.POST, request.FILES, prefix='authors')
        book_formset = BookFormSet(request.POST, request.FILES, prefix='books')
        if author_formset.is_valid() and book_formset.is_valid():
            for author_form in author_formset:
                author_form.save()
            for book_form in book_formset:
                book_form.save()
            return HttpResponseRedirect(reverse_lazy('p_library:author_list'))
    else:
        author_formset = AuthorFormSet(prefix='authors')
        book_formset = BookFormSet(prefix='books')
    return render(
	    request,
		'manage_books_authors.html',
		{
	        'author_formset': author_formset,
			'book_formset': book_formset,
		}
	)

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

def books_list(request):
    template = loader.get_template('books.html')
    books = Book.objects.all()
    biblio_data = {
        "title": "мою библиотеку",
        "books": books,
    }
    return HttpResponse(template.render(biblio_data, request))

def book_increment(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/books/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/books/')
            book.copy_count += 1
            book.save()
        return redirect('/books/')
    else:
        return redirect('/books/')


def book_decrement(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/books/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/books/')
            if book.copy_count < 1:
                book.copy_count = 0
            else:
                book.copy_count -= 1
            book.save()
        return redirect('/books/')
    else:
        return redirect('/books/')

def books_publ(request):
    template = loader.get_template('publishing.html')

    publishers = Publisher.objects.all()
    data = {
        "publishers": publishers,
    }
    return HttpResponse(template.render(data, request))