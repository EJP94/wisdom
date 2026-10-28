"""Descarga episodios del podcast desde su feed RSS y lista los que faltan.

Uso:
    .venv\\Scripts\\python.exe descargar.py [--desde 1] [--hasta 100] [--especiales]

Sin --hasta llega hasta el número más alto del feed. Con --especiales también baja
los episodios sin número (audios\\especial - AAAA-MM-DD - Título.mp3).

El número de cada episodio es el oficial, el de su descripción ("Ep. #12 | ...").
Las etiquetas que trae cada MP3 (número de pista, título) están desfasadas en el
original, así que el script las reescribe con el número y título correctos.

Cada audio queda en audios\\NNN - Título.mp3. Lo que ya existe no se vuelve a
bajar. Los números que no están en el feed van a audios\\FALTANTES.md, con los
episodios vecinos para ubicarlos a mano en Listen Notes; basta guardarlos como
"NNN - Título.mp3" para que cuenten como presentes (y se etiqueten) la próxima vez.
"""

import argparse
import re
import shutil
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from html import unescape
from pathlib import Path
from urllib.parse import unquote, urlsplit

import mutagen

FEED = "https://anchor.fm/s/f27edd10/podcast/rss"
AUDIOS = Path("audios")
AGENTE = {"User-Agent": "Mozilla/5.0 (transcript; descarga personal de podcast)"}
NUMERO = re.compile(r"Ep(?:isode)?\s*\.?\s*#\s*(\d+)", re.IGNORECASE)
ARCHIVO = re.compile(r"^(\d{3})(b\d+)? - (.+)$")
EXTENSIONES = {".mp3", ".m4a"}
# Números que el usuario confirmó (2026-10-23) que no están ni en el feed ni en Listen Notes
NO_DISPONIBLES = {*range(51, 59), 76, 86, 666}


def leer_feed() -> tuple[dict, list[dict]]:
    """Datos del podcast y sus episodios, del más antiguo al más nuevo."""
    with urllib.request.urlopen(urllib.request.Request(FEED, headers=AGENTE), timeout=60) as r:
        raiz = ET.fromstring(r.read())
    canal = raiz.find("channel")
    podcast = {
        "titulo": canal.findtext("title").strip(),
        "autor": canal.findtext("{http://www.itunes.com/dtds/podcast-1.0.dtd}author", "").strip(),
    }
    episodios = []
    for item in reversed(list(canal.iter("item"))):
        descripcion = unescape(re.sub(r"<[^>]+>", " ", item.findtext("description") or ""))
        m = NUMERO.search(descripcion)
        url = item.find("enclosure").get("url")
        original = Path(urlsplit(unquote(url)).path).name  # el MP3 real va codificado al final
        episodios.append(
            {
                "numero": int(m.group(1)) if m else None,
                "titulo": (item.findtext("title") or "").strip(),
                "fecha": datetime.strptime(item.findtext("pubDate")[5:16], "%d %b %Y"),
                "url": url,
                "extension": Path(original).suffix or ".mp3",
            }
        )
    return podcast, episodios


def limpiar(titulo: str) -> str:
    """Título apto para nombre de archivo en Windows, sin perder significado ("80/20" → "80-20")."""
    t = titulo.replace("/", "-").replace(":", " -").replace("|", " -").replace('"', "'")
    t = re.sub(r'[<>\\?*\x00-\x1f]', "", t)
    return re.sub(r"\s+", " ", t).strip().rstrip(". ")


def prefijo(numero: int, repeticion: int = 0) -> str:
    """'012', o '404b1' para el segundo episodio que el feed numera igual."""
    return f"{numero:03d}" + (f"b{repeticion}" if repeticion else "")


def con_prefijo(pref: str) -> list[Path]:
    return sorted(a for a in AUDIOS.glob(f"{pref} - *") if a.suffix.lower() in EXTENSIONES)


def descargar(url: str, destino: Path) -> None:
    parcial = destino.with_name(destino.name + ".part")
    with urllib.request.urlopen(urllib.request.Request(url, headers=AGENTE), timeout=120) as r, open(parcial, "wb") as f:
        shutil.copyfileobj(r, f, length=1 << 20)
    parcial.replace(destino)


def etiquetar(ruta: Path, numero: int | None, titulo: str, anio: int | None, podcast: dict) -> bool:
    """Deja número de pista, título, álbum, autor y año correctos. True si cambió algo."""
    audio = mutagen.File(ruta, easy=True)
    if audio.tags is None:
        audio.add_tags()
    deseado = {"title": titulo, "album": podcast["titulo"], "artist": podcast["autor"]}
    if anio:
        deseado["date"] = str(anio)
    if numero is not None:
        deseado["tracknumber"] = str(numero)
    cambios = {k: v for k, v in deseado.items() if v and audio.tags.get(k) != [v]}
    if numero is None and "tracknumber" in audio.tags:
        del audio.tags["tracknumber"]
        cambios["tracknumber"] = None
    for k, v in cambios.items():
        if v is not None:
            audio.tags[k] = v
    if cambios:
        audio.save()
    return bool(cambios)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser()
    p.add_argument("--desde", type=int, default=1)
    p.add_argument("--hasta", type=int)
    p.add_argument("--especiales", action="store_true")
    args = p.parse_args()

    AUDIOS.mkdir(exist_ok=True)
    podcast, episodios = leer_feed()
    por_numero = {}
    for e in episodios:
        if e["numero"] is not None:
            por_numero.setdefault(e["numero"], []).append(e)
    if args.hasta is None:
        args.hasta = max(por_numero)

    # (episodio, prefijo para buscar versiones anteriores, nombre definitivo)
    pendientes = []
    faltantes = []
    for n in range(args.desde, args.hasta + 1):
        if n not in por_numero:
            if not con_prefijo(prefijo(n)):
                faltantes.append(n)
            continue
        for k, e in enumerate(por_numero[n]):
            pref = prefijo(n, k)
            pendientes.append((e, pref, f"{pref} - {limpiar(e['titulo'])}{e['extension']}"))
    if args.especiales:
        for e in episodios:
            if e["numero"] is None:
                pref = f"especial - {e['fecha']:%Y-%m-%d}"
                pendientes.append((e, pref, f"{pref} - {limpiar(e['titulo'])}{e['extension']}"))

    bajados = renombrados = ya = 0
    errores = []
    del_feed = {}  # nombre de archivo -> episodio, para etiquetar
    for e, pref, nombre in pendientes:
        destino = AUDIOS / nombre
        del_feed[nombre] = e
        if destino.exists():
            ya += 1
            continue
        anteriores = con_prefijo(pref)
        try:
            if anteriores:  # mismo episodio con un nombre de una versión anterior del script
                anteriores[0].rename(destino)
                renombrados += 1
                print(f"renombrado {anteriores[0].name} -> {nombre}", flush=True)
            else:
                descargar(e["url"], destino)
                bajados += 1
                print(f"bajado    {nombre}", flush=True)
        except Exception as error:  # un episodio caído no detiene el resto
            errores.append(nombre)
            print(f"ERROR     {nombre}: {error}", flush=True)

    etiquetados = etiquetar_todo(del_feed, podcast)
    escribir_faltantes(faltantes, episodios, args)
    escribir_inventario(por_numero, args)
    por_bajar = [n for n in faltantes if n not in NO_DISPONIBLES]
    print(
        f"\nBajados {bajados}, renombrados {renombrados}, ya estaban {ya}, etiquetas corregidas {etiquetados}, "
        f"errores {len(errores)}, faltan {len(por_bajar)}: {por_bajar}, "
        f"no disponibles {len(faltantes) - len(por_bajar)}"
    )
    for nombre in errores:
        print(f"  con error: {nombre}")


def etiquetar_todo(del_feed: dict, podcast: dict) -> int:
    """Etiqueta todos los audios: los del feed con sus datos, los manuales según su nombre."""
    corregidos = 0
    for ruta in sorted(AUDIOS.iterdir()):
        if ruta.suffix.lower() not in EXTENSIONES:
            continue
        e = del_feed.get(ruta.name)
        m = ARCHIVO.match(ruta.stem)
        numero = int(m.group(1)) if m else None
        if e:
            titulo, anio = e["titulo"], e["fecha"].year
        elif m:
            # Agregado a mano: se conserva el título de su etiqueta; si no tiene, sale del nombre
            etiquetas = mutagen.File(ruta, easy=True).tags
            titulo, anio = ((etiquetas or {}).get("title") or [m.group(3)])[0], None
        else:
            continue
        try:
            corregidos += etiquetar(ruta, numero, titulo, anio, podcast)
        except Exception as error:
            print(f"ERROR al etiquetar {ruta.name}: {error}", flush=True)
    return corregidos


def escribir_faltantes(faltantes: list[int], episodios: list[dict], args) -> None:
    numerados = [e for e in episodios if e["numero"] is not None]
    fmt = lambda e: f'Ep. #{e["numero"]} {e["titulo"]} ({e["fecha"]:%Y-%m-%d})' if e else "—"

    def tabla(numeros: list[int]) -> list[str]:
        filas = ["| Ep. | Episodio anterior | Episodio siguiente |", "|---|---|---|"]
        for n in numeros:
            antes = max((e for e in numerados if e["numero"] < n), key=lambda e: e["numero"], default=None)
            despues = min((e for e in numerados if e["numero"] > n), key=lambda e: e["numero"], default=None)
            filas.append(f"| {n} | {fmt(antes)} | {fmt(despues)} |")
        return filas

    por_bajar = [n for n in faltantes if n not in NO_DISPONIBLES]
    no_disponibles = [n for n in faltantes if n in NO_DISPONIBLES]
    lineas = [
        f"# Episodios que faltan (Ep. #{args.desde} a #{args.hasta})",
        "",
        'Los números son los oficiales: el "Ep. #N" de la descripción de cada episodio.',
        "",
        "## Por bajar a mano",
        "",
    ]
    if por_bajar:
        lineas += [
            "No están en el feed. Bájalos de Listen Notes y guárdalos en esta carpeta como",
            "`NNN - Título.mp3` (por ejemplo `013 - Título del episodio.mp3`). Los vecinos sirven",
            "para ubicarlos por fecha.",
            "",
            *tabla(por_bajar),
        ]
    else:
        lineas.append("Ninguno: todo lo disponible está descargado.")
    if no_disponibles:
        lineas += [
            "",
            "## No disponibles",
            "",
            "No están en el feed ni en Listen Notes (confirmado por el usuario el 2026-10-23).",
            "",
            *tabla(no_disponibles),
        ]
    (AUDIOS / "FALTANTES.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")


def escribir_inventario(por_numero: dict, args) -> None:
    """audios\\INVENTARIO.csv: una fila por número, con su estado y archivo."""
    filas = ["episodio;estado;fecha;titulo;archivo"]
    for n in range(args.desde, args.hasta + 1):
        feed = por_numero.get(n, [])
        archivos = [a for k in range(max(len(feed), 1)) for a in con_prefijo(prefijo(n, k))]
        estado = "descargado" if archivos else ("no disponible" if n in NO_DISPONIBLES else "falta")
        if archivos and not feed:
            estado = "manual"  # no está en el feed, lo agregó el usuario
        titulo = " / ".join(e["titulo"] for e in feed) or (ARCHIVO.match(archivos[0].stem).group(3) if archivos else "")
        fecha = f"{feed[0]['fecha']:%Y-%m-%d}" if feed else ""
        filas.append(f'{n};{estado};{fecha};"{titulo}";"{" / ".join(a.name for a in archivos)}"')
    for a in sorted(AUDIOS.glob("especial - *")):
        if a.suffix.lower() in EXTENSIONES:
            filas.append(f'especial;descargado;{a.name.split(" - ")[1]};"{a.stem.split(" - ", 2)[2]}";"{a.name}"')
    (AUDIOS / "INVENTARIO.csv").write_text("\n".join(filas) + "\n", encoding="utf-8-sig")


if __name__ == "__main__":
    main()
