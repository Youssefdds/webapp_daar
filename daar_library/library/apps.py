from django.apps import AppConfig
import threading


class LibraryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'library'
    # def ready(self):
    #     from .views import build_global_graph
    #     import threading

    #     # Construire le graphe dans un thread séparé pour ne pas bloquer le serveur
    #     threading.Thread(target=build_global_graph, daemon=True).start()
