"""
Google Workspace commands
"""

import csv
import os
import subprocess
from pathlib import Path

from rich.console import Console
from typer import Exit, Typer

from pjecz_gob_mx_cli_typer.config.settings import get_settings

app = Typer(name="googleworkspace", help="Google Workspace commands")


@app.command()
def copiar(esta_rama: str = ""):
    """Copiar archivos desde Google Workspace al directorio SOURCES_DIR leyendo RCLONE_REMOTES_CSV"""
    console = Console()
    console.print("Copiando archivos desde Google Workspace al directorio SOURCES_DIR...")

    # Obtener la configuración
    settings = get_settings()
    sources_dir = Path(settings.SOURCES_DIR)
    rclone_remotes_csv = Path(settings.RCLONE_REMOTES_CSV)

    # Leer el archivo rclone-remotes.csv
    with open(rclone_remotes_csv, newline="", encoding="utf-8") as puntero:
        lector = csv.DictReader(puntero)
        for fila in lector:
            rama = fila["RAMA"]
            rclone_config = fila["RCLONE_CONFIG"]

            # Saltar si se especificó una rama y no coincide
            if esta_rama and rama != esta_rama:
                continue

            # Definir los parámetros de origen y destino para rclone
            rclone_source = f"{rclone_config}:"
            destination_path = str(sources_dir / rama)

            # Crear el directorio de destino si no existe
            os.makedirs(destination_path, exist_ok=True)

            # Ejecutar el comando rclone copy
            command = ["rclone", "copy", rclone_source, destination_path]
            console.print(f"Ejecutando: {' '.join(command)}")
            try:
                result = subprocess.run(command, capture_output=True, check=True, text=True)
            except subprocess.CalledProcessError as error:
                console.print(f"[red]Error al ejecutar rclone copy para la rama {rama}[/red]")
                console.print(error.stderr)
                raise Exit(code=1)

            # Si el resultado no es exitoso, mostrar el error y salir
            if result.returncode != 0:
                console.print(f"[red]Error al copiar archivos para la rama {rama}[/red]")
                console.print(result.stderr)
                raise Exit(code=1)

            # Mostrar mensaje de éxito
            console.print(f"[green]Archivos copiados exitosamente para la rama {rama}[/green]")

    # Mensaje final
    console.print("[green]Proceso de copia completado exitosamente.[/green]")
