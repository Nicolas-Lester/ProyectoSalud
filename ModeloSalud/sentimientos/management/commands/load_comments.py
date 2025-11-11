from django.core.management.base import BaseCommand
from django.conf import settings
import pandas as pd
from sentimientos.models import Comment
import os

class Command(BaseCommand):
    help = "Carga comentarios desde un CSV (solo si la tabla está vacía)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--path", 
            type=str, 
            required=False,
            default=None,
            help="Ruta al CSV (opcional, usa ruta por defecto)"
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Forzar carga aunque ya existan datos"
        )

    def handle(self, *args, **opts):
        # Verificar si ya hay comentarios en la base de datos
        total_existentes = Comment.objects.count()
        
        if total_existentes > 0 and not opts.get("force"):
            self.stdout.write(
                self.style.WARNING(
                    f"⚠️  Ya existen {total_existentes} comentarios en la base de datos.\n"
                    f"   No se cargará el CSV para evitar duplicados.\n"
                    f"   Usa --force para cargar de todas formas."
                )
            )
            return
        
        # Ruta del CSV (por defecto busca en la raíz del proyecto)
        path = opts.get("path")
        if not path:
            # Buscar el CSV en la ubicación por defecto
            base_dir = settings.BASE_DIR.parent  # Sale de ModeloSalud/
            path = os.path.join(base_dir, "Comentarios_de_pacientes.csv")
        
        # Verificar que existe el archivo
        if not os.path.exists(path):
            self.stderr.write(
                self.style.ERROR(
                    f"❌ No se encontró el archivo CSV en: {path}\n"
                    f"   Especifica la ruta con --path=\"ruta/al/archivo.csv\""
                )
            )
            return
        
        # Cargar el CSV
        self.stdout.write(f"📂 Cargando comentarios desde: {path}")
        
        try:
            df = pd.read_csv(path)
            created = 0
            
            for _, row in df.iterrows():
                # Verificar que no exista un comentario idéntico
                texto = row.get("texto", "").strip()
                if texto and not Comment.objects.filter(texto=texto).exists():
                    Comment.objects.create(
                        fecha=row.get("fecha"),
                        texto=texto,
                        etiqueta=row.get("etiqueta", "").lower()
                    )
                    created += 1
            
            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Proceso completado!\n"
                    f"   - Comentarios nuevos cargados: {created}\n"
                    f"   - Total en base de datos: {Comment.objects.count()}"
                )
            )
        
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f"❌ Error al cargar el CSV: {str(e)}")
            )
