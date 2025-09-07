from bookshelf.models import Book

bookshelf = Book(title='1984',author='George Orwell', publication_year=1949)
bookshelf.save()

<!-- Successful Creation of Book instance. -->
Book.objects.all().values()