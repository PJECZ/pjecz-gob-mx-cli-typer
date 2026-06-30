"""
Astro commands
"""

import csv
import os
import subprocess
from pathlib import Path

from rich.console import Console
from typer import Exit, Typer

from pjecz_gob_mx_cli_typer.config.settings import get_settings

app = Typer(name="astro", help="Astro commands")


@app.command()
def generar(esta_rama: str = ""):
    """Generar archivos para Astro en GENERATED_DIR leyendo RCLONE_REMOTES_CSV"""
    console = Console()
    console.print("Pendiente de implementar la funcionalidad.")
