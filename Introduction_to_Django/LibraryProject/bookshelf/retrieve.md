Book.objects.get()

Book.objects.all().values()
<!-- Results. -->
QuerySet [{'id': 1, 'title': '1984', 'author': 'George Orwell', 'publication_year': 1949}]