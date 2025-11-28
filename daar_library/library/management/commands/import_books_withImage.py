import os
import json
from django.core.management.base import BaseCommand
from library.models import Book
from library.elasticsearch_client import es, INDEX_NAME  # ton client Elasticsearch

LIBRARY_DIR = "libraryBooks"  # chemin vers ton dossier avec les txt et metadata.json

class Command(BaseCommand):
    help = "Import books from library folder and index them in Elasticsearch"

    def handle(self, *args, **options):
        metadata_path = os.path.join(LIBRARY_DIR, "metadata.json")
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        for book_id, data in metadata.items():
            # Lire le contenu du livre
            text_file = os.path.join(LIBRARY_DIR, data["filename"])
            if os.path.exists(text_file):
                with open(text_file, "r", encoding="utf-8") as tf:
                    content = tf.read()
            else:
                content = ""

            # Créer ou mettre à jour le livre dans Django
            book_obj, created = Book.objects.update_or_create(
                title=data["title"],
                defaults={
                    "author": ", ".join([a["name"] for a in data.get("authors", [])]),
                    "image_url": data.get("cover_image", ""),
                    "text_content": content
                }
            )

            

            self.stdout.write(self.style.SUCCESS(f"Imported & indexed: {book_obj.title}"))
