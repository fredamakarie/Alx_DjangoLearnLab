from bookshelf.models import Book

x=Book.objects.all()[0]

x.delete()

(1, {'bookshelf.Book': 1})

Book.objects.all().values()

QuerySet []