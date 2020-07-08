from django import forms
from p_library.models import Author, Book, Reader

class AuthorForm(forms.ModelForm):

    full_name = forms.CharField(widget=forms.TextInput)

    class Meta:
        model = Author
        fields = '__all__'

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

class ReaderForm(forms.ModelForm):
    class Meta:
        model = Reader
        fields = '__all__'

class ReaderSessionForm(forms.ModelForm):
    class Meta:
        model = Reader
        fields = ["name"]