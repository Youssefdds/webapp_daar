from django.core.management.base import BaseCommand
from library.models import Book
from library.elasticsearch_client import es, INDEX_NAME

class Command(BaseCommand):
    help = "Index all Book objects into Elasticsearch"

    def handle(self, *args, **kwargs):
        # Delete index if exists (optional, ensures fresh indexing)
        if es.indices.exists(index=INDEX_NAME):
            self.stdout.write(f"Deleting existing index '{INDEX_NAME}'...")
            es.indices.delete(index=INDEX_NAME)

        # Create the index with mappings
        self.stdout.write(f"Creating index '{INDEX_NAME}'...")
        es.indices.create(
            index=INDEX_NAME,
            body={
                "mappings": {
                    "properties": {
                        "title": {"type": "text"},
                        "author": {"type": "text"},
                        "image_url": {"type": "keyword"},
                        "text_content": {"type": "text"}
                    }
                }
            }
        )

        # Index all books
        total = Book.objects.count()
        self.stdout.write(f"Indexing {total} books...")

        for book in Book.objects.all():
            doc = {
                "id": book.id,
                "title": book.title,
                "author": book.author or "",
                "image_url": book.image_url or "",
                "text_content": book.text_content or ""
            }
            es.index(index=INDEX_NAME, id=book.id, document=doc)

        self.stdout.write(self.style.SUCCESS(f"Successfully indexed {total} books into '{INDEX_NAME}'"))
