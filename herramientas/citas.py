"""Expande citas abreviadas y verifica citas textuales contra los transcripts.

Uso: citas.py holistic-alpha [--solo-verificar]

Abreviaturas que expande en episodios/, conceptos/, practicas/, mapas/ y salidas/:
  {4@06:28}   enlace al párrafo del transcript del episodio 4 que empieza en 06:28
  {E4}        enlace a la nota del episodio 4
  {R4@06:28}  referencia completa: fecha · episodio · minuto

Verifica que cada cita `> "texto" [[...#^mMMSS|MM:SS]]` esté textual en ese párrafo.
"""
import re, sys
from pathlib import Path

vault = Path(sys.argv[1])
solo_verificar = "--solo-verificar" in sys.argv

transcripts = {int(re.search(r"^episodio: (\d+)", f.read_text(), re.M)[1]): f
               for f in (vault / "fuentes/transcripts").glob("*.md")}
episodios = {}
fechas = {}
for f in (vault / "episodios").glob("*.md"):
    t = f.read_text()
    n = int(re.search(r"^episodio: (\d+)", t, re.M)[1])
    episodios[n] = f.stem
    fechas[n] = re.search(r"^fecha: (\S+)", t, re.M)[1]

parrafos = {}
for n, f in transcripts.items():
    for m in re.finditer(r"^\*\*\[\d\d:\d\d\]\*\* (.*) \^m(\d{4})$", f.read_text(), re.M):
        parrafos[(n, m[2])] = m[1]

errores = []

def ancla(n, ts):
    clave = (n, ts.replace(":", ""))
    if clave not in parrafos:
        errores.append(f"no existe el párrafo {ts} en el episodio {n}")
    return f"[[{transcripts[n].stem}#^m{clave[1]}|{ts}]]"

def expandir(t):
    t = re.sub(r"\{R(\d+)@(\d\d:\d\d)\}", lambda m: f"{fechas[int(m[1])]} · [[{episodios[int(m[1])]}|Ep {int(m[1])}]] · {ancla(int(m[1]), m[2])}", t)
    t = re.sub(r"\{E(\d+)\}", lambda m: f"[[{episodios[int(m[1])]}|Ep {int(m[1])}]]", t)
    return re.sub(r"\{(\d+)@(\d\d:\d\d)\}", lambda m: ancla(int(m[1]), m[2]), t)

def normal(s):
    return re.sub(r"\s+", " ", s.replace("’", "'")).strip().lower()

citas = 0
for carpeta in ["episodios", "conceptos", "practicas", "mapas", "salidas"]:
    for f in sorted((vault / carpeta).glob("*.md")):
        t = f.read_text()
        nuevo = t if solo_verificar else expandir(t)
        if nuevo != t:
            f.write_text(nuevo)
        for m in re.finditer(r'^> "(.+)" \[\[[^#\]]+#\^m(\d{4})\|', nuevo, re.M):
            citas += 1
            n = next(k for k, v in transcripts.items() if f"[[{v.stem}#^m{m[2]}|" in m[0])
            if normal(m[1]) not in normal(parrafos.get((n, m[2]), "")):
                errores.append(f"{f.name}: cita no textual en ep {n} {m[2]}: {m[1][:60]}")

print(f"{citas} citas revisadas")
for e in errores:
    print("ERROR", e)
sys.exit(1 if errores else 0)
