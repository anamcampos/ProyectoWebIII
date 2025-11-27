import requests
from pathlib import Path
import hashlib
import shutil
import os
import logging

LOG = logging.getLogger("scraper")

def safe_filename_from_url(url):
    # extrae nombre razonable del URL
    name = url.split("/")[-1].split("?")[0]
    if not name:
        name = hashlib.sha256(url.encode()).hexdigest()
    return name

def download_file(url, dest_dir="downloads", timeout=30):
    """
    Descarga el archivo a dest_dir y devuelve la ruta local completa.
    Reintenta poco; manejo de errores mínimo.
    """
    os.makedirs(dest_dir, exist_ok=True)
    local_name = safe_filename_from_url(url)
    dest_path = Path(dest_dir) / local_name
    try:
        with requests.get(url, stream=True, timeout=timeout) as r:
            r.raise_for_status()
            with open(dest_path, "wb") as f:
                shutil.copyfileobj(r.raw, f)
        LOG.info(f"Downloaded file {url} -> {dest_path}")
        return str(dest_path)
    except Exception as e:
        LOG.error(f"Failed to download {url}: {e}")
        # si falló, asegúrate de no dejar archivo parcial
        try:
            if dest_path.exists():
                dest_path.unlink()
        except Exception:
            pass
        return None

def sha256_of_file(path, chunk_size=65536):
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception as e:
        LOG.error(f"sha256 read error {path}: {e}")
        return None

def remove_local_file(path):
    try:
        p = Path(path)
        if p.exists():
            p.unlink()
            LOG.info(f"Local file removed: {path}")
            return True
    except Exception as e:
        LOG.error(f"Error removing local file {path}: {e}")
    return False