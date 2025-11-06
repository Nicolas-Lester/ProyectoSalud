from django.core.management.base import BaseCommand
from django.conf import settings
import pandas as pd
from sentimientos.models import Comment
import os

class Command(BaseCommand):
    help = "Carga comentarios desde un CSV"

    def add_arguments(self, parser):
        parser.add_argument("--path", type=str, required=True, help="Ruta al CSV")

    def handle(self, *args, **opts):
        path = opts["path"]
        if not os.path.exists(path):
            self.stderr.write(self.style.ERROR(f"No existe: {path}"))
            return
        df = pd.read_csv(path)
        created = 0
        for _, row in df.iterrows():
            Comment.objects.create(
                fecha=row.get("fecha"),
                texto=row.get("texto", ""),
                etiqueta=row.get("etiqueta", "").lower()
            )
            created += 1
        self.stdout.write(self.style.SUCCESS(f"Cargados {created} comentarios"))
