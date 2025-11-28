import re
from collections import defaultdict
from django.core.management.base import BaseCommand
from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from library.models import Book  # <-- ON UTILISE TON MODEL

"""
Ce script construit un index inversé complet à partir des objets Book stockés
dans la base Django. L’index inversé est ensuite envoyé dans Elasticsearch.

Structure stockée dans ES :
    term → { book_id: count, book_id: count, ... }
"""

class Command(BaseCommand):
    help = "Construit un index inversé à partir du modèle Django Book et l'envoie dans Elasticsearch"

    def handle(self, *args, **kwargs):

        # ----------------------------------------------------------------------
        # 1) Connexion Elasticsearch
        # ----------------------------------------------------------------------
        es = Elasticsearch("http://localhost:9200", timeout=60)
        index_name = "books"

        # ----------------------------------------------------------------------
        # 2) Supprimer puis créer l’index Elasticsearch
        # ----------------------------------------------------------------------
        if es.indices.exists(index=index_name):
            es.indices.delete(index=index_name)
            self.stdout.write(self.style.WARNING(f"🗑 Ancien index '{index_name}' supprimé"))

        es.indices.create(
            index=index_name,
            body={
                "settings": {
                    "index": {
                        "max_result_window": 50000
                    }
                },
                "mappings": {
                    "properties": {
                        "term": {"type": "keyword"},
                        "part": {"type": "integer"},
                        "books": {"type": "flattened"}
                    }
                }
            }
        )

        self.stdout.write(self.style.SUCCESS(f"✅ Nouvel index créé : {index_name}"))

        # ----------------------------------------------------------------------
        # 3) Récupération des livres depuis la BDD
        # ----------------------------------------------------------------------
        self.stdout.write("📚 Lecture des livres depuis Book.objects...")

        all_books = Book.objects.all()
        total_books = all_books.count()

        if total_books == 0:
            self.stdout.write(self.style.ERROR("❌ Aucun livre trouvé dans la base !"))
            return

        self.stdout.write(f"📘 {total_books} livres chargés depuis la base.")

        # ----------------------------------------------------------------------
        # 4) Construction de l'index inversé
        # ----------------------------------------------------------------------
        inverted_index = defaultdict(lambda: defaultdict(int))
        processed_count = 0

        for book in all_books:
            if not book.text_content:
                continue

            text = book.text_content.lower()

            # Extraction de tous les mots (même regex que ton script)
            words = re.findall(r"[a-zàâçéèêëîïôûùüÿñœ]+", text)

            for word in words:
                inverted_index[word][str(book.id)] += 1

            processed_count += 1
            if processed_count % 100 == 0:
                self.stdout.write(f"  ➜ {processed_count} livres traités...")

        total_terms = len(inverted_index)

        self.stdout.write(self.style.SUCCESS(
            f"📘 Index inversé construit → {processed_count} livres, {total_terms} termes uniques."
        ))

        # ----------------------------------------------------------------------
        # 5) Envoi à Elasticsearch (avec découpage chunk > 500)
        # ----------------------------------------------------------------------
        self.stdout.write("📤 Envoi de l'index dans Elasticsearch...")

        MAX_BOOKS_PER_DOC = 500
        actions = []
        docs_indexed = 0
        large_terms = []

        for term, books_dict in inverted_index.items():

            postings = list(books_dict.items())
            nb_books = len(postings)

            # Cas : trop de livres → découpage
            if nb_books > MAX_BOOKS_PER_DOC:
                large_terms.append((term, nb_books))

                for part_index, i in enumerate(range(0, nb_books, MAX_BOOKS_PER_DOC)):
                    chunk = dict(postings[i:i + MAX_BOOKS_PER_DOC])

                    actions.append({
                        "_index": index_name,
                        "_id": f"{term}_part{part_index}",
                        "_source": {
                            "term": term,
                            "part": part_index,
                            "books": chunk,
                        }
                    })

            else:
                # Cas normal
                actions.append({
                    "_index": index_name,
                    "_id": term,
                    "_source": {
                        "term": term,
                        "part": 0,
                        "books": dict(books_dict),
                    }
                })

            # Envoi batch
            if len(actions) >= 1000:
                success, errors = bulk(es, actions, raise_on_error=False, request_timeout=60)
                docs_indexed += success

                if errors:
                    self.stdout.write(self.style.WARNING(f"⚠ {len(errors)} erreurs d’indexation."))

                self.stdout.write(f"  ✓ {docs_indexed} documents envoyés...")
                actions = []

        # Envoi du dernier batch
        if actions:
            success, errors = bulk(es, actions, raise_on_error=False, request_timeout=60)
            docs_indexed += success

        self.stdout.write(self.style.SUCCESS(f"🎉 Indexation terminée : {docs_indexed} documents envoyés."))

        # ----------------------------------------------------------------------
        # 6) Affichage des mots découpés
        # ----------------------------------------------------------------------
        if large_terms:
            self.stdout.write(self.style.WARNING("\nℹ Mots trop fréquents (découpés en plusieurs parties) :"))
            for term, nb_books in sorted(large_terms, key=lambda x: x[1], reverse=True)[:10]:
                parts = (nb_books + MAX_BOOKS_PER_DOC - 1) // MAX_BOOKS_PER_DOC
                self.stdout.write(f"  • '{term}' : {nb_books} livres → {parts} parties")
