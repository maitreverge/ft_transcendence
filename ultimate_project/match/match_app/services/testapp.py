# ton_app/apps.py
from django.apps import AppConfig
import threading
import time


class TonAppConfig(AppConfig):
    name = "match_app"

    def ready(self):
        # Code à exécuter au démarrage de l'app
        threading.Thread(target=ma_tache_de_fond, daemon=True).start()


def ma_tache_de_fond():
    while True:
        print("houlala", flush=True)
        time.sleep(1)
        # ta boucle de traitement
        pass
