from bookshelf.models import Book

Book.objects.create

bookshelf = Book(title='1984',author='George Orwell', publication_year=1949)
bookshelf.save()

<!-- Successful Creation of Book instance. -->
Book.objects.all().values()


Book.objects.get()

Book.objects.all().values()
<!-- Results. -->
QuerySet [{'id': 1, 'title': '1984', 'author': 'George Orwell', 'publication_year': 1949}]


 from bookshelf.models import Book

x = Book.objects.all()[0]

x.title
<!-- Results. -->
'1984'

book.title = 'Nineteen Eighty-Four'

x.title = 'Nineteen Eighty-Four'
x.save()

Book.objects.all().values()
<!-- Results. -->
<QuerySet [{'id': 1, 'title': 'Nineteen Eighty-Four', 'author': 'George Orwell', 'publication_year': 1949}]>



from bookshelf.models import Book

x=Book.objects.all()[0]

x.delete()

(1, {'bookshelf.Book': 1})

Book.objects.all().values()

QuerySet []