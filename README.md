# Wisdom

Vaults de Obsidian con conocimiento destilado, una por tema.

- `holistic-alpha/`: vault piloto del podcast Holistic Alpha, ver su [README](holistic-alpha/README.md)
  - `fuentes/transcripts/`: un transcript por episodio, con `[mm:ss]` y ancla `^mMMSS` por párrafo para citar
- `herramientas/`: scripts para generar las fuentes

## Transcribir episodios

1. `transcribir_parakeet.py audios/ --salida parakeet/ [--cpu]` usa NVIDIA Parakeet TDT 0.6B v3 y deja `.txt` y `.json` por audio
2. `armar_vault.py parakeet/ holistic-alpha/fuentes/transcripts` arma el Markdown con frontmatter y corrige nombres mal escuchados

Los audios se nombran `NNN - Título.mp3`.
Cada transcript lista sus correcciones en el frontmatter.

## Destilar episodios

`citas.py holistic-alpha` expande las citas abreviadas a enlaces y verifica cada cita textual contra su transcript.
