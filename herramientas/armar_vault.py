import json, re, sys
from pathlib import Path

src, dst = Path(sys.argv[1]), Path(sys.argv[2])
dst.mkdir(parents=True, exist_ok=True)

FIXES = [
    (r"Alpha Mail", "Alpha Male", "Alpha Mail"),
    (r"Stephen ?Mathis|StevenMathis", "Steven Mathis", "Stephen Mathis"),
    (r"\b8020\b", "80/20", "8020"),
    (r"caramel emple", "caramel apple", "caramel emple"),
    (r"kick ass(?:e)?ness", "kick-assness", "kick assness"),
    (r"gradually Get used", "gradually get used", "Get used"),
]
# Frase que Parakeet omite en el trozo largo; sale al transcribir 00:55-01:10 por separado
EP4 = ("There's incredible immune responses that happen. But you know",
       "There's incredible immune responses that happen. Um you there's a, uh, really a lot of physical and physiological benefits of the cold. Um but you know")

def mmss(s):
    return f"{int(s // 60):02d}:{int(s % 60):02d}"

for jf in sorted(src.glob("*.json")):
    d = json.loads(jf.read_text())
    num, title = jf.stem.split(" - ", 1)
    notes = []
    paras = []
    for s in d["segmentos"]:
        t = s["texto"]
        if not t:
            continue
        for pat, rep, label in FIXES:
            t, n = re.subn(pat, rep, t)
            if n:
                notes.append(f"{mmss(s['inicio'])}: «{label}» → «{rep}»")
        if num == "004" and EP4[0] in t:
            t = t.replace(EP4[0], EP4[1])
            notes.append(f"{mmss(s['inicio'])}: frase omitida por el modelo, restaurada al re-transcribir ese tramo")
        paras.append(f"**[{mmss(s['inicio'])}]** {t}")
    fm = [
        "---",
        f'title: "{title}"',
        "podcast: Holistic Alpha",
        "host: Steven Mathis",
        f"episodio: {int(num)}",
        f'duracion: "{mmss(d["duracion_s"])}"',
        "tipo: transcript",
        "idioma: en",
        f"transcriptor: {d['modelo']}",
        "tags: [fuente, transcript, holistic-alpha]",
        "correcciones:",
    ] + [f'  - "{n}"' for n in notes] + ["---", "", f"# {int(num)}. {title}", ""]
    (dst / f"{num} - {title}.md").write_text("\n".join(fm) + "\n" + "\n\n".join(paras) + "\n")
    print(num, len(paras), "párrafos,", len(notes), "correcciones")
