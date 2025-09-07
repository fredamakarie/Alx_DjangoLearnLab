 from bookshelf.models import Book

x = Book.objects.all()[0]

x.title
<!-- Results. -->
'1984'

x.title = 'Nineteen Eighty-Four'
x.save()

Book.objects.all().values()
<!-- Results. -->
<QuerySet [{'id': 1, 'title': 'Nineteen Eighty-Four', 'author': 'George Orwell', 'publication_year': 1949}]>